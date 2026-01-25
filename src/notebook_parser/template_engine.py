"""
Template loading and rendering for markdown notes.
"""

from pathlib import Path
from datetime import datetime
import re


class TemplateEngine:
    """Simple template engine for markdown note generation."""

    def __init__(self, template_path: Path):
        """
        Initialize template engine with a template file.

        Args:
            template_path: Path to the markdown template file

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        self.template_path = template_path
        self.template_content = template_path.read_text()

    def render(self, **kwargs) -> str:
        """
        Render template with provided values.

        Args:
            **kwargs: Key-value pairs to replace in template

        Returns:
            Rendered template as string
        """
        result = self.template_content

        # Replace all {{variable}} placeholders
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))

        return result

    @staticmethod
    def get_default_template() -> Path:
        """Get path to default note template."""
        # Get project root (notebook-parser directory)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        return project_root / "templates" / "note-template.md"
