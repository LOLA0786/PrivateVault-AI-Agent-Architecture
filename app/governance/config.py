import os

DRIFT_POLICY = os.getenv("DRIFT_POLICY", "alert")  
# options: alert | block
