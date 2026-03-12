from pv_merkle_log import create_receipt, merkle_root
from tabulate import tabulate

agents = [
    {"agent":"research_agent","action":"read_docs","result":"allowed"},
    {"agent":"analysis_agent","action":"export_data","result":"blocked"},
    {"agent":"payment_agent","action":"execute_payment","result":"blocked"},
    {"agent":"fraud_agent","action":"freeze_account","result":"allowed"}
]

rows = []

for a in agents:
    receipt = create_receipt(
        agent=a["agent"],
        action=a["action"],
        result=a["result"],
        model="grok-4"
    )
    rows.append([
        receipt["agent"],
        receipt["action"],
        receipt["result"],
        receipt["hash"][:10]
    ])

root = merkle_root()

print("\nPRIVATEVAULT MULTI-AGENT GOVERNANCE TEST\n")

print(tabulate(
    rows,
    headers=["Agent","Action","Policy Result","Receipt Hash"],
    tablefmt="github"
))

print("\nMerkle Root:")
print(root)
