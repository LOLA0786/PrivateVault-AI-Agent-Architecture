import os
import httpx

GROK_ENDPOINT = "https://api.x.ai/v1/chat/completions"

async def call_grok(messages):
    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        return {
            "mode": "mock",
            "model": "grok",
            "response": "mock response",
            "fingerprint": "mock"
        }

    # convert plain text messages to structured format
    formatted_messages = []
    for m in messages:
        formatted_messages.append({
            "role": m["role"],
            "content": [
                {"type": "text", "text": m["content"]}
            ]
        })

    payload = {
        "model": "grok-4-0709",
        "messages": messages
    }

    timeout = httpx.Timeout(60.0, connect=20.0)
    async with httpx.AsyncClient(http2=False, timeout=timeout) as client:
        for attempt in range(3):
            try:
                resp = await client.post(
                    GROK_ENDPOINT,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-4-fast-reasoning",
                        "messages": messages,
                        "temperature": 0,
                        "max_tokens": 50
                    }
                )
                resp.raise_for_status()
                break
            except Exception as e:
                if attempt == 2:
                    raise
    data = resp.json()

    return {
        "mode": "live",
        "model": data.get("model"),
        "response": data["choices"][0]["message"]["content"],
        "usage": data.get("usage", {}),
        "fingerprint": data.get("system_fingerprint")
    }
