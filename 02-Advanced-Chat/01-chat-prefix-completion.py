from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

"""
使用了前缀补全（Prefix Completion）的方式，即给定部分代码，让模型完成剩余部分

# 实现原理

1. 给定部分代码，让模型完成剩余部分
2. 模型会根据给定的代码，生成剩余部分
3. 将生成的代码与给定的代码拼接起来，形成完整的代码
4. 返回完整的代码

# 适用场景

1. 代码补全工具
2. 代码片段生成
3. 编程辅助工具

# 实现设置  

prefix 参数 ： 给定部分代码，让模型完成剩余部分
stop 参数 ： 停止生成代码的条件

"""

# 使用 DeepSeek API
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

messages = [
    {"role": "user", "content": "Please write quick sort code, not include any other text, not explaination"},
    {"role": "assistant", "content": "```python\n", "prefix": True}
]

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",  # 使用正确的模型名称
    messages=messages,
    stop=["```"],
)

# 打印完整的响应信息，方便调试
print("完整响应：", response)
print("\n生成的代码：")
print(response.choices[0].message.content)