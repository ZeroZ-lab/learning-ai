from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 因为网络问题，使用阿里云平台中的DeepSeek代替
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

response = client.chat.completions.create(
    model="deepseek-v3",
        messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": """ 你好！两个小数 9.11和9.8 哪一个大？  """},
    ],
    # 1.将此处的Stream 改为 True，这为Stream模式
    stream=True
)

# 处理流式响应并打印内容
content = ""

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        content_piece = chunk.choices[0].delta.content
        print(content_piece, end="")  # 实时打印每个片段
        content += content_piece

print("\n\n完整回答:")
print(content)

