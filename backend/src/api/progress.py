from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.db import get_session
from ..models.base import Progress, User, Chapter
from ..api.deps import get_current_user
from datetime import datetime, date

router = APIRouter()

from pydantic import BaseModel
from typing import Optional

class ProgressRequest(BaseModel):
    chapter_slug: str
    is_completed: bool
    quiz_score: Optional[int] = None

@router.post("/")
def update_progress(
    request: ProgressRequest,
    user: User = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    chapter_slug = request.chapter_slug
    is_completed = request.is_completed
    quiz_score = request.quiz_score
    chapter = session.exec(select(Chapter).where(Chapter.slug == chapter_slug)).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    progress = session.get(Progress, (user.id, chapter.id))
    if not progress:
        progress = Progress(user_id=user.id, chapter_id=chapter.id)
    
    progress.is_completed = is_completed
    if quiz_score is not None:
        progress.quiz_score = quiz_score
    
    if is_completed:
        progress.completed_at = datetime.utcnow()
    
    # Update Streak
    today = date.today()
    if user.last_active_date:
        if user.last_active_date.date() == today:
            pass # Already active today
        elif (today - user.last_active_date.date()).days == 1:
            user.streak_count += 1
        else:
            user.streak_count = 1
    else:
        user.streak_count = 1
    
    user.last_active_date = datetime.utcnow()
    
    session.add(progress)
    session.add(user)
    session.commit()
    
    return {
        "status": "updated", 
        "streak": user.streak_count,
        "is_completed": progress.is_completed
    }
