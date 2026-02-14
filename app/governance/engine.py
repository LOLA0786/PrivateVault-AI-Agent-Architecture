def evaluate(classification: dict, policy: dict) -> dict:
    for rule in policy.get("rules", []):
        condition = rule.get("condition", {})

        match = True
        for key, value in condition.items():
            if classification.get(key) != value:
                match = False
                break

        if match:
            return {
                "action": rule.get("action"),
                "reason": "Matched policy rule"
            }

    return {
        "action": "ALLOW",
        "reason": "Default allow"
    }
