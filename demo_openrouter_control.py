from openrouter_client import call_model
from pv_tool_guard import evaluate_output, log_event
from pv_merkle_log import create_receipt, merkle_root, generate_proof, load_ledger

import json

def print_table(title, data):
    print(f"\n=== {title} ===")
    max_key = max(len(k) for k in data.keys())
    for k, v in data.items():
        print(f"{k.ljust(max_key)} : {v}")

def run_agent(prompt):
    print("\n=== USER INPUT ===")
    print(prompt)

    response = call_model(
        f"""
Return ONLY valid JSON.

Schema:
{{
  "action": "string",
  "amount": number,
  "to": "string"
}}

User request: {prompt}
"""
    )

    print("\n=== MODEL OUTPUT ===")
    print(response)

    allowed, violations = evaluate_output(response)

    log_event(prompt, "openrouter", response, allowed, violations)

    try:
        parsed = json.loads(response)
        action = parsed.get("action", "unknown")
        amount = parsed.get("amount", "NA")
        to = parsed.get("to", "NA")
    except:
        action, amount, to = "unparsed", "NA", "NA"

    result = "ALLOWED" if allowed else "BLOCKED"

    receipt = create_receipt(
        agent="openrouter-agent",
        action=action,
        result=result,
        model="qwen-openrouter"
    )

    root = merkle_root()

    ledger = load_ledger()
    index = len(ledger) - 1
    proof = generate_proof(index)

    # 📊 TABLE OUTPUTS
    print_table("CONTROL DECISION", {
        "Allowed": allowed,
        "Result": result,
        "Violations": ", ".join(violations) if violations else "None"
    })

    print_table("ACTION DETAILS", {
        "Action": action,
        "Amount": amount,
        "Recipient": to
    })

    print_table("CRYPTO RECEIPT", {
        "Agent": receipt["agent"],
        "Model": receipt["model"],
        "Timestamp": receipt["timestamp"],
        "Hash": receipt["hash"][:16] + "..."
    })

    print_table("MERKLE PROOF", {
        "Root": root[:16] + "..." if root else None,
        "Proof": ", ".join([p[:10] + "..." for p in proof]) if proof else "None",
        "Index": index
    })

    if allowed:
        print("\n=== EXECUTION ===")
        print("Executing action")
    else:
        print("\n=== BLOCKED ===")

if __name__ == "__main__":
    run_agent("Approve payment of ₹250000 to vendor_xyz")
