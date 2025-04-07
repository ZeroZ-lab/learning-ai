from fastapi import APIRouter
from .chat import router as chat_router
from .summary import router as summary_router
from .redbook import router as redbook_router
from .weather import router as weather_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["chat"])
router.include_router(summary_router, prefix="/summary", tags=["summary"])
router.include_router(redbook_router, prefix="/redbook", tags=["redbook"])
router.include_router(weather_router, prefix="/weather", tags=["weather"]) 