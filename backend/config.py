# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ ERROR: GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")