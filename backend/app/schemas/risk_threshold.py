from pydantic import BaseModel
from typing import Optional


class RiskThresholdBase(BaseModel):
    location_id: Optional[int] = None
    hazard_type: str
    risk_level: str
    min_value: float
    max_value: float
    notes: Optional[str] = None


class RiskThresholdCreate(RiskThresholdBase):
    pass


class RiskThreshold(RiskThresholdBase):
    id: int

    class Config:
        from_attributes = True
