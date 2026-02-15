from policy_engine import authorize_intent, infer_risk
from decision_ledger import DecisionLedger
from audit_logger import log_audit_event
from tool_authorization import ToolAuthorization

try:
    from emergency_brake import is_brake_engaged
except:
    def is_brake_engaged():
        return False

ledger = DecisionLedger()
tool_auth = ToolAuthorization()

def enforce_enterprise_policy(tenant_id, action, metadata=None):
    if is_brake_engaged():
        raise RuntimeError("Emergency brake engaged")

    principal = {"tenant_id": tenant_id}
    context = metadata or {}

    decision = authorize_intent(action, principal, context)
    risk = infer_risk(action, principal, context)

    log_audit_event({
        "tenant": tenant_id,
        "action": action,
        "decision": decision,
        "risk": risk
    })

    if not decision.get("allowed", True):
        raise PermissionError("Enterprise policy blocked action")

    return {"decision": decision, "risk": risk}

def authorize_enterprise_tool(user_id, role, tool_name, params=None):
    params = params or {}

    if not tool_auth.is_tool_authorized(role, tool_name):
        raise PermissionError(f"Role '{role}' not permitted to use '{tool_name}'")

    signature = tool_auth.generate_action_signature(
        user_id,
        role,
        tool_name,
        params
    )

    return {
        "authorized": True,
        "signature": signature
    }

def record_enterprise_event(event):
    ledger.append(event)
