from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

# 示例1：简单的数学问题
print("\n" + "="*50)
print("🤖 示例1：简单的数学问题")
print("="*50)

response = client.chat.completions.create(
    model="deepseek-v3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": """ 你好！两个小数 9.11和9.8 哪一个大？  """},
    ],
    stream=True
)

# 初始化内容变量，用于存储完整的响应
content = ""

# 遍历流式响应的每个数据块
# 后端会以数据流（stream）的形式返回响应，每次返回一小段内容
# 这种机制可以让用户实时看到生成的内容，而不需要等待整个响应完成
# 
# 示例输出效果：
# 1. 第一个数据块可能返回: "让"
# 2. 第二个数据块可能返回: "我们"
# 3. 第三个数据块可能返回: "来"
# 4. 第四个数据块可能返回: "比较"
# 5. 第五个数据块可能返回: "一下"
# ... 以此类推，直到完整回答生成完毕
#
# 最终用户会看到类似这样的实时输出：
# 让我们来比较一下这两个数字。9.11和9.8，虽然9.11看起来数字更多，
# 但实际上9.8更大，因为小数点后的第一位8比1大。
for chunk in response:
    # 检查当前数据块是否包含内容
    # delta.content 表示相对于前一个数据块新增的内容
    if chunk.choices[0].delta.content is not None:
        # 获取当前数据块的内容
        content_piece = chunk.choices[0].delta.content
        # 实时打印当前数据块的内容，end="" 确保不换行
        print(content_piece, end="")
        # 将当前数据块的内容追加到完整内容中
        content += content_piece

print("\n\n完整回答:")
print(content)

# # 示例2：更复杂的推理问题
# print("\n" + "="*50)
# print("🤖 示例2：复杂的推理问题")
# print("="*50)

# response = client.chat.completions.create(
#     model="deepseek-v3",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": """请解释一下为什么太阳从东边升起，西边落下？"""},
#     ],
#     stream=True
# )

# content = ""
# for chunk in response:
#     if chunk.choices[0].delta.content is not None:
#         content_piece = chunk.choices[0].delta.content
#         print(content_piece, end="")
#         content += content_piece

# print("\n\n完整回答:")
# print(content)

