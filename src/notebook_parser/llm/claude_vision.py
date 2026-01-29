"""
Claude vision integration for high-quality handwriting recognition.
"""

import os
from pathlib import Path
from anthropic import Anthropic
from ..image_optimizer import optimize_for_llm, image_to_base64
from ..prompt_loader import PromptLoader


def extract_with_claude(
    image_path: Path,
    template_content: str,
    api_key: str = None,
    optimize: bool = True,
    grayscale: bool = False,
    prompt_name: str = None
) -> str:
    """
    Extract text from image using Claude vision API.

    Args:
        image_path: Path to notebook image
        template_content: Template to guide extraction
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        optimize: Whether to optimize image (resize, compress)
        grayscale: Convert to grayscale to save tokens
        prompt_name: Name of prompt to use (without .txt). If None, uses default

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

    # Load prompt
    if prompt_name:
        base_prompt = PromptLoader.load_prompt(prompt_name)
    else:
        base_prompt = PromptLoader.get_default_prompt()

    # Craft full prompt with template context
    prompt = f"""{base_prompt}

The extracted text will be used to fill this template:

{template_content}"""

    # Call Claude vision API
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 vision model
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


def extract_with_claude_tags(
    image_path: Path,
    template_content: str,
    api_key: str = None,
    optimize: bool = True,
    grayscale: bool = False
) -> tuple[str, str]:
    """
    Extract text from image using Claude vision API with two-step process:
    1. Generate tags for main topics
    2. Use tags as context to extract better bullet points

    Args:
        image_path: Path to notebook image
        template_content: Template to guide extraction
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        optimize: Whether to optimize image (resize, compress)
        grayscale: Convert to grayscale to save tokens

    Returns:
        Tuple of (extracted_text, generated_tags)
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

    # Step 1: Generate tags
    tags_prompt = PromptLoader.load_prompt("generate-tags")

    tags_message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=256,
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
                        "text": tags_prompt
                    }
                ],
            }
        ],
    )

    generated_tags = tags_message.content[0].text.strip()

    # Step 2: Extract bullet points with tags context
    bullet_points_prompt = PromptLoader.load_prompt("bullet-points-with-tags")
    # Insert the generated tags into the prompt
    bullet_points_prompt = bullet_points_prompt.replace("{tags}", generated_tags)

    # Add template context
    full_prompt = f"""{bullet_points_prompt}

The extracted text will be used to fill this template:

{template_content}"""

    # Call Claude vision API for bullet points
    content_message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
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
                        "text": full_prompt
                    }
                ],
            }
        ],
    )

    extracted_text = content_message.content[0].text.strip()

    return extracted_text, generated_tags
