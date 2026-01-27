"""
Ollama integration for local LLM vision models.
Requires Ollama to be installed and running locally.
"""

import requests
from pathlib import Path
from ..image_optimizer import optimize_for_llm, image_to_base64
from ..prompt_loader import PromptLoader


def extract_with_ollama(
    image_path: Path,
    template_content: str,
    model: str = "llama3.2-vision", # lava:13b
    ollama_url: str = "http://localhost:11434",
    optimize: bool = True,
    grayscale: bool = False,
    prompt_name: str = None
) -> str:
    """
    Extract text from image using local Ollama vision model.

    Args:
        image_path: Path to notebook image
        template_content: Template to guide extraction
        model: Ollama model name (e.g., llama3.2-vision, llava)
        ollama_url: Ollama API endpoint
        optimize: Whether to optimize image
        grayscale: Convert to grayscale
        prompt_name: Name of prompt to use (without .txt). If None, uses default

    Returns:
        Extracted text
    """
    # Check if Ollama is running
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise ConnectionError(
            f"Cannot connect to Ollama at {ollama_url}\n"
            "Make sure Ollama is installed and running:\n"
            "  brew install ollama (macOS)\n"
            "  ollama serve\n"
            "  ollama pull llama3.2-vision"
        )

    # Optimize image if requested
    if optimize:
        image_bytes = optimize_for_llm(
            image_path,
            max_size=1024,  # Smaller for local models
            quality=75,
            grayscale=grayscale
        )
    else:
        image_bytes = image_path.read_bytes()

    # Convert to base64
    image_b64 = image_to_base64(image_bytes)

    # Load prompt
    if prompt_name:
        base_prompt = PromptLoader.load_prompt(prompt_name)
    else:
        base_prompt = PromptLoader.get_default_prompt()

    # Craft full prompt with template context
    prompt = f"""{base_prompt}

The extracted text will be used to fill this template:

{template_content}"""

    # Call Ollama API
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False
    }

    response = requests.post(
        f"{ollama_url}/api/generate",
        json=payload,
        timeout=600  # Vision models can be slow
    )
    response.raise_for_status()

    # Extract text from response
    result = response.json()
    extracted_text = result.get("response", "").strip()

    return extracted_text
