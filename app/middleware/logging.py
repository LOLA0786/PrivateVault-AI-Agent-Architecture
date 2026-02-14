import time
import json
from fastapi import Request

async def logging_middleware(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = round((time.time() - start) * 1000, 2)

    log = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration,
        "tenant_id": getattr(request.state, "tenant_id", "unknown")
    }

    print(json.dumps(log))

    return response
