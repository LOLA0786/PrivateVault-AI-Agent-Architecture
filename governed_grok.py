import asyncio
from app.providers.grok_provider import call_grok
from app.governance.data_protection import contains_sensitive_data

async def main():
    prompt = input("Enter prompt: ")

    flagged_by_policy = False
    drift_detected = False

    response = await call_grok(prompt)

    # 🚨 DATA LEAK PREVENTION
    if contains_sensitive_data(response):
        flagged_by_policy = True
        response = (
            "⚠️ Sensitive personal data cannot be disclosed.\n"
            "Please provide an anonymized or aggregated summary instead."
        )

    print("\n=== GOVERNED RESPONSE ===\n")
    print(response)
    print("\nPolicy Flagged:", flagged_by_policy)
    print("Drift events:", drift_detected)

if __name__ == "__main__":
    asyncio.run(main())
