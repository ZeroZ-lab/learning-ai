from pathlib import Path
from openai import OpenAI


client = OpenAI()

speech_file_path = Path(__file__).parent / "dist" / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="一只水晶乌龟"
)

#将response写入文件
with open(speech_file_path, "wb") as f:
    f.write(response.content)

print(f"✓ Speech saved successfully to: {speech_file_path}")