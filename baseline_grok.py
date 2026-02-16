import pandas as pd
import asyncio
from app.providers.grok_provider import call_grok

DATA_PATH = "data/creditcard.csv"

async def analyze():

    df = pd.read_csv(DATA_PATH).sample(200)

    correct = 0

    for _, row in df.iterrows():

        prompt = f"""
Transaction amount: {row['Amount']}
Should this be flagged as fraud? Answer YES or NO.
"""

        result = await call_grok(prompt)

        answer = result["response"]

        predicted = 1 if "yes" in answer else 0

        if predicted == row["Class"]:
            correct += 1

    print("Baseline accuracy:", correct / len(df))

asyncio.run(analyze())
