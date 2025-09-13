# backend/models/user_input.py
"""
This module defines the Pydantic model for validating and structuring user input
in the business profile questionnaire. It ensures the input is well-typed,
bounded (e.g., area ≥ 0), and semantically meaningful for downstream processing.
"""

from pydantic import BaseModel, Field
from typing import Optional


class BusinessProfile(BaseModel):
    """
    Pydantic model representing a business profile submitted via the questionnaire.

    Fields:
        business_name: Name of the business.
        business_type: Type/category of the business (e.g., restaurant, cafe).
        business_area_sqm: Total area of the business in square meters.
        seating_capacity: Maximum number of seats or customers at once.

        has_gas_installation: Whether the business uses gas.
        serves_meat: Whether the business serves meat-based products.
        offers_delivery: Whether the business provides delivery services.

        uses_open_fire: Whether open flame is used in operations.
        has_industrial_kitchen: Whether there's an industrial-grade kitchen setup.
        serves_alcohol: Whether alcoholic beverages are served or sold.
        has_outdoor_area: Whether the business has an outdoor seating/dining area.
        has_music_or_noise: Whether music or other significant noise is played.
    """

    business_name: str = Field(..., description="Name of the business")
    business_type: str = Field(..., description="Type of business (e.g., restaurant, cafe)")
    business_area_sqm: float = Field(..., ge=0, description="Size of the business in square meters")
    seating_capacity: int = Field(..., ge=0, description="Number of seats or max occupancy")

    has_gas_installation: bool = Field(..., description="Does the business use gas?")
    serves_meat: Optional[bool] = Field(False, description="Does the business serve meat?")
    offers_delivery: Optional[bool] = Field(False, description="Does the business offer delivery services?")

    uses_open_fire: Optional[bool] = Field(False, description="Does the business use open fire?")
    has_industrial_kitchen: Optional[bool] = Field(False, description="Does the business have an industrial kitchen?")
    serves_alcohol: Optional[bool] = Field(False, description="Does the business serve alcoholic beverages?")
    has_outdoor_area: Optional[bool] = Field(False, description="Is there an outdoor seating area?")
    has_music_or_noise: Optional[bool] = Field(False, description="Does the business play music or generate noise?")
