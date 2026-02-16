from src.services.content import ContentService
from src.core.db import engine
from sqlmodel import Session, select
from src.models.base import Chapter

def debug():
    print("Initializing ContentService...")
    service = ContentService()
    print(f"Storage Type: {service.storage_type}")
    if hasattr(service, 'local_path'):
        print(f"Local Path: {service.local_path}")
    
    with Session(engine) as session:
        slug = "chapter-1-assessment"
        print(f"Looking for chapter: {slug}")
        chapter = session.exec(select(Chapter).where(Chapter.slug == slug)).first()
        
        if not chapter:
            print("Chapter NOT found in DB!")
            return
            
        print(f"Found Chapter: {chapter.title}")
        print(f"R2 Key: {chapter.r2_key}")
        
        print("Attempting to fetch content...")
        content = service.get_content(chapter.r2_key, db_content=chapter.content)
        
        if content:
            print("SUCCESS: Content fetched successfully!")
            print(f"First 50 chars: {content[:50]}...")
        else:
            print("FAILURE: Content is None")

if __name__ == "__main__":
    debug()
