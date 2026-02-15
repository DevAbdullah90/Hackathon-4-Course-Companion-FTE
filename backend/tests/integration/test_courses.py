from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.base import Course

def test_list_courses_empty(client: TestClient):
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_courses_with_data(client: TestClient, session: Session):
    course = Course(title="Test Course", slug="test-course", description="Test Description")
    session.add(course)
    session.commit()
    
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Course"
    assert data[0]["slug"] == "test-course"
