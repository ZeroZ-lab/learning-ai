from openai import OpenAI
import os
import requests
import json

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
        "content": "你是一个天气预报员，请根据用户的问题，使用 function calling 获取天气信息, 你非常了解各个城市的 邮编，110101 是北京市的邮编",
    },
    {"role": "user", "content": "How's the weather in 北京?"},
]
message = send_messages(messages)

print(f"\n👤 User>\t {messages[1]['content']}")

# 查看返回的 tool_calls 是否有内容，并打印出来
tool_calls = message.tool_calls
print(f"\n🛠️ Tool Calls>\t {tool_calls}")

if tool_calls:
    messages.append({"role": "assistant", "content": "", "tool_calls": tool_calls})
    available_functions = {"get_weather": get_weather}
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = tool_call.function.arguments
        function_response = function_to_call(function_args)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_response)
            }
        )
        print(f"\n🔧 Tool Call>\t {tool_call}")
        print(f"📝 Function Name>\t {function_name}")
        print(f"📋 Function Args>\t {function_args}")
        print(f"📊 Function Response>\t {function_response}")

    print(f"\n📨 Messages>\t {messages}")
    second_message = send_messages(messages)
    print(f"\n🤖 Second Message>\t {second_message}")
