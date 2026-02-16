# Universal Fix Prompt for Gemini CLI (Neon DB + Stability)

**Role:** You are a Senior Full-Stack Engineer expert in React (Vite), FastAPI (Python), SQLModel, and PostgreSQL (Neon).

**Context:**
I have an "AI Course Companion" project that is currently unstable. I want to switch from SQLite to **Neon Serverless PostgreSQL** and fix critical frontend issues.

**Current Issues:**
1.  **Dashboard Crash (403 Forbidden):** The Dashboard page (`/`) crashes or flickers because `AdaptivePath.tsx` (and possibly other components) receives a 403 Forbidden error for non-premium users, and the global error handler (`api.ts`) might be redirecting aggressively.
2.  **Lesson Not Found:** `ContentService` fails to find local content files due to incorrect path resolution.
3.  **Database:** Currently using SQLite, need to switch to Neon PostgreSQL.

**Your Task:**
Systematically fix the stack. **Do not ask for permission for each file.**

### Step 1: Database Switch (Neon PostgreSQL)
1.  **Dependencies:** Ensure `psycopg2-binary` is installed (add to `backend/requirements.txt` if missing).
2.  **Config (`backend/src/core/config.py`):**
    *   Load `DATABASE_URL` from `.env`.
    *   Update `engine` creation to support Neon:
        ```python
        engine = create_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)
        # Ensure sslmode=require is handled if not in the URL string
        ```
    *   **Remove** any hardcoded `STORAGE_TYPE = "local"`. It should respect `.env`.
3.  **Environment:**
    *   Create `backend/.env` with:
        ```env
        DATABASE_URL=postgresql://[user]:[password]@[hostname]/[dbname]?sslmode=require
        STORAGE_TYPE=local
        GEMINI_API_KEY=dummy
        SECRET_KEY=dev-secret-key
        ```
        *(Instruct user to replace placeholders with their real Neon credentials)*.

### Step 2: Fix Backend Reliability
1.  **ContentService (`backend/src/services/content.py`):**
    *   Fix path resolution: Use `pathlib.Path(__file__).parent.parent.parent / "local_content"` to reliably find the directory, regardless of where the script is run from.
2.  **Unified Seed Script (`backend/seed_full.py`):**
    *   This script MUST run against the **Neon DB**.
    *   Re-create tables (`SQLModel.metadata.create_all(engine)`).
    *   Create a **Premium User** (`test@example.com` / `password`).
    *   Create **Course**, **Module**, and **Assessment Chapter** (`r2_key="mod1/assessment.md"`).
    *   Ensure dummy content (`backend/local_content/mod1/assessment.md`) exists.

### Step 3: Fix Frontend Stability & 403 Error
1.  **Handle 403 Gracefully (`frontend/src/components/AdaptivePath.tsx`):**
    *   Wrap data fetching in a `try/catch`.
    *   **If 403 is caught**: Do NOT crash or redirect. Set a state `isPremiumLocked = true`.
    *   Render a "Premium Feature" card: *"Upgrade to Premium to unlock your output."* with a button to separate upgrade page or just text.
2.  **Robust Auth (`frontend/src/lib/api.ts`):**
    *   **Disable** the automatic redirect to `/login` for 403 errors on the interceptor. Let individual components handle 403s (like showing a lock screen) so the dashboard doesn't flicker/reload loop.
3.  **Dashboard Safety (`frontend/src/pages/Dashboard.tsx`):**
    *   Review `dashboards.map` rendering. Ensure it checks if `dash.course` exists before accessing properties to prevent "Cannot read properties of undefined" errors.

### Step 4: Verification Plan
1.  Run `pip install psycopg2-binary`.
2.  Update `.env` with Neon connection string.
3.  Run `python backend/seed_full.py`.
4.  Restart Backend (`uvicorn`) and Frontend (`npm run dev`).
5.  Check Dashboard: It should load. `AdaptivePath` should show "Upgrade" (if using non-premium user) or content (if using test premium user).
