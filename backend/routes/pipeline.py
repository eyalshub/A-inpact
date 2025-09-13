# backend/routes/pipeline.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging
import json
from pathlib import Path
import tempfile

from backend.core.full_pipeline import run_pipeline

router = APIRouter()
logger = logging.getLogger(__name__)


# === Request model for path-based pipeline run ===
class PipelineRequest(BaseModel):
    profile_path: str = Field(..., description="Path to the business profile JSON file")
    source_doc_path: str = Field(..., description="Path to the regulatory source document")
    output_dir: str = Field(..., description="Directory to store intermediate and final outputs")


@router.post("/pipeline/run")
def run_full_pipeline(req: PipelineRequest):
    """
    Run the full pipeline (Stages 1–4) using file paths only.

    Returns:
        JSON with report path if successful.
    """
    try:
        logger.info(f"Running pipeline for profile={req.profile_path}, source_doc={req.source_doc_path}")
        report_path = run_pipeline(
            profile_path=req.profile_path,
            source_doc_path=req.source_doc_path,
            output_dir=req.output_dir,
        )
        report_path = Path(report_path).resolve()

        if not report_path.exists():
            raise HTTPException(status_code=500, detail=f"Report not found at {report_path}")

        return {"status": "success", "report_path": str(report_path)}

    except Exception as e:
        logger.exception("Pipeline run failed")
        raise HTTPException(status_code=500, detail=str(e))


# === Inline business profile schema for JSON-based pipeline run ===
class BusinessProfile(BaseModel):
    business_name: str
    area_sqm: int
    num_seats: int
    uses_gas: bool = False
    delivers: bool = False
    has_meat: bool = False
    uses_fryer: bool = False
    has_alcohol: bool = False
    serves_dairy: bool = False
    has_seating: bool = True
    is_open_air: bool = False
    uses_gas_grill: bool = False
    is_kosher: bool = False


class PipelineRunJSONRequest(BaseModel):
    profile: BusinessProfile
    source_doc_path: str
    output_dir: str


@router.post("/pipeline/run_json")
def run_full_pipeline_json(req: PipelineRunJSONRequest):
    """
    Run the full pipeline using an inlined JSON profile (no file upload needed).

    Returns:
        JSON with report path, report text, and original profile data.
    """
    try:
        # Save profile to a temporary file to simulate file-based input
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8") as tmp:
            json.dump(req.profile.dict(), tmp, ensure_ascii=False, indent=2)
            tmp_path = Path(tmp.name)

        logger.info(f"Running pipeline with JSON profile={req.profile.business_name}, saved at {tmp_path}")

        report_path = run_pipeline(
            profile_path=tmp_path,
            source_doc_path=req.source_doc_path,
            output_dir=req.output_dir,
        )
        report_path = Path(report_path).resolve()

        if not report_path.exists():
            logger.error(f"❌ Report file not found: {report_path}")
            raise HTTPException(status_code=500, detail=f"Report file not found at {report_path}")

        try:
            with open(report_path, "r", encoding="utf-8") as f:
                report_text = f.read()
        except Exception as e:
            logger.error(f"❌ Failed to read report file {report_path}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to read report file: {e}")

        return {
            "status": "success",
            "report_path": str(report_path),
            "report_text": report_text,
            "profile": req.profile.dict(),
        }

    except Exception as e:
        logger.exception("Pipeline run (JSON) failed")
        raise HTTPException(status_code=500, detail=str(e))
