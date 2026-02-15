---
id: 002
title: course-companion-spec
stage: spec
date: 2026-02-12
surface: agent
model: gemini-2.0-flash
feature: course-companion
branch: 001-course-companion
user: user
command: /sp.specify
labels: ["spec", "feature", "zero-backend-llm"]
links:
  spec: specs/001-course-companion/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-course-companion/spec.md
 - specs/001-course-companion/checklists/requirements.md
tests:
 - none
---

## Prompt

Write a complete Specification Document for Phase 1 of a Course Companion FTE teaching AI Agent Development. Scope: Phase 1 ONLY (Zero-Backend-LLM). Include: 1. Product Overview 2. Course Structure (Modules, Chapters, Subtopics) 3. User Personas (Beginner, Intermediate, Advanced) 4. Feature Requirements: - Content Delivery - Chapter Navigation - Grounded Q&A - Rule-Based Quizzes - Progress Tracking - Freemium Gate 5. ChatGPT App Responsibilities 6. Backend Responsibilities (Deterministic Only) 7. API Design Overview (REST endpoints) 8. Data Models (User, Progress, Chapter, Quiz) 9. Runtime Agent Skills Required: - concept-explainer - quiz-master - socratic-tutor - progress-motivator 10. Non-Functional Requirements: - Scalability - Latency - Cost Constraints - Zero LLM backend enforcement Do NOT include hybrid intelligence. Explicitly mention that backend contains ZERO LLM calls.

## Response snapshot

Created feature specification for 'Course Companion Phase 1'.
Defined 5 prioritized user stories (Content, Quiz, Grounded Q&A, Freemium, Progress).
Detailed functional requirements enforcing Zero-Backend-LLM and deterministic behavior.
Specified key entities (User, Course, Module, Chapter, Quiz, Progress).
Defined measurable success criteria (Latency < 200ms, Zero LLM calls).
Created quality checklist.

## Outcome

- ✅ Impact: Feature specification created.
- 🧪 Tests: N/A
- 📁 Files: specs/001-course-companion/spec.md, specs/001-course-companion/checklists/requirements.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Successfully navigated the conflict between "include API details" and "no implementation details" by framing them as Key Entities and Functional Requirements.

## Evaluation notes (flywheel)

- Failure modes observed: `create-new-feature.ps1` script argument parsing failed on Windows.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): Fix PowerShell script argument handling.
