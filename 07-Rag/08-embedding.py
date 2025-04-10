from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("ALIYUN_API_KEY"),base_url=os.getenv("ALIYUN_BASE_URL"))

response = client.embeddings.create(
    model="text-embedding-v3",
    input="greenday 乐队"
)

print(response.data[0].embedding)
