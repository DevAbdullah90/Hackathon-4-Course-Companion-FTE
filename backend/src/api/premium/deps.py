from fastapi import Depends, HTTPException, status
from ...api.deps import get_current_user
from ...models.base import User

def get_current_premium_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required to access this content."
        )
    return user

import time
from collections import defaultdict

# Simple in-memory store: user_id -> list of timestamps
request_history = defaultdict(list)

def check_rate_limit(user: User = Depends(get_current_premium_user)) -> User:
    now = time.time()
    user_id = str(user.id)
    history = request_history[user_id]
    
    # Clean old requests (> 1 hour)
    # limit: 50 req/hr
    valid_history = [t for t in history if now - t < 3600]
    request_history[user_id] = valid_history
    
    if len(valid_history) >= 50:
        raise HTTPException(status_code=429, detail="Hourly rate limit exceeded (50 req/hr)")
        
    # Burst check (last minute)
    # limit: 10 req/min
    minute_history = [t for t in valid_history if now - t < 60]
    if len(minute_history) >= 10: 
        raise HTTPException(status_code=429, detail="Burst limit exceeded (10 req/min)")
        
    request_history[user_id].append(now)
    return user
