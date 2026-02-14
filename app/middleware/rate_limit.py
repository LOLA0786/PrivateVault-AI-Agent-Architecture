import time
from fastapi import Request, HTTPException

RATE_LIMIT = 60  # requests per minute
tenant_requests = {}

async def rate_limit_middleware(request: Request, call_next):
    tenant_id = request.headers.get("x-tenant-id", "default")
    now = int(time.time())

    window = now // 60

    key = f"{tenant_id}:{window}"

    tenant_requests[key] = tenant_requests.get(key, 0) + 1

    if tenant_requests[key] > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    response = await call_next(request)
    return response
