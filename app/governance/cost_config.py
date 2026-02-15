import os

# Max cost per single request (in usd ticks)
MAX_COST_PER_REQUEST = int(os.getenv("MAX_COST_PER_REQUEST", "100000000"))

# Max cumulative cost per session
MAX_SESSION_COST = int(os.getenv("MAX_SESSION_COST", "500000000"))

COST_POLICY = os.getenv("COST_POLICY", "alert")
# options: alert | block
