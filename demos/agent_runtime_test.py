import asyncio
from openclaw_hook import intercept

actions = [
    {"amount": 500},
    {"amount": 200000},
    {"amount": 300000, "external_transfer": True}
]

async def run():
    for action in actions:
        decision = await intercept(action)

        if decision == "BLOCK":
            print("⛔ Execution stopped\n")
        else:
            print("➡️ Executing action\n")

asyncio.run(run())
