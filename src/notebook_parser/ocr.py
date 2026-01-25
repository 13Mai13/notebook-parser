"""
OCR functionality for extracting text from images.
"""

from pathlib import Path
from PIL import Image
import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


def preprocess_image(image_path: Path) -> Image.Image:
    """
    Enhance image quality for better OCR.

    Args:
        image_path: Path to the image file

    Returns:
        Preprocessed PIL Image in RGB mode

    Raises:
        ValueError: If image cannot be read
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Contrast enhancement using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced)

    return Image.fromarray(denoised).convert("RGB")


def extract_text_local(image_path: Path, preprocess: bool = True, model_name: str = "microsoft/trocr-large-handwritten") -> str:
    """
    Extract text from image using local TrOCR model.

    Args:
        image_path: Path to the image file
        preprocess: Whether to apply image preprocessing
        model_name: Name of the TrOCR model to use

    Returns:
        Extracted text from the image

    Raises:
        ValueError: If image cannot be processed
    """
    # Load model
    processor = TrOCRProcessor.from_pretrained(model_name)
    ocr_model = VisionEncoderDecoderModel.from_pretrained(model_name)

    # Load and optionally preprocess image
    if preprocess:
        image = preprocess_image(image_path)
    else:
        image = Image.open(image_path).convert("RGB")

    # Perform OCR
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = ocr_model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return text
