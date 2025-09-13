# backend/tests/test_llm_client_ollama.py

import os
from pathlib import Path
from backend.utils.llm_client import call_llm_with_yaml_prompt

def test_call_ollama_llama32():
    # נכריח את הספק להיות ollama
    os.environ["PROVIDER"] = "ollama"
    os.environ["OLLAMA_MODEL"] = "llama3.2"

    prompt_path = Path("backend/prompts/report_prompt.yaml")
    example_input = {
        "business_profile": {
            "area_sqm": 80,
            "seats": 35,
            "uses_gas": True,
            "delivers": True,
            "has_meat": False
        },
        "matched_rules": [
            {
                "title": "דרישת בטיחות בגז",
                "authority": "כבאות",
                "priority": 1,
                "description": "על העסק לוודא תקינות מערכת גז בהתאם לתקנים."
            }
        ]
    }

    response = call_llm_with_yaml_prompt(
        yaml_path=prompt_path,
        json_input=example_input,
        provider="ollama",   # ← נבדק רק מול Ollama
        verbose=True
    )

    assert isinstance(response, str)
    assert len(response) > 20
    print("\n\n📄 Ollama Response:\n", response)
