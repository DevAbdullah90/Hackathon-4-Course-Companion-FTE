# Tasks: Phase 3 Web LMS

**Input**: Design documents from `specs/003-web-lms-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included to ensure reliability and regression validation of Phase 1 & 2 features.

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- All descriptions include file paths and atomic goals.

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Infrastructure Initialization)

**Purpose**: Initialize frontend and backend environments.

- [x] T001 [P] Initialize FastAPI project in backend/src/ with base configuration in backend/src/core/config.py
- [x] T002 [P] Initialize React TypeScript project in frontend/src/ using Vite and Tailwind CSS
- [x] T003 [P] Configure Neon Postgres connection string with sslmode=require in backend/.env
- [x] T004 [P] Setup logging and error handling base in backend/src/core/logging.py

---

## Phase 2: Foundational (Backend Consolidation & Security)

**Purpose**: Core logic, security, and data persistence layers.

- [x] T005 [P] Implement SQLModel schemas for User, Progress, and TokenUsage in backend/src/models/
- [x] T010 [P] Implement JWT-based Authentication system in backend/src/api/auth.py
- [x] T011 [P] Implement role-based access control (RBAC) middleware in backend/src/api/deps.py
- [x] T012 [P] Setup Alembic for database migrations and run initial migration in backend/alembic/
- [x] T013 [P] Implement connection pooling configuration for Neon in backend/src/core/db.py (Scalability: handle 100k users)
- [x] T014 [P] Security Hardening: Implement CORS and secure headers in backend/src/main.py

---

## Phase 3: User Story 1 - Core Learning Flow (Priority: P1) 🎯 MVP

**Goal**: Deliver a complete end-to-end LMS experience for free users.

**Independent Test**: User can log in, view a course, read a lesson, and complete an MCQ quiz with progress saved.

### Implementation for User Story 1

- [x] T015 [P] [US1] Implement /api/v1/courses and /api/v1/chapters/{slug} endpoints in backend/src/api/courses.py
- [x] T016 [P] [US1] Implement /api/v1/progress update logic in backend/src/api/progress.py (Regression: verify Phase 1 content mapping)
- [x] T017 [P] [US1] Create Frontend API client with JWT support in frontend/src/lib/api.ts
- [x] T018 [P] [US1] Dashboard Implementation: Create Course List and Progress Overview in frontend/src/pages/Dashboard.tsx
- [x] T019 [P] [US1] Lesson Viewer: Implement Markdown content rendering with code snippets in frontend/src/components/LessonViewer.tsx
- [x] T020 [P] [US1] Quiz Interface: Implement interactive MCQ engine with immediate feedback in frontend/src/components/Quiz.tsx
- [x] T021 [P] [US1] Progress Visualization: Add progress bars to course cards and lessons in frontend/src/components/ProgressBar.tsx
- [x] T022 [US1] Regression Check: Verify that local content loading (Phase 1) works within the new web lesson viewer
- [x] T023 [US1] Validation: Test core learning flow with mock data to ensure 95% navigation success (SC-001)

**Checkpoint**: Core LMS is functional and independently testable.

---

## Phase 4: User Story 2 - Premium Hybrid Experience (Priority: P2)

**Goal**: Integrate AI-graded assessments and adaptive paths for premium users.

**Independent Test**: Premium user submits a written answer and receives AI feedback.

### Implementation for User Story 2

- [x] T024 [P] [US2] Hybrid Intelligence Layer: Implement LLM grading logic in backend/src/services/llm.py (Isolation: Principle II)
- [x] T025 [P] [US2] Cost Tracking Integration: Implement token logging and cost estimation in backend/src/services/cost.py
- [x] T026 [P] [US2] Implement /api/v1/premium/grade endpoint in backend/src/api/premium/assessments.py
- [x] T027 [P] [US2] Implement /api/v1/premium/adaptive-path endpoint in backend/src/api/premium/adaptive.py
- [x] T028 [P] [US2] Premium Upgrade UI: Create subscription gate and upgrade flow in frontend/src/pages/Upgrade.tsx
- [x] T029 [P] [US2] Hybrid Feature Integration: Create UI for AI feedback and recommended study path in frontend/src/components/PremiumFeatures.tsx
- [x] T030 [US2] Performance: Ensure AI response delivery is within 12s (SC-004) via streaming or optimized prompts
- [x] T031 [US2] Regression Check: Verify that Phase 2 Hybrid features (if any) are correctly integrated into the new API

**Checkpoint**: Hybrid features are gated and functional for premium users.

---

## Phase 5: User Story 3 - System Administration (Priority: P3)

**Goal**: Provide admins with analytics and cost visibility.

**Independent Test**: Admin can view aggregate charts and usage data.

### Implementation for User Story 3

- [x] T032 [P] [US3] Admin Analytics: Implement /api/v1/admin/analytics for aggregate reporting in backend/src/api/admin/analytics.py
- [x] T033 [P] [US3] Create Admin Panel with usage and cost charts in frontend/src/pages/Admin.tsx
- [x] T034 [US3] Validation: Verify cost tracking accuracy (SC-005) against mock LLM usage data

---

## Final Phase: Polish, Performance & Deployment

**Purpose**: Final hardening and production readiness.

- [ ] T035 [P] Performance Optimization: Implement Redis/In-memory caching for frequently accessed course metadata
- [x] T036 [P] Security Hardening: Implement rate limiting for API endpoints in backend/src/core/security.py
- [ ] T037 [P] Testing & Validation: Run load tests to simulate 100k concurrent users (SC-002)
- [x] T038 [P] Deployment Preparation: Configure Docker and CI/CD pipelines for backend and frontend
- [x] T039 [P] Final Regression: Verify all Phase 1 & 2 features work without regressions in the Phase 3 web environment

---

## Dependencies & Execution Order
1. **Infrastructure (Phase 1 & 2)**: Must be completed first.
2. **MVP Core (Phase 3)**: High priority. US1 is the primary deliverable.
3. **Premium (Phase 4)**: Depends on US1 foundation.
4. **Admin (Phase 5)**: Depends on US2 data generation.
5. **Production (Final Phase)**: Runs concurrently or after stories.

## Parallel Execution Examples
- **US1 Frontend/Backend**: T015 (API) and T018-T021 (UI) can run in parallel.
- **US2 Integration**: T024 (LLM Service) and T028 (Upgrade UI) can run in parallel.

## Implementation Strategy
- **MVP First**: Focus exclusively on US1 to deliver a working LMS.
- **Incremental Delivery**: Layer US2 (Premium) and US3 (Admin) onto the solid core.
- **Test-Driven**: Each task includes measurable completion criteria for automated verification.
