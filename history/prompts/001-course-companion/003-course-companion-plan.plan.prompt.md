---
id: 003
title: course-companion-plan
stage: plan
date: 2026-02-12
surface: agent
model: gemini-2.0-flash
feature: course-companion
branch: 001-course-companion
user: user
command: /sp.plan
labels: ["plan", "architecture", "zero-backend-llm", "fastapi"]
links:
  spec: specs/001-course-companion/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-course-companion/plan.md
 - specs/001-course-companion/research.md
 - specs/001-course-companion/data-model.md
 - specs/001-course-companion/contracts/openapi.yaml
 - specs/001-course-companion/quickstart.md
tests:
 - none
---

## Prompt

Create a detailed Engineering Plan for implementing Phase 1 of the Course Companion FTE using:

Backend: FastAPI (Python)
Storage: Cloudflare R2
Database: PostgreSQL (Neon or Supabase)
Frontend: ChatGPT App (OpenAI Apps SDK)

Plan must include:

1. Project structure (folder hierarchy)
2. API grouping:
   - /chapters
   - /navigation
   - /quizzes
   - /progress
   - /search
   - /access
3. Content ingestion strategy into R2
4. Deterministic quiz grading logic
5. Progress tracking logic
6. Search implementation strategy
7. Freemium gating logic
8. ChatGPT App manifest structure
9. Skill loading structure
10. Deployment strategy (Fly.io or Railway)

Emphasize Zero-Backend-LLM compliance at every step.

## Response snapshot

Created detailed implementation plan for Course Companion Phase 1.
Plan confirms 5/5 constitution checks.
Architecture: Hybrid (FastAPI + ChatGPT App).
Decisions made:
- PostgreSQL for data.
- Cloudflare R2 for content.
- Static answer key grading.
- Fly.io for deployment.
Generated artifacts: plan.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md.

## Outcome

- ✅ Impact: Technical plan ratified.
- 🧪 Tests: N/A
- 📁 Files: specs/001-course-companion/*
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The strict separation of concerns (backend=deterministic, frontend=intelligence) is now concrete in the file structure and API design.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` still failing on Windows execution.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): Use `setup-plan.ps1` for next phase but fix `create-phr` path for windows manually in future.
