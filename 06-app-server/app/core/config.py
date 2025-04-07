from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM Learning API"
    
    # DeepSeek 配置
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: Optional[str] = None
    
    # OpenAI 配置
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    
    # OpenRouter 配置
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: Optional[str] = None
    
    # 阿里云配置
    ALIYUN_API_KEY: Optional[str] = None
    ALIYUN_BASE_URL: Optional[str] = None
    
    # 高德地图配置
    AMAP_API_KEY: Optional[str] = None
    
    # 服务器配置
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 