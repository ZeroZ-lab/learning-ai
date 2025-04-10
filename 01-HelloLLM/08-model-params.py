"""
模型参数配置示例

这个文件展示了如何配置不同的模型参数来影响生成结果。

主要参数说明：
1. temperature (温度)
   - 范围：0.0 - 2.0
   - 作用：控制输出的随机性
   - 值越高，输出越随机；值越低，输出越确定

2. top_p (核采样)
   - 范围：0.0 - 1.0
   - 作用：控制输出的多样性
   - 值越高，输出越多样；值越低，输出越保守

3. max_tokens (最大token数)
   - 作用：控制生成的最大长度
   - 值越大，生成的内容可能越长

4. presence_penalty (存在惩罚)
   - 范围：-2.0 - 2.0
   - 作用：控制是否避免重复内容
   - 正值鼓励新内容，负值允许重复

5. frequency_penalty (频率惩罚)
   - 范围：-2.0 - 2.0
   - 作用：控制词频的影响
   - 正值降低常见词的概率，负值增加常见词的概率
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

print("\n" + "="*50)
print("🤖 模型参数配置示例")
print("="*50)

# 测试不同温度值
temperatures = [0.1, 0.5, 1.0, 1.5]
for temp in temperatures:
    print(f"\n🌡️ 温度测试: {temp}")
    print("-"*30)
    
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "请用一句话描述春天的特点"}
        ],
        temperature=temp,
        max_tokens=100
    )
    
    print(f"🤖 生成结果：")
    print("✨"*20)
    print(response.choices[0].message.content)
    print("✨"*20)

# 测试不同top_p值
top_ps = [0.1, 0.5, 0.9]
for top_p in top_ps:
    print(f"\n🎯 Top-p测试: {top_p}")
    print("-"*30)
    
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "请用一句话描述夏天的特点"}
        ],
        top_p=top_p,
        max_tokens=100
    )
    
    print(f"🤖 生成结果：")
    print("✨"*20)
    print(response.choices[0].message.content)
    print("✨"*20)

# 测试惩罚参数
print("\n⚖️ 惩罚参数测试")
print("-"*30)
response = client.chat.completions.create(
    model="deepseek-v3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "请用三句话描述秋天的特点，每句话都要包含'秋天'这个词"}
    ],
    presence_penalty=0.5,
    frequency_penalty=0.5,
    max_tokens=200
)

print(f"🤖 生成结果：")
print("✨"*20)
print(response.choices[0].message.content)
print("✨"*20)

print("\n" + "="*50)
print("🎉 参数测试完成")
print("="*50) 