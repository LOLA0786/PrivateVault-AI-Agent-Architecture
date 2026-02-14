import os
import requests

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

def call_grok(prompt: str):
    for attempt in range(3):
        try:
            response = requests.post(
                GROK_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-4-latest",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0
                },
                timeout=5,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == 2:
                raise
