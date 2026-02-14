import os
from app.providers.grok import call_grok

PROVIDER = os.getenv("MODEL_PROVIDER", "grok")

def call_model(prompt):
    if PROVIDER == "grok":
        return call_grok(prompt)
    raise ValueError("Unknown provider")
