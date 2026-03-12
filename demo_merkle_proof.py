from pv_merkle_log import create_receipt, merkle_root, generate_proof
import json

create_receipt("fraud_agent", "transfer_attempt", "blocked", "grok-4")
create_receipt("payment_agent", "execute_payment", "allowed", "grok-4")
create_receipt("analysis_agent", "export_data", "blocked", "grok-4")

root = merkle_root()
proof = generate_proof(0)

print("\nPRIVATEVAULT EXECUTION RECEIPT\n")
print("Merkle Root:")
print(root)

print("\nProof for first decision:")
print(json.dumps(proof, indent=2))
