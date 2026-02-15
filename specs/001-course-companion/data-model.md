# Data Model: Course Companion Phase 1

## Entities

### User
Represents a learner in the system.
- **id**: UUID (PK)
- **email**: String (Unique)
- **premium_status**: Boolean (Default: False)
- **streak_count**: Integer (Default: 0)
- **last_active_date**: Date
- **created_at**: Timestamp

### Course
Top-level container for educational material.
- **id**: UUID (PK)
- **slug**: String (Unique, URL-friendly)
- **title**: String
- **description**: Text
- **is_published**: Boolean

### Module
A grouped section of chapters.
- **id**: UUID (PK)
- **course_id**: UUID (FK -> Course.id)
- **title**: String
- **order_index**: Integer

### Chapter
A single unit of content.
- **id**: UUID (PK)
- **module_id**: UUID (FK -> Module.id)
- **title**: String
- **slug**: String
- **r2_key**: String (Path to content in R2, e.g., `course-1/mod-1/ch-1.md`)
- **is_premium**: Boolean (Default: False)
- **order_index**: Integer

### Quiz
An assessment attached to a chapter.
- **id**: UUID (PK)
- **chapter_id**: UUID (FK -> Chapter.id)
- **content**: JSONB (List of questions, options)
  ```json
  [
    {
      "id": "q1",
      "text": "What is an Agent?",
      "options": {"A": "...", "B": "..."},
      "correct_option": "A"
    }
  ]
  ```

### Progress
Tracks completion and scores.
- **user_id**: UUID (PK, FK)
- **chapter_id**: UUID (PK, FK)
- **is_completed**: Boolean
- **quiz_score**: Integer (0-100, Nullable)
- **completed_at**: Timestamp

## Relationships
- Course (1) -> (N) Module
- Module (1) -> (N) Chapter
- Chapter (1) -> (1) Quiz (Optional)
- User (1) -> (N) Progress
