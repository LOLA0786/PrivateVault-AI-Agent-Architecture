import datetime
from pv_tool_guard import evaluate_output

tests = [
    '{"action":"send_email"}',
    '{"action":"delete_database"}',
    '{"action":"transfer_funds"}',
    '{"action":"read_docs"}'
]

print("\nPRIVATEVAULT OUTPUT GOVERNANCE TEST\n")

for t in tests:
    allowed, violations = evaluate_output(t)

    status = "ALLOWED" if allowed else "BLOCKED"

    print(f"{status} | input='{t}' | violations={violations}")

print("\nTimestamp:", datetime.datetime.now(datetime.UTC).isoformat())
