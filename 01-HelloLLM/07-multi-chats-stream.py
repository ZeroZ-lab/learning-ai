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

# Round 1
print("Round 1 对话开始：")
response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=True
)

# 流式输出
full_response = ""
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
        full_response += content

print("\n\nRound 1 对话结束")

# 将完整回复添加到消息历史
messages.append({"role": "assistant", "content": full_response})

# Round 2
messages.append({"role": "user", "content": """ 你能告诉我世界上最大的洋吗？ """})

print("\nRound 2 对话开始：")
response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=True
)

# 流式输出
full_response = ""
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
        full_response += content

print("\n\nRound 2 对话结束") 