import hashlib
import json
import time

ledger = []

def sha(data):
    return hashlib.sha256(data.encode()).hexdigest()

def create_receipt(agent, action, result, model):
    record = {
        "agent": agent,
        "action": action,
        "result": result,
        "model": model,
        "timestamp": time.time()
    }

    encoded = json.dumps(record, sort_keys=True)
    record_hash = sha(encoded)

    record["hash"] = record_hash
    ledger.append(record)

    return record

def merkle_root():
    hashes = [r["hash"] for r in ledger]

    if not hashes:
        return None

    while len(hashes) > 1:
        new_level = []

        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left
            new_level.append(sha(left + right))

        hashes = new_level

    return hashes[0]

def generate_proof(index):
    hashes = [r["hash"] for r in ledger]
    proof = []

    while len(hashes) > 1:
        new_level = []

        for i in range(0, len(hashes), 2):
            left = hashes[i]
            right = hashes[i+1] if i+1 < len(hashes) else left

            if i == index or i+1 == index:
                sibling = right if i == index else left
                proof.append(sibling)
                index = i // 2

            new_level.append(sha(left + right))

        hashes = new_level

    return proof
