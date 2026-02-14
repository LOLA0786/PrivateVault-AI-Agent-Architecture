import os
import logging

from app.ai.providers import grok_provider, openai_provider

PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "grok")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "openai")

logger = logging.getLogger("model_router")

def run_model(prompt: str, tenant_id: str, temperature: float = 0.2) -> str:
    last_error = None

    # Try primary
    try:
        if PRIMARY_MODEL == "grok":
            return grok_provider.run(prompt, temperature)
        elif PRIMARY_MODEL == "openai":
            return openai_provider.run(prompt, temperature)
        else:
            raise Exception(f"Unknown PRIMARY_MODEL: {PRIMARY_MODEL}")
    except Exception as e:
        logger.error(f"Primary model failed for tenant {tenant_id}: {e}")
        last_error = e

    # Try fallback
    try:
        if FALLBACK_MODEL == "grok":
            return grok_provider.run(prompt, temperature)
        elif FALLBACK_MODEL == "openai":
            return openai_provider.run(prompt, temperature)
        else:
            raise Exception(f"Unknown FALLBACK_MODEL: {FALLBACK_MODEL}")
    except Exception as e:
        logger.error(f"Fallback model failed for tenant {tenant_id}: {e}")
        last_error = e

    raise Exception(f"All model providers failed: {last_error}")
