AGENT = {
    "name": "analysis_agent",
    "permissions": ["read_transactions"]
}

REQUEST = {
    "tool": "execute_payment",
    "amount": 5000
}

def check_permission(agent, request):
    if request["tool"] not in agent["permissions"]:
        return {"status": "blocked", "reason": "permission_escalation"}
    return {"status": "allowed"}

print(check_permission(AGENT, REQUEST))
