import requests
import os

SIEM_URL = os.getenv("SIEM_URL")

def send_to_siem(payload):
    if not SIEM_URL:
        return
    try:
        requests.post(SIEM_URL, json=payload, timeout=2)
    except:
        pass
