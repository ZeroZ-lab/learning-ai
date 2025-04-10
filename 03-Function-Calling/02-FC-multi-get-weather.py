from openai import OpenAI
import os
import requests
import json
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

"""
使用 function calling 获取天气信息

"""

# 使用 DeepSeek API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat", messages=messages, tools=tools
    )
    return response.choices[0].message


# 高德地图 API 密钥
# 从高德地图获取天气
AMAP_API_KEY = os.getenv("AMAP_API_KEY")


def search_city_code(args):
    if isinstance(args, str):
        args = json.loads(args)
    city_name = args.get("city_name")
    
    try:
        # 读取Excel文件，指定使用openpyxl引擎
        df = pd.read_excel('./03-Function-Calling/data/AMap_adcode_citycode.xlsx', engine='openpyxl')
        
        # 打印前几行数据，用于调试
        print("Debug - First few rows of dataframe:")
        print(df.head())
        print("\nDebug - Column names:", df.columns.tolist())
        
        # 使用模糊匹配
        result = df[df.iloc[:, 0].str.contains(city_name, na=False)]
        if not result.empty:
            return {"adcode": str(result.iloc[0]['adcode'])}
        
        return {"error": f"City not found: {city_name}"}
    except Exception as e:
        return {"error": f"Error processing request: {str(e)}"}


def get_weather(args):
    if isinstance(args, str):
        args = json.loads(args)
    location = args.get("location")
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={location}&key={AMAP_API_KEY}"
    response = requests.get(url)
    return response.json()


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_city_code",
            "description": "根据城市名称查找对应的城市代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "城市名称",
                    }
                },
                "required": ["city_name"],
            },
        },
    },
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


messages = [
    {
        "role": "system",
        "content": "你是一个天气预报员，请根据用户的问题，使用 function calling 获取天气信息。当用户询问某个城市的天气时，你需要先使用 search_city_code 函数查找该城市的代码，然后使用 get_weather 函数获取天气信息。如果找不到城市代码，请告诉用户。",
    },
    {"role": "user", "content": "How's the weather in 杭州 和 上海?"},
]

while True:
    message = send_messages(messages)
    
    # 如果没有工具调用，直接打印回复并退出
    if not message.tool_calls:
        print(f"\n🤖 Assistant>\t {message.content}")
        break
        
    # 处理工具调用
    messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})
    
    # 执行所有工具调用
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_to_call = {
            "get_weather": get_weather,
            "search_city_code": search_city_code
        }[function_name]
        
        function_args = tool_call.function.arguments
        function_response = function_to_call(function_args)
        
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_response)
            }
        )
        print(f"\n🛠️ Tool Call>\t {tool_call}")
        print(f"📝 Function Name>\t {function_name}")
        print(f"📋 Function Args>\t {function_args}")
        print(f"📊 Function Response>\t {function_response}")
