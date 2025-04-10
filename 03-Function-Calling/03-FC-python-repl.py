from openai import OpenAI
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

load_dotenv()

"""
使用 function calling 获取天气信息，并支持 Python 代码执行

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
        df = pd.read_excel(
            "./03-Function-Calling/data/AMap_adcode_citycode.xlsx", engine="openpyxl"
        )

        # 打印前几行数据，用于调试
        print("Debug - First few rows of dataframe:")
        print(df.head())
        print("\nDebug - Column names:", df.columns.tolist())

        # 使用模糊匹配
        result = df[df.iloc[:, 0].str.contains(city_name, na=False)]
        if not result.empty:
            return {"adcode": str(result.iloc[0]["adcode"])}

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


def execute_python_code(args):
    """执行 Python 代码并返回结果"""
    if isinstance(args, str):
        args = json.loads(args)
    code = args.get("code")

    # 创建输出捕获
    stdout = io.StringIO()
    stderr = io.StringIO()

    try:
        # 重定向标准输出和错误输出
        with redirect_stdout(stdout), redirect_stderr(stderr):
            # 创建新的命名空间
            local_vars = {}
            # 执行代码
            exec(code, globals(), local_vars)

        # 获取输出
        output = stdout.getvalue()
        error = stderr.getvalue()

        # 返回结果
        result = {
            "output": output,
            "error": error,
            "variables": {
                k: str(v) for k, v in local_vars.items() if not k.startswith("_")
            },
        }

    except Exception as e:
        result = {"error": str(e), "output": "", "variables": {}}

    return result


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
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "执行 Python 代码并返回结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要执行的 Python 代码",
                    }
                },
                "required": ["code"],
            },
        },
    },
]


messages = [
    {
        "role": "system",
        "content": """你是一个天气预报员和 Python 代码执行器。你可以：
1. 使用 search_city_code 和 get_weather 函数获取天气信息
2. 使用 execute_python_code 函数执行 Python 代码，比如温度转换等
当你需要执行计算或转换时，请生成相应的 Python 代码并执行。""",
    },
    {"role": "user", "content": "杭州与北京今天多少度？华氏温度是多少？"},
]

while True:
    message = send_messages(messages)

    # 如果没有工具调用，直接打印回复并退出
    if not message.tool_calls:
        print(f"\n🤖 Assistant>\t {message.content}")
        break

    # 处理工具调用
    messages.append(
        {
            "role": "assistant",
            "content": message.content,
            "tool_calls": message.tool_calls,
        }
    )

    # 执行所有工具调用
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_to_call = {
            "get_weather": get_weather,
            "search_city_code": search_city_code,
            "execute_python_code": execute_python_code,
        }[function_name]

        function_args = tool_call.function.arguments
        function_response = function_to_call(function_args)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_response),
            }
        )
        print(f"\n🛠️ Tool Call>\t {tool_call}")
        print(f"📝 Function Name>\t {function_name}")
        print(f"📋 Function Args>\t {function_args}")
        print(f"📊 Function Response>\t {function_response}")
