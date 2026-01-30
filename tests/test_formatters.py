"""
Tests for formatters module.
"""

import pytest
from pathlib import Path
from datetime import datetime
from src.notebook_parser.formatters import format_for_template


def test_format_for_template_basic(temp_test_image):
    """Test basic template formatting."""
    result = format_for_template("Test content", temp_test_image)

    assert result["title"] == temp_test_image.stem
    assert result["source"] == temp_test_image.name
    assert result["date"] == datetime.now().strftime("%Y-%m-%d")
    assert result["tags"] == "#notes #handwritten"
    assert result["key_idea"] == "Test content"
    assert result["key_points"] == "Test content"


def test_format_for_template_with_generated_tags(temp_test_image):
    """Test template formatting with generated tags."""
    generated_tags = "#python #machine-learning #ai"
    result = format_for_template("Test content", temp_test_image, generated_tags)

    assert result["tags"] == "#python #machine-learning #ai #notes #handwritten"


def test_format_for_template_with_custom_source(temp_test_image):
    """Test template formatting with custom source."""
    custom_source = "My Lecture Notes - Week 1"
    result = format_for_template("Test content", temp_test_image, custom_source=custom_source)

    assert result["source"] == custom_source


def test_format_for_template_with_tags_and_custom_source(temp_test_image):
    """Test template formatting with both generated tags and custom source."""
    generated_tags = "#python #programming"
    custom_source = "CS101 Lecture 3"
    result = format_for_template(
        "Test content",
        temp_test_image,
        generated_tags,
        custom_source
    )

    assert result["tags"] == "#python #programming #notes #handwritten"
    assert result["source"] == custom_source


def test_format_for_template_empty_text(temp_test_image):
    """Test template formatting with empty text."""
    result = format_for_template("", temp_test_image)

    assert result["key_idea"] == "*No text extracted*"
    assert result["key_points"] == "*No text extracted*"


def test_format_for_template_whitespace_only(temp_test_image):
    """Test template formatting with whitespace only."""
    result = format_for_template("   \n  \t  ", temp_test_image)

    assert result["key_idea"] == "*No text extracted*"
