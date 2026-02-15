from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.db import get_session
from ..models.base import Chapter, User, Module
from ..services.content import ContentService
from .deps import get_current_user

router = APIRouter()
content_service = ContentService()

@router.get("/{slug}/content")
def get_chapter_content(
    slug: str, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chapter = session.exec(select(Chapter).where(Chapter.slug == slug)).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    if chapter.is_premium and not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium content")
    
    content = content_service.get_content(chapter.r2_key, db_content=chapter.content)
    if content is None:
         raise HTTPException(status_code=500, detail="Content unavailable")

    # Find next chapter
    # 1. Next chapter in same module
    next_chapter = session.exec(
        select(Chapter)
        .where(Chapter.module_id == chapter.module_id)
        .where(Chapter.order_index > chapter.order_index)
        .order_by(Chapter.order_index)
    ).first()

    if not next_chapter:
        # 2. First chapter of next module
        current_module = session.get(Module, chapter.module_id)
        if current_module:
            next_module = session.exec(
                select(Module)
                .where(Module.course_id == current_module.course_id)
                .where(Module.order_index > current_module.order_index)
                .order_by(Module.order_index)
            ).first()
            
            if next_module:
                next_chapter = session.exec(
                    select(Chapter)
                    .where(Chapter.module_id == next_module.id)
                    .order_by(Chapter.order_index)
                ).first()

    return {
        "id": chapter.id,
        "title": chapter.title,
        "markdown_content": content,
        "next_chapter_slug": next_chapter.slug if next_chapter else None,
        "quiz": chapter.quiz.content if chapter.quiz else None
    }
