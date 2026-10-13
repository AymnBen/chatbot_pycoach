import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
BASE_URL = os.getenv("BASE_URL_GROQ", "https://api.groq.com/openai/v1")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
TIMEOUT = float(os.getenv("MODEL_TIMEOUT", "45"))
ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
