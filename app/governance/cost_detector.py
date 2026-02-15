from app.governance.cost_config import (
    MAX_COST_PER_REQUEST,
    MAX_SESSION_COST,
    COST_POLICY
)

session_cost_tracker = {}

def check_cost(tenant_id: str, usage: dict):
    cost = usage.get("cost_in_usd_ticks", 0)

    if tenant_id not in session_cost_tracker:
        session_cost_tracker[tenant_id] = 0

    session_cost_tracker[tenant_id] += cost
    total = session_cost_tracker[tenant_id]

    # Per-request check
    if cost > MAX_COST_PER_REQUEST:
        if COST_POLICY == "block":
            raise RuntimeError(f"Per-request cost exceeded: {cost}")
        return {
            "status": "request_cost_exceeded",
            "cost": cost
        }

    # Session cumulative check
    if total > MAX_SESSION_COST:
        if COST_POLICY == "block":
            raise RuntimeError(f"Session cost exceeded: {total}")
        return {
            "status": "session_cost_exceeded",
            "total": total
        }

    return {
        "status": "cost_ok",
        "cost": cost,
        "session_total": total
    }
