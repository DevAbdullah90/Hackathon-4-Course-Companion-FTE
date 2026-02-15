---
name: integrating-neon-postgres
description: Integrates Neon Serverless Postgres with Python backends. Use when the user requests database setup, SQLModel/SQLAlchemy configuration for Neon, or handling serverless connection pooling.
---

# Integrating Neon Postgres

## When to use this skill
- Setting up a production-ready Postgres database using Neon.
- Configuring `DATABASE_URL` for SQLModel or SQLAlchemy.
- Handling serverless connection parameters (e.g., `sslmode=require`).
- Integrating Neon's branching workflows into the development lifecycle.

## Workflow
1.  **Environment Setup**: Ensure `DATABASE_URL` is in `.env` with the `sslmode=require` parameter.
2.  **Connection Configuration**: Configure the engine with `pool_pre_ping=True` for serverless stability.
3.  **Schema Migration**: Initialize or update migrations using Alembic.
4.  **Validation**: Run the `test_connection.py` script to verify the link.

### Integration Checklist
- [ ] `DATABASE_URL` uses the `postgresql://` (or `postgresql+psycopg2://`) scheme.
- [ ] `sslmode=require` is appended to the connection string.
- [ ] `SQLModel` engine is configured for pooling.
- [ ] Alembic `env.py` is updated to pull from the environment.

## Instructions

### Connection String Template
Neon requires SSL. Your `.env` should look like:
```env
DATABASE_URL=postgresql://[user]:[password]@[hostname]/[dbname]?sslmode=require
```

### Python Engine Setup (SQLModel)
```python
from sqlmodel import create_engine
from .config import settings

# For Neon, pool_pre_ping ensures we reconnect after serverless scale-down
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    pool_pre_ping=True
)
```

### Handling Branching
When using Neon branches, create a separate `.env` for each branch or use a dynamic resolver if the agent supports it.

## Resources
- [See TEST_CONNECTION.py](scripts/test_connection.py)
- [See ALEMBIC_CONFIG.md](resources/ALEMBIC_CONFIG.md)
