from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ...services.llm import LLMService
from ...services.cost import CostTracker
from ...models.premium import FeatureType
from ...models.base import User
from ...core.db import get_session
from .deps import get_current_premium_user, check_rate_limit
from sqlmodel import Session

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_rate_limit) # Rate limit applies
):
    llm = LLMService()
    try:
        response_text, p_tok, c_tok = llm.chat_with_tutor(request.message, request.context)
        
        # Log usage
        CostTracker.log_usage(
            session,
            current_user.id,
            FeatureType.CHAT, 
            p_tok,
            c_tok,
            llm.model
        )
        
        return ChatResponse(response=response_text)
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="AI Tutor is temporarily unavailable")
