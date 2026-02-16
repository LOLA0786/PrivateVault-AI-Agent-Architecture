"""
PrivateVault Safety Layer
Deterministic enforcement before execution.
This layer cannot be bypassed.
"""

from datetime import datetime
import json
from pathlib import Path

LEDGER_FILE = Path("ai_firewall_ledger.jsonl")

# --- Policy thresholds ---
MAX_AMOUNT = 100000
MAX_RISK_SCORE = 0.70


def risk_score(action: dict) -> float:
    """
    Simple deterministic risk scoring.
    Extend later with ML signals.
    """
    score = 0.0

    if action.get("amount", 0) > MAX_AMOUNT:
        score += 0.5

    if action.get("sensitive"):
        score += 0.3

    if action.get("external_transfer"):
        score += 0.3

    return min(score, 1.0)


def policy_check(action: dict) -> str:
    """
    Deterministic policy enforcement.
    Returns: APPROVE | REVIEW | BLOCK
    """
    score = risk_score(action)

    if score > MAX_RISK_SCORE:
        return "BLOCK"

    if score > 0.4:
        return "REVIEW"

    return "APPROVE"


def log_decision(action: dict, decision: str):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "decision": decision
    }

    with LEDGER_FILE.open("a") as f:
        f.write(json.dumps(record) + "\n")


def enforce(action: dict) -> str:
    """
    Main safety gate.
    """
    decision = policy_check(action)
    log_decision(action, decision)
    return decision
