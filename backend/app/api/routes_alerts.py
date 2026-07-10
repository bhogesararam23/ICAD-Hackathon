from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.schemas.alert import Alert as AlertSchema
from app.db.session import get_db

router = APIRouter(tags=["alerts"])


@router.get("/locations/{location_id}/alerts", response_model=List[AlertSchema])
async def get_location_alerts(
    location_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get alerts for a location (paginated, most recent first)."""
    result = await db.execute(
        select(Alert)
        .where(Alert.location_id == location_id)
        .order_by(desc(Alert.created_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/alerts", response_model=List[AlertSchema])
async def get_all_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all alerts across locations (paginated, most recent first)."""
    result = await db.execute(
        select(Alert)
        .order_by(desc(Alert.created_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
