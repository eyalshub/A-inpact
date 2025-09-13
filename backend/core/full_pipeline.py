# backend/core/full_pipeline.py

import uuid
from datetime import datetime
from pathlib import Path
import json

from backend.core.regulation_parser import parse_to_json
from backend.core.regulation_parser import convert_to_json

from backend.scripts.extract_regulations import extract_text
from backend.core.matcher import run_full_match
from backend.core.report_generator import generate_report

def generate_run_id() -> str:
    """Generate a unique run ID based on timestamp and UUID suffix"""
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

def load_profile(profile_path: str) -> dict:
    """Load business profile from JSON file"""
    with open(profile_path, encoding="utf-8") as f:
        return json.load(f)

def run_pipeline(profile_path: str, source_doc_path: str, output_dir: str = "data"):
    """
    Run the full regulatory pipeline:
    1. Extract regulation from source document
    2. Load user profile
    3. Match relevant rules
    4. Generate final report
    """
    run_id = generate_run_id()
    print(f"\n🚀 Starting pipeline run: {run_id}")
    print(f"📁 Output base directory: {output_dir}")
    
    output_dir = Path(output_dir)
    processed_dir = output_dir / "processed"
    matches_dir = output_dir / "matches"
    report_dir = Path("C:/Users/eyals/MyProjects/A-Impact/data/report")


    # Ensure directories exist
    for dir_path in [processed_dir, matches_dir, report_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📂 Ensured directory exists: {dir_path}")

    # Step 1 – Extract and convert regulation document
    print(f"\n🔎 Step 1: Extracting regulation from PDF:\n👉 {source_doc_path}")
    try:
        text = extract_text(source_doc_path)
        print(f"✅ Extracted {len(text)} characters from regulation document.")
    except Exception as e:
        print(f"❌ Failed to extract text from PDF: {e}")
        raise

    reg_json_path = processed_dir / f"reg_{run_id}.json"
    try:
        convert_to_json(text, output_path=str(reg_json_path))
        print(f"✅ Regulation JSON saved to: {reg_json_path}")
    except Exception as e:
        print(f"❌ Failed to convert text to JSON: {e}")
        raise

    # Step 2 – Load user profile
    print(f"\n👤 Step 2: Loading user profile from:\n👉 {profile_path}")
    try:
        profile = load_profile(profile_path)
        print(f"✅ Loaded profile with keys: {list(profile.keys())}")
    except Exception as e:
        print(f"❌ Failed to load profile: {e}")
        raise

    # Step 3 – Run matcher
    print(f"\n⚙️ Step 3: Running rule matching engine...")
    try:
        match_result = run_full_match(
            profile=profile,
            profile_id=run_id,
            use_regdoc=True,
            regdoc_path=str(reg_json_path)
        )
        print("✅ Matcher completed.")
    except Exception as e:
        print(f"❌ Matcher failed: {e}")
        raise

    match_file = match_result.get("match_file", str(matches_dir / f"match_{run_id}.json"))
    print(f"📄 Match file path: {match_file}")

    # Step 4 – Generate report
    print(f"\n📝 Step 4: Generating final compliance report...")
    try:
        report_path = generate_report(
            match_file_path=match_file,
            output_dir=str(report_dir)
        )
        report_path = Path(report_path).resolve() 
        print(f"✅ Report generated at: {report_path}")
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        raise

    print("\n🎉 Pipeline completed successfully.")
    print(f"📄 Final match file: {match_file}")
    print(f"📑 Final report file: {report_path}")
    return report_path