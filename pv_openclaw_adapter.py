import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4-latest")

GROK_URL = "https://api.x.ai/v1/chat/completions"

def call_grok(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROK_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(GROK_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    return {
        "model": data.get("model"),
        "content": data["choices"][0]["message"]["content"],
        "raw": data
    }
