from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
        
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-v3",
            messages=[msg.dict() for msg in request.messages],
            stream=False
        )
        
        return ChatResponse(
            response=response.choices[0].message.content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 