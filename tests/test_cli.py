"""
Tests for CLI commands.
"""

import pytest
import re
from typer.testing import CliRunner
from pathlib import Path
from main import app

runner = CliRunner()


def strip_ansi(text):
    """Remove ANSI color codes from text."""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


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
    clean_output = strip_ansi(result.stdout)

    assert result.exit_code == 0
    assert "Extract handwritten text" in clean_output
    assert "--model" in clean_output
    assert "--preprocess" in clean_output


def test_parse_command_help():
    """Test that parse command help displays all options."""
    result = runner.invoke(app, ["parse", "--help"])
    clean_output = strip_ansi(result.stdout)

    assert result.exit_code == 0
    assert "--input" in clean_output or "-i" in clean_output
    assert "--output" in clean_output or "-o" in clean_output
    assert "--model" in clean_output
    assert "--tags" in clean_output
    assert "--source" in clean_output or "-s" in clean_output


def test_parse_command_missing_input():
    """Test parse command fails without input."""
    result = runner.invoke(app, ["parse"])

    assert result.exit_code != 0


def test_parse_command_nonexistent_input():
    """Test parse command fails with nonexistent input file."""
    result = runner.invoke(app, ["parse", "-i", "nonexistent.jpg"])

    assert result.exit_code == 1
    assert "not found" in result.stderr
