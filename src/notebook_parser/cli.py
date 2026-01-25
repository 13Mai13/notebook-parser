"""
CLI commands for notebook-parser.
"""

import typer
from pathlib import Path
from typing import Optional

from .ocr import extract_text_local, preprocess_image
from .template_engine import TemplateEngine
from .formatters import format_for_template

app = typer.Typer(help="Parse physical notebook images to markdown notes")


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
        typer.echo("Loading model...", err=True)
        text = extract_text_local(image_path, preprocess=preprocess, model_name=model)

        typer.echo("\n--- Extracted Text ---", err=True)
        typer.echo(text)

    except Exception as e:
        typer.echo(f"Error processing image: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def parse(
    input_path: Path = typer.Option(..., "--input", "-i", help="Input image file"),
    output: Path = typer.Option(..., "--output", "-o", help="Output markdown file"),
    template: Optional[Path] = typer.Option(
        None,
        "--template",
        "-t",
        help="Custom template file (default: templates/note-template.md)"
    ),
    model: str = typer.Option(
        "local",
        "--model",
        help="Model to use: 'local' (TrOCR) or 'claude' (API)"
    ),
    preprocess: bool = typer.Option(
        True,
        "--preprocess/--no-preprocess",
        help="Apply image optimization"
    ),
) -> None:
    """
    Parse notebook image to markdown note.

    Example:
        notebook-parser parse -i notebook.jpg -o note.md
    """
    # Validate input
    if not input_path.exists():
        typer.echo(f"Error: Input file '{input_path}' not found.", err=True)
        raise typer.Exit(1)

    # Load template
    if template is None:
        template_path = TemplateEngine.get_default_template()
    else:
        template_path = template

    if not template_path.exists():
        typer.echo(f"Error: Template '{template_path}' not found.", err=True)
        raise typer.Exit(1)

    try:
        typer.echo(f"Processing {input_path.name}...", err=True)

        # Extract text based on model choice
        if model == "local":
            typer.echo("Using local TrOCR model...", err=True)
            extracted_text = extract_text_local(input_path, preprocess=preprocess)
        elif model == "claude":
            typer.echo("Error: Claude API integration not yet implemented.", err=True)
            typer.echo("Use --model local for now.", err=True)
            raise typer.Exit(1)
        else:
            typer.echo(f"Error: Unknown model '{model}'. Use 'local' or 'claude'.", err=True)
            raise typer.Exit(1)

        # Format into template variables
        template_vars = format_for_template(extracted_text, input_path)

        # Render template
        engine = TemplateEngine(template_path)
        markdown_content = engine.render(**template_vars)

        # Write output
        output.write_text(markdown_content)

        typer.echo(f"\n✓ Successfully created: {output}", err=True)
        typer.echo(f"  Title: {template_vars['title']}", err=True)
        typer.echo(f"  Source: {template_vars['source']}", err=True)

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
