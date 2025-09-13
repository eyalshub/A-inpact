# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

from backend.utils.logging_config import setup_logging
from backend.routes import questionnaire, report, pipeline

# ===============================
# Logging
# ===============================
setup_logging()
logger = logging.getLogger(__name__)

# ===============================
# FastAPI App
# ===============================
app = FastAPI(
    title="A-Impact Business Licensing API",
    version="1.0.0",
    description=(
        "מערכת להערכת רישוי עסקים בישראל. "
        "כוללת שאלון → מנוע התאמה → יצירת דוח חכם באמצעות LLM."
    ),
)

# ===============================
# CORS Middleware
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # אפשר לשים כאן כתובת מדויקת של הפרונט
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Routers
# ===============================
app.include_router(questionnaire.router, prefix="/api/v1", tags=["questionnaire"])
app.include_router(report.router, prefix="/api/v1", tags=["report"])
app.include_router(pipeline.router, prefix="/api/v1", tags=["pipeline"])

# ===============================
# Static Frontend
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(BASE_DIR, "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# ===============================
# Root Endpoint
# ===============================
@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "status": "ok",
        "service": "A-Impact API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/questionnaire",
            "/api/v1/report/generate",
            "/api/v1/pipeline/run_json",
            "/frontend/index.html"
        ]
    }
