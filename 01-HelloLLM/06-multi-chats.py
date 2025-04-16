"""
多轮对话示例 (Multi-turn Chat Example)

这个文件展示了如何使用 OpenAI API 进行多轮对话。主要特点：

1. 对话上下文保持
   - 使用 messages 列表存储完整的对话历史
   - 每轮对话都会将新的消息添加到历史记录中
   - 系统会自动维护对话的上下文

2. 对话流程
   - Round 1: 询问世界上有几个大洋
   - Round 2: 基于第一轮的回答，询问最大的洋是哪个
   - 展示了如何构建连贯的多轮对话

3. 技术要点
   - 使用 messages 数组维护对话历史
   - 每轮对话都包含完整的上下文
   - 展示了 assistant 和 user 角色的消息格式

这个示例对于理解如何构建连贯的对话系统非常有帮助。
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
print("🤖 多轮对话示例")
print("="*50)

messages.append({"role": "user", "content": """ 你好！世界上有几个大洋？ """})

# Round 1
print("\n🔄 Round 1 对话开始")
print("-"*30)
print("👤 用户提问：世界上有几个大洋？")
print("-"*30)

response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

print("🤖 助手回复：")
print("✨"*20)
print(response.choices[0].message.content)
print("✨"*20)
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

print("🔄 Round 2 对话开始")
print("-"*30)
print("👤 用户提问：你能告诉我世界上最大的洋吗？")
print("-"*30)

response = client.chat.completions.create(
    model="deepseek-v3", messages=messages, stream=False
)

print("🤖 助手回复：")
print("✨"*20)
print(response.choices[0].message.content)
print("✨"*20)
print("Round 2 对话结束")

messages.append(
    {
        "role": "assistant",
        "content": response.choices[0].message.content,
    }
)

print("\n" + "="*50)
print("📝 对话历史")
print("="*50)
for msg in messages:
    role_icon = "👤" if msg["role"] == "user" else "🤖" if msg["role"] == "assistant" else "⚙️"
    print(f"\n{role_icon} {msg['role']}:")
    print("-"*30)
    print(msg["content"])
print("\n" + "="*50)
