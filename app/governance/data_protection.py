import re

PII_PATTERNS = [
    r'\b\d{10}\b',              # phone numbers
    r'\b\d{3}-\d{2}-\d{4}\b',   # SSN pattern
    r'@',                       # emails
]

def contains_sensitive_data(text):
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return True
    return False
