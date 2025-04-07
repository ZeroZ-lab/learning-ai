from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

router = APIRouter()

class WeatherRequest(BaseModel):
    location: str

class WeatherResponse(BaseModel):
    weather_info: dict
    description: str = ""

# 高德地图 API 密钥
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

def get_weather(location: str) -> dict:
    """直接调用高德地图 API 获取天气信息"""
    if not AMAP_API_KEY:
        raise HTTPException(status_code=500, detail="AMAP_API_KEY is not configured")
    
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={location}&key={AMAP_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查 HTTP 错误
        data = response.json()
        
        # 检查 API 返回状态
        if data.get("status") != "1":
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get weather info: {data.get('info', 'Unknown error')}"
            )
        
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse weather data: {str(e)}")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获得给定城市code的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市的code",
                    }
                },
                "required": ["location"],
            },
        },
    },
]

@router.post("/weather", response_model=WeatherResponse)
async def get_weather_info(request: WeatherRequest):
    try:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_BASE_URL")
        )

        # 使用 function calling 方式
        messages = [
            {
                "role": "system",
                "content": "你是一个天气预报员，请根据用户的问题，使用 function calling 获取天气信息, 你非常了解各个城市的邮编，110101 是北京市的邮编",
            },
            {"role": "user", "content": f"How's the weather in {request.location}?"},
        ]

        logger.info(f"Sending request to OpenAI with location: {request.location}")

        try:
            # 第一次调用获取 tool_calls
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=messages,
                tools=tools
            )
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI API call failed: {str(e)}"
            )
        
        if not response.choices or not response.choices[0].message:
            logger.error("No response from OpenAI")
            raise HTTPException(status_code=500, detail="No response from OpenAI")
            
        message = response.choices[0].message
        logger.info(f"Received response from OpenAI: {message}")

        if not message.tool_calls:
            logger.error("No tool calls in response")
            raise HTTPException(status_code=400, detail="No tool calls in response")

        # 处理 tool_calls
        messages.append({"role": "assistant", "content": "", "tool_calls": message.tool_calls})
        available_functions = {"get_weather": get_weather}
        
        function_response = None
        for tool_call in message.tool_calls:
            if not tool_call.function:
                continue
                
            function_name = tool_call.function.name
            if function_name not in available_functions:
                continue
                
            function_to_call = available_functions[function_name]
            try:
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(function_args.get("location", request.location))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(function_response)
                    }
                )
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse function arguments: {str(e)}")
                continue

        if not function_response:
            logger.error("Failed to get weather information from function call")
            raise HTTPException(status_code=500, detail="Failed to get weather information")

        # 第二次调用获取最终响应
        try:
            second_response = client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=messages
            )
        except Exception as e:
            logger.error(f"Second OpenAI API call failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Second OpenAI API call failed: {str(e)}"
            )

        if not second_response.choices or not second_response.choices[0].message:
            logger.error("No final response from OpenAI")
            raise HTTPException(status_code=500, detail="Failed to get final response from OpenAI")

        # 格式化天气描述
        weather_info = function_response
        if weather_info.get("lives") and isinstance(weather_info["lives"], list) and len(weather_info["lives"]) > 0:
            weather_data = weather_info["lives"][0]
            description = (
                f"{weather_data.get('province', '')}{weather_data.get('city', '')}的天气情况：\n"
                f"天气：{weather_data.get('weather', '未知')}\n"
                f"温度：{weather_data.get('temperature', '未知')}℃\n"
                f"风向：{weather_data.get('winddirection', '未知')}\n"
                f"风力：{weather_data.get('windpower', '未知')}\n"
                f"湿度：{weather_data.get('humidity', '未知')}%\n"
                f"发布时间：{weather_data.get('reporttime', '未知')}"
            )
        else:
            description = second_response.choices[0].message.content

        return WeatherResponse(
            weather_info=weather_info,
            description=description
        )

    except HTTPException as e:
        logger.error(f"HTTP Exception: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 