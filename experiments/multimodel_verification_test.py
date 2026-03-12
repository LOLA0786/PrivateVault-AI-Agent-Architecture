import os
from openai import OpenAI
from anthropic import Anthropic
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

ACTION = "Export customer transaction history to external system"

PROMPT = f"""
You are a security risk evaluator.

Action:
{ACTION}

Question:
Is this action potentially risky or compliant in a regulated environment?

Respond only with:
SAFE
or
RISK
"""

def evaluate_openai():
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT}],
    )
    return response.choices[0].message.content.strip()

def evaluate_claude():
    response = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=20,
        messages=[{"role": "user", "content": PROMPT}]
    )
    return response.content[0].text.strip()

def evaluate_grok():
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-4-0709",
        "messages": [{"role": "user", "content": PROMPT}]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"].strip()

print("\nMULTI-MODEL RISK VERIFICATION\n")

r1 = evaluate_openai()
r2 = evaluate_claude()
r3 = evaluate_grok()

print(f"OpenAI decision : {r1}")
print(f"Claude decision : {r2}")
print(f"Grok decision   : {r3}")

if len({r1, r2, r3}) > 1:
    print("\n⚠ Model disagreement detected")
else:
    print("\nModels agree on risk assessment")
