from app.ai.model_router import run_model
from app.governance.policy_loader import load_policy
from app.governance.engine import evaluate
from app.metrics.prometheus import REQUEST_COUNT, BLOCK_COUNT, ALLOW_COUNT, REQUEST_LATENCY

import json
import hashlib
import time


def classifier_agent(input_text: str, tenant_id: str):
    prompt = f"""
Classify the following text and return JSON only:

{{"sensitivity": "LOW|HIGH", "contains_pii": true|false, "risk_score": 0-1}}

Text:
{input_text}
"""

    raw_output = run_model(
        prompt=prompt,
        tenant_id=tenant_id,
        temperature=0.2
    )

    return json.loads(raw_output)


def risk_agent(classification: dict, tenant_id: str):
    if tenant_id == "fintech" and classification["sensitivity"] == "HIGH":
        classification["risk_score"] = min(1.0, classification["risk_score"] + 0.1)

    return classification


def policy_agent(classification: dict, tenant_id: str):
    policy = load_policy(tenant_id)
    return evaluate(classification, policy)


def audit_agent(classification: dict):
    return hashlib.sha256(
        json.dumps(classification).encode()
    ).hexdigest()


def run_pipeline(input_text: str, tenant_id: str, user_id: str):
    REQUEST_COUNT.inc()

    start = time.time()

    classification = classifier_agent(input_text, tenant_id)
    classification = risk_agent(classification, tenant_id)
    decision = policy_agent(classification, tenant_id)
    ledger_hash = audit_agent(classification)

    if decision["action"] == "BLOCK":
        BLOCK_COUNT.inc()
    else:
        ALLOW_COUNT.inc()

    REQUEST_LATENCY.observe(time.time() - start)

    return {
        "tenant_id": tenant_id,
        "classification": classification,
        "governance": {
            "policy": decision,
            "risk": {
                "risk_level": classification["sensitivity"]
            }
        },
        "ledger_hash": ledger_hash
    }
