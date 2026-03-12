import json
from datetime import datetime, timezone

LEDGER_FILE = "ai_firewall_ledger.jsonl"

BLOCKED_ACTIONS = [
    "approve_payment",
    "system.exec"
]

def evaluate_output(output_text: str):
    violations = []

    try:
        parsed = json.loads(output_text)

        action = parsed.get("action")

        if action in BLOCKED_ACTIONS:
            violations.append(f"blocked_action:{action}")

        if parsed.get("override") is True:
            violations.append("override_attempt")

    except Exception:
        # Not structured JSON; allow natural text
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
        "output_excerpt": output[:300]
    }

    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
