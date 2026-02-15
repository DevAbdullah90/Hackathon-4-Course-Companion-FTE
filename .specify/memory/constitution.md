<!--
SYNC IMPACT REPORT
Version: 2.0.0 -> 3.0.0 (Phase 3: Web Application Shift)
Modified Principles:
- "I. Immutable Core (Zero-Backend-LLM)" -> "I. Backend Integrity & Strategic LLM Usage" (Expanded for Web API)
- "II. Hybrid Intelligence Containment" -> "II. Premium Isolation & Hybrid Containment" (Refined for SaaS scale)
Added Sections:
- "VI. Full-Stack LMS Completeness"
- "VII. Web-First Architectural Principles"
- "VIII. Scalability & SaaS Production Readiness"
Templates Requiring Updates:
- .specify/templates/plan-template.md (✅ updated)
- .specify/templates/spec-template.md (✅ updated)
- .specify/templates/tasks-template.md (✅ updated)
Follow-up: Ensure all future specs for Phase 3 features reference Principle VI and VIII.
-->

# Course Companion FTE (Hackathon IV) Constitution

## Core Principles

### I. Backend Integrity & Strategic LLM Usage
The system foundation remains deterministic. For all core LMS functionalities (content delivery, navigation, standard quizzes), the backend MUST NOT call any LLM APIs. Phase 1 deterministic logic is immutable and must remain reliable. Backend services may utilize LLM APIs ONLY for premium-gated, non-deterministic educational enhancements as defined in Principle II.

### II. Premium Isolation & Hybrid Containment
Hybrid intelligence features must be strictly contained to maintain system performance and financial integrity:
1.  **Premium-Gated Only**: Hybrid features are exclusively for authenticated, premium-tier users. Free-tier users must NEVER trigger a backend LLM call.
2.  **Performance Preservation**: Hybrid intelligence must not degrade the latency or availability of the core learning flow for any user.
3.  **Architectural Isolation**: Hybrid services must be clearly separated from core services at the API and code level (e.g., `/premium/*` namespace).
4.  **User-Initiated**: AI intervention must always be explicitly requested by the user.

### III. Justification & Preference for Rules
Deterministic, rule-based logic is the primary choice. Hybrid intelligence is a fallback.
-   **Last Resort**: LLM calls are permitted only where deterministic logic is provably insufficient for the educational goal.
-   **Specification Justification**: Every hybrid feature must document why rule-based logic cannot achieve the desired outcome.

### IV. Cost Discipline & Observability
System sustainability depends on strict financial monitoring:
-   **Usage Logging**: Every LLM request must log token usage, model identifiers, and estimated costs.
-   **Circuit Breakers**: Implement safeguards to prevent recursive AI calls or runaway token consumption.
-   **Administrative Transparency**: Cost metrics must be visible to system admins to ensure resource sustainability.

### V. Strict Content Grounding
Educational responses must be strictly grounded in the course material. Hallucination is a critical failure. If a query falls outside the scope of the provided content, the system MUST inform the user rather than speculating.

### VI. Full-Stack LMS Completeness
Phase 3 mandates a complete standalone web application experience. The system MUST provide:
1.  **Seamless Navigation**: Intuitive course and module exploration.
2.  **Immersive Viewing**: High-quality lesson and content delivery.
3.  **Interactive Quizzing**: Robust quiz interaction and feedback loops.
4.  **Progress Dashboard**: Centralized user tracking of learning milestones.
5.  **Premium Workflow**: Integrated upgrade paths for hybrid features.

### VII. Web-First Architectural Principles
The application must follow modern web standards:
1.  **Separation of Concerns**: Clear decoupling between the Frontend (React/SPA) and Backend (FastAPI/REST).
2.  **API-Driven**: All UI interactions must be powered by well-documented, versioned REST endpoints.
3.  **Responsive Design**: The interface must be functional across various device form factors.

### VIII. Scalability & SaaS Production Readiness
The system must be built for production deployment as a SaaS product:
1.  **Modular Design**: Architecture must be modular to allow for independent scaling of services.
2.  **State Management**: Use stateless backend patterns where possible, leveraging external stores (Postgres/Redis) for persistence.
3.  **Security Baseline**: All endpoints must be secured with industry-standard authentication (JWT/OAuth2).
4.  **Deployment Reliability**: Infrastructure-as-Code and CI/CD readiness are mandatory for all core components.

## Governance

This Constitution is the ultimate authority for architectural decisions.
-   **Core Protection**: Principle I remains the bedrock; modifications require significant justification and ADR documentation.
-   **Compliance**: All Phase 3 features must pass a "Constitution Check" against all principles before implementation.
-   **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH) applies to this document.

**Version**: 3.0.0 | **Ratified**: 2026-02-12 | **Last Amended**: 2026-02-13
