"""
Ollama integration for local LLM vision models.
Requires Ollama to be installed and running locally.
"""

import requests
from pathlib import Path
from ..image_optimizer import optimize_for_llm, image_to_base64


def extract_with_ollama(
    image_path: Path,
    template_content: str,
    model: str = "llama3.2-vision", # lava:13b
    ollama_url: str = "http://localhost:11434",
    optimize: bool = True,
    grayscale: bool = False
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

    # Craft prompt
    prompt = f"""You are an expert at reading handwritten notes from notebook images.

Extract ALL the text from this notebook page image. Be thorough and accurate.

The extracted text will be used to fill this template:

{template_content}

Instructions:
1. Read all handwritten text carefully
2. Preserve the structure (headings, lists, paragraphs)
3. Return ONLY the extracted text content for the "Key Idea" section
4. Do not add explanations or meta-commentary
5. If text is unclear, make your best attempt

Return the extracted text:"""

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
