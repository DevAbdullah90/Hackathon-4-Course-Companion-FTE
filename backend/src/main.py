from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import api_router
from .core.config import settings
from .core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Course Companion Backend",
    description="Deterministic backend for Course Companion FTE (Zero-Backend-LLM)",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok", "zero_llm_compliant": True}
