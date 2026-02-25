import os
import requests
import asyncio

API_KEY = os.getenv("GROK_API_KEY")

async def run(prompt, model="grok-4"):

    loop = asyncio.get_event_loop()

    def request():
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            },
            timeout=30
        )
        return r.json()["choices"][0]["message"]["content"]

    text = await loop.run_in_executor(None, request)

    return {
        "model": model,
        "response": text
    }
