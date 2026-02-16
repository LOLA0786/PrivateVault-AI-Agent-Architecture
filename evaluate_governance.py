import os
import pandas as pd
import asyncio
from app.providers.grok_provider import call_grok
from app.governance.governance_adapter import enforce_enterprise_policy
from app.governance.drift_detector import check_drift
from app.governance.cost_detector import check_cost
from app.governance.cost_anomaly_detector import check_cost_anomaly

DATA_PATH = "data/creditcard.csv"
SAMPLE_SIZE = 500

async def analyze_transaction(row):
    prompt = f"""
Transaction:
Amount: {row.get('amount')}
Country: {row.get('country')}
Merchant Category: {row.get('category')}
Time: {row.get('timestamp')}

Is this transaction suspicious? Explain.
"""

    # Policy enforcement BEFORE model execution
    policy = enforce_enterprise_policy(
        "enterprise_demo",
        "model_execution",
        {"amount": row.get("amount")}
    )

    result = await call_grok(prompt)

    # Drift detection
    drift = check_drift(result.get("system_fingerprint"))

    # Cost & anomaly
    cost = check_cost("enterprise_demo", result.get("usage"))
    anomaly = check_cost_anomaly("enterprise_demo", result.get("usage"))

    return {
        "model_risk_text": result.get("response"),
        "policy": policy,
        "drift": drift,
        "cost": cost,
        "anomaly": anomaly
    }

async def run():
    df = pd.read_csv(DATA_PATH)

    sample = df.sample(min(SAMPLE_SIZE, len(df)))

    results = []
    blocked = 0

    for _, row in sample.iterrows():
        try:
            res = await analyze_transaction(row)
            results.append(res)
        except Exception as e:
            blocked += 1

    print("\n=== RESULTS ===")
    print("Transactions processed:", len(sample))
    print("Blocked by governance:", blocked)

    drift_events = sum(1 for r in results if r["drift"].get("status") == "drift_detected")
    anomalies = sum(1 for r in results if r["anomaly"].get("status") != "normal")

    print("Drift events:", drift_events)
    print("Cost anomalies:", anomalies)

if __name__ == "__main__":
    asyncio.run(run())
