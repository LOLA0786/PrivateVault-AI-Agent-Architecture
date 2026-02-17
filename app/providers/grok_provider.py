import os
import requests
import asyncio

URL = "https://api.x.ai/v1/chat/completions"

async def call_grok(messages):
    """
    Accepts either:
    - string prompt
    - list of {role, content}
    """

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY not set")

    # ✅ normalize input
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
        return requests.post(URL, headers=headers, json=payload)

    response = await loop.run_in_executor(None, send)

    if response.status_code != 200:
        print("\nGrok error:", response.text)

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
