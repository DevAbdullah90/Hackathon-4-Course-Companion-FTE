import logging
import os
from dotenv import load_dotenv

# Force load from root .env
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if not os.path.exists(root_env):
    root_env = os.path.abspath(os.path.join(os.getcwd(), ".env"))

print(f"DEBUG: Loading .env from: {root_env}")
load_dotenv(root_env, override=True)

from sqlmodel import Session, select
from src.core.config import settings
from src.core.db import engine, init_db
from src.core.security import get_password_hash
from src.models.base import User, Course, Module, Chapter, Progress, Quiz
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_full():
    logger.info("Initializing Database (Creating Tables)...")
    init_db()
    
    with Session(engine) as session:
        # 1. Create Premium User
        user_email = "test@example.com"
        user = session.exec(select(User).where(User.email == user_email)).first()
        if not user:
            logger.info(f"Creating premium user: {user_email}")
            user = User(
                email=user_email,
                hashed_password=get_password_hash("password"),
                is_premium=True,
                full_name="Test User"
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        else:
            logger.info(f"User {user_email} already exists.")
            if not user.is_premium:
                user.is_premium = True
                session.add(user)
                session.commit()

        # 2. Create Course
        course_slug = "ai-agent-dev"
        course = session.exec(select(Course).where(Course.slug == course_slug)).first()
        if not course:
            logger.info(f"Creating course: {course_slug}")
            course = Course(
                title="AI Agent Development",
                slug=course_slug,
                description="Learn to build autonomous AI agents with Python and LLMs.",
                is_published=True
            )
            session.add(course)
            session.commit()
            session.refresh(course)
        else:
             logger.info(f"Course {course_slug} already exists.")

        # 3. Create Module
        module_title = "Module 1: Foundations"
        module = session.exec(select(Module).where(Module.course_id == course.id, Module.title == module_title)).first()
        
        if not module:
            logger.info(f"Creating module: {module_title}")
            module = Module(
                course_id=course.id,
                title=module_title,
                description="Introduction to AI Agents",
                order_index=1
            )
            session.add(module)
            session.commit()
            session.refresh(module)
        else:
             logger.info(f"Module {module_title} already exists.")

        # 4. Create Chapter
        chapter_slug = "mod1-assessment"
        chapter = session.exec(select(Chapter).where(Chapter.slug == chapter_slug)).first()
        if not chapter:
            logger.info(f"Creating chapter: {chapter_slug}")
            chapter = Chapter(
                module_id=module.id,
                title="Module 1 Assessment",
                slug=chapter_slug,
                r2_key="mod1/assessment.md",
                is_premium=True,
                order_index=1
            )
            session.add(chapter)
            session.commit()
            session.refresh(chapter) # Refresh to get ID
            logger.info(f"Chapter {chapter_slug} created.")
        else:
            logger.info(f"Chapter {chapter_slug} already exists.")
        
        # 5. Create Quiz (Required for Assessment)
        # Check if quiz exists for this chapter
        quiz = session.exec(select(Quiz).where(Quiz.chapter_id == chapter.id)).first()
        if not quiz:
            logger.info(f"Creating quiz for chapter: {chapter_slug}")
            quiz = Quiz(
                chapter_id=chapter.id,
                content={
                    "questions": [
                        {
                            "id": "q1", 
                            "text": "Explain the difference between tool-use and agentic workflow.",
                            "type": "essay"
                        }
                    ]
                }
            )
            session.add(quiz)
            session.commit()
        else:
            logger.info("Quiz already exists.")

        logger.info("Seeding complete!")

if __name__ == "__main__":
    seed_full()
