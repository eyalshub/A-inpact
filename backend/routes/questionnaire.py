# backend/routes/questionnaire.py
"""
API route for receiving business profile questionnaire submissions.

This endpoint accepts a structured business profile, validates it using Pydantic,
and returns the parsed data. In future versions, this will trigger rule matching logic.
"""

from fastapi import APIRouter
from backend.models.user_input import BusinessProfile
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()


@router.post("/questionnaire")
async def submit_questionnaire(profile: BusinessProfile):
    """
    Receive a submitted business profile from the frontend.

    Args:
        profile: Parsed and validated business profile (Pydantic model).

    Returns:
        JSON response confirming receipt and echoing back the profile.
    """
    logger.info(f"📥 Received questionnaire for business: {profile.business_name}")

    return {
        "message": "✅ Questionnaire submitted successfully",
        "data": profile.model_dump()
    }
