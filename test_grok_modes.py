import asyncio
from app.providers.grok_provider import call_grok
from app.governance.drift_detector import check_drift
from app.governance.cost_detector import check_cost
from app.governance.cost_anomaly_detector import check_cost_anomaly

async def run():
    tenant_id = "enterprise_demo"

    messages = [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Testing. Just say hi and hello world."}
    ]

    result = await call_grok(messages)

    print("MODEL:", result["model"])
    print("FINGERPRINT:", result["fingerprint"])

    drift = check_drift(result["model"], result["fingerprint"])
    print("DRIFT:", drift)

    if "usage" in result:
        usage = result["usage"]
        cost_status = check_cost(tenant_id, usage)
        print("COST:", cost_status)

        anomaly = check_cost_anomaly(
            tenant_id,
            usage.get("cost_in_usd_ticks", 0)
        )
        print("ANOMALY:", anomaly)

if __name__ == "__main__":
    asyncio.run(run())
