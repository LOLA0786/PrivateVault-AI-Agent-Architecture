"""
Safety enforcement rules
"""

POLICY_VERSION = "2026-02-25-v1"

def enforce(action):

    if action.get("pii"):
        return "BLOCK"

    if action.get("amount", 0) > 100000:
        return "REVIEW"

    return "APPROVE"
