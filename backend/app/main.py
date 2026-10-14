"""
ReSkillAI - Career Intelligence Platform Backend
Main FastAPI Application Entrypoint
"""
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes import (
    health,
    auth,
    resume,
    profile,
    assessment,
    careers,
    skill_gap,
    roadmap,
    learning,
    progress,
    jobs,
    intelligence,
    coach,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Deterministic Career Intelligence & Skill Navigation API for ReSkillAI",
)

# Enable CORS for frontend clients (Web & Android Capacitor)
# Note: allow_origins cannot contain '*' when allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://localhost",
        "http://localhost",
        "capacitor://localhost",
    ],
    allow_origin_regex=r"^(https?|capacitor)://(localhost|127\.0\.0\.1|10\.0\.2\.2)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router with /api prefix
api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(resume.router)
api_router.include_router(profile.router)
api_router.include_router(assessment.router)
api_router.include_router(careers.router)
api_router.include_router(skill_gap.router)
api_router.include_router(roadmap.router)
api_router.include_router(learning.router)
api_router.include_router(progress.router)
api_router.include_router(jobs.router)
api_router.include_router(intelligence.router)
api_router.include_router(coach.router)

# Mount /api
app.include_router(api_router)

# Serve the React frontend from the project root's dist folder
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "dist"
INDEX_FILE = FRONTEND_DIR / "index.html"


@app.get("/", include_in_schema=False)
def serve_frontend():
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)

    return {
        "service": "ReSkillAI Backend",
        "version": "1.0.0",
        "status": "operational",
        "message": "Frontend build not found. Run npm run build.",
        "docs_url": "/docs",
        "api_prefix": "/api",
    }


# Serve built frontend assets (JS, CSS, images)
if FRONTEND_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="frontend-assets",
    )


# Support React client-side routes
@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend_routes(full_path: str):
    if full_path.startswith("api/") or full_path in {"docs", "openapi.json", "redoc"}:
        raise HTTPException(status_code=404, detail="Not found")

    requested_file = FRONTEND_DIR / full_path

    if requested_file.is_file():
        return FileResponse(requested_file)

    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)

    raise HTTPException(status_code=404, detail="Frontend build not found")
