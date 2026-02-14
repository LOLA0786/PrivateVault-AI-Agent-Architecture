from pydantic import BaseModel, Field
from typing import Literal

class ClassificationResult(BaseModel):
    sensitivity: Literal["HIGH", "MEDIUM", "LOW"]
    contains_pii: bool
    risk_score: float = Field(ge=0, le=1)
