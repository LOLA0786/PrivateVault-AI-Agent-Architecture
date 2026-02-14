from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String)
    user_id = Column(String)
    prompt_id = Column(String)
    output_hash = Column(String)
    previous_hash = Column(String)
    current_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
