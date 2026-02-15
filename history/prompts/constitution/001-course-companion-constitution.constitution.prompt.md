---
id: 001
title: course-companion-constitution
stage: constitution
date: 2026-02-12
surface: agent
model: gemini-2.0-flash
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "setup", "architecture"]
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

/sp.constitution Write the Constitution for a Course Companion FTE built for Hackathon IV.

The system MUST strictly follow Zero-Backend-LLM architecture.

Non-negotiable rules:

1. Backend MUST NOT call any LLM APIs.
2. Backend must be fully deterministic.
3. ChatGPT App handles all reasoning, explanation, tone adaptation, and tutoring intelligence.
4. Backend responsibilities are limited to:
   - Serving course content verbatim from Cloudflare R2
   - Navigation (next/previous chapter)
   - Rule-based quiz grading using answer keys
   - Progress tracking and streak storage
   - Keyword/semantic search
   - Freemium access control
5. If content is not in the course material, the assistant must say: “This topic is not covered in this course.”
6. All educational responses must be grounded strictly in served content.
7. System must scale to 100k+ users with near-zero marginal cost.
8. Architecture must clearly separate deterministic APIs from any future hybrid features.
9. All design decisions must optimize for:
   - Cost efficiency
   - Scalability
   - Auditability
   - Consistency (99%+ predictable behavior)

Include:
- Core philosophy
- Guardrails
- Architectural commandments
- Educational behavior principles
- Anti-hallucination policy

## Response snapshot

Created the constitution for the Course Companion FTE (Hackathon IV) project.
Defined 5 core principles:
1. Zero-Backend-LLM Architecture
2. Deterministic Backend Responsibility
3. Strict Content Grounding
4. Scalability & Efficiency
5. Clean Architectural Separation

Established governance rules enforcing strict adherence to the Zero-Backend-LLM constraint.

## Outcome

- ✅ Impact: Established project constitution.
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The strict Zero-Backend-LLM constraint is a strong architectural driver that will simplify the backend significantly but places high responsibility on the client/ChatGPT App.

## Evaluation notes (flywheel)

- Failure modes observed: Shell script for PHR creation failed on Windows.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): Fix shell script or use native tool first.
