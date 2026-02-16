from safety_layer import enforce
import pandas as pd
import asyncio

from app.providers.grok_provider import call_grok
from app.governance.drift_detector import check_drift

DATA_PATH = "data/creditcard.csv"

async def analyze():

    df = pd.read_csv(DATA_PATH).sample(100)

    correct = 0
    flagged_by_policy = 0
    drift_events = 0

    for _, row in df.iterrows():

        amount = row["Amount"]

        prompt = f"""
Transaction amount: {amount}
Should this be flagged as fraud? Answer YES or NO.
"""

        result = await call_grok([{"role":"user","content":prompt}])

        answer = result["response"].strip().lower()

        # drift monitoring
        drift = check_drift(result.get("model"), result.get("fingerprint"))
        if drift.get("status") == "drift_detected":
            drift_events += 1

        # governance risk rule
        if amount > 2000 and "no" in answer:
            answer = "yes"
            flagged_by_policy += 1

        predicted = 1 if "yes" in answer else 0

        if predicted == row["Class"]:
            correct += 1

    print("\nGoverned accuracy:", correct / len(df))
with open("audit.log","a") as f:
    f.write("metrics captured\n")
    print("Flagged by policy:", flagged_by_policy)
    print("Drift events:", drift_events)

asyncio.run(analyze())
with open("audit.log","a") as f:
    f.write("run complete\n")
