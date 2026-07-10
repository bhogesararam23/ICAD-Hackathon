from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel
from app.data_sources.base import HazardReadingDTO
from app.models.risk_threshold import RiskThreshold
from app.schemas.risk_threshold import RiskThreshold as RiskThresholdSchema


class RiskClassificationResult(BaseModel):
    risk_level: str
    current_value: float
    threshold_used: Optional[RiskThresholdSchema] = None
    explanation: str


class RiskCalculator(ABC):
    hazard_type: str

    @abstractmethod
    def classify(
        self,
        readings: list[HazardReadingDTO],
        thresholds: list[RiskThreshold]
    ) -> RiskClassificationResult:
        pass
