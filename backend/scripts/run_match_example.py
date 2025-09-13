# backend/scripts/run_match_example.py

import sys
import json
from pathlib import Path

# Enable absolute imports from backend/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.core.matcher import run_full_match

# 👤 Example business profile (Stage 2 – user answers)
example_profile = {
    "business_name": "הדר עוגיות",
    "business_type": "בית קפה",
    "business_area_sqm": 60,
    "seating_capacity": 40,
    "has_gas_installation": True,
    "offers_delivery": True,
    "serves_meat": False,
    "uses_open_fire": False,
    "has_industrial_kitchen": False,
    "serves_alcohol": False,
    "has_outdoor_area": False,
    "has_music_or_noise": False
}

# 🏁 Run matching
if __name__ == "__main__":
    result = run_full_match(profile=example_profile, profile_id="restaurant_eyal")

    print(f"\n🔍 Total matches found: {len(result['matches'])}")
    if result.get("gaps"):
        print(f"⚠️ Gaps detected: {len(result['gaps'])}")

    # Save results
    out_path = Path("data/matches/match_restaurant_eyal.json")
    out_path.parent.mkdir(exist_ok=True, parents=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"📦 Results saved to: {out_path.resolve()}")
