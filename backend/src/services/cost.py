from sqlmodel import Session
from uuid import UUID
from ..models.premium import TokenUsage, FeatureType

# Gemini 1.5 Flash Pricing (approximate)
PRICE_INPUT_PER_TOKEN = 0.075 / 1_000_000
PRICE_OUTPUT_PER_TOKEN = 0.30 / 1_000_000

class CostTracker:
    @staticmethod
    def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens * PRICE_INPUT_PER_TOKEN) + (completion_tokens * PRICE_OUTPUT_PER_TOKEN)

    @staticmethod
    def log_usage(
        session: Session,
        user_id: UUID,
        feature_type: FeatureType,
        prompt_tokens: int,
        completion_tokens: int,
        model_name: str
    ) -> TokenUsage:
        cost = CostTracker.calculate_cost(prompt_tokens, completion_tokens)
        
        usage = TokenUsage(
            user_id=user_id,
            feature_type=feature_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=model_name,
            estimated_cost_usd=cost
        )
        session.add(usage)
        session.commit()
        session.refresh(usage)
        return usage
