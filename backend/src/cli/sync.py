# Simple CLI script to sync local/seed data to DB
# Real impl would scan R2 bucket
from sqlmodel import Session, select
from ..core.db import engine, init_db
from ..models.base import Course, Module, Chapter

def sync_data():
    init_db()
    with Session(engine) as session:
        # Correctly query using SELECT and slug, instead of session.get() with an invalid UUID string
        # session.get expects a valid Primary Key (UUID), "seed-course-id" is not a UUID
        statement = select(Course).where(Course.slug == "ai-agents")
        existing_course = session.exec(statement).first()
        
        if existing_course:
             print("Seed data already exists.")
             return

        # Create Seed Course
        c1 = Course(title="AI Agent Dev", slug="ai-agents", description="Learn 8-layer architecture")
        session.add(c1)
        session.commit()
        session.refresh(c1)

        # Create Module 1
        m1 = Module(course_id=c1.id, title="Foundations", order_index=1)
        session.add(m1)
        session.commit()
        session.refresh(m1)

        # Create Chapter 1
        ch1 = Chapter(module_id=m1.id, title="Deterministic vs Agentic", slug="det-vs-agent", r2_key="mod1/ch1.md", order_index=1)
        session.add(ch1)
        session.commit()

        print("Sync complete.")

if __name__ == "__main__":
    sync_data()
