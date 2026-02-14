from app.system.health import router as health_router
from fastapi import FastAPI
from app.router import router
from app.middleware.logging import logging_middleware
from app.middleware.rate_limit import rate_limit_middleware
from app.metrics.prometheus import metrics_endpoint

app = FastAPI(title="PrivateVault AI Governance Engine")
app.include_router(health_router)

app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)

app.include_router(router)

@app.get("/metrics")
def metrics():
    return metrics_endpoint()

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    return {"status": "ready"}
