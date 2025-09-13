# backend/tests/test_matcher.py
import json
from pathlib import Path
from backend.core.matcher import match_rules, save_match_result, run_full_match

EXAMPLE_RULES = [
    {
        "id": "MOH_WATER",
        "title": "Potable Water",
        "authority": "Ministry of Health",
        "severity": "mandatory",
        "applies_if": {"uses_gas": True},
        "requirements": [{"name": "Connect to certified water system"}, {"name": "Periodic disinfection"}],
        "source": {"section": "4", "sub": "4.6"},
        "tags": ["water"]
    },
    {
        "id": "POLICE_CCTV_EXEMPT",
        "title": "CCTV exemption under 200 seats & no alcohol",
        "authority": "Police",
        "severity": "info",
        "applies_if": {"seats_max": 200, "serves_alcohol": False},
        "requirements": [{"name": "Exempt from CCTV requirements"}],
        "source": {"section": "3", "sub": "3.8"},
        "tags": ["cctv"]
    }
]

def test_rule_matching_applies_correctly():
    profile = {"uses_gas": True, "seats": 120, "serves_alcohol": False}
    result = match_rules(profile, EXAMPLE_RULES)
    assert len(result["matches"]) == 2
    ids = [r["id"] for r in result["matches"]]
    assert "MOH_WATER" in ids
    assert "POLICE_CCTV_EXEMPT" in ids

def test_rule_matching_ignores_non_applicable():
    profile = {"uses_gas": False, "seats": 250, "serves_alcohol": True}
    result = match_rules(profile, EXAMPLE_RULES)
    assert result["matches"] == []

def test_gap_detection_exists():
    profile = {"uses_gas": True}
    result = match_rules(profile, EXAMPLE_RULES)
    assert any("gap" in g for g in result["gaps"])

def test_save_match_result_creates_file(tmp_path):
    dummy_result = {"profile": {"seats": 100}, "matches": [], "gaps": []}
