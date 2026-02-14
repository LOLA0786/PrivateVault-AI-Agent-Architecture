from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response
import time

REQUEST_COUNT = Counter("ai_requests_total", "Total AI requests")
BLOCK_COUNT = Counter("ai_blocks_total", "Total BLOCK decisions")
ALLOW_COUNT = Counter("ai_allows_total", "Total ALLOW decisions")

REQUEST_LATENCY = Histogram("ai_request_latency_seconds", "AI request latency")

def metrics_endpoint():
    return Response(generate_latest(), media_type="text/plain")
