import asyncio
from app.providers.grok_provider import call_grok

async def main():
    prompt = input("Enter prompt: ")

    flagged_by_policy = False
    drift_detected = False

    try:
        response = await call_grok(prompt)
    except Exception as e:
        print("Error:", e)
        return

    print("\n=== GOVERNED RESPONSE ===\n")
    print(response)
    print("\nFlagged by policy:", flagged_by_policy)
    print("Drift events:", drift_detected)

if __name__ == "__main__":
    asyncio.run(main())
