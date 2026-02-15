# Implementation Plan: Course Companion Phase 1 (Zero-Backend-LLM)

**Branch**: `001-course-companion` | **Date**: 2026-02-12 | **Spec**: [specs/001-course-companion/spec.md](../spec.md)
**Input**: Feature specification from `specs/001-course-companion/spec.md`

## Summary

Implement the backend and frontend structure for a Course Companion FTE. The backend will be a deterministic FastAPI service serving content from Cloudflare R2, managing auth/progress via PostgreSQL, and enforcing zero LLM calls. The frontend will be a ChatGPT App (OpenAI Apps SDK) handling all pedagogical intelligence.

## Technical Context

**Language/Version**: Python 3.11+ (Backend)
**Primary Dependencies**: FastAPI (Web Framework), SQLAlchemy/Pydantic (ORM/Data), Boto3 (R2 Access)
**Storage**: PostgreSQL (Neon/Supabase) for user/progress; Cloudflare R2 for static content
**Testing**: pytest (Unit/Integration)
**Target Platform**: Fly.io or Railway (Containerized Backend)
**Project Type**: Hybrid (Backend API + ChatGPT App Manifest)
**Performance Goals**: <200ms API latency for content/navigation
**Constraints**: ZERO LLM calls from backend (Strict audit requirement)
**Scale/Scope**: 10k+ concurrent users, scalable stateless architecture

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Zero-Backend-LLM Architecture**: ✅ Plan explicitly forbids LLM calls in backend.
- **II. Deterministic Backend Responsibility**: ✅ Backend limited to content, auth, grading.
- **III. Strict Content Grounding**: ✅ Enforced by frontend prompt design (out of scope for backend logic but supported by content API).
- **IV. Scalability & Efficiency**: ✅ R2 + Stateless FastAPI meets 100k+ scale goal.
- **V. Clean Architectural Separation**: ✅ Clear boundary: Backend = Deterministic, Frontend = Probabilistic.

## Project Structure

### Documentation (this feature)

```text
specs/001-course-companion/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # Routes: chapters, quizzes, etc.
│   ├── core/            # Config, security, database
│   ├── models/          # SQLModel/Pydantic schemas
│   ├── services/        # Business logic (R2, Grading)
│   └── main.py          # App entrypoint
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
└── requirements.txt

frontend/                # ChatGPT App definition
├── manifest.json        # OpenAI plugin/app manifest
├── openapi.yaml         # API definition for ChatGPT
└── instructions.md      # System prompt for the Agent
```

**Structure Decision**: Split repository into `backend/` (Python service) and `frontend/` (Configuration for ChatGPT App). This reflects the architectural separation required by the constitution.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |
