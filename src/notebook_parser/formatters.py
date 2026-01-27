"""
Formatters for converting OCR text to structured markdown.
"""

from datetime import datetime
from pathlib import Path


def format_for_template(extracted_text: str, source_image: Path) -> dict:
    """
    Format extracted OCR text into template variables.

    Args:
        extracted_text: Raw text from OCR
        source_image: Path to source image file

    Returns:
        Dictionary of template variables
    """
    # Use image filename (without extension) as title
    title = source_image.stem

    # Use current date
    date = datetime.now().strftime("%Y-%m-%d")

    # Source is the image filename
    source = source_image.name

    # Default tags
    tags = "#notes #handwritten"

    # Key idea is the extracted text (trimmed)
    key_idea = extracted_text.strip() if extracted_text.strip() else "*No text extracted*"

    return {
        "title": title,
        "source": source,
        "date": date,
        "tags": tags,
        "key_idea": key_idea,
        "key_points": key_idea,  # Alias for bullet-points template
    }
