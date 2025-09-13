# backend/routes/report.py
"""
API route for generating a regulatory report from an existing match file.

This endpoint allows the frontend or other services to trigger LLM-based report generation
by referencing a precomputed match file (e.g., match_restaurant_eyal.json).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import logging

from backend.core.report_generator import generate_llm_report_from_file

router = APIRouter()
logger = logging.getLogger(__name__)

# Default location of match JSON files
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "matches"


class ReportFromFileRequest(BaseModel):
    """
    Request model for generating a report from an existing JSON match file.
    """
    filename: str = Field(..., description="Name of the match JSON file (e.g., match_restaurant_eyal.json)")
    model: str = Field(default="gpt-4", description="LLM provider or model name to use (optional)")


@router.post("/report-from-file")
def report_from_file(request: ReportFromFileRequest):
    """
    Generate a regulatory compliance report from a saved match file.

    Request Body:
    {
      "filename": "match_restaurant_eyal.json",
      "model": "gpt-4"  // optional
    }

    Returns:
        JSON response with report content and metadata.
    """
    file_path = DATA_DIR / request.filename

    if not file_path.exists():
        logger.warning(f"❌ Match file not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {request.filename}")

    try:
        logger.info(f"📄 Generating report from file: {file_path} using model: {request.model}")
        report = generate_llm_report_from_file(file_path, model=request.model)

        return {
            "message": "✅ Report generated successfully",
            "filename": request.filename,
            "model": request.model,
            "report": report
        }

    except Exception as e:
        logger.exception("❌ Report generation failed")
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
