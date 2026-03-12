import hashlib

BASELINE = "Policy violation detected"
CURRENT = "Policy violation detected"

def fingerprint(text):
    return hashlib.sha256(text.encode()).hexdigest()

baseline_fp = fingerprint(BASELINE)
current_fp = fingerprint(CURRENT)

if baseline_fp != current_fp:
    print({"drift_detected": True})
else:
    print({"drift_detected": False})
