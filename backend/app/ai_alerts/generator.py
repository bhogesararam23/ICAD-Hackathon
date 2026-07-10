from pathlib import Path
from app.ai_alerts.client import AnthropicClient
from app.models.location import Location
from app.risk_engine.base import RiskClassificationResult
from app.data_sources.base import HazardReadingDTO


# Load the prompt template once at module load time
PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompts" / "alert_template.txt"
with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
    ALERT_PROMPT_TEMPLATE = f.read()


class AlertGenerator:
    def __init__(self):
        self.client = AnthropicClient()

    async def generate_alert(
        self,
        location: Location,
        hazard_type: str,
        risk_result: RiskClassificationResult,
        latest_reading: HazardReadingDTO
    ) -> tuple[str, dict]:
        """Generate an AI alert using the template and Anthropic API.
        
        Args:
            location: The Location model instance
            hazard_type: The type of hazard
            risk_result: The RiskClassificationResult
            latest_reading: The latest HazardReadingDTO (for unit)
            
        Returns:
            A tuple of (generated_alert_text, raw_context_dict)
        """
        # Fill in the prompt template
        prompt = ALERT_PROMPT_TEMPLATE.format(
            location_name=location.name,
            country=location.country,
            hazard_type=hazard_type.replace("_", " ").title(),
            risk_level=risk_result.risk_level.title(),
            current_value=risk_result.current_value,
            unit=latest_reading.unit,
            explanation=risk_result.explanation
        )

        # Call the Anthropic API
        alert_text = await self.client.generate_text(prompt)

        # Prepare the raw context dict for storage
        raw_context = {
            "location_name": location.name,
            "country": location.country,
            "hazard_type": hazard_type,
            "risk_level": risk_result.risk_level,
            "current_value": risk_result.current_value,
            "unit": latest_reading.unit,
            "explanation": risk_result.explanation,
            "prompt_used": prompt
        }

        return alert_text, raw_context
