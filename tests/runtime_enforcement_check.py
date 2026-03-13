import json
import datetime
from pv_tool_guard import enforce_tool_policy
from pv_receipt import create_receipt
from pv_merkle_log import merkle_root

tenant = "enterprise_demo"

tests = [
    {"tool": "delete_database", "expected": "blocked"},
    {"tool": "send_email", "expected": "allowed"},
    {"tool": "export_customer_data", "expected": "blocked"},
    {"tool": "read_docs", "expected": "allowed"}
]

results = []

for t in tests:
    decision = enforce_tool_policy(tenant=tenant, tool=t["tool"])
    receipt = create_receipt(
        agent="test_agent",
        action=t["tool"],
        result=decision["status"],
        model="governance-test"
    )

    results.append({
        "tool": t["tool"],
        "expected": t["expected"],
        "actual": decision["status"],
        "receipt_hash": receipt["hash"][:10]
    })

print("\nPRIVATEVAULT RUNTIME ENFORCEMENT TEST\n")

for r in results:
    status = "PASS" if r["expected"] == r["actual"] else "FAIL"
    print(f"{status} | tool={r['tool']} | expected={r['expected']} | actual={r['actual']} | receipt={r['receipt_hash']}")

print("\nMerkle Root:")
print(merkle_root())

print("\nTimestamp:", datetime.datetime.now(datetime.UTC).isoformat())
