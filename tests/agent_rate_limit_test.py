REQUESTS = 120
LIMIT = 50

def rate_limit(count):
    if count > LIMIT:
        return {"status": "blocked", "reason": "rate_limit_exceeded"}
    return {"status": "allowed"}

print(rate_limit(REQUESTS))
