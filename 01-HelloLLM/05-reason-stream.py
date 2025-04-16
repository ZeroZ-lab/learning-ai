from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

print("\n" + "="*50)
print("🤖 开始流式推理过程")
print("="*50)

response = client.chat.completions.create(
    model="deepseek-r1",
        messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": """ 你好！两个小数 9.11和9.8 哪一个大？  """},
    ],
    # 1.将此处的Stream 改为 True，这为Stream模式
    stream=True
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""

print("-"*30)


for chunk in response:
    # 获取思考过程
    reasoning_chunk = chunk.choices[0].delta.reasoning_content
    # 获取回复
    answer_chunk = chunk.choices[0].delta.content
    # 如果思考过程不为空，则打印思考过程
    if reasoning_chunk is not None and reasoning_chunk != "":
        print(reasoning_chunk, end="")  # 实时流式输出思考过程
        reasoning_content += reasoning_chunk
    # 如果回复不为空，则打印回复。回复一般会在思考过程结束后返回
    elif answer_chunk is not None and answer_chunk != "":
        # 如果是第一次接收到回复内容，打印提示信息
        if answer_content == "":
            print("\n" + "-"*30)
            print("正式回答开始")
            print("-"*30 + "\n")
        print(answer_chunk, end="")  # 实时流式输出最终答案
        answer_content += answer_chunk

print("\n\n" + "="*50)
print("📝 完整输出：")
print("="*50)
print("\n🤔 思考过程：")
print("-"*30)
print(reasoning_content)
print("\n💡 最终答案：")
print("-"*30)
print(answer_content)
print("\n" + "="*50)
