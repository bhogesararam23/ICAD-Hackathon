from app.risk_engine.threshold_calculator import ThresholdCalculator


class DroughtCalculator(ThresholdCalculator):
    hazard_type = "rainfall"
