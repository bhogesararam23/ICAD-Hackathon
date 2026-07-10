from datetime import datetime
import httpx
from app.config import settings
from app.data_sources.base import HazardDataSource, HazardReadingDTO


class RainfallSource(HazardDataSource):
    hazard_type = "rainfall"

    async def fetch(self, latitude: float, longitude: float) -> list[HazardReadingDTO]:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["precipitation_sum"],
            "timezone": "auto",
            "past_days": 7,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.OPEN_METEO_BASE_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()
        
        readings = []
        daily_data = data.get("daily", {})
        times = daily_data.get("time", [])
        precipitation = daily_data.get("precipitation_sum", [])
        
        for time_str, precip in zip(times, precipitation):
            if precip is not None:
                recorded_at = datetime.fromisoformat(time_str)
                readings.append(HazardReadingDTO(
                    value=precip,
                    unit="mm",
                    recorded_at=recorded_at,
                    source="Open-Meteo"
                ))
        
        return readings
