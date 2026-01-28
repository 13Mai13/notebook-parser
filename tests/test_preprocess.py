"""
Tests for image preprocessing functionality.
"""

import pytest
from pathlib import Path
from PIL import Image
import numpy as np
from notebook_parser.ocr import preprocess_image


def test_preprocess_image_returns_pil_image(test_image_path):
    """Test that preprocessing returns a PIL Image."""
    result = preprocess_image(test_image_path)
    assert isinstance(result, Image.Image)


def test_preprocess_image_converts_to_rgb(test_image_path):
    """Test that preprocessing converts image to RGB mode."""
    result = preprocess_image(test_image_path)
    assert result.mode == "RGB"


def test_preprocess_image_with_temp_image(temp_test_image):
    """Test preprocessing with a temporary test image."""
    result = preprocess_image(temp_test_image)
    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


def test_preprocess_image_nonexistent_file(nonexistent_image):
    """Test that preprocessing raises error for non-existent file."""
    with pytest.raises(ValueError, match="Could not read image"):
        preprocess_image(nonexistent_image)


def test_preprocess_image_corrupted_file(corrupted_image):
    """Test that preprocessing raises error for corrupted file."""
    with pytest.raises(ValueError, match="Could not read image"):
        preprocess_image(corrupted_image)


def test_preprocess_image_output_dimensions(test_image_path):
    """Test that preprocessing maintains image dimensions."""
    original = Image.open(test_image_path)
    processed = preprocess_image(test_image_path)

    # Dimensions should be the same
    assert processed.size == original.size
