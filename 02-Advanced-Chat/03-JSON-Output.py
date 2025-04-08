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

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=messages,
    response_format={"type": "json_object"},
    max_tokens=1000,
    temperature=0.7
)

# 打印完整的响应信息，方便调试
print("完整响应：", response)
# 解析 JSON 并美化输出
json_data = json.loads(response.choices[0].message.content)
print(json.dumps(json_data, indent=4, ensure_ascii=False))
