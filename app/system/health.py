from fastapi import APIRouter
import time

router = APIRouter()

START_TIME = time.time()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }

@router.get("/health/live")
def liveness():
    return {"status": "alive"}

@router.get("/health/ready")
def readiness():
    # later you can check model providers, DB, redis, etc
    return {"status": "ready"}
