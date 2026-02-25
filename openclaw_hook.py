import asyncio
from execution_controller import execute
from app.providers.grok_provider import call_grok

async def intercept(action):

    print("\n📡 Intercepted action:", action)

    def operation():
        return {"executed": True}

    result = execute(action, operation)

    if result.get("status") == "blocked":
        explanation = await call_grok(
            f"Explain the security risk of this blocked action: {action}"
        )
        print("🧠 Risk Explanation:", explanation["response"])
        print("🔐 Decision: BLOCK")
        return "BLOCK"

    if result.get("status") == "requires_human_review":
        print("🔐 Decision: REVIEW")
        return "REVIEW"

    print("✅ Action executed")
    return "APPROVE"
