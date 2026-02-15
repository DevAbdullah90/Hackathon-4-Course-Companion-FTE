# Implementation Plan: Phase 2 Hybrid Intelligence

**Branch**: `002-phase-2-hybrid` | **Date**: 2026-02-13 | **Spec**: [specs/002-phase-2-hybrid/spec.md](./spec.md)
**Input**: Feature specification from `specs/002-phase-2-hybrid/spec.md`

## Summary
Implement "Hybrid Intelligence" features (LLM-Graded Assessment and Adaptive Learning Path) strictly for Premium users. This involves adding a new `/premium` API namespace, a `TokenUsage` tracking system, and integration with the Gemini 1.5 Flash API, ensuring zero impact on the existing deterministic core.

## Technical Context
**Language/Version**: Python 3.11+ (FastAPI)
**Primary Dependencies**: `google-generativeai` (for LLM), `sqlmodel` (existing ORM), `alembic` (migrations).
**Storage**: PostgreSQL (via SQLModel).
**Testing**: `pytest` for unit/integration tests.
**Performance Goals**: < 2s for LLM grading (using Flash), zero latency impact on core routes.
**Constraints**: Strict isolation of Hybrid logic; mandatory cost logging.

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **I. Immutable Core**: Passed. New features are additive and isolated in `/premium`.
-   **II. Containment**: Passed. Features are user-initiated, scoped, and gated.
-   **III. Rules Preference**: Passed. Grading reasoning requires LLM; deterministic fallback impossible for semantic depth.
-   **IV. Cost Discipline**: Passed. `TokenUsage` table and `CostTracker` service included in design.
-   **V. Content Grounding**: Passed. Prompts will inject chapter content.

## Project Structure

### Documentation (this feature)
```text
specs/002-phase-2-hybrid/
├── plan.md              # This file
├── research.md          # Provider selection & Cost tracking strategy
├── data-model.md        # New SQLModel entities
├── quickstart.md        # How to test premium features
├── contracts/           # OpenAPI specs
│   └── openapi.yaml
└── tasks.md             # (To be created)
```

### Source Code (backend)
```text
backend/src/
├── api/
│   ├── premium/                # NEW: Isolated namespace
│   │   ├── __init__.py
│   │   ├── assessments.py      # FR-H1
│   │   ├── adaptive.py         # FR-H2
│   │   └── deps.py             # Premium verification dependency
│   └── routes.py               # Update to include premium router
├── core/
│   └── config.py               # Add GEMINI_API_KEY
├── models/
│   ├── premium.py              # NEW: PremiumAssessment, TokenUsage tables
│   └── user.py                 # Update: Add is_premium field
├── services/
│   ├── llm.py                  # NEW: Abstracted LLM client (Gemini)
│   └── cost.py                 # NEW: Token logging logic
└── main.py                     # App entry point
```

## Implementation Phases

### Phase 1: Foundation & Data Layer
1.  **Dependency**: Add `google-generativeai` to `requirements.txt`.
2.  **Models**: Create `PremiumAssessment` and `TokenUsage` models. Update `User` model.
3.  **Migration**: Generate and apply Alembic migration.
4.  **Service**: Implement `CostTracker` service (writes to DB).

### Phase 2: LLM Integration
1.  **Service**: Implement `LLMService` using Gemini 1.5 Flash.
    -   Include prompt engineering for Grading (injecting rubric).
    -   Include prompt engineering for Adaptive Path (injecting profile).
    -   Wire up `CostTracker` to log every call.

### Phase 3: API Layer
1.  **Dependency**: Implement `get_current_premium_user`.
2.  **Endpoints**:
    -   `POST /premium/assessments/grade`: Calls LLMService -> Grading.
    -   `GET /premium/adaptive-path`: Calls QuizService (stats) -> LLMService -> Recommendations.
3.  **Router**: Register `/premium` router in `main.py` (or `api/routes.py`).

### Phase 4: Testing & Verification
1.  **Unit Tests**: Mock LLM responses to test parsing and cost logging.
2.  **Integration Tests**:
    -   Verify Free User gets 403.
    -   Verify Premium User gets 200 (with mock LLM).
    -   Verify `TokenUsage` record created.
3.  **Performance**: Check latency overhead.

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| LLM Usage | Reasoning Grading | Regex/Keywords cannot assess "reasoning depth" or "nuance". |
| New Database Tables | Cost Auditability | Logging to text files is not queryable for admin dashboards. |
