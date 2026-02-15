# Feature Specification: Phase 2 Hybrid Intelligence

**Feature Branch**: `002-phase-2-hybrid`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: "Write a Phase 2 Specification Document... Scope: Add Hybrid Intelligence Premium Features... LLM-Graded Assessment... Adaptive Learning Path..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - LLM-Graded Assessment (Priority: P1)

As a **Premium User**, I want to receive detailed AI-generated feedback on my free-form written answers, so that I can understand the nuances of the topic beyond simple multiple-choice correctness.

**Why this priority**: Core value proposition of the Hybrid Intelligence phase. Justifies the premium tier.

**Independent Test**: Can be fully tested by submitting a text response to a designated "Open-Ended" question type and verifying the receipt of structured feedback + score, without affecting other course modules.

**Acceptance Scenarios**:

1.  **Given** I am a logged-in Premium User on an assessment page, **When** I submit a paragraph-long answer to an open-ended question, **Then** the system returns a rubric-based score (1-5) and specific text feedback highlighting strengths and weaknesses.
2.  **Given** I am a Free User, **When** I view an open-ended question, **Then** the input area is disabled or overlaid with an "Upgrade to Premium" prompt.

---

### User Story 2 - Adaptive Learning Path (Priority: P1)

As a **Premium User**, I want the system to analyze my quiz history and suggest specific modules to review, so that I can focus on my weak areas efficiently.

**Why this priority**: enhancing engagement and learning efficiency using AI pattern recognition.

**Independent Test**: Can be tested by simulating a user with low scores in specific categories (e.g., "Prompt Engineering") and verifying that the "Recommended Next Steps" widget points to relevant remedial chapters.

**Acceptance Scenarios**:

1.  **Given** I have completed 3+ quizzes with mixed performance, **When** I visit the Course Dashboard, **Then** I see a "Personalized Study Plan" section listing 2-3 specific chapters tagged "Recommended Review" based on my lowest-scoring topics.
2.  **Given** my performance changes (I ace the remedial quiz), **When** I refresh the Dashboard, **Then** the recommendations update to focus on the next weakest area or advanced topics.

---

### User Story 3 - Cost & Access Control (Priority: P1)

As a **System Administrator**, I need to ensure Free Users never trigger LLM calls and Premium Users are rate-limited, so that the system remains financially viable and secure.

**Why this priority**: Constitution Requirement (IV. Cost Discipline).

**Independent Test**: Simulate a Free User attempting to hit the `/premium/*` endpoints directly and verify `403 Forbidden` is returned with zero backend LLM tokens consumed.

**Acceptance Scenarios**:

1.  **Given** a Free User session, **When** an API call is made to `/premium/grade-assessment`, **Then** the server returns `403 Forbidden` immediately.
2.  **Given** a Premium User submitting assessments rapidly, **When** they exceed the defined rate limit (e.g., 10/hour), **Then** the system temporarily blocks further requests with a `429 Too Many Requests` status.

### Edge Cases

-   **Non-premium access attempt**: User downgrades or token expires during a session. System must re-validate permission on every hybrid call.
-   **Excessive hybrid usage**: User spams the assessment button. System must enforce rate limits and circuit breakers.
-   **Invalid submission**: User submits gibberish or empty text to the grader. System must detect low-quality input cheaply (rule-based) before calling the LLM.
-   **LLM Service Failure**: Upstream API is down. System must degrade gracefully (e.g., "Grading temporarily unavailable, try again later") without crashing the deterministic course flow.

## Requirements *(mandatory)*

### Overview of Phase 2 Objective
Enhance the educational depth of the Course Companion by introducing selective, user-initiated AI features (Assessment Grading and Adaptive Paths) for Premium users, while strictly strictly adhering to the Zero-Backend-LLM constraint for the core free tier.

### Distinction of Features
-   **Phase 1 (Deterministic)**: Content delivery, navigation, multiple-choice quizzes, static answer keys, simple keyword search, streak tracking. **No LLM usage.**
-   **Phase 2 (Hybrid)**: Free-text analysis, reasoning evaluation, personalized study path generation based on complex behavioral patterns. **LLM usage allowed via isolated Premium endpoints.**

### Premium Tier Definition
A user account state, verified via persistent authentication (e.g., JWT claim or database flag), that grants access to endpoints under the `/premium/*` namespace.

### Functional Requirements

#### FR-H1: LLM-Graded Assessment
-   **FR-H1.1**: System MUST accept free-form text input from Premium users for specific "Open-Ended" questions.
-   **FR-H1.2**: System MUST evaluate the submission against a hidden rubric (reasoning depth, factual accuracy, clarity).
-   **FR-H1.3**: System MUST return a structured JSON response containing: `score` (integer), `feedback` (string), and `reasoning` (string).
-   **FR-H1.4**: *Justification*: Rule-based grading is insufficient because assessing "reasoning depth" requires semantic understanding of natural language which regex/keyword matching cannot reliably provide.

#### FR-H2: Adaptive Learning Path
-   **FR-H2.1**: System MUST aggregate a user's quiz performance data across different topic tags.
-   **FR-H2.2**: System MUST identify "Weak Topics" where average score < threshold (e.g., 70%).
-   **FR-H2.3**: System MUST generate a list of recommended chapters mapping to these Weak Topics.
-   **FR-H2.4**: *Justification*: While simple thresholds are deterministic, the "Personalized Study Recommendation" may require synthesizing performance across multiple related dimensions (e.g., user is good at "Syntax" but bad at "Logic" -> suggest specific logic exercises). Phase 2 aims to use LLM to generate the *narrative* and *nuanced* path, though a deterministic fallback is acceptable for MVP. *Correction*: Per strict containment, if the recommendation logic *can* be deterministic, it should be. If the requirement is to use LLM for *generative* advice (e.g., "You seem to struggle with loops, try visualizing them like this..."), then it fits Phase 2. We will assume the requirement implies **generative coaching** based on the path.

#### FR-H3: Cost Awareness & Observability
-   **FR-H3.1**: System MUST log the token count (prompt + completion) and estimated cost for every call to the LLM.
-   **FR-H3.2**: System MUST associate every LLM cost event with a specific User ID.

### Key Entities

-   **PremiumAssessment**: Links a `User`, `Chapter`, and `LLMFeedback`.
-   **LearningProfile**: Aggregated stats for a user used to feed the Adaptive Path generator.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: **Zero Leakage**: 0% of Free User requests trigger an LLM backend call.
-   **SC-002**: **Performance Isolation**: P95 latency for standard content navigation remains < 200ms (unchanged from Phase 1), regardless of Hybrid feature load.
-   **SC-003**: **Personalization Impact**: Premium users interacting with Adaptive Path recommendations show a 15% improvement in subsequent quiz scores on identified weak topics compared to a control group (or pre-intervention baseline).
-   **SC-004**: **Cost Visibility**: 100% of LLM transactions are logged with cost data available in the admin dashboard within 5 minutes.
