import hashlib
import json
import time
import os

LEDGER_FILE = "merkle_ledger.jsonl"

def sha(data):
    return hashlib.sha256(data.encode()).hexdigest()

def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []

    with open(LEDGER_FILE, "r") as f:
        return [json.loads(line) for line in f]

def save_record(record):
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

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

    save_record(record)

    return record

def get_hashes():
    ledger = load_ledger()
    return [r["hash"] for r in ledger]

def merkle_root():
    hashes = get_hashes()

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
    hashes = get_hashes()
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
