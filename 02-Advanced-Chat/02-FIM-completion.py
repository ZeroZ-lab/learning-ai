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

response = client.completions.create(
    model="deepseek/deepseek-chat",
    prompt="def fib(a):",
    suffix="    return fib(a-1) + fib(a-2)",
    max_tokens=128
)

# 打印完整的响应信息，方便调试
print("完整响应：", response)
print("\n生成的代码：")
print(response.choices[0].text)