from sqlmodel import Session, select
from src.core.db import engine
from src.models.base import User
from src.core.security import get_password_hash

def create_test_user():
    email = "tester@example.com"
    password = "password123"
    
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            print(f"Test user {email} already exists. Updating to Premium.")
            user.is_premium = True
            session.add(user)
            session.commit()
            return

        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name="Test User",
            is_active=True,
            is_premium=True,
            is_superuser=False
        )
        session.add(user)
        session.commit()
        print(f"Created test user: {email} / {password}")

if __name__ == "__main__":
    create_test_user()
