from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 因为网络问题，使用阿里云平台中的DeepSeek代替
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL")
)

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]

messages.append({"role": "user", "content": """ 你好！世界上有几个大洋？ """})

response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

# Round 1
messages.append(
    {
        "role": "assistant",
        "content": response.choices[0].message.content,
    }
)

print(f"Messages Round 1: {messages}")
print(f"Messages Round 1 Assistant: {response.choices[0].message.content}")

# Round 2
messages.append(
    {
        "role": "user",
        "content": """ 你能告诉我世界上最大的洋吗？ """,
    }
)

response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

print(f"Messages Round 2: {messages}")
print(f"Messages Round 2 Assistant: {response.choices[0].message.content}")
