"""
CLI tool for extracting text from handwritten images using TrOCR.
"""

import typer
from pathlib import Path
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import cv2
import numpy as np

app = typer.Typer(help="Extract handwritten text from images using TrOCR")


def preprocess_image(image_path: Path) -> Image.Image:
    """Enhance image quality for better OCR."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(enhanced)
    
    return Image.fromarray(denoised).convert("RGB")


@app.command()
def read(
    image_path: Path = typer.Argument(..., help="Path to handwritten image"),
    model: str = typer.Option(
        "microsoft/trocr-large-handwritten",
        "--model",
        "-m",
        help="TrOCR model to use"
    ),
    preprocess: bool = typer.Option(
        True,
        "--preprocess/--no-preprocess",
        help="Apply image preprocessing"
    ),
) -> None:
    """Extract handwritten text from image (100% local)."""
    if not image_path.exists():
        typer.echo(f"Error: File '{image_path}' not found.", err=True)
        raise typer.Exit(1)
    
    try:
        # Show loading message on stderr so it doesn't interfere with output
        typer.echo("Loading model...", err=True)
        
        processor = TrOCRProcessor.from_pretrained(model)
        ocr_model = VisionEncoderDecoderModel.from_pretrained(model)
        
        typer.echo("Processing image...", err=True)
        
        # Load and preprocess image
        if preprocess:
            image = preprocess_image(image_path)
        else:
            image = Image.open(image_path).convert("RGB")
        
        # Perform OCR
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = ocr_model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        typer.echo("\n--- Extracted Text ---", err=True)
        typer.echo(text)
        
    except Exception as e:
        typer.echo(f"Error processing image: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()