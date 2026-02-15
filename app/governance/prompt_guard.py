import re

BLOCK_PATTERNS = [
    r"ignore previous instructions",
    r"bypass policy",
    r"disable security",
    r"reveal system prompt",
    r"transfer \$?\d+",
    r"delete database",
    r"exfiltrate",
    r"send all data",
    r"admin override"
]

def check_prompt_risk(text: str):
    lowered = text.lower()

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, lowered):
            return {
                "status": "blocked",
                "reason": f"Matched pattern: {pattern}"
            }

    return {"status": "safe"}
