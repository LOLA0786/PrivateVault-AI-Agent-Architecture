from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/live")
def live():
    return {"alive": True}

@router.get("/ready")
def ready():
    return {"ready": True}
