"""
Tests for template engine module.
"""

import pytest
from pathlib import Path
from src.notebook_parser.template_engine import TemplateEngine


def test_template_engine_init_with_valid_template(tmp_path):
    """Test TemplateEngine initialization with valid template."""
    template_path = tmp_path / "test_template.md"
    template_path.write_text("**Title**: {{title}}\n**Content**: {{content}}")

    engine = TemplateEngine(template_path)

    assert engine.template_path == template_path
    assert "{{title}}" in engine.template_content


def test_template_engine_init_with_nonexistent_template(tmp_path):
    """Test TemplateEngine initialization with nonexistent template."""
    template_path = tmp_path / "nonexistent.md"

    with pytest.raises(FileNotFoundError):
        TemplateEngine(template_path)


def test_template_engine_render_basic(tmp_path):
    """Test basic template rendering."""
    template_path = tmp_path / "test_template.md"
    template_path.write_text("**Title**: {{title}}\n**Author**: {{author}}")

    engine = TemplateEngine(template_path)
    result = engine.render(title="Test Title", author="Test Author")

    assert "**Title**: Test Title" in result
    assert "**Author**: Test Author" in result
    assert "{{title}}" not in result
    assert "{{author}}" not in result


def test_template_engine_render_with_multiple_variables(tmp_path):
    """Test rendering with multiple variables."""
    template_path = tmp_path / "test_template.md"
    template_content = """
**Title**: {{title}}
**Date**: {{date}}
**Tags**: {{tags}}

## Content

{{content}}
"""
    template_path.write_text(template_content)

    engine = TemplateEngine(template_path)
    result = engine.render(
        title="My Note",
        date="2026-01-29",
        tags="#test #note",
        content="This is the content."
    )

    assert "**Title**: My Note" in result
    assert "**Date**: 2026-01-29" in result
    assert "**Tags**: #test #note" in result
    assert "This is the content." in result


def test_template_engine_render_with_unused_variables(tmp_path):
    """Test rendering ignores unused variables."""
    template_path = tmp_path / "test_template.md"
    template_path.write_text("**Title**: {{title}}")

    engine = TemplateEngine(template_path)
    result = engine.render(title="Test", unused="Ignored")

    assert "**Title**: Test" in result
    assert "Ignored" not in result


def test_template_engine_get_default_template():
    """Test getting default template path."""
    default_path = TemplateEngine.get_default_template()

    assert default_path.name == "bullet-points-template.md"
    assert "templates" in str(default_path)
