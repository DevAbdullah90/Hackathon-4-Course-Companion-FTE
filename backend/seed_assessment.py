from src.core.db import engine
from sqlmodel import Session, select
from src.models.base import Chapter, Module, Course, Quiz

def seed():
    with Session(engine) as session:
        # FInd a course
        course = session.exec(select(Course)).first()
        if not course:
            print("No course found. Please run main seeder first.")
            return

        # Find a module
        module = session.exec(select(Module).where(Module.course_id == course.id)).first()
        if not module:
            module = Module(title="Introduction", slug="intro", course_id=course.id, order_index=1, description="Intro module")
            session.add(module)
            session.commit()
            session.refresh(module)

        # Create Assessment Chapter
        slug = "chapter-1-assessment"
        existing = session.exec(select(Chapter).where(Chapter.slug == slug)).first()
        
        if not existing:
            chapter = Chapter(
                title="Chapter 1 Assessment",
                slug=slug,
                module_id=module.id,
                r2_key="mod1/assessment.md", # This acts as the key for local storage too
                order_index=99,
                is_premium=True
            )
            session.add(chapter)
            session.commit()
            session.refresh(chapter)
            
            # Add a dummy quiz for it so it doesn't crash if Frontend expects quiz
            quiz = Quiz(
                chapter_id=chapter.id,
                title="Assessment Quiz",
                content={"questions": [{"id": "q1", "text": "Describe the key differences between HTML, CSS, and JavaScript."}]}
            )
            session.add(quiz)
            session.commit()

            print(f"Created Assessment Chapter: {chapter.title} (slug: {slug})")
        else:
            print(f"Assessment Chapter already exists: {slug}")

if __name__ == "__main__":
    seed()
