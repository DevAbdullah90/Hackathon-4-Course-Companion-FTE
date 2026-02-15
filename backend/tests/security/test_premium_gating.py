from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.base import User, Course, Module, Chapter
from unittest.mock import patch

def test_rate_limit(client: TestClient, session: Session):
    # Setup data
    course = Course(title="C1", description="D1", slug="c1")
    session.add(course)
    module = Module(course=course, title="M1", order_index=1)
    session.add(module)
    chapter = Chapter(module=module, title="Ch1", slug="ch1", r2_key="ch1.md", order_index=1, is_premium=True)
    session.add(chapter)
    session.commit()

    user = User(email="rate@test.com", is_premium=True)
    session.add(user)
    session.commit()
    
    with patch("src.services.llm.LLMService.generate_study_path") as mock_path:
        mock_path.return_value = ({"weak_topics": []}, 0, 0)
        
        # Burst limit is 10/min.
        for i in range(10):
            response = client.get(
                "/api/v1/premium/adaptive-path",
                auth=("rate@test.com", "pass")
            )
            assert response.status_code == 200, f"Request {i} failed"
            
        # 11th should fail
        response = client.get(
            "/api/v1/premium/adaptive-path",
            auth=("rate@test.com", "pass")
        )
        assert response.status_code == 429
