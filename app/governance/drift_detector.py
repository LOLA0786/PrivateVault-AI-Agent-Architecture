import json
import os
from app.governance.config import DRIFT_POLICY

REGISTRY_FILE = "model_fingerprint_registry.json"

def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

def check_drift(model: str, fingerprint: str):
    registry = load_registry()
    previous = registry.get(model)

    if not previous:
        registry[model] = fingerprint
        save_registry(registry)
        return {"status": "baseline_created"}

    if previous != fingerprint:
        registry[model] = fingerprint
        save_registry(registry)

        if DRIFT_POLICY == "block":
            raise RuntimeError(
                f"MODEL DRIFT DETECTED for {model}: {previous} → {fingerprint}"
            )

        return {
            "status": "drift_detected",
            "previous": previous,
            "current": fingerprint
        }

    return {"status": "no_drift"}
