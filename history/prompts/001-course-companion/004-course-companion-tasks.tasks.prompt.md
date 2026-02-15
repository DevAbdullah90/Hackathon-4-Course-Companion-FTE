---
id: 004
title: course-companion-tasks
stage: tasks
date: 2026-02-12
surface: agent
model: gemini-2.0-flash
feature: course-companion
branch: 001-course-companion
user: user
command: /sp.tasks
labels: ["tasks", "plan", "zero-backend-llm"]
links:
  spec: specs/001-course-companion/spec.md
  plan: specs/001-course-companion/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-course-companion/tasks.md
tests:
 - none
---

## Prompt

Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.

Context for task generation: Break Phase 1 implementation into granular engineering tasks. Tasks must be grouped into: 1. Backend Setup 2. Database Setup 3. Cloudflare R2 Setup 4. API Development 5. Quiz Engine 6. Progress System 7. Access Control 8. Search System 9. ChatGPT App Integration 10. Runtime Skills Creation 11. Testing & Validation 12. Deployment Each task must: - Be atomic - Have clear completion criteria - Mention Zero-Backend-LLM validation checks

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Response snapshot

Generated `specs/001-course-companion/tasks.md` containing 35 tasks across 8 phases.
- Phase 1: Setup (Backend structure, Docker)
- Phase 2: Foundational (DB, R2, Models, Auth)
- Phase 3: US1 Content (MVP)
- Phase 4: US2 Quizzes
- Phase 5: US3 Chat Integration
- Phase 6: US4 Freemium
- Phase 7: US5 Progress
- Phase 8: Polish
Tasks are organized by User Story dependencies with clear "Independent Test" criteria for each story.

## Outcome

- ✅ Impact: Actionable task list created.
- 🧪 Tests: N/A
- 📁 Files: specs/001-course-companion/tasks.md
- 🔁 Next prompts: /sp.analyze (consistency check) or /sp.implement
- 🧠 Reflection: Task granularity is sufficient for automated execution. The separation of Backend vs ChatGPT App tasks is clear.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` on Windows.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None.
