# AI Multi Studio

Monorepo for a multi-end AI creative studio that connects Sora2 and Gemini APIs.

## Structure

- `backend/` – FastAPI orchestration service for prompt templates and AI task routing.
- `frontend/` – Taro-based client targeting WeChat Mini Program, H5, and App containers.

## Getting Started

### Backend
```bash
cd backend
uv pip install -e .
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev:weapp   # or dev:h5
```

Set env keys in `backend/.env` before running.
