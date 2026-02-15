from src.services.cost import CostTracker
from src.models.premium import FeatureType
from sqlmodel import Session, create_engine, SQLModel
from uuid import uuid4

def test_cost_calculation():
    prompt_tokens = 1000
    completion_tokens = 500
    
    # Prices: 0.075 / 1M and 0.30 / 1M
    expected_cost = (1000 * 0.075 / 1_000_000) + (500 * 0.30 / 1_000_000)
    # 0.000075 + 0.00015 = 0.000225
    
    calculated = CostTracker.calculate_cost(prompt_tokens, completion_tokens)
    assert abs(calculated - 0.000225) < 1e-9

def test_log_usage():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        user_id = uuid4()
        usage = CostTracker.log_usage(
            session,
            user_id,
            FeatureType.ASSESSMENT,
            1000,
            500,
            "gemini-1.5-flash"
        )
        
        assert usage.user_id == user_id
        assert usage.prompt_tokens == 1000
        assert usage.completion_tokens == 500
        assert usage.estimated_cost_usd > 0
