from typing import Type
from app.data_sources.base import HazardDataSource
from app.data_sources.rainfall_source import RainfallSource
from app.data_sources.river_discharge_source import RiverDischargeSource


# Registry mapping hazard_type strings to source classes
_data_source_registry: dict[str, Type[HazardDataSource]] = {
    RainfallSource.hazard_type: RainfallSource,
    RiverDischargeSource.hazard_type: RiverDischargeSource,
}


def get_data_source(hazard_type: str) -> Type[HazardDataSource]:
    """Get the data source class for a given hazard type.
    
    Args:
        hazard_type: The type of hazard (e.g., "rainfall", "river_discharge")
        
    Returns:
        The HazardDataSource subclass for the given hazard type
        
    Raises:
        ValueError: If no data source is registered for the given hazard type
    """
    if hazard_type not in _data_source_registry:
        raise ValueError(
            f"No data source registered for hazard type '{hazard_type}'. "
            f"Available types: {', '.join(_data_source_registry.keys())}"
        )
    return _data_source_registry[hazard_type]
