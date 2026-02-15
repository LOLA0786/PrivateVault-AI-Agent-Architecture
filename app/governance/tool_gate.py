from app.governance.tool_permissions import TENANT_TOOL_WHITELIST

def enforce_tool_permission(tenant_id: str, tool_name: str):
    allowed = TENANT_TOOL_WHITELIST.get(tenant_id, [])

    if tool_name not in allowed:
        raise PermissionError(
            f"Tool '{tool_name}' not permitted for tenant '{tenant_id}'"
        )

    return {"status": "allowed", "tool": tool_name}
