# backend/core/report_generator.py
import json
from pathlib import Path
from backend.utils.llm_client import call_llm_with_yaml_prompt
import argparse

# Path to the YAML prompt template used by the LLM
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "report_prompt.yaml"


def generate_llm_report(profile: dict, rules: list) -> str:
    """
    Generate a personalized regulatory compliance report in Hebrew using an LLM.

    Args:
        profile: Business profile dictionary (e.g., area, seating, gas usage).
        rules: List of matched regulatory rules for this business.

    Returns:
        A regulatory report string (in Hebrew).
    """
    json_input = {
        "business_profile": profile,
        "matched_rules": rules
    }

    return call_llm_with_yaml_prompt(
        yaml_path=PROMPT_PATH,
        json_input=json_input,
        provider="google",   # Can be made configurable
        verbose=True
    )


def generate_llm_report_from_file(json_path: Path) -> str:
    """
    Load a match result JSON file and generate a regulatory report.

    Args:
        json_path: Path to the JSON file with 'profile' and 'matches'.

    Returns:
        A regulatory report string (in Hebrew).

    Raises:
        FileNotFoundError: If the provided file does not exist.
        ValueError: If expected keys are missing in the JSON.
    """
    if not json_path.exists():
        raise FileNotFoundError(f"❌ JSON file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "profile" not in data or "matches" not in data:
        raise ValueError("❌ JSON must contain 'profile' and 'matches' keys")

    return generate_llm_report(
        profile=data["profile"],
        rules=data["matches"]
    )


def generate_report(match_file_path: str, output_dir: str = "data/report") -> str:
    """
    Full pipeline for generating a compliance report from match results.

    1. Load match results from file
    2. Generate LLM-based report
    3. Save report to a .txt file

    Args:
        match_file_path: Path to the match JSON file.
        output_dir: Output directory to save the report.

    Returns:
        Path to the saved report file (as string).
    """
    report_text = generate_llm_report_from_file(Path(match_file_path))

    # Derive a unique report filename based on match file name
    profile_id = Path(match_file_path).stem.replace("match_", "")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_file_path = Path(output_dir) / f"report_{profile_id}.txt"

    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"✅ Report saved to: {report_file_path}")
    return str(report_file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--match", type=str, required=True, help="Path to match file")
    args = parser.parse_args()

    report = generate_report(args.match)
    print(report)
