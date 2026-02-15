from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Course

with Session(engine) as session:
    courses = session.exec(select(Course)).all()
    for c in courses:
        print(f"ID: {c.id} | Title: {c.title} | Slug: {c.slug} | Desc: {c.description}")
