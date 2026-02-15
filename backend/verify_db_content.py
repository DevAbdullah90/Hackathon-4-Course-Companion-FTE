from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Chapter

def verify_content():
    print("Verifying content in Database...")
    with Session(engine) as session:
        chapters = session.exec(select(Chapter)).all()
        for chapter in chapters:
            content_preview = (chapter.content[:50] + "...") if chapter.content else "None"
            print(f"Chapter: {chapter.title}")
            print(f"  - Content stored in DB: {bool(chapter.content)}")
            print(f"  - Preview: {content_preview}")
            print("-" * 20)

if __name__ == "__main__":
    verify_content()
