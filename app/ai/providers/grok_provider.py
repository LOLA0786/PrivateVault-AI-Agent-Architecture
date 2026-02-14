import os
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

def run(prompt: str, temperature: float = 0.2) -> str:
    if not GROK_API_KEY:
        raise Exception("GROK_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-4-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post(GROK_API_URL, json=payload, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]
