from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

# 因为网络问题，使用阿里云平台中的DeepSeek代替
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

IMAGE_PATH = "./04-Multi-Modal/data/image-1.png"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "描述这张照片",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这些照片是什么，他们有什么区别？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bkimg.cdn.bcebos.com/pic/bd315c6034a85edf55d3739744540923dd547523",
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bkimg.cdn.bcebos.com/pic/500fd9f9d72a6059252d39d2626d239b033b5ab50cfb",
                    },
                },
            ],
        },
    ],
    stream=False,
    temperature=0.0,
)

print(response.choices[0].message.content)
