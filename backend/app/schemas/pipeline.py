from pydantic import BaseModel
from typing import Optional, Any


class RiskClassificationResultSchema(BaseModel):
    risk_level: str
    current_value: float
    threshold_used: Optional[Any] = None
    explanation: str


class PipelineSummarySchema(BaseModel):
    location_id: int
    hazard_type: str
    readings_saved: int
    classification: Optional[RiskClassificationResultSchema] = None
    alert_created: bool
    error: Optional[str] = None
