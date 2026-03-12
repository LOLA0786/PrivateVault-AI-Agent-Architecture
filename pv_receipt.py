import hashlib
import json
import time

previous_hash = "GENESIS"

def create_receipt(agent, action, result, model):
    global previous_hash
    
    record = {
        "agent": agent,
        "action": action,
        "result": result,
        "model": model,
        "timestamp": time.time(),
        "previous_hash": previous_hash
    }

    encoded = json.dumps(record, sort_keys=True).encode()
    receipt_hash = hashlib.sha256(encoded).hexdigest()

    record["hash"] = receipt_hash
    previous_hash = receipt_hash

    print(json.dumps(record, indent=2))

create_receipt(
    agent="fraud_agent",
    action="execute_payment",
    result="blocked",
    model="grok-4"
)
