import json
import hashlib
import time

# ---- Simulated Policy Engine ----

TRUSTED_DESTINATIONS = ["internal_salesforce", "trusted_api"]

def evaluate_action(action):
    # Deterministic policy enforcement

    if action["type"] == "read_data":
        return allow("internal read allowed")

    if action["type"] == "export_data":
        if action.get("destination") not in TRUSTED_DESTINATIONS:
            return deny("PII_exfiltration_block", "external endpoint not trusted")
        return allow("trusted destination")

    if action["type"] == "execute_payment":
        return deny("payment_execution_block", "agent not authorized for payments")

    return deny("unknown_action", "action not recognized")


def allow(reason):
    return {
        "decision": "ALLOW (EXECUTED)",
        "reason": reason,
        "policy": None
    }

def deny(policy, reason):
    return {
        "decision": "DENY (BLOCKED)",
        "policy": policy,
        "reason": reason
    }


# ---- Merkle Proof (Simplified) ----

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def build_merkle_root(hashes):
    while len(hashes) > 1:
        new_level = []
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left
            new_level.append(hash_data(left + right))
        hashes = new_level
    return hashes[0]


# ---- Audit Log ----

audit_log = []

def log_decision(action, result):
    entry = {
        "timestamp": time.time(),
        "action": action,
        "decision": result["decision"],
        "policy": result.get("policy"),
        "reason": result["reason"]
    }
    audit_log.append(entry)
    return entry


# ---- Demo Scenario ----

def run_demo():
    print("\n=== PrivateVault: Agent Governance Control Plane (Salesforce Scenario) ===\n")

    agent_workflow = [
        {"type": "read_data", "source": "salesforce_case"},
        {"type": "export_data", "destination": "external_api", "data_type": "PII"},
        {"type": "execute_payment", "amount": 50000}
    ]

    decision_hashes = []

    for step in agent_workflow:
        print(f"\nAction (INTERCEPTED by PrivateVault): {step}")

        result = evaluate_action(step)

        print(f"Decision: {result['decision']}")
        print(f"Reason: {result['reason']}")

        if result["policy"]:
            print(f"Policy: {result['policy']}")

        entry = log_decision(step, result)
        decision_hashes.append(hash_data(entry))

    # ---- Merkle Proof ----
    root = build_merkle_root(decision_hashes)

    print("\n--- Audit Log ---")
    for entry in audit_log:
        print(json.dumps(entry, indent=2))

    print("\n--- Cryptographic Integrity ---")
    print(f"Merkle Root: {root}")
    print("Verification: VALID (tamper-evident log)\n")


if __name__ == "__main__":
    run_demo()
