from app.observability.metrics import router as metrics_router
from app.observability.health import router as health_router
from app.middleware.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from app.router import router
from app.models.database import engine
from app.models.schemas import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrivateVault AI Agent Engine")
app.include_router(metrics_router)
app.include_router(health_router)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}
