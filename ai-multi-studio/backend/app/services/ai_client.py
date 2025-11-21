from __future__ import annotations

from typing import Any, Dict

import httpx

from app.core.config import settings


class AIClient:
    def __init__(self) -> None:
        self._http = httpx.AsyncClient(timeout=30.0)

    async def generate_video(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self._http.post(
            f"{settings.sora_base_url}/v1/videos",
            headers={"Authorization": f"Bearer {settings.sora_api_key}"},
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def generate_image(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self._http.post(
            f"{settings.gemini_base_url}/v1beta/models/gemini-pro-vision:generate",
            params={"key": settings.gemini_api_key},
            json=payload,
        )
        response.raise_for_status()
        return response.json()


ai_client = AIClient()
