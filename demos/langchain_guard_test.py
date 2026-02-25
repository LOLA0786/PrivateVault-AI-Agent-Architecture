import asyncio
from governed_tools import governed_export, governed_transfer

async def run():

    print("\n--- SAFE ACTION ---")
    print(await governed_transfer.arun(500))

    print("\n--- REVIEW ACTION ---")
    print(await governed_transfer.arun(200000))

    print("\n--- BLOCKED ACTION ---")
    print(await governed_export.arun("all"))

asyncio.run(run())
