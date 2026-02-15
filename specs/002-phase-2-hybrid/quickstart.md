# Quickstart: Phase 2 Hybrid Features

## Prerequisites
- `GEMINI_API_KEY` set in `.env`.
- Database migrated (`alembic upgrade head`).

## Running the Server
```bash
uvicorn src.main:app --reload
```

## Testing Premium Features (Manual)

1. **Set User to Premium**:
   ```sql
   UPDATE user SET is_premium = true WHERE email = 'your@email.com';
   ```

2. **Call Grading Endpoint**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/premium/assessments/grade \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"chapter_id": "ch1", "question_id": "q1", "user_answer": "AI is..."}'
   ```

3. **Verify Cost Tracking**:
   Check the `tokenusage` table:
   ```sql
   SELECT 
     feature_type, 
     COUNT(*) as calls, 
     SUM(estimated_cost_usd) as total_cost 
   FROM tokenusage 
   GROUP BY feature_type;
   ```

4. **Rate Limit Test**:
   - Make 11 rapid requests to `/api/v1/premium/adaptive-path`.
   - 11th should return 429.
