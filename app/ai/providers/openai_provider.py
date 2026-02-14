import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def run(prompt: str, temperature: float = 0.2) -> str:
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY not set")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content
