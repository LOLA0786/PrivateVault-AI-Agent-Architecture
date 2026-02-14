from fastapi import APIRouter
from pydantic import BaseModel
from app.ai_gateway import execute_ai
import traceback

router = APIRouter()

class AIRequest(BaseModel):
    tenant_id: str
    user_id: str
    input_text: str

@router.post("/ai/classify")
def classify(request: AIRequest):
    try:
        return execute_ai(request)
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}
