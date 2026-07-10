from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hazard_reading import HazardReading
from app.schemas.hazard_reading import HazardReading as HazardReadingSchema
from app.schemas.pipeline import PipelineSummarySchema
from app.db.session import get_db
from app.services.pipeline import run_pipeline_for_location

router = APIRouter(tags=["hazards"])


@router.get("/locations/{location_id}/hazards/{hazard_type}/latest", response_model=HazardReadingSchema)
async def get_latest_hazard_reading(
    location_id: int,
    hazard_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Get the latest hazard reading for a location and hazard type."""
    result = await db.execute(
        select(HazardReading)
        .where(HazardReading.location_id == location_id)
        .where(HazardReading.hazard_type == hazard_type)
        .order_by(desc(HazardReading.recorded_at))
        .limit(1)
    )
    reading = result.scalar_one_or_none()
    if not reading:
        raise HTTPException(status_code=404, detail="No hazard readings found for this location and type")
    return reading


@router.post("/locations/{location_id}/hazards/{hazard_type}/refresh", response_model=PipelineSummarySchema)
async def refresh_hazard_data(
    location_id: int,
    hazard_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Trigger pipeline run for a location + hazard type and return results."""
    summary = await run_pipeline_for_location(location_id, hazard_type, db)
    if summary.error:
        raise HTTPException(status_code=500, detail=summary.error)
    return summary
