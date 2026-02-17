import asyncio
from app.providers.grok_provider import call_grok

async def analyze():
    prompt = input("Enter prompt: ")

    try:
        result = await call_grok(prompt)
    except Exception as e:
        print("Error:", e)
        return

    print("\n=== BASELINE RESPONSE ===\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(analyze())
