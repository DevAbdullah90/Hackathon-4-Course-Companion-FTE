from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course, Module, Chapter, Progress

course_id_to_delete = "228adaed-e413-4a05-8296-a0ebf57b3c72"

with Session(engine) as session:
    course = session.get(Course, course_id_to_delete)
    if course:
        print(f"Deleting course: {course.title} (ID: {course.id})")
        
        # 1. Find Modules
        modules = session.exec(select(Module).where(Module.course_id == course.id)).all()
        for module in modules:
            # 2. Find Chapters in Module
            chapters = session.exec(select(Chapter).where(Chapter.module_id == module.id)).all()
            for chapter in chapters:
                # 3. Delete Progress for Chapter
                chapter_progress = session.exec(select(Progress).where(Progress.chapter_id == chapter.id)).all()
                for p in chapter_progress:
                    session.delete(p)
                
                # 4. Delete Chapter
                session.delete(chapter)
            
            # 5. Delete Module
            session.delete(module)
        
        print(f"Deleted {len(modules)} Modules and related Chapters/Progress.")

        # 6. Delete Course
        session.delete(course)
        session.commit()
        print("Successfully deleted course and all dependencies.")
    else:
        print(f"Course with ID {course_id_to_delete} not found.")
