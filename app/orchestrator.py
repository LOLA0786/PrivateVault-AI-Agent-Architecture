from app.agents.policy import enforce_policy

def governance_flow(classification_result):
    policy = enforce_policy(classification_result)

    # placeholder for risk agent later
    risk = {
        "risk_level": "HIGH" if classification_result["risk_score"] > 0.8 else "LOW"
    }

    return {
        "policy": policy,
        "risk": risk
    }
