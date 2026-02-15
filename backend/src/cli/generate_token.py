from datetime import timedelta
from jose import jwt
from ..core.config import settings

def create_access_token(user_id: str):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(encoded_jwt)

if __name__ == "__main__":
    create_access_token("032ecefc-d781-4993-8911-bcbb23376610")
