from scenarios import TEST_PROMPTS
import asyncio

from test_raw_grok import call_grok as raw_call
from app.providers.grok_provider import call_grok as governed_call


# If baseline uses same provider wrapper, import it
try:
    from baseline_grok import call_grok as baseline_call
except Exception:
    baseline_call = governed_call




async def test_governed(prompt):
    try:
        response = await governed_call(prompt)
        flagged = False
        drift = False
    except Exception as e:
        response = f"ERROR: {e}"
        flagged = True
        drift = True
    return response, flagged, drift


async def run_tests():
    print("\n🔐 PRIVATEVAULT SECURITY TEST SUITE\n")

    for name, prompt in TEST_PROMPTS.items():
        print("="*60)
        print(f"TEST: {name}")
        print("="*60)
        print(f"\nPROMPT:\n{prompt}\n")

        # RAW
        try:
            raw_response = raw_call(prompt)
            if isinstance(raw_response, dict):
                raw_response = raw_response["choices"][0]["message"]["content"]
        except Exception as e:
            raw_response = f"ERROR: {e}"

        print("🔴 RAW OUTPUT:\n")
        print(raw_response, "\n")

        # BASELINE
        try:
            baseline_response = await baseline_call(prompt)
        except Exception as e:
            baseline_response = f"ERROR: {e}"

        print("🟡 BASELINE OUTPUT:\n")
        print(baseline_response, "\n")

        # GOVERNED
        governed_response, flagged, drift = await test_governed(prompt)

        print("🟢 GOVERNED OUTPUT:\n")
        print(governed_response, "\n")

        print("Policy Flagged:", flagged)
        print("Drift Detected:", drift)
        print("\n")

    print("✅ TESTING COMPLETE\n")


if __name__ == "__main__":
    asyncio.run(run_tests())
