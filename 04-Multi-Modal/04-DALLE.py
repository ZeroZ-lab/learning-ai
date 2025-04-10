from openai import OpenAI
import os
import requests
from datetime import datetime


client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt="一只水晶乌龟",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url
print("\n" + "="*50)
print("Generated image URL:")
print(image_url)

# 下载并保存图片
print("\nDownloading image...")
image_response = requests.get(image_url)
if image_response.status_code == 200:
    # 生成文件名：使用时间戳确保唯一性
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./04-Multi-Modal/dist/crystal_turtle_{timestamp}.png"
    
    # 保存图片
    with open(filename, "wb") as f:
        f.write(image_response.content)
    print(f"✓ Image saved successfully to: {filename}")
else:
    print("✗ Failed to download image")
print("="*50)
