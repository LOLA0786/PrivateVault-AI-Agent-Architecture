from app.metrics import BLOCK_COUNT
import os

ALERT_THRESHOLD = int(os.getenv("BLOCK_ALERT_THRESHOLD", "50"))

def check_block_spike():
    if BLOCK_COUNT._value.get() > ALERT_THRESHOLD:
        print("ALERT: Block spike detected")
