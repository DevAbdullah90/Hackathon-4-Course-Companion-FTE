# Implementation Plan: Phase 3 Web Application

**Branch**: `003-web-lms-app` | **Date**: 2026-02-13 | **Spec**: [specs/003-web-lms-app/spec.md](spec.md)

## Summary
Transforming the Course Companion into a standalone, production-ready SaaS LMS. This involves implementing a React-based SPA frontend, a robust FastAPI backend with JWT authentication, a Neon Postgres database for persistent progress tracking, and a strictly isolated hybrid intelligence layer for premium features.

## Technical Context
**Language/Version**: Python 3.12+, TypeScript 5+  
**Primary Dependencies**: FastAPI, React 18+, SQLModel, Alembic, OpenAI SDK (for Gemini), Tailwind CSS  
**Storage**: Neon Postgres (Relational), Local/R2 (Content Storage)  
**Testing**: Pytest (Backend), Vitest/Playwright (Frontend)  
**Target Platform**: Vercel (Frontend), Hugging Face Spaces / Railway (Backend)  
**Performance Goals**: 100k concurrent users, <200ms API latency (p95)  
**Constraints**: Zero-LLM core, Premium-gated AI, 12s AI response limit  
**Scale/Scope**: SaaS-ready architecture with separate auth and analytics  

## Constitution Check
- [x] **Principle I & II**: Feature does not bypass deterministic core. Hybrid logic (grading/paths) is isolated in `/api/v1/premium` and strictly gated.
- [x] **Principle VI**: Delivers complete LMS experience (Dashboard, Viewer, Quizzes, Progress).
- [x] **Principle VIII**: Uses stateless backend, pooled DB connections (Neon), and modular service separation for scalability.

## Project Structure

```text
backend/
├── src/
│   ├── api/            # REST Endpoints (v1)
│   │   ├── auth.py     # JWT & Role management
│   │   ├── courses.py  # Navigation & Metadata
│   │   ├── progress.py # Persistence
│   │   └── premium/    # Isolated Hybrid Services
│   ├── core/           # Config, DB, Security
│   ├── models/         # SQLModel Schemas
│   └── services/       # Core Logic (Content, Quiz, Cost)
└── tests/

frontend/
├── src/
│   ├── api/            # API Clients
│   ├── components/     # UI Kit (LessonViewer, Quiz, Dashboard)
│   ├── context/        # Auth & Progress State
│   ├── pages/          # Dashboard, Course, Login
│   └── lib/            # Utils & Hooks
└── tests/
```

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
