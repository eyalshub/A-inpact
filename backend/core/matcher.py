# backend/core/matcher.py
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from datetime import datetime

# 📥 Optional engine: matches raw free-text regulation documents
from backend.core.matcher_from_regdoc import match_from_regdoc

# Priority level constants for severity ranking
MANDATORY = 1
RECOMMENDED = 2
INFO = 3


def load_compiled_rules(path: str = "data/processed/compiled_rules.json") -> List[Dict[str, Any]]:
    """
    Load a list of compiled regulatory rules from a JSON file.

    Args:
        path: Path to the compiled rules JSON file.

    Returns:
        List of rule dictionaries.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        print("🔍 First 3 entries in rules file:", data[:3])
        return data


def _applies(profile: Dict[str, Any], applies_if: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Internal helper to evaluate whether a rule applies to the given profile.

    Supports exact match and maximum thresholds via keys ending in '_max'.

    Args:
        profile: Business profile data.
        applies_if: Condition dict defined in the rule.

    Returns:
        A tuple: (True/False if rule applies, list of matching reasons or reasons for rejection)
    """
    reasons = []

    for key, val in applies_if.items():
        if key.endswith("_max"):
            actual = profile.get(key.replace("_max", ""))
            if actual is not None and actual <= val:
                reasons.append(f"{key.replace('_max','')} ≤ {val}")
            else:
                return False, [f"{key.replace('_max','')} > {val}"]
        else:
            if profile.get(key) == val:
                reasons.append(f"{key} == {val}")
            else:
                return False, [f"{key} != {val}"]

    return True, reasons


def match_rules(profile: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Match a business profile against a list of compiled rules and return results.

    Args:
        profile: Business profile dictionary.
        rules: List of compiled rule dictionaries.

    Returns:
        A result dictionary including matched rules and identified compliance gaps.
    """
    matches = []
    gaps = []

    for rule in rules:
        ok, reasons = _applies(profile, rule.get("applies_if", {}))
        if not ok:
            continue

        severity = rule.get("severity", "info")
        priority = {"mandatory": MANDATORY, "recommended": RECOMMENDED, "info": INFO}.get(severity, INFO)

        match = {
            "id": rule["id"],
            "title": rule.get("title"),
            "authority": rule.get("authority"),
            "severity": severity,
            "priority": priority,
            "applies_because": reasons,
            "requirements": [req["name"] for req in rule.get("requirements", [])],
            "source": rule.get("source"),
            "tags": rule.get("tags", [])
        }
        matches.append(match)

        # Special case: identify disinfection gaps in mandatory rules
        if severity == "mandatory" and "חיטוי" in json.dumps(match, ensure_ascii=False):
            gaps.append({
                "rule_id": rule["id"],
                "gap": "Missing official disinfection documents",
                "suggested_action": "Provide latest certified water disinfection documentation"
            })

    return {
        "profile": profile,
        "matches": matches,
        "gaps": gaps
    }


def generate_unique_profile_id(profile: Dict[str, Any]) -> str:
    """
    Generate a unique filename-friendly identifier for a profile based on name and timestamp.

    Args:
        profile: Business profile dictionary.

    Returns:
        Unique string identifier (e.g. 'my_bakery_20250913_153000')
    """
    name = profile.get("name", "business").lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}"


def save_match_result(profile_id: str, result: dict, folder: str = "data/matches") -> str:
    """
    Save the match result to a JSON file and return its path.

    Args:
        profile_id: The identifier for the profile.
        result: Dictionary containing match result data.
        folder: Directory to save match result in.

    Returns:
        String path to the saved JSON file.
    """
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    outfile = path / f"match_{profile_id}.json"

    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved match result to {outfile}")
    return str(outfile)


def run_full_match(
    profile: Dict[str, Any],
    profile_id: str = None,
    use_regdoc: bool = False,
    regdoc_path: str = "data/processed/reg-4.2A-2022.json"
) -> Dict[str, Any]:
    """
    Run the complete matching process on a business profile.

    Can choose between:
    - Structured rules (compiled)
    - Raw regdoc (parsed free-text JSON)

    Args:
        profile: Business profile data.
        profile_id: Optional profile identifier (auto-generated if not provided).
        use_regdoc: Whether to use the raw regulation doc engine.
        regdoc_path: Path to the regdoc JSON file.

    Returns:
        A dictionary with match status, file path, and (optionally) number of matches.
    """
    profile_id = profile_id or generate_unique_profile_id(profile)
    print(f"🚀 Running match for profile: {profile_id}")

    if use_regdoc:
        # Run raw document matching engine
        match_from_regdoc(
            profile=profile,
            regdoc_path=regdoc_path,
            output_dir="data/matches",
            profile_id=profile_id
        )
        match_file = f"data/matches/match_{profile_id}.json"
        return {
            "message": "✅ Match done via regdoc engine",
            "match_file": match_file
        }

    # Default: compiled rule engine
    rules = load_compiled_rules()
    result = match_rules(profile, rules)
    match_file = save_match_result(profile_id, result)
    return {
        "message": "✅ Match done via compiled rules",
        "match_file": match_file,
        "num_matches": len(result["matches"])
    }
