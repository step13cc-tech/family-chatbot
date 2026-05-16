import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
BOT_NAME = os.getenv("BOT_NAME", "家族ボット")
BOT_PERSONALITY = os.getenv(
    "BOT_PERSONALITY",
    "やさしく、短めに、日本語で話す家族のような口調",
)
