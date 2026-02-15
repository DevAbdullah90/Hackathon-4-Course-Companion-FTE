import os
from sqlmodel import create_engine, Session, select, text
import sys

def test_db():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("Error: DATABASE_URL not found in environment.")
        return False

    if "sslmode=require" not in url:
        print("Warning: sslmode=require missing from DATABASE_URL. Neon may reject connection.")

    try:
        engine = create_engine(url)
        with Session(engine) as session:
            # Simple health check
            session.exec(text("SELECT 1"))
        print("Success: Connected to Neon Postgres.")
        return True
    except Exception as e:
        print(f"Connection Failed: {e}")
        return False

if __name__ == "__main__":
    if test_db():
        sys.exit(0)
    else:
        sys.exit(1)
