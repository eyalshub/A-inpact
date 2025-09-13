# backend/scripts/compile_rules_from_regdoc.py
import json
from pathlib import Path
import sys

# Add project root to sys.path to enable absolute imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.extract_regulations import extract_text
from core.regulation_parser import parse_to_json

INPUT = Path("data/processed/reg-4.2A-2022.json")
OUTPUT = Path("data/processed/compiled_rules.json")

# Mapping Hebrew phrases → business profile fields
def detect_applies_if_conditions(content: str) -> dict:
    """
    Heuristically map text content to applies_if conditions that match BusinessProfile fields.
    """
    applies_if = {}

    if "גז" in content:
        applies_if["has_gas_installation"] = True
    if "80 מ״ר" in content or "80 מטר" in content:
        applies_if["business_area_sqm"] = {"max": 80}
    if "מעל 100 מקומות" in content:
        applies_if["seating_capacity"] = {"min": 100}
    if "משלוחים" in content:
        applies_if["offers_delivery"] = True
    if "בשר" in content:
        applies_if["serves_meat"] = True
    if "אש פתוחה" in content:
        applies_if["uses_open_fire"] = True
    if "מטבח תעשייתי" in content:
        applies_if["has_industrial_kitchen"] = True
    if "אלכוהול" in content:
        applies_if["serves_alcohol"] = True
    if "אזור חיצוני" in content or "מרפסת" in content:
        applies_if["has_outdoor_area"] = True
    if "מוזיקה" in content or "רעש" in content:
        applies_if["has_music_or_noise"] = True
    if "כשר" in content:
        applies_if["is_kosher"] = True

    return applies_if


def compile_rules(data):
    """
    Converts parsed regulation JSON into a flat list of rule dicts with metadata and conditions.
    """
    rules = []
    for section in data.get("sections", []):
        authority = section.get("title", "Unknown Authority")
        for sub in section.get("subsections", []):
            content = sub.get("content", "").strip()
            if not content:
                continue

            applies_if = detect_applies_if_conditions(content)
            if not applies_if:
                continue  # Skip irrelevant rules

            rule = {
                "id": f"R-{section['id']}-{sub['id']}",
                "title": sub.get("title", "לא צויין"),
                "authority": authority,
                "severity": "mandatory", 
                "applies_if": applies_if,
                "requirements": [{"name": content}],
                "source": {
                    "section_id": section["id"],
                    "subsection_id": sub["id"]
                }
            }
            rules.append(rule)

    print(f"✅ Compiled {len(rules)} rules with applies_if conditions")
    return rules


if __name__ == "__main__":
    with open(INPUT, encoding="utf-8") as f:
        data = json.load(f)

    rules = compile_rules(data)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)

    print(f"📦 Saved to: {OUTPUT.resolve()}")
