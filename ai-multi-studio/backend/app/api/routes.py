from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_client import ai_client

router = APIRouter(prefix="/ai", tags=["ai"])


class PromptPayload(BaseModel):
    prompt: str = Field(..., description="用户自定义或模板生成的提示词")
    mode: str = Field("video", description="video 或 image")
    meta: dict[str, str] | None = Field(default=None, description="附加参数，如行业、风格")


@router.post("/generate")
async def generate_asset(payload: PromptPayload):
    try:
        if payload.mode == "video":
            result = await ai_client.generate_video({
                "prompt": payload.prompt,
                "metadata": payload.meta or {},
            })
        else:
            result = await ai_client.generate_image({
                "prompt": payload.prompt,
                "metadata": payload.meta or {},
            })
        return {"status": "queued", "result": result}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=str(exc)) from exc
