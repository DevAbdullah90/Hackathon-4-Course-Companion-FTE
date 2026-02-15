from sqlmodel import SQLModel, create_engine
from .config import settings

# pool_pre_ping=True is recommended for serverless Postgres (Neon)
# to handle connections that may have been closed by the server.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
