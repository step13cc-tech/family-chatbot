from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.llm import chat_completion
from app.models import AVAILABLE_MODELS, default_model_id, resolve_model

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"

app = FastAPI(title="Family Chatbot (Groq only)")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/api/models")
async def list_models() -> dict:
    return {
        "models": AVAILABLE_MODELS,
        "default": default_model_id(),
    }


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=50)
    model: str | None = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(
        STATIC / "index.html",
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    try:
        history = [{"role": m.role, "content": m.content} for m in body.history]
        reply, model_id = await chat_completion(history, body.message, body.model)
        return ChatResponse(reply=reply, model=model_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
