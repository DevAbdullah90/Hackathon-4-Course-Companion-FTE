from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..core.db import get_session
from ..models.base import Chapter, Quiz, Progress
from ..services.quiz import QuizService
from typing import Dict
from datetime import datetime

router = APIRouter()
quiz_service = QuizService()

@router.post("/{chapter_id}/grade")
def grade_quiz(chapter_id: str, submission: Dict[str, str], session: Session = Depends(get_session)):
    # 1. Get Quiz for Chapter
    # Note: Simplified query, assumes 1-1 relation via Chapter.quiz
    # Ideally query Quiz where chapter_id matches
    # For now fetching chapter first
    chapter = session.get(Chapter, chapter_id)
    if not chapter or not chapter.quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this chapter")
    
    quiz = chapter.quiz
    answer_key = quiz.content.get("answer_key", {})

    # 2. Grade
    result = quiz_service.grade_quiz(submission, answer_key)

    # 3. Save Progress (simplified - ideally via ProgressService)
    # This logic overlaps with US5, but adding basic save here for completeness of "Grading"
    # Assuming user_id is passed or mocked for now (Phase 1 MVP)
    # Real implementation would use current_user from auth
    
    return result
