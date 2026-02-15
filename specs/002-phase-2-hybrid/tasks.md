# Tasks: Phase 2 Hybrid Intelligence

**Branch**: `002-phase-2-hybrid` | **Spec**: [specs/002-phase-2-hybrid/spec.md](./spec.md)
**Plan**: [specs/002-phase-2-hybrid/plan.md](./plan.md)

## Summary
Implement Phase 2 Hybrid Intelligence features (LLM-Graded Assessment and Adaptive Learning Path) with strict separation from the deterministic core.

## Phase 1: Setup
*Objective: Prepare the environment and dependencies for hybrid features.*

- [ ] T001 Update `backend/requirements.txt` to include `google-generativeai`
- [ ] T002 Update `backend/core/config.py` to read `GEMINI_API_KEY` from environment
- [ ] T003 Create `backend/api/premium/__init__.py` to initialize the premium namespace
- [ ] T004 Create `backend/models/premium.py` file placeholder

## Phase 2: Foundational (Blocking)
*Objective: Implement data models, migrations, and cost tracking infrastructure.*

- [ ] T005 Update `User` model in `backend/models/user.py` with `is_premium` field
- [ ] T006 Implement `PremiumAssessment` and `TokenUsage` models in `backend/models/premium.py`
- [ ] T007 Generate and apply Alembic migration for new tables
- [ ] T008 Implement `CostTracker` service in `backend/services/cost.py` to log token usage
- [ ] T009 Implement `get_current_premium_user` dependency in `backend/api/premium/deps.py`
- [ ] T010 Implement `LLMService` in `backend/services/llm.py` with Gemini 1.5 Flash client

## Phase 3: User Story 1 - LLM-Graded Assessment (Priority: P1)
*Objective: Enable Premium users to receive AI feedback on free-form answers.*
*Independent Test*: POST /premium/assessments/grade returns feedback for Premium user, 403 for Free user.

- [ ] T011 [US1] Implement `grade_assessment` method in `backend/services/llm.py` with rubric prompt
- [ ] T012 [US1] Create `backend/api/premium/assessments.py` with `POST /grade` endpoint
- [ ] T013 [US1] Integrate `CostTracker` into `grade_assessment` flow
- [ ] T014 [US1] Update `backend/api/routes.py` to include `premium_router`
- [ ] T015 [US1] Create integration test `backend/tests/integration/test_premium_assessment.py` (Mock LLM)

## Phase 4: User Story 2 - Adaptive Learning Path (Priority: P1)
*Objective: Generate personalized study recommendations based on quiz history.*
*Independent Test*: GET /premium/adaptive-path returns tailored chapter list.

- [ ] T016 [US2] Implement `get_user_weak_topics` in `backend/services/quiz.py` (Aggregation logic)
- [ ] T017 [US2] Implement `generate_study_path` in `backend/services/llm.py` (Generative coaching)
- [ ] T018 [US2] Create `backend/api/premium/adaptive.py` with `GET /adaptive-path` endpoint
- [ ] T019 [US2] Create integration test `backend/tests/integration/test_adaptive_path.py`

## Phase 5: User Story 3 - Cost & Access Control (Priority: P1)
*Objective: Enforce rate limits and ensure zero leakage to free tier.*
*Independent Test*: Verify 429 on spamming and 403 on free tier access.

- [ ] T020 [US3] Implement in-memory rate limiter in `backend/api/premium/deps.py`
- [ ] T021 [US3] Apply rate limit dependency to `/premium` routes
- [ ] T022 [US3] Create security test `backend/tests/security/test_premium_gating.py`

## Phase 6: Polish
*Objective: Final verification and cleanup.*

- [ ] T023 Verify no deterministic modules import `backend/services/llm.py`
- [ ] T024 Add admin view query for `TokenUsage` to `quickstart.md`
- [ ] T025 Run full regression suite to ensure Phase 1 unaffected

## Dependencies

1. **Setup** (T001-T004) -> **Foundational** (T005-T010)
2. **Foundational** -> **US1** (T011-T015) & **US2** (T016-T019) & **US3** (T020-T022)
   - US1, US2, US3 can generally proceed in parallel after Phase 2.

## Parallel Execution Opportunities
- T011/T012 (Grading logic) and T016/T017 (Adaptive logic) can be built simultaneously by different developers.
- T020 (Rate Limiting) can be implemented alongside feature development.

## Implementation Strategy
- **Step 1**: Infrastructure (Models + Cost Service).
- **Step 2**: US1 (Assessment) - High value, creates the pattern for LLM usage.
- **Step 3**: US2 (Adaptive) - Adds complexity on top of US1 pattern.
- **Step 4**: US3 (Hardening) - Ensure limits before "release".
