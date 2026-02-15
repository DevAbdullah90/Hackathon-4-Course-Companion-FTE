# Research: Phase 3 Web LMS

## Decision: JWT-based Authentication
- **Rationale**: Standard for stateless FastAPI backends. Scales easily for 100k users. Allows easy role-based access control (RBAC) via claims.
- **Alternatives considered**: Session cookies (rejected due to cross-domain complexities if frontend/backend are hosted separately).

## Decision: Neon Serverless Postgres with Connection Pooling
- **Rationale**: Scalable storage that handles variable load. Integrated via SQLModel.
- **Alternatives considered**: SQLite (rejected, not production-ready for 100k users).

## Decision: Isolated Premium Service Layer
- **Rationale**: Adheres to Constitution Principle II. Ensures LLM dependencies don't bloat the core service container.
- **Alternatives considered**: Integrated LLM calls (rejected for performance and isolation concerns).

## Decision: Staggered Dashboard Aggregation
- **Rationale**: To handle 100k users, the dashboard will fetch high-level progress summaries first, then lazy-load detailed module analytics.
- **Alternatives considered**: Single massive join query (rejected for database performance reasons).
