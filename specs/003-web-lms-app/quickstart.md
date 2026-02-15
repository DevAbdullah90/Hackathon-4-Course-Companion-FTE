# Quickstart: Phase 3 Web LMS

## Development Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create `.env` with `DATABASE_URL` (Neon) and `SECRET_KEY`.
4. `alembic upgrade head`
5. `uvicorn src.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment
- **Backend**: Deploy `backend/` to a platform supporting FastAPI. Set environment variables.
- **Frontend**: Build `frontend/` and deploy static files to Vercel/Netlify.
