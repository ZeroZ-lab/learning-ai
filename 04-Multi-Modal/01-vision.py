from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")
)

IMAGE_PATH = "./04-Multi-Modal/data/image-1.png"

print("\n" + "="*50)
print(f"Processing image: {IMAGE_PATH}")
print("="*50 + "\n")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)
print("✓ Image encoded successfully\n")

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that responds in Markdown.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": ""},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
            ],
        },
    ],
    stream=False,
    temperature=0.0,
)

print("="*50)
print("Response:")
print("="*50)
print(response.choices[0].message.content)
print("="*50)
