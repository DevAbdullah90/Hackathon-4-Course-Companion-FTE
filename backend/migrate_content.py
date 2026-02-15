import os
from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import Chapter
from src.core.config import settings

def migrate_content():
    print("Starting content migration to Database...")
    with Session(engine) as session:
        chapters = session.exec(select(Chapter)).all()
        
        for chapter in chapters:
            if chapter.content:
                print(f"Skipping {chapter.title} (already has content in DB)")
                continue

            # Construct local path based on r2_key (which stores relative path like 'mod1/ch1.md')
            # For simplicity, we assume r2_key matches the local structure or we try to find it.
            # In previous steps we saw `local_content/mod1/ch1.md` and r2_key might be just filename or path.
            # Let's check `models/base.py` again or `add_chapter.py`.
            # `add_chapter.py` used `r2_key="agentic-patterns.md"`.
            # `debug_chapters.py` output showed slugs.
            
            # Let's assume standard path: local_content/{r2_key}
            file_path = os.path.join(settings.LOCAL_STORAGE_PATH, chapter.r2_key)
            
            # Use 'mod1/ch1.md' if r2_key is just 'ch1.md'? 
            # In `content.py`, `get_local_content` uses `os.path.join(self.local_path, key)`.
            
            if not os.path.exists(file_path):
                 # Try finding it recursively if simple join fails
                 found = False
                 for root, dirs, files in os.walk(settings.LOCAL_STORAGE_PATH):
                     if chapter.r2_key in files:
                         file_path = os.path.join(root, chapter.r2_key)
                         found = True
                         break
                 if not found:
                    print(f"Warning: Content file not found for {chapter.title} (Key: {chapter.r2_key})")
                    # Set default content for missing files (like the new chapter)
                    chapter.content = f"# {chapter.title}\n\nContent coming soon."
                    session.add(chapter)
                    continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    chapter.content = content
                    session.add(chapter)
                    print(f"Migrated: {chapter.title}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        session.commit()
    print("Migration complete.")

if __name__ == "__main__":
    migrate_content()
