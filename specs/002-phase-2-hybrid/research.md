# Research: Phase 2 Hybrid Intelligence

**Feature Branch**: `002-phase-2-hybrid`
**Date**: 2026-02-13

## 1. LLM Provider Selection

**Objective**: Select an LLM provider that balances cost, reasoning capability (for grading), and speed.

**Options Considered**:
1.  **OpenAI (GPT-4o-mini)**: Low cost, high speed, excellent reasoning for grading.
2.  **Google (Gemini 1.5 Flash)**: Extremely low cost, large context window (good for feeding whole chapters for grounding), fast.
3.  **Anthropic (Claude 3 Haiku)**: Good reasoning, slightly more expensive than Flash.

**Decision**: **Gemini 1.5 Flash** (via `google-generativeai` SDK).
**Rationale**:
-   **Cost**: Significantly cheaper per token, aligning with Principle IV.
-   **Context**: 1M+ token window allows us to pass full chapter content for "Strict Content Grounding" (Principle V) without complex RAG in the first iteration.
-   **Speed**: "Flash" tier ensures minimal latency overhead.

## 2. Cost Tracking Mechanism

**Objective**: Log estimated cost per request (Principle IV).

**Approach**:
-   **Token Counting**: The Gemini API returns `usageMetadata` (promptTokenCount, candidatesTokenCount).
-   **Storage**: Create a `TokenUsage` table in SQLModel.
-   **Calculation**: Apply current pricing (e.g., $0.075/1M input, $0.30/1M output) at runtime or aggregation time.
-   **Implementation**: A service wrapper `LLMService` that handles the call and writes to the DB in a background task (FastAPI `BackgroundTasks`) to avoid blocking the response.

## 3. Rate Limiting Strategy

**Objective**: Prevent abuse and runaway costs (Principle IV).

**Options**:
1.  **`fastapi-limiter` (Redis)**: Robust, standard.
2.  **In-Memory**: Simple, but resets on restart/scaling.
3.  **Database-backed**: Reliable but slow.

**Decision**: **In-Memory (Leaky Bucket)** for MVP, graduating to Redis if scaling.
**Rationale**: Keeps dependencies low (no Redis required for MVP).
**Limits**:
-   Premium Users: 50 requests/hour/user.
-   Burst: 5 requests/minute.

## 4. Premium Verification

**Objective**: Strictly gate `/premium/*` endpoints (Principle II).

**Approach**:
-   Extend `User` model with `is_premium` (boolean) or `tier` (enum).
-   Create a dependency `get_current_premium_user` that calls `get_current_user` and checks the flag.
-   If check fails: Raise `HTTPException(403, detail="Premium subscription required")`.
