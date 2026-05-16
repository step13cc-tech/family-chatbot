from __future__ import annotations

import httpx

from app.config import BOT_NAME, BOT_PERSONALITY, GROQ_API_KEY, GROQ_MODEL

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


def build_system_prompt() -> str:
    return (
        f"あなたは{BOT_NAME}です。{BOT_PERSONALITY}。"
        "これまでの会話を踏まえて自然に返答してください。"
    )


async def chat_completion(history: list[dict[str, str]], user_text: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY を .env に設定してください")

    messages = [{"role": "system", "content": build_system_prompt()}, *history]
    messages.append({"role": "user", "content": user_text})

    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(
            GROQ_CHAT_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "temperature": 0.7,
            },
        )
        res.raise_for_status()
        data = res.json()

    return data["choices"][0]["message"]["content"].strip()
