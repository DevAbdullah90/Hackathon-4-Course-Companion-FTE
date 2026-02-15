from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from ...core.db import get_session
from ...models.premium import TokenUsage
from ...models.base import User, Progress
from ..deps import get_current_admin_user

router = APIRouter()

@router.get("/summary")
def get_system_summary(
    session: Session = Depends(get_session),
    admin: User = Depends(get_current_admin_user)
):
    total_users = session.exec(select(func.count(User.id))).one()
    premium_users = session.exec(select(func.count(User.id)).where(User.is_premium == True)).one()
    
    total_tokens = session.exec(select(func.sum(TokenUsage.prompt_tokens + TokenUsage.completion_tokens))).one() or 0
    total_cost = session.exec(select(func.sum(TokenUsage.estimated_cost_usd))).one() or 0
    
    # Usage by feature
    # Using SQLAlchemy style for grouping
    from sqlalchemy import select as sa_select
    usage_by_feature = session.exec(
        sa_select(TokenUsage.feature_type, func.count(TokenUsage.id), func.sum(TokenUsage.estimated_cost_usd))
        .group_by(TokenUsage.feature_type)
    ).all()
    
    return {
        "users": {
            "total": total_users,
            "premium": premium_users,
            "free": total_users - premium_users
        },
        "llm_usage": {
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "by_feature": [
                {"feature": row[0], "calls": row[1], "cost": round(row[2], 4)} 
                for row in usage_by_feature
            ]
        }
    }
