from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

print("\n" + "="*50)
print("Initializing OpenAI client...")
print("="*50 + "\n")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

print("✓ Client initialized successfully\n")

print("="*50)
print("Sending request to OpenAI API...")
print("="*50 + "\n")

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
                {"type": "text", "text": ""},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bkimg.cdn.bcebos.com/pic/bd315c6034a85edf55d3739744540923dd547523",
                        "detail": "high",
                    },
                },
            ],
        },
    ],
    stream=False,
    temperature=0.0,
)

print("✓ API request completed successfully\n")

print("="*50)
print("Response:")
print("="*50)
print(response.choices[0].message.content)
print("="*50)
