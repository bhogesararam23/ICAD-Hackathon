from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HazardReadingDTO:
    value: float
    unit: str
    recorded_at: datetime
    source: str


class HazardDataSource(ABC):
    hazard_type: str

    @abstractmethod
    async def fetch(self, latitude: float, longitude: float) -> list[HazardReadingDTO]:
        pass
