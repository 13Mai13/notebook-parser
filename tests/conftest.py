"""
Pytest fixtures for notebook-parser tests.
"""

import sys
from pathlib import Path

# Add project root to Python path so we can import main
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from PIL import Image
import numpy as np


@pytest.fixture
def test_image_path():
    """Path to existing test image."""
    return Path("data/test_image_1.jpeg")


@pytest.fixture
def temp_test_image(tmp_path):
    """Create a temporary test image for testing."""
    img_path = tmp_path / "test.jpg"
    # Create a simple white image with some text-like patterns
    img = Image.new('RGB', (100, 100), color='white')
    img.save(img_path)
    return img_path


@pytest.fixture
def nonexistent_image(tmp_path):
    """Path to a non-existent image."""
    return tmp_path / "does_not_exist.jpg"


@pytest.fixture
def corrupted_image(tmp_path):
    """Create a corrupted image file."""
    img_path = tmp_path / "corrupted.jpg"
    img_path.write_text("This is not an image")
    return img_path
