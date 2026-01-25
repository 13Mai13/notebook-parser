"""
Image optimization for LLM vision models.
Resize, compress, and optimize images to reduce tokens while maintaining quality.
"""

import base64
from pathlib import Path
from PIL import Image
import io


def optimize_for_llm(
    image_path: Path,
    max_size: int = 1568,  # Claude's recommended max dimension
    quality: int = 85,
    grayscale: bool = False
) -> bytes:
    """
    Optimize image for LLM vision processing.

    Args:
        image_path: Path to image file
        max_size: Maximum dimension (width or height) in pixels
        quality: JPEG quality (1-100, lower = smaller file)
        grayscale: Convert to grayscale to reduce tokens

    Returns:
        Optimized image as bytes
    """
    img = Image.open(image_path)

    # Convert to grayscale if requested (reduces tokens by ~3x)
    if grayscale:
        img = img.convert('L')
    else:
        img = img.convert('RGB')

    # Resize if image is too large
    width, height = img.size
    if width > max_size or height > max_size:
        # Calculate new size maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save to bytes with compression
    buffer = io.BytesIO()
    if grayscale:
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
    else:
        img.save(buffer, format='JPEG', quality=quality, optimize=True)

    return buffer.getvalue()


def image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode('utf-8')
