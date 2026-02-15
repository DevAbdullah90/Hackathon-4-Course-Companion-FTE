from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course, User

def check_db():
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        users = session.exec(select(User)).all()
        
        print(f"--- DB CHECK ---")
        print(f"Users found: {len(users)}")
        print(f"Courses found: {len(courses)}")
        
        for c in courses:
            print(f"Course: {c.title} ({c.slug})")

if __name__ == "__main__":
    check_db()
