---
id: 002
title: Course Companion Phase 2 Constitution
stage: constitution
date: 2026-02-13
surface: agent
model: gemini-cli
feature: course-companion-phase-2
branch: 001-course-companion
user: abdullah9873
command: /sp.constitution
labels: ["governance", "phase-2", "hybrid-intelligence"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution Write the Constitution for Phase 2 of the Course Companion FTE.

Context:
Phase 1 is fully implemented using Zero-Backend-LLM architecture.
Phase 2 introduces selective Hybrid Intelligence features.

Non-negotiable principles:

1. Phase 1 deterministic architecture MUST remain unchanged.
2. Hybrid intelligence must be:
   - Feature-scoped
   - User-initiated
   - Premium-gated
   - Architecturally isolated
   - Cost-tracked
3. Hybrid APIs must exist under a clearly separated namespace (e.g., /premium/*).
4. No hybrid feature may auto-trigger during normal course usage.
5. Free-tier users must never trigger backend LLM calls.
6. LLM calls must be used only where rule-based logic is insufficient.
7. Each hybrid feature must clearly justify why Zero-Backend-LLM cannot achieve the same outcome.
8. Token usage and estimated cost per request must be logged.
9. System must prevent runaway LLM loops or recursive calls.
10. Hybrid intelligence must enhance educational depth without replacing structured course flow.

Include:
- Architectural commandments
- Premium gating doctrine
- Cost-discipline policy
- Separation-of-concerns enforcement
- Hybrid safety constraints

## Response snapshot

Updated constitution to v2.0.0. Added Hybrid Intelligence Containment principles while preserving Phase 1 Zero-Backend core.

## Outcome

- ✅ Impact: Constitution updated to Phase 2 requirements.
- 🧪 Tests: N/A
- 📁 Files: Updated constitution.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Major version bump due to architectural relaxation for Hybrid features.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): none
