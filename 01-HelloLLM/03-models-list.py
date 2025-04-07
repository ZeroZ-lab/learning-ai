from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 通过接口获取所有可用的模型

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

models_list = client.models.list()
print(models_list)
print(models_list.data)
