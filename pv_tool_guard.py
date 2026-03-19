import json
from datetime import datetime, timezone

LEDGER_FILE = "ai_firewall_ledger.jsonl"

BLOCKED_ACTIONS = [
    "approve_payment",
    "transfer_money"
]

def normalize_action(action: str):
    action = action.lower()

    if "approve" in action or "payment" in action:
        return "approve_payment"

    if "transfer" in action:
        return "transfer_money"

    return action


def evaluate_output(output_text: str):
    violations = []

    try:
        parsed = json.loads(output_text)

        raw_action = parsed.get("action", "")
        action = normalize_action(raw_action)

        amount = parsed.get("amount", 0)

        # 🚨 Rule 1: blocked action
        if action in BLOCKED_ACTIONS:
            violations.append(f"blocked_action:{action}")

        # 🚨 Rule 2: high-risk amount
        if amount and amount > 100000:
            violations.append("high_amount")

        # 🚨 Rule 3: override attempt
        if parsed.get("override") is True:
            violations.append("override_attempt")

    except Exception:
        return True, []

    if violations:
        return False, violations

    return True, []


def log_event(prompt, model, output, allowed, violations):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt": prompt,
        "allowed": allowed,
        "violations": violations,
        "output_excerpt": str(output)[:300]
    }

    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
