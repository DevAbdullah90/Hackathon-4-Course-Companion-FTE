---
id: 006
title: course-companion-spec-v2
stage: spec
date: 2026-02-12
surface: agent
model: gemini-2.0-flash
feature: course-companion
branch: 001-course-companion
user: user
command: /sp.specify
labels: ["spec", "feature", "zero-implementation-details"]
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

Write a comprehensive Product Specification for Phase 1 of the "Course Companion FTE." The selected topic for this course is: **AI Agent Development (8-Layer Architecture & Agent Factory).** Strictly adhere to the following constraints to satisfy the Quality Checklist: 1. **User Value Focus**: Define the product as a 24/7 digital tutor that helps students master AI Agent architecture. 2. **Zero Implementation Details**: DO NOT mention Python, FastAPI, SQL, R2, or specific LLM models. Refer only to "The Backend" and "The Interface." 3. **Course Structure**: - Module 1: Agent Foundations (Deterministic vs. Agentic). - Module 2: The 8-Layer Agent Factory Model. - Module 3: Zero-Backend-LLM vs. Hybrid Intelligence. - Module 4: Developing with Spec-Driven Design. 4. **Functional Requirements & Acceptance Criteria**: - **Content Delivery**: Users can request and read specific chapters. *Criteria: System delivers exact module content upon request.* - **Navigation**: Users can move linearly (Next/Back) or jump to chapters. *Criteria: Navigation state is maintained.* - **Grounded Q&A**: System answers questions ONLY from the syllabus. *Criteria: If info is missing, system must say "Topic not covered."* - **Rule-Based Quizzes**: End-of-module tests. *Criteria: System grades based on a fixed key and explains the correct answer.* - **Progress Tracking**: Persistent learning state. *Criteria: User can ask "Where did I leave off?" and get an accurate answer.* 5. **Measurable Success Criteria**: - 100% adherence to grounded content (No hallucinations). - 100% accuracy in rule-based quiz grading. - Successful content retrieval for all 4 modules. 6. **Edge Cases**: - Handling off-topic user queries. - Handling users who skip chapters to attempt quizzes. - Handling ambiguous quiz answers. 7. **Scope Boundaries**: Phase 1 includes content, navigation, and rule-based testing. It EXCLUDES AI-generated feedback and custom learning paths (which are Phase 2). Write this for a non-technical stakeholder to ensure it passes the Feature Readiness check.

## Response snapshot

Updated feature specification for 'Course Companion Phase 1'.
Spec rewritten to be strictly implementation-agnostic (0 technical details).
Defined 4 Modules (Agent Foundations, 8-Layer Model, Zero-Backend, Spec-Driven Design).
Defined 4 User Stories (Structured Learning, Grounded Clarification, Knowledge Validation, Persistent Progress).
Updated quality checklist to PASS status.

## Outcome

- ✅ Impact: Feature specification updated and validated.
- 🧪 Tests: N/A
- 📁 Files: specs/001-course-companion/spec.md, specs/001-course-companion/checklists/requirements.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The constraint to remove all implementation details forced a cleaner separation between "What" (spec) and "How" (plan).

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` on Windows.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None.
