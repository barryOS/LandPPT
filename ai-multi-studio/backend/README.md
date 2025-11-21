# AI Multi Studio Backend

FastAPI-based orchestration layer for Sora2 and Gemini integrations.

## Quickstart

```bash
uv pip install -e .
uvicorn app.main:app --reload
```

Expose the following env vars via `.env`:

```
SORA_API_KEY="sk-..."
GEMINI_API_KEY="ya29..."
```
