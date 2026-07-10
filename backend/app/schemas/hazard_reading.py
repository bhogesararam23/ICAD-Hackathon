from pydantic import BaseModel
from datetime import datetime


class HazardReadingBase(BaseModel):
    location_id: int
    hazard_type: str
    value: float
    unit: str
    recorded_at: datetime
    source: str


class HazardReadingCreate(HazardReadingBase):
    pass


class HazardReading(HazardReadingBase):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True
