from typing import Optional
from app.data_sources.base import HazardReadingDTO
from app.models.risk_threshold import RiskThreshold
from app.risk_engine.base import RiskCalculator, RiskClassificationResult


class ThresholdCalculator(RiskCalculator):
    # Subclasses will set hazard_type
    hazard_type: str

    def classify(
        self,
        readings: list[HazardReadingDTO],
        thresholds: list[RiskThreshold]
    ) -> RiskClassificationResult:
        # If no readings, return low risk by default
        if not readings:
            return RiskClassificationResult(
                risk_level="low",
                current_value=0.0,
                threshold_used=None,
                explanation="No hazard readings available"
            )
        
        # Get the latest reading
        latest_reading = max(readings, key=lambda r: r.recorded_at)
        current_value = latest_reading.value
        
        # Filter thresholds: prefer location-specific, else global
        location_thresholds = [t for t in thresholds if t.location_id is not None]
        applicable_thresholds = location_thresholds if location_thresholds else [t for t in thresholds if t.location_id is None]
        
        # Risk level priority (higher first)
        risk_priority = {"high": 3, "moderate": 2, "low": 1}
        sorted_thresholds = sorted(
            applicable_thresholds,
            key=lambda t: risk_priority.get(t.risk_level, 0),
            reverse=True
        )
        
        # Find the first threshold that the value falls into
        selected_threshold: Optional[RiskThreshold] = None
        for threshold in sorted_thresholds:
            if threshold.min_value <= current_value <= threshold.max_value:
                selected_threshold = threshold
                break
        
        # If no matching threshold, default to low
        if not selected_threshold:
            return RiskClassificationResult(
                risk_level="low",
                current_value=current_value,
                threshold_used=None,
                explanation=f"No threshold defined for value {current_value}"
            )
        
        return RiskClassificationResult(
            risk_level=selected_threshold.risk_level,
            current_value=current_value,
            threshold_used=selected_threshold,
            explanation=(
                f"Latest value {current_value} falls into {selected_threshold.risk_level} risk "
                f"range [{selected_threshold.min_value}, {selected_threshold.max_value}]"
            )
        )
