def enforce_policy(classification_result):
    if classification_result["sensitivity"] == "HIGH":
        return {
            "action": "BLOCK",
            "reason": "High sensitivity data detected"
        }

    return {
        "action": "ALLOW",
        "reason": "No policy violations"
    }
