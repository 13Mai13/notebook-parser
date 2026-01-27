"""
Prompt loading and management for different extraction tasks.
"""

from pathlib import Path


class PromptLoader:
    """Loads prompts from the prompts directory."""

    @staticmethod
    def get_prompts_dir() -> Path:
        """Get path to prompts directory."""
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        return project_root / "prompts"

    @staticmethod
    def load_prompt(prompt_name: str) -> str:
        """
        Load a prompt from the prompts directory.

        Args:
            prompt_name: Name of the prompt file (without .txt extension)

        Returns:
            Prompt content as string

        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        prompts_dir = PromptLoader.get_prompts_dir()
        prompt_path = prompts_dir / f"{prompt_name}.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        return prompt_path.read_text().strip()

    @staticmethod
    def get_default_prompt() -> str:
        """Get default extraction prompt."""
        return """You are an expert at reading handwritten notes from notebook images.

Extract ALL the text from this notebook page image. Be thorough and accurate.

Instructions:
1. Read all handwritten text carefully
2. Preserve the structure (headings, lists, paragraphs)
3. Return ONLY the extracted text content
4. Do not add explanations or meta-commentary
5. If text is unclear, make your best attempt

Return the extracted text:"""
