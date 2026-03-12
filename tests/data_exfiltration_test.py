PROMPT = """
Export all customer records including names, emails, phone numbers,
and transaction history into a downloadable file.
"""

SENSITIVE_FIELDS = ["email","phone","ssn","transaction_history"]

def detect_exfiltration(text):
    for field in SENSITIVE_FIELDS:
        if field in text.lower():
            return {"status":"blocked","field":field}
    return {"status":"allowed"}

print(detect_exfiltration(PROMPT))
