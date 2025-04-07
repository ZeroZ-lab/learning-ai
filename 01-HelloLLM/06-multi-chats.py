from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL")
)

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]

messages.append({"role": "user", "content": """ 你好！世界上有几个大洋？ """})

# Round 1
print("Round 1 对话开始：")
response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

print(f"Round 1 助手回复：{response.choices[0].message.content}")
print("Round 1 对话结束\n")

messages.append(
    {
        "role": "assistant",
        "content": response.choices[0].message.content,
    }
)

# Round 2
messages.append(
    {
        "role": "user",
        "content": """ 你能告诉我世界上最大的洋吗？ """,
    }
)

print("Round 2 对话开始：")
response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

print(f"Round 2 助手回复：{response.choices[0].message.content}")
print("Round 2 对话结束")
