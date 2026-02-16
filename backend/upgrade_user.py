from src.core.db import engine
from sqlmodel import Session, select
from src.models.base import User

def upgrade_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        if not users:
            print("No users found!")
            return

        for user in users:
            print(f"Found user: {user.email} (Premium: {user.is_premium})")
            if not user.is_premium:
                user.is_premium = True
                session.add(user)
                print(f"-> Upgraded {user.email} to Premium.")
            else:
                print(f"-> {user.email} is already Premium.")
        
        session.commit()
        print("All users updated.")

if __name__ == "__main__":
    upgrade_all_users()
