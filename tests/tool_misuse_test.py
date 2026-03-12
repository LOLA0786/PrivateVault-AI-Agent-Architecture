import json

AGENT_ACTION = {
    "tool": "transfer_funds",
    "arguments": {
        "amount": 25000,
        "currency": "USD",
        "destination": "external_account"
    }
}

POLICY_LIMIT = 5000

def enforce_policy(action):
    if action["arguments"]["amount"] > POLICY_LIMIT:
        return {"status": "blocked", "reason": "exceeds_limit"}
    return {"status": "allowed"}

print(json.dumps(enforce_policy(AGENT_ACTION), indent=2))
