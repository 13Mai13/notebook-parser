"""
Tests for prompt loader module.
"""

import pytest
from pathlib import Path
from src.notebook_parser.prompt_loader import PromptLoader


def test_get_prompts_dir():
    """Test getting prompts directory."""
    prompts_dir = PromptLoader.get_prompts_dir()

    assert prompts_dir.exists()
    assert prompts_dir.name == "prompts"


def test_load_prompt_bullet_points():
    """Test loading bullet-points prompt."""
    prompt = PromptLoader.load_prompt("bullet-points")

    assert len(prompt) > 0
    assert "handwritten" in prompt.lower() or "notes" in prompt.lower()


def test_load_prompt_clean_bullet_points():
    """Test loading clean-bullet-points prompt."""
    prompt = PromptLoader.load_prompt("clean-bullet-points")

    assert len(prompt) > 0
    assert "handwritten" in prompt.lower() or "notes" in prompt.lower()


def test_load_prompt_generate_tags():
    """Test loading generate-tags prompt."""
    prompt = PromptLoader.load_prompt("generate-tags")

    assert len(prompt) > 0
    assert "tag" in prompt.lower()


def test_load_prompt_bullet_points_with_tags():
    """Test loading bullet-points-with-tags prompt."""
    prompt = PromptLoader.load_prompt("bullet-points-with-tags")

    assert len(prompt) > 0
    assert "{tags}" in prompt
    assert "context" in prompt.lower()


def test_load_prompt_nonexistent():
    """Test loading nonexistent prompt raises error."""
    with pytest.raises(FileNotFoundError):
        PromptLoader.load_prompt("nonexistent-prompt")


def test_get_default_prompt():
    """Test getting default prompt."""
    prompt = PromptLoader.get_default_prompt()

    assert len(prompt) > 0
    assert "handwritten" in prompt.lower()
    assert "extract" in prompt.lower()
