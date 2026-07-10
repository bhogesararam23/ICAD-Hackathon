from datetime import datetime, timedelta
from app.data_sources.base import HazardDataSource, HazardReadingDTO


class RiverDischargeSource(HazardDataSource):
    hazard_type = "river_discharge"

    async def fetch(self, latitude: float, longitude: float) -> list[HazardReadingDTO]:
        # TODO: Implement real GloFAS integration (Global Flood Alert System) API integration
        # For now, return mock data for testing
        now = datetime.utcnow()
        mock_readings = [
            HazardReadingDTO(
                value=123.5,
                unit="m³/s",
                recorded_at=now - timedelta(days=i),
                source="Mock GloFAS (stubbed data)"
            )
            for i in range(7)
        ]
        
        # Add some variability to the mock data
        mock_readings[2].value = 456.7  # A higher value to test threshold crossing
        mock_readings[5].value = 789.0
        
        return mock_readings
