# backend/core/matcher_from_regdoc.py
import json
import re
from pathlib import Path
from typing import Dict, Any, List

# 🧠 Synonyms map for semantic keyword matching
SYNONYMS: Dict[str, List[str]] = {
    "uses_gas": [
        "גז", "שימוש בגז", "מתקני גז", "בלוני גז", "מערכת גז", "אספקת גז", "תשתית גז", "חיבור גז"
    ],
    "delivers": [
        "משלוחים", "שליחויות", "שירות משלוחים", "שילוח", "אספקה לבית הלקוח", "הזמנות טלפוניות"
    ],
    "has_meat": [
        "בשר", "מנות בשריות", "בשר אדום", "בשר עוף", "הגשת בשר", "מזון מן החי", "שחיטה", "חומרי גלם מן החי"
    ],
    "uses_fryer": [
        "טיגון", "מכשירי טיגון", "סיר טיגון", "צ'יפסר", "מכשירי חימום שמן", "שמן רותח"
    ],
    "has_alcohol": [
        "מכירת אלכוהול", "הגשת משקאות חריפים", "רישיון משקאות", "שתייה חריפה"
    ],
    "serves_dairy": [
        "מוצרי חלב", "גבינות", "יוגורט", "מנות חלביות", "הגשת חלב", "תפריט חלבי"
    ],
    "has_seating": [
        "מקומות ישיבה", "כיסאות ושולחנות", "אזור הסעדה", "ישיבה במקום", "ישיבה במסעדה"
    ],
    "is_open_air": [
        "אוויר פתוח", "מרפסת", "חצר", "הסעדה חיצונית", "איזור ישיבה פתוח", "שולחנות מחוץ למבנה"
    ],
    "uses_gas_grill": [
        "גריל גז", "מתקן גריל", "גריל", "צלייה", "ברביקיו", "מתקן צלייה"
    ],
    "is_kosher": [
        "כשרות", "רבנות", "תעודת כשרות", "פיקוח הלכתי", "בשר חלק", "כשר למהדרין"
    ]
}


def _keyword_match(key: str, content: str) -> bool:
    """
    Check if any synonym for the given profile key appears in the regulation content.

    Args:
        key: A profile attribute key (e.g., 'uses_gas').
        content: A text segment from a regulation document.

    Returns:
        True if a match is found, False otherwise.
    """
    return any(word in content for word in SYNONYMS.get(key, []))


def _extract_number(text: str) -> int:
    """
    Extract the first numeric value found in the given text.

    Used for interpreting 'up to' or 'above' rules.

    Args:
        text: The text from which to extract a number.

    Returns:
        The first number found, or 0 if none exists.
    """
    match = re.search(r"\d+", text.replace(",", ""))
    return int(match.group()) if match else 0


def match_conditions(content: str, profile: Dict[str, Any]) -> List[str]:
    """
    Match a regulation text segment against business profile attributes.

    Args:
        content: A section of regulation text.
        profile: Business profile dictionary.

    Returns:
        A list of reasons indicating which profile attributes matched this content.
    """
    reasons = []

    for key, value in profile.items():
        if isinstance(value, bool) and value:
            if key in content or _keyword_match(key, content):
                reasons.append(f"✔ {key} == True")

        elif isinstance(value, (int, float)):
            if f"{value}" in content:
                reasons.append(f"✔ {key} == {value}")
            number = _extract_number(content)
            if "עד" in content and value <= number:
                reasons.append(f"✔ {key} ≤ {value}")
            elif "מעל" in content and value > number:
                reasons.append(f"✔ {key} > {value}")

    return reasons


def match_from_regdoc(
    profile: Dict[str, Any],
    regdoc_path: str,
    output_dir: str,
    profile_id: str
) -> str:
    """
    Scan a structured regulation document and extract applicable rules for a business profile.

    Args:
        profile: Business profile dictionary.
        regdoc_path: Path to the regulation document (in structured JSON format).
        output_dir: Directory where the match results will be saved.
        profile_id: Unique identifier for this profile/run.

    Returns:
        Path to the generated match result JSON file.
    """
    with open(regdoc_path, encoding="utf-8") as f:
        regdoc = json.load(f)

    matches = []

    for section in regdoc.get("sections", []):
        authority = section.get("title", "Unknown Authority")

        for sub in section.get("subsections", []):
            content = sub.get("content", "").strip()
            if not content:
                continue

            reasons = match_conditions(content, profile)
            if not reasons:
                continue

            matches.append({
                "rule_id": f"{section['id']}-{sub['id']}",
                "title": sub.get("title", "Untitled"),
                "authority": authority,
                "applies_because": reasons,
                "requirement_text": content
            })

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    outfile = Path(output_dir) / f"match_{profile_id}.json"

    # Save match results to JSON file
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump({
            "profile": profile,
            "matches": matches,
            "total_matches": len(matches)
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ Match completed: {len(matches)} matches saved to {outfile}")
    return str(outfile)
