ROLE_OVERRIDE = {
    "admin": {"HIGH": "ALLOW_WITH_LOG"},
    "auditor": {"HIGH": "ALLOW"},
}

def apply_role_override(role, sensitivity, action):
    if role in ROLE_OVERRIDE and sensitivity in ROLE_OVERRIDE[role]:
        return ROLE_OVERRIDE[role][sensitivity]
    return action
