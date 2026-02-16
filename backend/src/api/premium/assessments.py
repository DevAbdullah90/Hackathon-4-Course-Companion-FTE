from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Dict, Any

from ...models.premium import PremiumAssessment, FeatureType
from ...models.base import User, Quiz
from ...services.llm import LLMService
from ...services.cost import CostTracker
from ...core.db import get_session
from .deps import get_current_premium_user, check_rate_limit

router = APIRouter()

class AssessmentRequest(BaseModel):
    chapter_id: str
    question_id: str
    user_answer: str

class AssessmentResponse(BaseModel):
    score: int
    feedback: Dict[str, Any]
    reasoning: str
    usage_id: str

@router.post("/grade", response_model=AssessmentResponse)
async def grade_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_rate_limit)
):
    # Fetch quiz content to get question text (Grounding)
    # We join Chapter to match by chapter_id (which is a string slug in request?)
    # Wait, spec says chapter_id is string. User model has UUID.
    # Chapter model has `slug` (string) and `id` (UUID).
    # Assuming request uses slug for chapter_id or UUID string?
    # Let's check Chapter model. It has slug and id. Usually public API uses slug.
    # I'll try to find by slug or ID.
    
    # Simple query: find Quiz linked to Chapter where slug == request.chapter_id
    from ...models.base import Chapter
    statement = select(Quiz).join(Chapter).where(Chapter.slug == request.chapter_id)
    quiz = session.exec(statement).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this chapter")
        
    # Extract question text
    question_text = None
    # Assume content structure: { "questions": [ {"id": "q1", "text": "..."} ] }
    questions = quiz.content.get("questions", [])
    for q in questions:
        if q.get("id") == request.question_id:
            question_text = q.get("text")
            break
            
    if not question_text:
        # Fallback if structure differs or question missing
        raise HTTPException(status_code=404, detail="Question ID not found in quiz content")

    # Call LLM
    llm = LLMService()
    result, p_tok, c_tok = llm.grade_assessment(question_text, request.user_answer)
    
    # Log usage synchronously for MVP reliability
    usage = CostTracker.log_usage(
        session,
        current_user.id,
        FeatureType.ASSESSMENT,
        p_tok,
        c_tok,
        llm.model
    )
    
    # Save assessment record
    assessment = PremiumAssessment(
        user_id=current_user.id,
        chapter_id=request.chapter_id,
        question_context=question_text,
        user_answer=request.user_answer,
        score=result.get("score", 0),
        llm_feedback=result.get("feedback", {}),
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)
    
    return AssessmentResponse(
        score=assessment.score,
        feedback=assessment.llm_feedback,
        reasoning=result.get("reasoning", ""),
        usage_id=str(usage.id)
    )
