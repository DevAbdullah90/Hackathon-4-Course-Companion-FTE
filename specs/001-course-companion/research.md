# Research & Decisions: Course Companion Phase 1

**Feature**: Course Companion Phase 1 (Zero-Backend-LLM)
**Date**: 2026-02-12

## Decisions

### 1. Database Choice: PostgreSQL (Neon/Supabase)
- **Decision**: Use PostgreSQL managed by Neon or Supabase.
- **Rationale**: Relational data (users, progress, courses, quizzes) fits SQL perfectly. JSONB support allows flexible quiz structures.
- **Alternatives**: 
  - *DynamoDB*: Overkill for Phase 1, strictly typed SQL schemas are safer for "FTE" consistency.
  - *SQLite*: Not suitable for 100k+ users stateless deployment.

### 2. Content Storage: Cloudflare R2
- **Decision**: Store all course markdown/assets in Cloudflare R2.
- **Rationale**: Zero egress fees is critical for "near-zero marginal cost" goal (Principle IV). S3-compatible API makes integration easy with `boto3`.
- **Alternatives**:
  - *AWS S3*: High egress fees for popular courses.
  - *Database*: Bloats DB, harder to cache via CDN.

### 3. Quiz Grading: Static Answer Keys
- **Decision**: Quizzes stored as JSON with an `answer_key` field (e.g., `{"q1": "A", "q2": "C"}`). Backend compares submission against this key.
- **Rationale**: 100% deterministic (Principle II). No "fuzzy" grading.
- **Alternatives**:
  - *LLM Grading*: Explicitly forbidden by Constitution.
  - *Client-side Grading*: Insecure; users could spoof full scores.

### 4. Search Strategy: PostgreSQL Full-Text Search
- **Decision**: Use PostgreSQL's `tsvector` for keyword search over course content index.
- **Rationale**: "Good enough" for Phase 1. Deterministic (Principle II). No extra infrastructure (like Elasticsearch) needed.
- **Alternatives**:
  - *Vector Search (pgvector)*: Hybrid/Semantic, but keeping it simple/deterministic for Phase 1 MVP is safer. Can upgrade to `pgvector` later without breaking architecture.

### 5. Deployment: Fly.io
- **Decision**: Deploy Dockerized FastAPI to Fly.io.
- **Rationale**: Global distribution (optional later), scale-to-zero capability (cost efficiency), simple CLI.
- **Alternatives**:
  - *Railway*: Also good, but Fly's machine model offers fine-grained control for stateless APIs.

## Outstanding Questions (Resolved)

- *How to sync R2 content with DB index?* 
  - **Resolution**: A "Sync" admin endpoint will scan R2 buckets and update the `chapters` table in Postgres. This ensures the API knows about available content without checking R2 on every request.

- *How to handle Freemium gating?*
  - **Resolution**: `is_premium` boolean on `Chapter` model. Middleware checks `User.premium_status` vs `Chapter.is_premium`.
