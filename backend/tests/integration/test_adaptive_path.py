from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.base import User, Course, Module, Chapter, Progress
from unittest.mock import patch
from uuid import uuid4

def test_adaptive_path(client: TestClient, session: Session):
    # Setup data
    course = Course(title="C1", description="D1", slug="c1")
    session.add(course)
    module = Module(course=course, title="Weak Module", order_index=1)
    session.add(module)
    chapter = Chapter(module=module, title="Ch1", slug="ch1", r2_key="ch1.md", order_index=1, is_premium=True)
    session.add(chapter)
    session.commit()
    
    user = User(email="premium@test.com", is_premium=True)
    session.add(user)
    session.commit()
    
    # Add progress with low score
    progress = Progress(user_id=user.id, chapter_id=chapter.id, is_completed=True, quiz_score=50)
    session.add(progress)
    session.commit()
    
    # Mock LLM
    with patch("src.services.llm.LLMService.generate_study_path") as mock_path:
        mock_path.return_value = (
            {"weak_topics": ["Weak Module"], "recommendations": [{"topic": "Weak Module", "action_item": "Review Ch1"}]},
            100, 50
        )
        
        response = client.get(
            "/api/v1/premium/adaptive-path",
            auth=("premium@test.com", "pass")
        )
        
    assert response.status_code == 200
    data = response.json()
    assert data["weak_topics"] == ["Weak Module"]

def test_adaptive_path_free_user(client: TestClient, session: Session):
    user = User(email="free@test.com", is_premium=False)
    session.add(user)
    session.commit()
    
    response = client.get(
        "/api/v1/premium/adaptive-path",
        auth=("free@test.com", "pass")
    )
    assert response.status_code == 403
