POLICY_MATRIX = {
    "default": {"HIGH": "BLOCK", "MEDIUM": "ALLOW", "LOW": "ALLOW"},
    "fintech": {"HIGH": "BLOCK", "MEDIUM": "BLOCK", "LOW": "ALLOW"},
}

def resolve_action(tenant_id, sensitivity):
    matrix = POLICY_MATRIX.get(tenant_id, POLICY_MATRIX["default"])
    return matrix.get(sensitivity, "BLOCK")
