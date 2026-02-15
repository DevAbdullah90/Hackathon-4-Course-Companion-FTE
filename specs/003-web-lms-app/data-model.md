# Data Model: Phase 3 Web LMS

## User
- **id**: UUID (PK)
- **email**: String (Unique)
- **hashed_password**: String
- **full_name**: String
- **is_premium**: Boolean (Default: False)
- **is_admin**: Boolean (Default: False)
- **created_at**: DateTime

## Course (Metadata from JSON/Storage)
- **id**: String (Slug)
- **title**: String
- **description**: Text
- **is_active**: Boolean

## UserProgress
- **id**: UUID (PK)
- **user_id**: UUID (FK)
- **chapter_slug**: String
- **status**: Enum (NOT_STARTED, IN_PROGRESS, COMPLETED)
- **last_accessed**: DateTime
- **score**: Integer (Optional, for quizzes)

## TokenUsage
- **id**: UUID (PK)
- **user_id**: UUID (FK)
- **feature**: Enum (GRADING, PATH_GEN)
- **prompt_tokens**: Integer
- **completion_tokens**: Integer
- **cost_usd**: Float
- **timestamp**: DateTime
