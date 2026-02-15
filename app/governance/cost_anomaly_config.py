import os

# multiplier that defines anomaly (e.g., 3x normal cost)
COST_SPIKE_MULTIPLIER = float(os.getenv("COST_SPIKE_MULTIPLIER", "3"))

ANOMALY_POLICY = os.getenv("ANOMALY_POLICY", "alert")
# options: alert | block
