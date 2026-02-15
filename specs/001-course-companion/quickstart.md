# Quickstart: Course Companion Phase 1

## Prerequisites
- Python 3.11+
- PostgreSQL (or Docker container)
- Cloudflare R2 Bucket (or S3 compatible mock like MinIO)

## Setup

1. **Clone & Install**
   ```bash
   git clone <repo>
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create `.env`:
   ```ini
   DATABASE_URL=postgresql://user:pass@localhost:5432/course_db
   R2_ENDPOINT_URL=https://<account>.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET_NAME=course-content
   ```

3. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start Server**
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Frontend (ChatGPT App)**
   - Expose backend via ngrok or deploy to Fly.io.
   - Import `frontend/manifest.json` into ChatGPT "My GPTs" configuration.
   - Paste `frontend/instructions.md` into the System Prompt.

## Verification
- Visit `http://localhost:8000/docs` to see Swagger UI.
- Test `GET /courses` (should return empty list initially).
