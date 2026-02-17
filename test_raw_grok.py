import os
import requests

URL = "https://api.x.ai/v1/chat/completions"

def call_grok(prompt: str):
    api_key = os.getenv("XAI_API_KEY")

    if not api_key:
        raise RuntimeError("❌ XAI_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-4",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(URL, headers=headers, json=payload)

    # debug output if API rejects request
    if response.status_code != 200:
        print("\n--- DEBUG RESPONSE ---")
        print(response.text)
        print("----------------------\n")

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    test_input = input("Enter prompt: ")
    result = call_grok(test_input)

    print("\n=== RAW GROK RESPONSE ===\n")
    print(result["choices"][0]["message"]["content"])
