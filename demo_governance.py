"""
PrivateVault Governance Demo
Shows APPROVE, REVIEW, BLOCK decisions + audit logging.
"""

from safety_layer import enforce
from pathlib import Path
import json

tests = [
    {"amount": 500},  # safe
    {"amount": 150000},  # review
    {"amount": 200000, "external_transfer": True},  # block
]

print("\n--- Governance Decision Demo ---\n")

for action in tests:
    decision = enforce(action)
    print(f"Action: {action}")
    print(f"Decision: {decision}")
    print("-" * 40)

print("\nLatest Audit Log Entries:\n")

ledger = Path("ai_firewall_ledger.jsonl")

if ledger.exists():
    lines = ledger.read_text().strip().split("\n")[-3:]
    for line in lines:
        print(json.dumps(json.loads(line), indent=2))
else:
    print("No ledger file found.")
