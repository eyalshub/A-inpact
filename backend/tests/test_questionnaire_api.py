#backend/tests/test_questionnaire_api.py
"""
Tests for the /questionnaire API endpoint.
This endpoint receives a BusinessProfile from the user and returns the same data back.
"""

import pytest


def test_submit_questionnaire_valid(client):
    """
    Checks that a valid questionnaire submission returns the same data back.
    """
    payload = {
        "business_name": "Eyal's Grill",
        "business_type": "restaurant",
        "business_area_sqm": 120.5,
        "seating_capacity": 40,
        "has_gas_installation": True,
        "serves_meat": True,
        "offers_delivery": True
    }

    response = client.post("/api/v1/questionnaire", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "✅ Questionnaire submitted successfully" in data["message"]
    assert data["data"]["business_name"] == "Eyal's Grill"
    assert data["data"]["business_type"] == "restaurant"
    assert data["data"]["seating_capacity"] == 40
    assert data["data"]["has_gas_installation"] is True
    assert data["data"]["offers_delivery"] is True


def test_submit_questionnaire_invalid_missing_field(client):
    """
    Checks that missing required fields trigger a validation error (422).
    """
    payload = {
        # Missing required "business_name"
        "business_type": "restaurant",
        "business_area_sqm": 80,
        "seating_capacity": 20,
        "has_gas_installation": False
    }

    response = client.post("/api/v1/questionnaire", json=payload)

    assert response.status_code == 422
    data = response.json()

    # Check that the missing field is mentioned in the error response
    error_fields = [err["loc"][-1] for err in data["detail"]]
    assert "business_name" in error_fields