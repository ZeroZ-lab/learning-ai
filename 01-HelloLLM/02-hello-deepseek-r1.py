from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 因为网络问题，使用阿里云平台中的DeepSeek代替
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

response = client.chat.completions.create(
    model="deepseek-r1",
        messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": """ 你好！两个小数 9.11和9.8 哪一个大？  """},
    ],
    stream=False
)

# 通过reasoning_content字段打印思考过程
print("思考过程：")
print(response.choices[0].message.reasoning_content)
# 通过content字段打印最终答案
print("最终答案：")
print(response.choices[0].message.content)