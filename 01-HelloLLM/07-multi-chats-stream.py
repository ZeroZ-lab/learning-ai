"""
多轮对话流式输出示例 (Multi-turn Chat with Streaming Example)

这个文件展示了如何在多轮对话中使用流式输出。主要特点：

1. 流式输出优势
   - 实时显示生成的内容
   - 提供更好的用户体验
   - 减少等待时间

2. 对话上下文保持
   - 使用 messages 列表存储完整的对话历史
   - 每轮对话都会将新的消息添加到历史记录中
   - 系统会自动维护对话的上下文

3. 技术要点
   - 使用 stream=True 开启流式输出
   - 实时收集并显示生成的内容
   - 维护完整的对话历史

这个示例展示了如何构建一个流畅的多轮对话系统。
"""

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

print("\n" + "="*50)
print("🤖 多轮对话流式输出示例")
print("="*50)

messages.append({"role": "user", "content": """ 你好！世界上有几个大洋？ """})

# Round 1
print("\n🔄 Round 1 对话开始")
print("-"*30)
print("👤 用户提问：世界上有几个大洋？")
print("-"*30)
print("🤖 助手回复：")
print("✨"*20)

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

print("\n")
print("✨"*20)
print("Round 1 对话结束\n")

# 将完整回复添加到消息历史
messages.append({"role": "assistant", "content": full_response})

# Round 2
messages.append({"role": "user", "content": """ 你能告诉我世界上最大的洋吗？ """})

print("🔄 Round 2 对话开始")
print("-"*30)
print("👤 用户提问：你能告诉我世界上最大的洋吗？")
print("-"*30)
print("🤖 助手回复：")
print("✨"*20)

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

print("\n")
print("✨"*20)
print("Round 2 对话结束")

# 将第二轮回复添加到消息历史
messages.append({"role": "assistant", "content": full_response})

print("\n" + "="*50)
print("📝 完整对话历史")
print("="*50)
print("\n🌐 对话概览：")
print(f"- 总轮次：2 轮")
print(f"- 总消息数：{len(messages)} 条")
print("-"*30)

for i, msg in enumerate(messages, 1):
    role_icon = "👤" if msg["role"] == "user" else "🤖" if msg["role"] == "assistant" else "⚙️"
    print(f"\n📌 消息 {i}:")
    print(f"{role_icon} {msg['role']}:")
    print("-"*30)
    print(msg["content"])
    if i < len(messages):
        print("-"*30)

print("\n" + "="*50)
print("🎉 对话结束")
print("="*50) 