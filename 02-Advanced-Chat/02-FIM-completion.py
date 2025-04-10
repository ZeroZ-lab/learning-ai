from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

"""
使用FIM（Factual Incompletion）的方式，即给定部分代码，让模型完成剩余部分  

# 实现原理

1. 给定部分代码，让模型完成剩余部分
2. 模型会根据给定的代码，生成剩余部分
3. 将生成的代码与给定的代码拼接起来，形成完整的代码
4. 返回完整的代码

# 适用场景

1. 代码补全工具
2. 代码片段生成
3. 编程辅助工具

"""

# 使用 DeepSeek API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

print("\n" + "="*50)
print("🤖 FIM代码补全示例")
print("="*50)

print("\n📝 请求信息：")
print("-"*30)
print("👤 用户请求：补全斐波那契数列函数")
print("📌 前缀代码：def fib(a):")
print("📌 后缀代码：    return fib(a-1) + fib(a-2)")
print(f"📏 最大token数：128")
print("-"*30)

response = client.completions.create(
    model="deepseek/deepseek-chat",
    prompt="def fib(a):",
    suffix="    return fib(a-1) + fib(a-2)",
    max_tokens=128
)

print("\n📊 响应信息：")
print("-"*30)
print(f"🆔 响应ID: {response.id}")
print(f"📅 创建时间: {response.created}")
print(f"📦 模型: {response.model}")
print(f"📝 完成原因: {response.choices[0].finish_reason}")
print("-"*30)

print("\n💻 生成的代码：")
print("✨"*20)
print("def fib(a):")
print(response.choices[0].text)
print("    return fib(a-1) + fib(a-2)")
print("✨"*20)

print("\n" + "="*50)
print("🎉 代码生成完成")
print("="*50)