# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    """Fixture that provides a TestClient for the FastAPI app."""
    return TestClient(app)
