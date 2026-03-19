import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_model(prompt, model="qwen/qwen3-next-80b-a3b-instruct"):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"OpenRouter error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
