from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.base import User, Course, Module, Chapter, Quiz
from src.models.premium import FeatureType
from src.services.llm import LLMService
from unittest.mock import patch
from uuid import uuid4

def test_grade_assessment_premium(client: TestClient, session: Session):
    # Setup Data Hierarchy
    course = Course(title="C1", description="D1", slug="c1")
    session.add(course)
    module = Module(course=course, title="M1", order_index=1)
    session.add(module)
    chapter = Chapter(module=module, title="Test", slug="ch1", r2_key="ch1.md", order_index=1, is_premium=True)
    session.add(chapter)
    session.commit() # Get IDs
    
    quiz_content = {"questions": [{"id": "q1", "text": "What is AI?"}]}
    quiz = Quiz(chapter_id=chapter.id, content=quiz_content)
    session.add(quiz)
    
    user = User(email="premium@test.com", is_premium=True)
    session.add(user)
    session.commit()

    # Mock LLM
    with patch("src.services.llm.LLMService.grade_assessment") as mock_grade:
        mock_grade.return_value = (
            {"score": 5, "feedback": {"strengths": ["Good logic"]}, "reasoning": "Perfect"},
            100, 50
        )
        
        # Override dependency or rely on Basic Auth. 
        # deps.py looks up user by email=username.
        response = client.post(
            "/api/v1/premium/assessments/grade",
            auth=("premium@test.com", "pass"), 
            json={
                "chapter_id": "ch1",
                "question_id": "q1",
                "user_answer": "AI is artificial intelligence."
            }
        )
        
    if response.status_code != 200:
        print(response.json())
        
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 5
    assert "usage_id" in data

def test_grade_assessment_free_user(client: TestClient, session: Session):
    user = User(email="free@test.com", is_premium=False)
    session.add(user)
    session.commit()
    
    response = client.post(
        "/api/v1/premium/assessments/grade",
        auth=("free@test.com", "pass"),
        json={"chapter_id": "ch1", "question_id": "q1", "user_answer": "test"}
    )
    assert response.status_code == 403
