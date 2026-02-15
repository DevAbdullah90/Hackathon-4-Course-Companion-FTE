# Feature Specification: Course Companion FTE Phase 1 (AI Agent Development)

**Feature Branch**: `001-course-companion`  
**Created**: 2026-02-12  
**Status**: Draft  
**Input**: User description provided in prompt (AI Agent Development Course, Zero-Backend-LLM, Phase 1 Scope).

## Product Overview

The **Course Companion FTE** is a 24/7 digital tutor designed to help students master the "AI Agent Development (8-Layer Architecture & Agent Factory)" curriculum. It provides a structured, interactive learning environment where students can read course material, navigate modules, take quizzes, and ask clarifying questions.

**Core Value Proposition**: A "Zero-Hallucination" educational tool that acts as a deterministic gateway to the curriculum, ensuring students learn *only* from the approved material without the noise or inaccuracy of general-purpose AI models.

**Phase 1 Scope**: Strictly limited to content delivery, navigation, grounded Q&A, and rule-based testing. Advanced features like custom learning paths or AI-generated feedback are explicitly out of scope.

## User Scenarios & Testing

### User Story 1 - Structured Learning (Priority: P1)

As a Student, I want to read through the 4 modules of the course linearly so that I can build my knowledge step-by-step.

**Why this priority**: Fundamental requirement. The product is a course delivery system first and foremost.

**Independent Test**: User can open Module 1, read Chapter 1, click "Next", and immediately see Module 1, Chapter 2.

**Acceptance Scenarios**:

1. **Given** a user is at the Course Home, **When** they request "Module 2: 8-Layer Agent Factory", **Then** the system displays the correct introductory text for that module.
2. **Given** a user is reading a chapter, **When** they click "Next", **Then** the system loads the subsequent chapter content without error.
3. **Given** a user navigates away and returns, **When** they ask "Where did I leave off?", **Then** the system identifies the last accessed chapter.

---

### User Story 2 - Grounded Clarification (Priority: P1)

As a Student, I want to ask questions about the current topic and receive answers *only* if they are found in the course text.

**Why this priority**: Distinguishes the tool from a static PDF. Provides interactive help while maintaining strict accuracy.

**Independent Test**: Ask a question defined in the text (e.g., "What is Layer 3?") and verify the answer. Ask an off-topic question (e.g., "Write me a poem") and verify the refusal.

**Acceptance Scenarios**:

1. **Given** the course covers "Deterministic vs. Agentic" in Module 1, **When** a user asks "What is the difference between deterministic and agentic?", **Then** the system provides the explanation from Module 1.
2. **Given** the user asks about "Quantum Computing" (not in syllabus), **When** the system processes the query, **Then** it responds with "This topic is not covered in this course."
3. **Given** the user asks for a code example not in the text, **When** the system processes it, **Then** it refuses to generate new code.

---

### User Story 3 - Knowledge Validation (Priority: P2)

As a Student, I want to take a quiz at the end of each module to prove I understood the material.

**Why this priority**: Validates learning outcomes and provides a sense of progress.

**Independent Test**: Complete a quiz with known correct/incorrect answers and verify the grade is mathematically accurate based on the key.

**Acceptance Scenarios**:

1. **Given** a user submits a quiz for Module 2, **When** they get 4 out of 5 questions correct, **Then** the system displays a score of 80% and highlights the one incorrect answer.
2. **Given** a user reviews a wrong answer, **When** they request an explanation, **Then** the system displays the pre-written explanation from the answer key.

---

### User Story 4 - Persistent Progress (Priority: P3)

As a Returning Student, I want my quiz scores and reading position saved so I don't lose my place.

**Why this priority**: Essential for a "Full-Time Equivalent" (FTE) feel; students engage over multiple sessions.

**Independent Test**: Complete a module, close the interface, reopen it, and verify the module is marked as "Completed".

**Acceptance Scenarios**:

1. **Given** a user completes Module 1, **When** they log out and back in, **Then** Module 1 is visually marked as "Complete."

## Requirements

### Functional Requirements

- **FR-001**: The System MUST store and retrieve the specific content for Modules 1, 2, 3, and 4 upon user request.
- **FR-002**: The Interface MUST provide "Next", "Previous", and "Table of Contents" navigation controls.
- **FR-003**: The System MUST maintain the state of the user's current location in the course across sessions.
- **FR-004**: The System MUST answer user queries by retrieving relevant text segments *strictly* from the loaded course modules.
- **FR-005**: The System MUST reply "This topic is not covered in this course" if a user query cannot be answered by the syllabus.
- **FR-006**: The System MUST administer multiple-choice quizzes at the end of each module.
- **FR-007**: The System MUST grade quizzes using a static, pre-defined answer key (no AI grading).
- **FR-008**: The System MUST persist user quiz scores.

### Key Entities

- **Student**: The learner accessing the content. Tracks progress and scores.
- **Course Module**: A major unit of the curriculum (e.g., "The 8-Layer Agent Factory Model").
- **Course Chapter**: A subunit of content within a Module.
- **Quiz**: A set of questions associated with a Module.
- **Answer Key**: The static truth source for grading quizzes.

## Success Criteria

### Measurable Outcomes

- **SC-001**: **100% Grounding Adherence**: In a test set of 100 queries (50 on-topic, 50 off-topic), the system correctly answers the on-topic ones using course text and refuses the off-topic ones 100% of the time.
- **SC-002**: **100% Grading Accuracy**: Quiz scores are identical to manual calculation based on the answer key for 100% of submissions.
- **SC-003**: **Content Availability**: Users can successfully load and read all chapters in Modules 1-4 with a success rate of 99.9%.
- **SC-004**: **State Retention**: User location and scores persist correctly across 100 consecutive login/logout cycles in testing.

### Edge Cases

- **Off-Topic Queries**: User asks about politics or general Python programming. -> System strictly refuses.
- **Skipping Ahead**: User tries to take the Module 4 quiz without reading the content. -> System allows access (Phase 1 does not enforce strict gating, only tracking) BUT warns the user.
- **Ambiguous Inputs**: User selects two answers for a single-choice question. -> System treats as invalid/incorrect or enforces single-select in UI.

## Scope Boundaries

- **In Scope**:
    - Module 1: Agent Foundations.
    - Module 2: 8-Layer Agent Factory.
    - Module 3: Zero-Backend-LLM Architecture.
    - Module 4: Spec-Driven Design.
    - Linear navigation.
    - Static text retrieval.
    - Rule-based quiz grading.
- **Out of Scope**:
    - AI-generated feedback on open-ended questions.
    - Personalized/adaptive learning paths.
    - Video content streaming.
    - Social features (leaderboards, chat with other students).
