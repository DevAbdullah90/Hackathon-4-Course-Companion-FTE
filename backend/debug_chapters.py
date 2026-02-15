from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course, Module, Chapter

def list_content():
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        for course in courses:
            print(f"Course: {course.title} (ID: {course.id})")
            modules = session.exec(select(Module).where(Module.course_id == course.id).order_by(Module.order_index)).all()
            for module in modules:
                print(f"  Module: {module.title} (Order: {module.order_index}, ID: {module.id})")
                chapters = session.exec(select(Chapter).where(Chapter.module_id == module.id).order_by(Chapter.order_index)).all()
                for chapter in chapters:
                    print(f"    Chapter: {chapter.title} (Order: {chapter.order_index}, Slug: {chapter.slug})")

if __name__ == "__main__":
    list_content()
