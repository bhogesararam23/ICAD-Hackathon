from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location
from app.schemas.location import Location as LocationSchema, LocationCreate
from app.db.session import get_db

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=List[LocationSchema])
async def list_locations(db: AsyncSession = Depends(get_db)):
    """List all locations."""
    result = await db.execute(select(Location))
    return result.scalars().all()


@router.post("", response_model=LocationSchema, status_code=201)
async def create_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new location."""
    db_location = Location(**location.model_dump())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location


@router.get("/{location_id}", response_model=LocationSchema)
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a location by ID."""
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location
