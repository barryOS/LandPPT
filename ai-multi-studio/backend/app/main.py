from fastapi import FastAPI

from app.api.routes import router as ai_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(ai_router, prefix=settings.api_prefix)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
