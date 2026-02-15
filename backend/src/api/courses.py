from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..core.db import get_session
from ..models.base import Course, Module, Chapter, Progress, User
from .deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Course])
def list_courses(session: Session = Depends(get_session)):
    # Explicitly join to ensure data is loaded, though SQLModel usually handles this if response_model is set.
    # However, for deep nesting (Course -> Module -> Chapter), we might need to be careful.
    # Let's try to just return the results and rely on SQLModel relationship loading.
    # If it fails, we might need a custom response model or explicit join.
    courses = session.exec(select(Course)).all()
    return courses


@router.get("/{slug}/dashboard")
def get_course_dashboard(
    slug: str, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    course = session.exec(select(Course).where(Course.slug == slug)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Calculate progress
    total_chapters = session.exec(
        select(Chapter)
        .join(Module)
        .where(Module.course_id == course.id)
        .order_by(Module.order_index, Chapter.order_index)
    ).all()
    
    completed_progress = session.exec(
        select(Progress)
        .where(Progress.user_id == current_user.id)
        .where(Progress.chapter_id.in_([c.id for c in total_chapters]))
        .where(Progress.is_completed == True)
    ).all()
    
    completed_ids = {p.chapter_id for p in completed_progress}
    
    # Find first incomplete chapter, or default to first chapter if all complete
    next_chapter = next(
        (c for c in total_chapters if c.id not in completed_ids), 
        total_chapters[0] if total_chapters else None
    )
    
    print(f"DEBUG: slug={slug}")
    print(f"DEBUG: total_chapters={len(total_chapters)}")
    print(f"DEBUG: completed_ids={len(completed_ids)}")
    print(f"DEBUG: next_chapter={next_chapter}")
    print(f"DEBUG: next_chapter_slug={next_chapter.slug if next_chapter else 'None'}")
    
    return {
        "course": course,
        "total_chapters": len(total_chapters),
        "completed_chapters": len(completed_progress),
        "percentage": (len(completed_progress) / len(total_chapters) * 100) if total_chapters else 0,
        "next_chapter_slug": next_chapter.slug if next_chapter else None
    }
