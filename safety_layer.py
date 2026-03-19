"""
Safety enforcement rules
"""

POLICY_VERSION = "2026-02-25-v1"

def enforce(action):
    # --- deny rules ---
    if isinstance(action, dict):
        tool = action.get("tool") or action.get("action")
        params = action.get("params", {})
        if tool == "transfer_money":
            amount = params.get("amount", action.get("amount", 0))
            if amount >= 1:
                return "BLOCKED: financial risk"
        if tool == "external_api_call":
            return "BLOCKED: data exfiltration"


    if action.get("pii"):
        return "BLOCK"

    if action.get("amount", 0) > 100000:
        return "REVIEW"

    return "APPROVE"
