AGENT = {
    "name": "analysis_agent",
    "permissions": ["read_transactions"]
}

TOOLS = {
    "read_transactions": True,
    "export_data": False,
    "execute_payment": False
}

CHAIN_ATTACK = [
    {"tool": "read_transactions"},
    {"tool": "export_data"},
    {"tool": "execute_payment"}
]

def enforce_chain(agent, chain):
    results = []
    for step in chain:
        tool = step["tool"]
        if tool not in agent["permissions"]:
            results.append({"tool": tool, "status": "blocked"})
        else:
            results.append({"tool": tool, "status": "allowed"})
    return results

print(enforce_chain(AGENT, CHAIN_ATTACK))
