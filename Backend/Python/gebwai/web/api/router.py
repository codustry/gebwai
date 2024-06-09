from fastapi.routing import APIRouter

from gebwai.web.api import echo, monitoring, LINE

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(LINE.router, prefix="/line", tags=["line"])
