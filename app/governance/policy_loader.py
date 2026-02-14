import os
import yaml

BASE_PATH = os.path.dirname(__file__)
POLICY_PATH = os.path.join(BASE_PATH, "policy_matrix")

def load_policy(tenant_id: str) -> dict:
    file_path = os.path.join(POLICY_PATH, f"{tenant_id}.yaml")

    if not os.path.exists(file_path):
        file_path = os.path.join(POLICY_PATH, "enterprise.yaml")

    with open(file_path, "r") as f:
        return yaml.safe_load(f)
