from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

class SummaryRequest(BaseModel):
    content: str
    format: str = "markdown"  # 可选：markdown, text, json

class SummaryResponse(BaseModel):
    summary: str

@router.post("/summary", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest):
    try:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )

        # 构建提示词
        prompt = f"""
        你的任务是为用户提供的内容生成简要总结。
        请把总结主要分为两个方面：优点和缺点。
        请根据内容中提到的缺点给出改进建议。
        请使用{request.format}格式展示总结。

        用户的内容会以三个#符号进行包围。

        ###
        {request.content}
        ###
        """

        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-v3",
            messages=[
                {"role": "system", "content": prompt},
            ],
            stream=False
        )

        return SummaryResponse(
            summary=response.choices[0].message.content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 