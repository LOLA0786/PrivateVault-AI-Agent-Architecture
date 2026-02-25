import os
import requests
import asyncio
import hashlib

URL = "https://api.x.ai/v1/chat/completions"

async def call_grok(messages):

    api_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("GROK_API_KEY not set")

    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    payload = {
        "model": "grok-4",
        "messages": messages,
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    loop = asyncio.get_event_loop()

    def send():
        try:
            return requests.post(URL, headers=headers, json=payload, timeout=25)
        except Exception as e:
            return None

    response = await loop.run_in_executor(None, send)

    if response is None or not response.text:
        return {
            "model": "grok-4",
            "response": "Risk explanation unavailable (network/API issue).",
            "fingerprint": "na",
            "usage": {}
        }

    try:
        data = response.json()
        text = data["choices"][0]["message"]["content"]
    except Exception:
        text = response.text[:200]

    fingerprint = hashlib.sha256(text.encode()).hexdigest()[:16]

    return {
        "model": "grok-4",
        "response": text,
        "fingerprint": fingerprint,
        "usage": {}
    }
