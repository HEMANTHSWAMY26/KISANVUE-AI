import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Reconfigure stdout for utf-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / ".env")

api_key = os.getenv("GEMINI_API_KEY", "").strip()

print("=" * 60)
print("KISANVUE AI — DIRECT GOOGLE GEMINI CONNECTIVITY VALIDATION")
print("=" * 60)

if not api_key:
    print("\nRESULT: FAILED")
    print("STATUS: GEMINI_API_KEY is missing")
    print("DETAIL: No API key was found in backend/.env. Please configure GEMINI_API_KEY to activate live Google Gemini calls.")
    sys.exit(1)

print(f"API Key detected (length: {len(api_key)} chars). Initializing google-genai SDK...")

try:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    print("google.genai.Client created successfully.")
    
    candidate_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash"]
    success = False
    
    for model_name in candidate_models:
        try:
            print(f"Calling Gemini model '{model_name}'...")
            response = client.models.generate_content(
                model=model_name,
                contents="You are an agricultural diagnostic system. Respond strictly with: {'status': 'connected', 'engine': 'Google Gemini'}"
            )
            if response and response.text:
                print("\nRESULT: SUCCESS")
                print("STATUS: CONNECTED")
                print("PROVIDER: Google Gemini")
                print("MODEL USED:", model_name)
                print("RAW RESPONSE:", response.text.strip())
                success = True
                break
        except Exception as e:
            print(f"Model '{model_name}' notice: {e}")

    if success:
        sys.exit(0)
    else:
        print("\nRESULT: FAILED")
        print("STATUS: GEMINI_API_CALL_ERROR")
        sys.exit(1)

except Exception as err:
    print("\nRESULT: FAILED")
    print("STATUS: GEMINI_API_CALL_ERROR")
    print("ERROR DETAIL:", str(err))
    sys.exit(1)
