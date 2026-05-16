from __future__ import annotations

from app.config import GROQ_MODEL

# Groq でよく使うモデル（サイトから選べる一覧）
AVAILABLE_MODELS: list[dict[str, str]] = [
    {
        "id": "llama-3.3-70b-versatile",
        "label": "Llama 3.3 70B（バランス・おすすめ）",
    },
    {
        "id": "llama-3.1-70b-versatile",
        "label": "Llama 3.1 70B",
    },
    {
        "id": "llama-3.1-8b-instant",
        "label": "Llama 3.1 8B（速い）",
    },
    {
        "id": "mixtral-8x7b-32768",
        "label": "Mixtral 8x7B",
    },
    {
        "id": "gemma2-9b-it",
        "label": "Gemma 2 9B",
    },
]

ALLOWED_MODEL_IDS = {m["id"] for m in AVAILABLE_MODELS}


def default_model_id() -> str:
    if GROQ_MODEL in ALLOWED_MODEL_IDS:
        return GROQ_MODEL
    return AVAILABLE_MODELS[0]["id"]


def resolve_model(requested: str | None) -> str:
    if requested and requested in ALLOWED_MODEL_IDS:
        return requested
    return default_model_id()
