import json
import hashlib
from app.policy.policy_matrix import resolve_action
from app.observability.metrics import REQUEST_TOTAL, BLOCK_TOTAL, REQUEST_LATENCY
import time
import os
import hashlib
import yaml
import json
import requests
from pydantic import ValidationError
from app.models.database import SessionLocal
from app.models.schemas import AuditLog
from app.models.ai_schemas import ClassificationResult
from app.agents.policy import enforce_policy
from app.orchestrator import governance_flow

GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_URL = "https://api.x.ai/v1/chat/completions"

def hash_text(text: str):
    return hashlib.sha256(text.encode()).hexdigest()

def load_prompt(prompt_id: str):
    with open(f"app/prompts/{prompt_id}.yaml", "r") as f:
        return yaml.safe_load(f)

def call_grok(model, prompt, temperature):
    response = requests.post(
        GROK_URL,
        headers={
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def execute_ai(request):
    prompt = f"""
Classify the following text and return JSON only:

{{"sensitivity": "LOW|HIGH", "contains_pii": true|false, "risk_score": 0-1}}

Text:
{request.input_text}
"""

    raw_output = call_grok("grok-4-latest", prompt, 0.2)

    try:
        classification = json.loads(raw_output)
    except Exception:
        raise Exception("Invalid AI response format")

    governance = {
        "policy": {
            "action": "BLOCK" if classification["sensitivity"] == "HIGH" else "ALLOW",
            "reason": "High sensitivity data detected"
            if classification["sensitivity"] == "HIGH"
            else "No policy violations"
        },
        "risk": {
            "risk_level": classification["sensitivity"]
        }
    }

    ledger_hash = hashlib.sha256(
        json.dumps(classification).encode()
    ).hexdigest()

    return {
        "tenant_id": request.tenant_id,
        "classification": classification,
        "governance": governance,
        "ledger_hash": ledger_hash
    }
