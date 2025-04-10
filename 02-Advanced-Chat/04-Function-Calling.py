from openai import OpenAI
import os
import json

from dotenv import load_dotenv

load_dotenv()

"""
⚠️⚠️⚠️⚠️非常重要！！！⚠️⚠️⚠️⚠️
Ai Agent 核心内容, 所有Agent 的实现都离不开Function Calling

# 实现原理

1. 使用 function 参数指定函数
2. 使用 function_call 参数指定函数
3. 使用 function_call_arguments 参数指定函数参数
4. 使用 function_call_arguments_schema 参数指定函数参数

# 适用场景

1. 调用外部函数
2. 调用外部API
3. 调用外部工具

# 实现设置

function 参数 ： 指定函数
function_call 参数 ： 指定函数


"""

# 使用 DeepSeek API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
print(f"\n👤 User>\t {messages[0]['content']}")

message = send_messages(messages)
# 打印工具调用信息
print(f"\n🛠️ Tool>\t {message.tool_calls[0]}")
tool = message.tool_calls[0]
messages.append(message)
# 模拟工具调用，实际调用的是get_weather函数
messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"\n🤖 Model>\t {message.content}")