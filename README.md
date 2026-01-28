# notebook-parser

Transform physical notebook images into structured markdown notes using AI vision models.

## Features

- **Multiple model support**: Choose between local TrOCR, Claude API, or local Ollama vision models
- **Image optimization**: Automatic resizing, compression, and optional grayscale conversion to reduce token usage
- **Template-based output**: Customizable markdown templates for consistent note formatting
- **Custom prompts**: Use different prompts for different extraction tasks (e.g., bullet points, detailed notes)
- **Test-driven development**: Comprehensive pytest suite with 73% test coverage

## Installation

```bash
git clone <repository-url>
cd notebook-parser
uv sync
```

## Quick Start

### Using Claude API (Best Quality)

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Set your API key (choose one method):

   **Option A: Using .env file (recommended)**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your key
   # ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

   **Option B: Export environment variable**
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

3. Parse a notebook image:
```bash
# With custom output path
uv run notebook-parser parse -i notebook.jpg -o note.md --model claude

# Or use default (outputs to results/notebook.md)
uv run notebook-parser parse -i notebook.jpg --model claude
```

**Note**: Uses Claude Sonnet 4.5 (latest model as of January 2026). If no output path is specified, files are saved to `results/` directory with the same name as the input file.

### Using Ollama (Local, Private)

1. Install and start Ollama:
```bash
brew install ollama  # macOS
ollama serve
ollama pull llama3.2-vision
```

2. Parse a notebook image:
```bash
uv run notebook-parser parse -i notebook.jpg -o note.md --model ollama
```

### Using TrOCR (Legacy, Lower Quality)

```bash
uv run notebook-parser parse -i notebook.jpg -o note.md --model local
```

## Usage

### Parse Command

```bash
notebook-parser parse [OPTIONS]
```

**Required Options:**
- `-i, --input PATH`: Input image file

**Optional Output:**
- `-o, --output PATH`: Output markdown file (default: `results/<input-name>.md`)

**Model Options:**
- `--model [local|claude|ollama]`: Model to use (default: local)
  - `local`: TrOCR (basic OCR, lower quality)
  - `claude`: Claude Sonnet 4.5 vision API (best quality, requires API key)
  - `ollama`: Local Ollama vision model (good quality, fully private)

**Image Optimization Options:**
- `--optimize/--no-optimize`: Optimize image for LLM vision (default: True)
- `--grayscale`: Convert to grayscale to save tokens (~3x reduction)

**Claude-specific Options:**
- `--api-key TEXT`: Anthropic API key (or set ANTHROPIC_API_KEY env var)

**Ollama-specific Options:**
- `--ollama-model TEXT`: Ollama model name (default: llama3.2-vision)
- `--ollama-url TEXT`: Ollama API endpoint (default: http://localhost:11434)

**Template Options:**
- `-t, --template PATH`: Custom template file (default: templates/note-template.md)
- `-p, --prompt TEXT`: Prompt name to use (without .txt extension, e.g., 'bullet-points')

### Read Command (Quick OCR)

Extract text quickly without template formatting:

```bash
notebook-parser read notebook.jpg
```

## Examples

### Basic usage with Claude (auto-output to results/)
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-xxx
uv run notebook-parser parse -i page1.jpg --model claude
# Outputs to: results/page1.md
```

### Specify custom output path
```bash
uv run notebook-parser parse -i page1.jpg -o my-notes/page1.md --model claude
```

### Grayscale optimization to save tokens
```bash
uv run notebook-parser parse -i page1.jpg --model claude --grayscale
```

### Using local Ollama with custom model
```bash
uv run notebook-parser parse -i page1.jpg --model ollama --ollama-model llava
```

### Custom template
```bash
uv run notebook-parser parse -i page1.jpg --template my-template.md
```

### Extract bullet points (basic)
```bash
uv run notebook-parser parse -i page1.jpg --model claude --template templates/bullet-points-template.md --prompt bullet-points
```

### Extract bullet points (clean, recommended)
```bash
uv run notebook-parser parse -i page1.jpg --model claude --template templates/bullet-points-template.md --prompt clean-bullet-points
```

### Disable optimization (use original image)
```bash
uv run notebook-parser parse -i page1.jpg --model claude --no-optimize
```

## Output Format

### Default Template

The default template (`templates/note-template.md`) creates notes with this structure:

```markdown
**Title**: <extracted-title>
**Source**: <image-filename>
**Date**: <current-date>
**Tags**: #notes #handwritten
**Status**: Raw Note

## Key Idea

<extracted-content>

## Why It Matters

*To be filled*

## How I Might Use It

*To be filled*
```

### Bullet Points Template

The bullet points template (`templates/bullet-points-template.md`) creates simpler notes:

```markdown
**Title**: <extracted-title>
**Source**: <image-filename>
**Date**: <current-date>
**Tags**: #notes #handwritten
**Status**: Bullet Points

## Key Points

<extracted-bullet-points>
```

## Custom Prompts

Prompts are stored in the `prompts/` directory and guide how the AI extracts text from your images.

### Available Prompts

- **bullet-points** (`prompts/bullet-points.txt`): Basic extraction as bullet points, handling arrows and schemas
- **clean-bullet-points** (`prompts/clean-bullet-points.txt`): Advanced extraction with interpretation, error correction, and cleaner output (recommended)

### Creating Custom Prompts

1. Create a new `.txt` file in the `prompts/` directory
2. Write your extraction instructions
3. Use it with: `--prompt your-prompt-name` (without .txt extension)

Example prompt structure:
```
These are handwritten notes, they may contain arrows and schemas too. Transform it to bullet points.
```

## Image Optimization

When using Claude or Ollama models with `--optimize` enabled (default):

- **Claude**: Images resized to max 1568px, JPEG quality 85
- **Ollama**: Images resized to max 1024px, JPEG quality 75
- **Grayscale**: Optional flag reduces token usage by ~3x

## Development

### Running Tests

```bash
uv run pytest -v
```

### Test Coverage

```bash
uv run pytest --cov=src
```

## Model Comparison

| Model | Quality | Speed | Cost | Privacy |
|-------|---------|-------|------|---------|
| TrOCR (local) | Low | Fast | Free | Full |
| Ollama (local) | Good | Medium | Free | Full |
| Claude API | Best | Fast | $3/1K images* | API calls |

*Estimated cost based on average image size and token usage

## Troubleshooting

### Claude API errors
- Ensure `ANTHROPIC_API_KEY` is set correctly
- Check API key has proper permissions at console.anthropic.com

### Ollama connection errors
- Verify Ollama is running: `ollama list`
- Check Ollama URL: `curl http://localhost:11434/api/tags`
- Pull the model: `ollama pull llama3.2-vision`

### Poor OCR results with TrOCR
- Use `--model claude` or `--model ollama` for better handwriting recognition
- TrOCR works best with typed text, not handwritten notes
