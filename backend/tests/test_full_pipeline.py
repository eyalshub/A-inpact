import json
import os
from pathlib import Path
from backend.core.full_pipeline import run_pipeline

def test_full_pipeline_creates_report(tmp_path):
    """
    Integration test: ensures full pipeline runs and output files are created.
    """

    # === Arrange ===
    profile_data = {
        "business_name": "מסעדת הדג הכחול",
        "area_sqm": 120,
        "num_seats": 40,
        "uses_gas": True,
        "delivers": True,
        "has_meat": True,
        "uses_fryer": True,
        "has_alcohol": False,
        "serves_dairy": False,
        "has_seating": True,
        "is_open_air": False,
        "uses_gas_grill": True,
        "is_kosher": True
    }

    profile_path = tmp_path / "profile_test.json"
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)

    source_doc = "data/rew/18-07-2022_4.2A.pdf"

    # === Act ===
    run_pipeline(
        profile_path=str(profile_path),
        source_doc_path=source_doc,
        output_dir=str(tmp_path)  # Use temporary output dir
    )

    # === Assert ===
    report_dir = Path("C:/Users/eyals/MyProjects/A-Impact/data/report")
    report_files = list(report_dir.glob("report_*.txt"))
    assert len(report_files) > 0, "❌ No report file was created."

    latest_report = max(report_files, key=os.path.getctime)
    with open(latest_report, encoding="utf-8") as f:
        content = f.read()

    assert "רישוי" in content or "דוח" in content or len(content) > 100
