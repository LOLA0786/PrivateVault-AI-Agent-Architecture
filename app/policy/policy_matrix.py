POLICY_MATRIX = {
    "default": {
        "HIGH": "BLOCK",
        "MEDIUM": "ALLOW",
        "LOW": "ALLOW"
    },
    "fintech_tenant": {
        "HIGH": "BLOCK",
        "MEDIUM": "BLOCK",
        "LOW": "ALLOW"
    },
    "enterprise_corp": {
        "HIGH": "ALLOW_WITH_LOG",
        "MEDIUM": "ALLOW",
        "LOW": "ALLOW"
    }
}

def resolve_action(tenant_id: str, sensitivity: str):
    matrix = POLICY_MATRIX.get(tenant_id, POLICY_MATRIX["default"])
    return matrix.get(sensitivity, "BLOCK")
