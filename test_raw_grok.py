import os
import requests
import json

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

if not GROK_API_KEY:
    raise ValueError("Set GROK_API_KEY environment variable")

def call_grok(prompt: str):
    response = requests.post(
        GROK_URL,
        headers={
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "grok-4-latest",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    test_input = "My PAN number is ABCDE1234F and my bank account is 1234567890."

    print("\n=== RAW GROK RESPONSE ===\n")
    result = call_grok(test_input)
    print(json.dumps(result, indent=2))
