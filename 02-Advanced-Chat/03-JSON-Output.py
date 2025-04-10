from openai import OpenAI
import os
import json

from dotenv import load_dotenv

load_dotenv()

"""
结构化输出： 

1. 使用 response_format 参数指定输出格式

# 适用场景

1. 需要模型输出特定格式的数据，如 JSON、HTML、XML 等

# 实现设置

response_format 参数 ： 指定输出格式


"""

# 使用 DeepSeek API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

print("\n" + "="*50)
print("🤖 JSON结构化输出示例")
print("="*50)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

print("\n📝 请求信息：")
print("-"*30)
print("👤 用户输入：")
print(user_prompt)
print("-"*30)
print("⚙️ 系统提示：")
print(system_prompt.strip())
print("-"*30)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

print("\n⚙️ 请求参数：")
print("-"*30)
print("📦 模型: deepseek/deepseek-chat")
print("📝 输出格式: JSON")
print("📏 最大token数: 1000")
print("🌡️ 温度: 0.7")
print("-"*30)

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=messages,
    response_format={"type": "json_object"},
    max_tokens=1000,
    temperature=0.7
)

print("\n📊 响应信息：")
print("-"*30)
print(f"🆔 响应ID: {response.id}")
print(f"📅 创建时间: {response.created}")
print(f"📦 模型: {response.model}")
print(f"📝 完成原因: {response.choices[0].finish_reason}")
print("-"*30)

print("\n💻 生成的JSON：")
print("✨"*20)
# 解析 JSON 并美化输出
json_data = json.loads(response.choices[0].message.content)
print(json.dumps(json_data, indent=4, ensure_ascii=False))
print("✨"*20)

print("\n" + "="*50)
print("🎉 JSON生成完成")
print("="*50)
