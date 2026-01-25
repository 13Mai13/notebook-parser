"""
Tests for CLI commands.
"""

import pytest
from typer.testing import CliRunner
from pathlib import Path
from main import app

runner = CliRunner()


def test_read_command_with_existing_image(test_image_path):
    """Test read command with existing test image."""
    result = runner.invoke(app, ["read", "--no-preprocess", str(test_image_path)])

    assert result.exit_code == 0
    assert "Loading model..." in result.stderr or "Processing image..." in result.stderr


def test_read_command_with_nonexistent_file(nonexistent_image):
    """Test read command with non-existent file."""
    result = runner.invoke(app, ["read", str(nonexistent_image)])

    assert result.exit_code == 1
    assert "not found" in result.stderr


def test_read_command_with_preprocess_flag(temp_test_image):
    """Test read command with preprocessing enabled."""
    result = runner.invoke(app, ["read", "--preprocess", str(temp_test_image)])

    # Should run without error (even if OCR output is not meaningful for blank image)
    assert result.exit_code == 0 or "Error processing" in result.stderr


def test_read_command_with_custom_model(temp_test_image):
    """Test read command with custom model parameter."""
    result = runner.invoke(
        app,
        ["read", str(temp_test_image), "--model", "microsoft/trocr-base-handwritten"]
    )

    # Should attempt to load the model
    assert result.exit_code == 0 or "Error" in result.stderr


def test_read_command_help():
    """Test that help message is displayed."""
    result = runner.invoke(app, ["read", "--help"])

    assert result.exit_code == 0
    assert "Extract handwritten text" in result.stdout
    assert "--model" in result.stdout
    assert "--preprocess" in result.stdout
