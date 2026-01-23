"""
CLI tool for extracting text from images using OCR.
"""

import typer
from pathlib import Path
import easyocr

app = typer.Typer(help="Extract text from images using OCR")


@app.command()
def read(
    image_path: Path = typer.Argument(..., help="Path to the image file"),
    lang: str = typer.Option("en", "--lang", "-l", help="Language code for OCR (e.g., 'en', 'de', 'fr')"),
) -> None:
    """Read and extract text from an image file."""
    if not image_path.exists():
        typer.echo(f"Error: File '{image_path}' not found.", err=True)
        raise typer.Exit(code=1)

    try:
        reader = easyocr.Reader([lang], verbose=False)
        results = reader.readtext(str(image_path))
        text = "\n".join([result[1] for result in results])
        typer.echo(text)
    except Exception as e:
        typer.echo(f"Error processing image: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
