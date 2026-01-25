"""
CLI commands for notebook-parser.
"""

import typer
from pathlib import Path
from typing import Optional

from .ocr import extract_text_local, preprocess_image
from .template_engine import TemplateEngine
from .formatters import format_for_template
from .llm.claude_vision import extract_with_claude
from .llm.ollama_vision import extract_with_ollama

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
        help="Model: 'local' (TrOCR), 'claude' (API), or 'ollama' (local LLM)"
    ),
    preprocess: bool = typer.Option(
        True,
        "--preprocess/--no-preprocess",
        help="Apply image optimization (for TrOCR only)"
    ),
    optimize: bool = typer.Option(
        True,
        "--optimize/--no-optimize",
        help="Optimize image for LLM vision (resize, compress)"
    ),
    grayscale: bool = typer.Option(
        False,
        "--grayscale",
        help="Convert to grayscale to save tokens (~3x reduction)"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    ),
    ollama_model: str = typer.Option(
        "llama3.2-vision",
        "--ollama-model",
        help="Ollama model name"
    ),
    ollama_url: str = typer.Option(
        "http://localhost:11434",
        "--ollama-url",
        help="Ollama API endpoint"
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

        # Load template content for LLM context
        template_content = template_path.read_text()

        # Extract text based on model choice
        if model == "local":
            typer.echo("Using local TrOCR model...", err=True)
            extracted_text = extract_text_local(input_path, preprocess=preprocess)

        elif model == "claude":
            typer.echo("Using Claude 3.5 Sonnet vision API...", err=True)
            if optimize:
                typer.echo(f"  Optimizing image (grayscale: {grayscale})...", err=True)
            extracted_text = extract_with_claude(
                image_path=input_path,
                template_content=template_content,
                api_key=api_key,
                optimize=optimize,
                grayscale=grayscale
            )

        elif model == "ollama":
            typer.echo(f"Using Ollama vision model ({ollama_model})...", err=True)
            if optimize:
                typer.echo(f"  Optimizing image (grayscale: {grayscale})...", err=True)
            extracted_text = extract_with_ollama(
                image_path=input_path,
                template_content=template_content,
                model=ollama_model,
                ollama_url=ollama_url,
                optimize=optimize,
                grayscale=grayscale
            )

        else:
            typer.echo(f"Error: Unknown model '{model}'.", err=True)
            typer.echo("Valid options: 'local', 'claude', or 'ollama'", err=True)
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
