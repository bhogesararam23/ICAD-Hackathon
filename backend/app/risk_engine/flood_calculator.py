from app.risk_engine.threshold_calculator import ThresholdCalculator


class FloodCalculator(ThresholdCalculator):
    hazard_type = "river_discharge"
