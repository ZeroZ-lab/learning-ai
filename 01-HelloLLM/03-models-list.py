from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 通过接口获取所有可用的模型
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

models_list = client.models.list()



# 打印标题和分隔线
print("\n" + "="*50)

# 打印原始数据
print("🤖 可用模型列表")
print(models_list)

print("="*50)

# 打印模型总数
print(f"\n📊 模型总数: {len(models_list.data)}")
print("-"*30)

# 遍历并打印每个模型的信息
for i, model in enumerate(models_list.data, 1):
    print(f"\n🔹 模型 {i}:")
    print(f"   ID: {model.id}")
    print(f"   创建时间: {model.created}")
    print(f"   所有者: {model.owned_by}")
    print("-"*30)

# 打印结束分隔线
print("\n" + "="*50)
