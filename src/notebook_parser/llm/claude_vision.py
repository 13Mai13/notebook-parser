"""
Claude vision integration for high-quality handwriting recognition.
"""

import os
from pathlib import Path
from anthropic import Anthropic
from ..image_optimizer import optimize_for_llm, image_to_base64


def extract_with_claude(
    image_path: Path,
    template_content: str,
    api_key: str = None,
    optimize: bool = True,
    grayscale: bool = False
) -> str:
    """
    Extract text from image using Claude vision API.

    Args:
        image_path: Path to notebook image
        template_content: Template to guide extraction
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        optimize: Whether to optimize image (resize, compress)
        grayscale: Convert to grayscale to save tokens

    Returns:
        Extracted and structured text matching template
    """
    # Get API key
    if api_key is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Set it via:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-xxx\n"
            "Or pass it with --api-key flag"
        )

    # Optimize image if requested
    if optimize:
        image_bytes = optimize_for_llm(
            image_path,
            max_size=1568,  # Claude's recommended size
            quality=85,
            grayscale=grayscale
        )
    else:
        image_bytes = image_path.read_bytes()

    # Convert to base64
    image_b64 = image_to_base64(image_bytes)

    # Create Claude client
    client = Anthropic(api_key=api_key)

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

    # Call Claude vision API
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Latest vision model
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    # Extract text from response
    extracted_text = message.content[0].text.strip()

    return extracted_text
