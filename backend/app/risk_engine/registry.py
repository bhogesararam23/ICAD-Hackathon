from typing import Type
from app.risk_engine.base import RiskCalculator
from app.risk_engine.flood_calculator import FloodCalculator
from app.risk_engine.drought_calculator import DroughtCalculator


# Registry mapping hazard_type strings to calculator classes
_risk_calculator_registry: dict[str, Type[RiskCalculator]] = {
    FloodCalculator.hazard_type: FloodCalculator,
    DroughtCalculator.hazard_type: DroughtCalculator,
}


def get_risk_calculator(hazard_type: str) -> Type[RiskCalculator]:
    """Get the risk calculator class for a given hazard type.
    
    Args:
        hazard_type: The type of hazard (e.g., "rainfall", "river_discharge")
        
    Returns:
        The RiskCalculator subclass for the given hazard type
        
    Raises:
        ValueError: If no risk calculator is registered for the given hazard type
    """
    if hazard_type not in _risk_calculator_registry:
        raise ValueError(
            f"No risk calculator registered for hazard type '{hazard_type}'. "
            f"Available types: {', '.join(_risk_calculator_registry.keys())}"
        )
    return _risk_calculator_registry[hazard_type]
