from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    hazard_readings: Mapped[List["HazardReading"]] = relationship(
        "HazardReading", back_populates="location", cascade="all, delete-orphan"
    )
    risk_thresholds: Mapped[List["RiskThreshold"]] = relationship(
        "RiskThreshold", back_populates="location", cascade="all, delete-orphan"
    )
    alerts: Mapped[List["Alert"]] = relationship(
        "Alert", back_populates="location", cascade="all, delete-orphan"
    )
