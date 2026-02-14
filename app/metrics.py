from prometheus_client import Counter, Histogram, generate_latest
from fastapi import APIRouter, Response
import time

REQUEST_COUNT = Counter("ai_requests_total", "Total AI requests")
BLOCK_COUNT = Counter("ai_block_total", "Total blocked decisions")
REQUEST_LATENCY = Histogram("ai_request_latency_seconds", "Request latency")

router = APIRouter()

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
