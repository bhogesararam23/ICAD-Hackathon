import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location
from app.models.hazard_reading import HazardReading
from app.models.risk_threshold import RiskThreshold
from app.models.alert import Alert
from app.data_sources.registry import get_data_source
from app.data_sources.base import HazardReadingDTO
from app.risk_engine.registry import get_risk_calculator
from app.risk_engine.base import RiskClassificationResult
from app.ai_alerts.generator import AlertGenerator

logger = logging.getLogger(__name__)


@dataclass
class PipelineSummary:
    location_id: int
    hazard_type: str
    readings_saved: int
    classification: Optional[RiskClassificationResult]
    alert_created: bool
    error: Optional[str] = None


async def run_pipeline_for_location(
    location_id: int,
    hazard_type: str,
    db: AsyncSession
) -> PipelineSummary:
    """Run the full early warning pipeline for a single location and hazard type."""
    summary = PipelineSummary(
        location_id=location_id,
        hazard_type=hazard_type,
        readings_saved=0,
        classification=None,
        alert_created=False
    )

    try:
        # Step 1: Load Location from DB
        logger.info(f"Step 1: Loading location {location_id}")
        location_result = await db.execute(select(Location).where(Location.id == location_id))
        location = location_result.scalar_one_or_none()
        if not location:
            raise ValueError(f"Location with id {location_id} not found")

        # Step 2: Get data source and fetch readings
        logger.info(f"Step 2: Fetching {hazard_type} readings for location {location_id}")
        data_source_class = get_data_source(hazard_type)
        data_source = data_source_class()
        readings_dto = await data_source.fetch(location.latitude, location.longitude)
        if not readings_dto:
            logger.warning(f"No readings returned for location {location_id}, hazard type {hazard_type}")
            summary.error = "No readings available"
            return summary

        # Step 3: Store new HazardReading rows in DB
        logger.info(f"Step 3: Saving {len(readings_dto)} readings for location {location_id}")
        fetched_at = datetime.utcnow()
        for dto in readings_dto:
            hazard_reading = HazardReading(
                location_id=location_id,
                hazard_type=hazard_type,
                value=dto.value,
                unit=dto.unit,
                recorded_at=dto.recorded_at,
                fetched_at=fetched_at,
                source=dto.source
            )
            db.add(hazard_reading)
        await db.commit()
        summary.readings_saved = len(readings_dto)

        # Step 4: Get risk calculator, load thresholds, classify
        logger.info(f"Step 4: Classifying risk for location {location_id}, hazard type {hazard_type}")
        risk_calculator_class = get_risk_calculator(hazard_type)
        risk_calculator = risk_calculator_class()
        
        # Load applicable thresholds (location-specific + global for this hazard type)
        thresholds_result = await db.execute(
            select(RiskThreshold)
            .where(RiskThreshold.hazard_type == hazard_type)
            .where(
                (RiskThreshold.location_id == location_id) | (RiskThreshold.location_id.is_(None))
            )
        )
        thresholds = thresholds_result.scalars().all()
        
        classification = risk_calculator.classify(readings_dto, thresholds)
        summary.classification = classification

        # Step 5 & 6: If moderate/high risk, generate and save alert
        if classification.risk_level in ["moderate", "high"]:
            logger.info(f"Step 5 & 6: Generating alert for location {location_id}, risk level {classification.risk_level}")
            latest_reading = max(readings_dto, key=lambda r: r.recorded_at)
            alert_generator = AlertGenerator()
            alert_text, raw_context = await alert_generator.generate_alert(
                location=location,
                hazard_type=hazard_type,
                risk_result=classification,
                latest_reading=latest_reading
            )
            
            new_alert = Alert(
                location_id=location_id,
                hazard_type=hazard_type,
                risk_level=classification.risk_level,
                generated_message=alert_text,
                raw_context=raw_context,
                created_at=datetime.utcnow()
            )
            db.add(new_alert)
            await db.commit()
            summary.alert_created = True
            logger.info(f"Alert created for location {location_id}")

    except Exception as e:
        logger.error(f"Pipeline failed for location {location_id}, hazard type {hazard_type}: {str(e)}", exc_info=True)
        summary.error = str(e)
        # Rollback in case of DB errors
        await db.rollback()

    return summary
