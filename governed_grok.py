import os
import requests
import asyncio

API_KEY = os.getenv("GROK_API_KEY")

BLOCK_KEYWORDS = ["password", "credit card", "ssn", "pii"]

async def run(prompt, model="grok-4"):

    for word in BLOCK_KEYWORDS:
        if word in prompt.lower():
            return {
                "model": model,
                "response": "Response blocked due to policy violation.",
                "blocked": True,
                "policy_triggered": "SENSITIVE_DATA"
            }

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
                    {"role": "system", "content": "You are a safe AI assistant."},
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
        "response": text,
        "blocked": False,
        "policy_triggered": None
    }
