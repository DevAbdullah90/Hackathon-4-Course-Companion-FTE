from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, JSON
from uuid import UUID, uuid4
from enum import Enum

class FeatureType(str, Enum):
    ASSESSMENT = "ASSESSMENT"
    ADAPTIVE_PATH = "ADAPTIVE_PATH"
    CHAT = "CHAT"

class PremiumAssessment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    chapter_id: str = Field(index=True)
    question_context: str
    user_answer: str
    llm_feedback: Dict = Field(default={}, sa_type=JSON)
    score: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TokenUsage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    feature_type: FeatureType
    prompt_tokens: int
    completion_tokens: int
    model_name: str
    estimated_cost_usd: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
