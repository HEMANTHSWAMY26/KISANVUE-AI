import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
_models = [GEMINI_MODEL, "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash"]
FALLBACK_MODELS = list(dict.fromkeys([m for m in _models if m]))

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Agricultural Monitoring Defaults (Guntur, AP - National Chilli Capital)
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "16.3067"))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "80.4365"))
DEFAULT_LOCATION_NAME = os.getenv("DEFAULT_LOCATION_NAME", "Guntur, Andhra Pradesh, India")
