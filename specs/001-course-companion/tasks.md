---
description: "Task list for Course Companion Phase 1 implementation"
---

# Tasks: Course Companion Phase 1 (Zero-Backend-LLM)

**Input**: Design documents from `/specs/001-course-companion/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml, research.md, quickstart.md
**Feature Branch**: `001-course-companion`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend project structure (src/api, src/core, src/models, src/services)
- [ ] T002 Initialize Python FastAPI project with requirements.txt (FastAPI, SQLModel, Boto3, uvicorn)
- [ ] T003 Create frontend directory structure for ChatGPT App manifest
- [ ] T004 [P] Configure Dockerfile for Fly.io deployment in backend/Dockerfile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Setup Database (PostgreSQL) connection and SQLModel engine in backend/src/core/db.py
- [ ] T006 [P] Implement R2 (S3) client configuration in backend/src/core/config.py
- [ ] T007 Create Base Data Models (User, Course, Module, Chapter, Progress, Quiz) in backend/src/models/
- [ ] T008 [P] Setup Alembic migrations and run initial migration
- [ ] T009 Implement API Router structure in backend/src/main.py and backend/src/api/routes.py
- [ ] T010 Setup authentication middleware (Basic/Bearer token placeholder) in backend/src/core/security.py

**Checkpoint**: Foundation ready - Database connected, Models defined, API shell running.

---

## Phase 3: User Story 1 - Access & Navigate Course Content (Priority: P1) 🎯 MVP

**Goal**: Users can browse course structure and read content served from R2.

**Independent Test**: Navigate /courses -> /structure -> /content via API and verify R2 content load.

### Implementation for User Story 1

- [ ] T011 [P] [US1] Implement R2Service to fetch markdown content in backend/src/services/content.py
- [ ] T012 [P] [US1] Create API endpoint `GET /courses` in backend/src/api/courses.py
- [ ] T013 [P] [US1] Create API endpoint `GET /courses/{id}/structure` in backend/src/api/courses.py
- [ ] T014 [US1] Create API endpoint `GET /chapters/{id}/content` in backend/src/api/chapters.py (Integration with R2Service)
- [ ] T015 [US1] Create "Sync Content" admin script to populate DB from R2 structure in backend/src/cli/sync.py

**Checkpoint**: Content delivery system is functional. Can read course material via API.

---

## Phase 4: User Story 2 - Rule-Based Quiz Assessment (Priority: P2)

**Goal**: Users can take quizzes and get deterministic grading.

**Independent Test**: Submit quiz answers to API and receive a score matching the static answer key.

### Implementation for User Story 2

- [ ] T016 [P] [US2] Implement QuizService for static grading logic in backend/src/services/quiz.py
- [ ] T017 [US2] Create API endpoint `POST /quizzes/{id}/grade` in backend/src/api/quizzes.py
- [ ] T018 [US2] Update Chapter model to include relation to Quiz in backend/src/models/chapter.py
- [ ] T019 [P] [US2] Add unit tests for deterministic grading logic in tests/unit/test_quiz_service.py

**Checkpoint**: Quiz engine functional. Zero LLM involvement verified by code inspection.

---

## Phase 5: User Story 3 - Grounded AI Tutoring (Priority: P2)

**Goal**: ChatGPT App can answer questions using ONLY course context.

**Independent Test**: Ask ChatGPT App a question about course content and verify response cites the text; ask out-of-scope question and verify refusal.

### Implementation for User Story 3

- [ ] T020 [P] [US3] Create `frontend/manifest.json` defining the ChatGPT App configuration
- [ ] T021 [P] [US3] Create `frontend/openapi.yaml` exposing only safe GET endpoints (content, structure)
- [ ] T022 [US3] Write System Instructions enforcing "Grounded Answers Only" in `frontend/instructions.md`
- [ ] T023 [US3] Add validation test: Verify backend logs show 0 outgoing LLM calls during chat interaction

**Checkpoint**: ChatGPT interface ready. Backend remains passive and deterministic.

---

## Phase 6: User Story 4 - Freemium Access Control (Priority: P3)

**Goal**: Restrict Premium content to upgraded users.

**Independent Test**: Try to access premium chapter as guest -> 403 Forbidden.

### Implementation for User Story 4

- [ ] T024 [P] [US4] Update User model with `premium_status` field in backend/src/models/user.py
- [ ] T025 [P] [US4] Update Chapter model with `is_premium` field in backend/src/models/chapter.py
- [ ] T026 [US4] Implement permission dependency `verify_premium_access` in backend/src/api/deps.py
- [ ] T027 [US4] Apply permission check to `GET /chapters/{id}/content` in backend/src/api/chapters.py

**Checkpoint**: Access control enforcement live.

---

## Phase 7: User Story 5 - Progress & Streak Tracking (Priority: P3)

**Goal**: Track user completion and streaks.

**Independent Test**: Complete chapter -> Progress saved. Log in next day -> Streak increments.

### Implementation for User Story 5

- [ ] T028 [P] [US5] Create ProgressService to handle completion logic in backend/src/services/progress.py
- [ ] T029 [US5] Create API endpoint `POST /chapters/{id}/progress` in backend/src/api/progress.py
- [ ] T030 [US5] Implement "Streak Calculation" logic on user login/activity in backend/src/services/user.py

**Checkpoint**: User state persistence functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements, Deployment, and Validation

- [ ] T031 [P] Setup Search endpoint `GET /search` using Postgres Full-Text Search in backend/src/api/search.py
- [ ] T032 Verify Zero-Backend-LLM compliance (Audit code for any OpenAI/LLM imports)
- [ ] T033 Deploy backend to Fly.io/Railway
- [ ] T034 Verify ChatGPT App connection to deployed backend
- [ ] T035 Update documentation (README, Quickstart) with deployment URLs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup & Foundational (Phases 1-2)**: BLOCK ALL User Stories.
- **US1 (Content)**: Blocks US2 (Quiz) and US3 (Chat) effectively, as they need content to function.
- **US2 (Quiz)**: Independent of US3/US4/US5.
- **US3 (Chat)**: Independent of US2/US4/US5.
- **US4 (Freemium)**: Modifies US1 (Content) endpoints.
- **US5 (Progress)**: Independent.

### Implementation Strategy

1. **Sprint 1**: Setup + Foundational + US1 (MVP: Content Delivery).
2. **Sprint 2**: US2 (Quizzes) + US3 (Chat Integration).
3. **Sprint 3**: US4 (Freemium) + US5 (Progress) + Polish.

## Notes

- **Zero-Backend-LLM**: Every task involving backend logic must strictly avoid LLM integrations.
- **ChatGPT App**: The "Frontend" is configuration only (manifest/yaml/instructions).
- **R2**: Content is "Source of Truth" for text; DB is "Source of Truth" for structure/metadata (synced).
