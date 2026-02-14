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
    db = SessionLocal()

    prompt_config = load_prompt("classifier_v1")

    full_prompt = f"""
{prompt_config["instruction"]}

Respond ONLY with valid JSON.
No explanation.
No markdown.

TEXT:
{request.input_text}
"""

    raw_output = call_grok(
        model="grok-4-latest",
        prompt=full_prompt,
        temperature=prompt_config["temperature"]
    )

    try:
        parsed = ClassificationResult.model_validate(json.loads(raw_output))
    except (json.JSONDecodeError, ValidationError) as e:
        db.close()
        return {"error": "Invalid AI response format", "details": str(e), "raw": raw_output}

    output_hash = hash_text(raw_output)

    # HASH CHAINING
    last_entry = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    previous_hash = last_entry.current_hash if last_entry else "GENESIS"
    current_hash = hash_text(previous_hash + output_hash)

    log = AuditLog(
        tenant_id=request.tenant_id,
        user_id=request.user_id,
        prompt_id=prompt_config["id"],
        output_hash=output_hash,
        previous_hash=previous_hash,
        current_hash=current_hash
    )

    db.add(log)
    db.commit()

    # MULTI-AGENT FLOW
    flow_result = governance_flow(parsed.model_dump())

    db.close()

    return {
        "tenant_id": request.tenant_id,
        "classification": parsed.model_dump(),
        "governance": flow_result,
        "ledger_hash": current_hash
    }
