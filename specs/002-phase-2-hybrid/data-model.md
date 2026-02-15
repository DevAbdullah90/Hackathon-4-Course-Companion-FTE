# Data Model: Phase 2 Hybrid Intelligence

## Entities

### 1. User (Extension)
*Existing entity, adding Premium fields.*

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_premium` | Boolean | Yes | Default `False`. Gates access to hybrid features. |
| `premium_since` | DateTime | No | Timestamp of upgrade. |

### 2. PremiumAssessment
*Stores the interaction for FR-H1.*

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key. |
| `user_id` | UUID | Yes | Foreign Key to `User`. |
| `chapter_id` | String | Yes | ID of the chapter being assessed. |
| `question_context` | Text | Yes | The prompt/question shown to the user. |
| `user_answer` | Text | Yes | The free-form text submitted. |
| `llm_feedback` | JSON | Yes | Structured feedback `{strengths: [], weaknesses: [], suggestions: ""}`. |
| `score` | Integer | Yes | Rubric score (1-5). |
| `created_at` | DateTime | Yes | Timestamp. |

### 3. TokenUsage
*Logs costs for Principle IV.*

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | Primary Key. |
| `user_id` | UUID | Yes | Foreign Key to `User`. |
| `feature_type` | Enum | Yes | `ASSESSMENT` or `ADAPTIVE_PATH`. |
| `prompt_tokens` | Integer | Yes | Input tokens. |
| `completion_tokens` | Integer | Yes | Output tokens. |
| `model_name` | String | Yes | E.g., `gemini-1.5-flash`. |
| `estimated_cost_usd` | Float | Yes | Calculated cost. |
| `timestamp` | DateTime | Yes | When the call happened. |

### 4. LearningProfile (Derived/Virtual)
*Aggregates data for FR-H2. May not be a physical table if computed on fly, but conceptual entity.*

| Field | Type | Description |
|-------|------|-------------|
| `weak_topics` | List[String] | Topics with <70% mastery. |
| `recommended_chapters` | List[String] | Chapters mapping to weak topics. |
