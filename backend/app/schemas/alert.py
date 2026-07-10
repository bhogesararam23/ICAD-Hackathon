from pydantic import BaseModel
from datetime import datetime
from typing import Any


class AlertBase(BaseModel):
    location_id: int
    hazard_type: str
    risk_level: str
    generated_message: str
    raw_context: Any


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
