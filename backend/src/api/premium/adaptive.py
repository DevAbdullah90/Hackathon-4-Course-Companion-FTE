from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session
from ...models.base import User
from ...models.premium import FeatureType
from ...services.llm import LLMService
from ...services.quiz import QuizService
from ...services.cost import CostTracker
from ...core.db import get_session
from .deps import get_current_premium_user, check_rate_limit

router = APIRouter()

@router.get("/adaptive-path")
async def get_adaptive_path(
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_rate_limit)
):
    quiz_service = QuizService()
    weak_modules = quiz_service.get_weak_modules(session, current_user.id)
    
    llm = LLMService()
    result, p_tok, c_tok = llm.generate_study_path(weak_modules)
    
    if p_tok > 0:
        # Log usage synchronously for MVP
        CostTracker.log_usage(
            session,
            current_user.id,
            FeatureType.ADAPTIVE_PATH,
            p_tok,
            c_tok,
            llm.model
        )
        
    return result
