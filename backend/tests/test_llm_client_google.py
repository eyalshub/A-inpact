# backend/tests/test_llm_client_google.py
import os
import json
from pathlib import Path
from backend.utils.llm_client import call_llm_with_yaml_prompt

def test_call_google_gemini():
    # Force the provider to be Google Gemini
    os.environ["PROVIDER"] = "google"
    os.environ["GOOGLE_MODEL"] = "gemini-1.5-flash"

    # Make sure GOOGLE_API_KEY is available in .env or environment
    assert os.getenv("GOOGLE_API_KEY"), "❌ Missing GOOGLE_API_KEY in environment"

    # Path to the YAML prompt file
    prompt_path = Path("backend/prompts/report_prompt.yaml")

    # Load the example JSON input (from matcher output)
    json_path = Path("data/matches/match_20250911_172054_401c2d.json")
    assert json_path.exists(), f"❌ JSON file not found: {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        example_input = json.load(f)

    # Call the LLM with structured prompt
    response = call_llm_with_yaml_prompt(
        yaml_path=prompt_path,
        json_input=example_input,
        provider="google",  # Explicitly testing Gemini
        verbose=True
    )

    # Basic assertions on the output
    assert isinstance(response, str)
    assert len(response) > 20
    print("\n\n📄 Google Gemini Response:\n", response)
