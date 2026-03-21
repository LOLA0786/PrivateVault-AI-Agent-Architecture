import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import re

load_dotenv()

app = FastAPI()

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

class EmailInput(BaseModel):
    email_text: str

def call_hf(prompt):
    url = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
    response = requests.post(
        url,
        headers=headers,
        json={"inputs": prompt}
    )

    try:
        return response.json()
    except Exception:
        return {
            "error": "HF API failed",
            "raw_response": response.text
        }

def evaluate_policy(text):
    match = re.search(r"(\d+)%", text)
    discount = int(match.group(1)) if match else 0

    if discount > 25:
        return {
            "status": "BLOCKED",
            "risk_level": "HIGH"
        }

    if discount > 20:
        return {
            "status": "REQUIRES_APPROVAL",
            "risk_level": "MEDIUM"
        }

    return {
        "status": "APPROVED",
        "risk_level": "LOW"
    }

@app.post("/process")
def process_email(input: EmailInput):
    intent = call_hf(input.email_text)

    policy = evaluate_policy(input.email_text)

    decision = {
        "intent": intent,
        "policy_result": policy,
        "final_status": policy["status"]
    }

    return decision
