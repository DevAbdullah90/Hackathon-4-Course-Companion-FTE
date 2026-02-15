# Alembic Configuration for Neon

When migrating to Neon Postgres, ensure your `alembic/env.py` dynamically loads the URL from your `Settings` or `.env` file to avoid hardcoding production credentials.

### env.py snippet
```python
from src.core.config import settings
from src.models import SQLModel # Ensure all models are imported

config = context.config
target_metadata = SQLModel.metadata

def run_migrations_online():
    # Use the URL from our central config
    connectable = create_engine(settings.DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

### Important Note
Neon's connection limit can be tight on the Free Tier. Always use `engine.dispose()` in long-running CLI scripts or ensure your FastAPI app uses a dependency-based session that closes connections promptly.
