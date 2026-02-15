from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course

with Session(engine) as session:
    # Find courses with title "AI Agent Dev"
    courses = session.exec(select(Course).where(Course.title == "AI Agent Dev")).all()
    print(f"Found {len(courses)} courses with title 'AI Agent Dev':")
    for c in courses:
        print(f"ID: {c.id}")
        print(f"Description: {c.description}")
        print("-" * 20)
