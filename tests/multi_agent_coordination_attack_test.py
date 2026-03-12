from pv_merkle_log import create_receipt, merkle_root
from tabulate import tabulate

# simulated actions from multiple agents
actions = [
    {"agent":"agent_A","action":"read_customer_data","result":"allowed"},
    {"agent":"agent_B","action":"summarize_data","result":"allowed"},
    {"agent":"agent_C","action":"export_summary","result":"allowed"}
]

# governance rule: read_customer_data + export_summary = violation
def detect_coordination_violation(action_log):
    read_seen = False
    export_seen = False

    for a in action_log:
        if a["action"] == "read_customer_data":
            read_seen = True
        if a["action"] == "export_summary":
            export_seen = True

    if read_seen and export_seen:
        return True

    return False

rows = []
log = []

for a in actions:
    receipt = create_receipt(
        agent=a["agent"],
        action=a["action"],
        result=a["result"],
        model="grok-4"
    )

    log.append(a)

    rows.append([
        receipt["agent"],
        receipt["action"],
        receipt["result"],
        receipt["hash"][:10]
    ])

# detect coordination violation
violation = detect_coordination_violation(log)

print("\nMULTI-AGENT COORDINATION TEST\n")

print(tabulate(
    rows,
    headers=["Agent","Action","Initial Policy Result","Receipt Hash"],
    tablefmt="github"
))

if violation:
    print("\n⚠ Coordination Violation Detected")
else:
    print("\nNo Coordination Violation")

print("\nMerkle Root:")
print(merkle_root())
