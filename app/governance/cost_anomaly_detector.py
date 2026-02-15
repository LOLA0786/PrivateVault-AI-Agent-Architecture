import json
import os
from app.governance.cost_anomaly_config import (
    COST_SPIKE_MULTIPLIER,
    ANOMALY_POLICY
)

BASELINE_FILE = "cost_baseline.json"

def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {}
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)

def save_baseline(data):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_cost_anomaly(tenant_id: str, cost: int):
    baseline = load_baseline()

    if tenant_id not in baseline:
        baseline[tenant_id] = {
            "avg_cost": cost,
            "count": 1
        }
        save_baseline(baseline)
        return {"status": "baseline_created"}

    avg = baseline[tenant_id]["avg_cost"]
    count = baseline[tenant_id]["count"]

    # anomaly detection
    if cost > avg * COST_SPIKE_MULTIPLIER:
        if ANOMALY_POLICY == "block":
            raise RuntimeError(
                f"Cost anomaly detected: {cost} vs avg {avg}"
            )
        return {
            "status": "anomaly_detected",
            "current_cost": cost,
            "average_cost": avg
        }

    # update rolling average
    new_avg = int((avg * count + cost) / (count + 1))
    baseline[tenant_id]["avg_cost"] = new_avg
    baseline[tenant_id]["count"] += 1
    save_baseline(baseline)

    return {
        "status": "normal",
        "current_cost": cost,
        "average_cost": new_avg
    }
