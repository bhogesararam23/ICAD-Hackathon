import asyncio
from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models.base import Base
from app.models.location import Location
from app.models.risk_threshold import RiskThreshold
from app.models.hazard_reading import HazardReading
from app.models.alert import Alert
from app.config import settings


async def seed_data():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # Create tables if they don't exist (optional, for dev)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Seed Locations (IGAD region)
        locations = [
            Location(
                name="Mogadishu",
                country="Somalia",
                latitude=2.0469,
                longitude=45.3182,
                region="Hirshabelle",
                created_at=datetime.now(UTC)
            ),
            Location(
                name="Addis Ababa",
                country="Ethiopia",
                latitude=9.0054,
                longitude=38.7636,
                region="Addis Ababa",
                created_at=datetime.now(UTC)
            ),
            Location(
                name="Nairobi",
                country="Kenya",
                latitude=-1.286389,
                longitude=36.817223,
                region="Nairobi County",
                created_at=datetime.now(UTC)
            ),
            Location(
                name="Khartoum",
                country="Sudan",
                latitude=15.5007,
                longitude=32.5599,
                region="Khartoum State",
                created_at=datetime.now(UTC)
            )
        ]

        # Check if locations already exist to avoid duplicates
        for loc in locations:
            existing = await session.execute(
                select(Location).where(Location.name == loc.name, Location.country == loc.country)
            )
            if existing.scalar_one_or_none() is None:
                session.add(loc)
                print(f"Added location: {loc.name}, {loc.country}")
            else:
                print(f"Location already exists: {loc.name}, {loc.country}")

        await session.commit()

        # Seed Default Risk Thresholds (global, location_id = None)
        default_thresholds = [
            # Rainfall (mm per day)
            RiskThreshold(
                location_id=None,
                hazard_type="rainfall",
                risk_level="low",
                min_value=0.0,
                max_value=20.0,
                notes="Light rainfall - no drought or flood risk"
            ),
            RiskThreshold(
                location_id=None,
                hazard_type="rainfall",
                risk_level="moderate",
                min_value=20.0,
                max_value=50.0,
                notes="Moderate rainfall - monitor for potential drought/flood"
            ),
            RiskThreshold(
                location_id=None,
                hazard_type="rainfall",
                risk_level="high",
                min_value=50.0,
                max_value=999.9,
                notes="Heavy rainfall - flood risk likely"
            ),
            # River Discharge (m³/s - example values)
            RiskThreshold(
                location_id=None,
                hazard_type="river_discharge",
                risk_level="low",
                min_value=0.0,
                max_value=100.0,
                notes="Normal river flow"
            ),
            RiskThreshold(
                location_id=None,
                hazard_type="river_discharge",
                risk_level="moderate",
                min_value=100.0,
                max_value=300.0,
                notes="Elevated river flow - monitor for flood risk"
            ),
            RiskThreshold(
                location_id=None,
                hazard_type="river_discharge",
                risk_level="high",
                min_value=300.0,
                max_value=9999.9,
                notes="High river flow - flood risk imminent"
            )
        ]

        # Check if default thresholds already exist
        for threshold in default_thresholds:
            existing = await session.execute(
                select(RiskThreshold)
                .where(RiskThreshold.location_id.is_(None))
                .where(RiskThreshold.hazard_type == threshold.hazard_type)
                .where(RiskThreshold.risk_level == threshold.risk_level)
            )
            if existing.scalar_one_or_none() is None:
                session.add(threshold)
                print(f"Added default threshold: {threshold.hazard_type} - {threshold.risk_level}")
            else:
                print(f"Default threshold already exists: {threshold.hazard_type} - {threshold.risk_level}")

        await session.commit()
        print("Seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_data())
