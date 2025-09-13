# backend/scripts/build_regulations_json.py
"""
Script to convert a raw regulatory document (PDF or DOCX)
into a structured JSON format compatible with the pipeline.

Steps:
1. Extract text from the document.
2. Parse the text into a hierarchical structure (chapters, subsections, content).
3. Save the result as JSON for downstream processing.
"""

import json
from pathlib import Path
import sys
import logging

# Add project root to sys.path for absolute imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.extract_regulations import extract_text
from core.regulation_parser import parse_to_json

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def build_json_from_file(
    input_path: str,
    output_path: str,
    doc_id: str,
    title: str
):
    """
    Full pipeline for converting a regulation file to structured JSON.

    Args:
        input_path: Path to the raw regulation document (PDF or DOCX).
        output_path: Path where structured JSON should be saved.
        doc_id: Unique identifier for the regulation document.
        title: Human-readable title of the regulation.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Step 1 – Extract raw text
    logger.info(f"📄 Extracting text from: {input_path.name}")
    text = extract_text(input_path)

    logger.info("💬 Extracted text preview:")
    print(text[:2000])  # Optional for manual debugging

    # Step 2 – Parse into structured JSON
    logger.info(f"🧠 Parsing text into structured format...")
    parsed = parse_to_json(text, doc_id=doc_id, title=title)

    # Step 3 – Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Saved structured JSON to: {output_path.resolve()}")


if __name__ == "__main__":
    # === Configuration for this run ===
    input_file = BASE_DIR / "data" / "rew" / "18-07-2022_4.2A.pdf"
    output_file = BASE_DIR / "data" / "processed" / "reg-4.2A-2022.json"
    doc_id = "reg-4.2A-2022"
    title = "מפרט אחיד לפריט 4.2א – בית אוכל"

    # Execute transformation
    build_json_from_file(
        input_path=input_file,
        output_path=output_file,
        doc_id=doc_id,
        title=title
    )

