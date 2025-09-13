# backend/core/regulation_parser.py
import re
import json
from typing import Dict, Any


def parse_to_json(text: str, doc_id: str, title: str) -> Dict[str, Any]:
    """
    Parse regulation text into a structured JSON format.

    Expected input format (simplified):
        - "פרק 1 - כותרת" → main chapter
        - "1.1 כותרת סעיף" → subsection
        - "1.1.1 תוכן" → subsection content
        - Indented or unmarked lines → continuation of previous content

    Args:
        text: Raw regulation text (from PDF or Word).
        doc_id: Unique identifier for the document.
        title: Human-readable document title.

    Returns:
        A dictionary representing the structured regulation document.
    """
    lines = text.splitlines()
    sections = []
    current_section = None
    current_subsection = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Debug log – raw line content
        print(f"[{i:03}] 🔹 Line: {line}")

        # Detect main section (e.g., "פרק 1 - הגדרות כלליות")
        match_section = re.match(r"פרק\s?(\d+)\s*[-–]\s*(.+)", line)
        if match_section:
            print(f"📘 Found Section: {match_section.group(1)} - {match_section.group(2)}")
            if current_section:
                sections.append(current_section)

            current_section = {
                "id": match_section.group(1),
                "title": match_section.group(2).strip(),
                "subsections": []
            }
            current_subsection = None
            continue

        # Detect subsection title (e.g., "1.1 סעיף כלשהו")
        match_sub = re.match(r"(\d+\.\d+)\s*[\.\-]?\s*(.+)", line)
        if match_sub:
            print(f"📗 Found Subsection: {match_sub.group(1)} - {match_sub.group(2)}")
            current_subsection = {
                "id": match_sub.group(1),
                "title": match_sub.group(2).strip(),
                "content": ""
            }
            if current_section:
                current_section["subsections"].append(current_subsection)
            continue

        # Detect subsection content line (e.g., "1.1.1 תוכן כלשהו")
        match_content = re.match(r"(\d+\.\d+\.\d+)\s*[\.\-]?\s*(.+)", line)
        if match_content and current_subsection:
            print(f"📝 Found Content Line: {match_content.group(1)} → {match_content.group(2)}")
            current_subsection["content"] += match_content.group(2).strip() + " "
            continue

        # Append unmarked line to existing content block
        if current_subsection:
            print(f"➡️ Appending to content: {line}")
            current_subsection["content"] += line + " "

    # Finalize last open section
    if current_section:
        sections.append(current_section)

    print(f"\n✅ Finished parsing. Total sections: {len(sections)}\n")
    return {
        "docId": doc_id,
        "title": title,
        "language": "he",
        "sections": sections
    }


def convert_to_json(text: str, output_path: str, doc_id: str = "auto", title: str = "Regulation Document") -> None:
    """
    Parse regulation text and export it as a structured JSON file.

    Args:
        text: Raw regulation text.
        output_path: File path to write structured JSON.
        doc_id: Document identifier (optional).
        title: Document title (optional).
    """
    parsed = parse_to_json(text, doc_id=doc_id, title=title)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    print(f"✅ Regulation JSON saved to: {output_path}")
