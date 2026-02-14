import os
from app.providers.grok_provider import call_grok

PROVIDER = os.getenv("MODEL_PROVIDER", "grok")

def call_model(prompt: str):
    if PROVIDER == "grok":
        return call_grok(prompt)
    raise ValueError("Unsupported model provider")
