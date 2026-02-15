from sqlmodel import Session, select
from ..core.db import engine
from ..models.base import User, Progress

def dump_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"Found {len(users)} users.")
        for u in users:
            print(f"User: {u.email}, ID: {u.id}")
            progress = session.exec(select(Progress).where(Progress.user_id == u.id)).all()
            print(f"  Progress: {len(progress)} chapters completed.")

if __name__ == "__main__":
    dump_users()
