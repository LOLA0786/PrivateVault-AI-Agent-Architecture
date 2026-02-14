from fastapi import FastAPI
from app.router import router
from app.models.database import engine
from app.models.schemas import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrivateVault AI Agent Engine")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}
