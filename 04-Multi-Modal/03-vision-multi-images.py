from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

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
