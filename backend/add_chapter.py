from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course, Module, Chapter

def add_chapter():
    with Session(engine) as session:
        # Get the first course
        course = session.exec(select(Course)).first()
        if not course:
            print("No course found. Creating one...")
            course = Course(title="AI Agent Dev", description="Test Course", is_published=True)
            session.add(course)
            session.commit()
            session.refresh(course)
            print(f"Created Course: {course.title}")

        # Get the first module
        module = session.exec(select(Module).where(Module.course_id == course.id)).first()
        if not module:
            print("No module found. Creating one...")
            module = Module(title="Foundations", description="Core concepts", order_index=1, course_id=course.id)
            session.add(module)
            session.commit()
            session.refresh(module)
            print(f"Created Module: {module.title}")
        
        # Check if chapter 2 exists
        chapter_2 = session.exec(select(Chapter).where(Chapter.slug == "agentic-patterns")).first()
        if chapter_2:
            print("Chapter 2 already exists.")
            return

        # Create Chapter 2
        chapter = Chapter(
            title="Agentic Patterns",
            slug="agentic-patterns",
            description="Introduction to agentic design patterns",
            r2_key="agentic-patterns.md", 
            order_index=2,
            module_id=module.id,
            is_premium=False,
            is_published=True
        )
        session.add(chapter)
        session.commit()
        print(f"Successfully added Chapter 2: {chapter.title}")

if __name__ == "__main__":
    add_chapter()
