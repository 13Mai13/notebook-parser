# notebook-parser

Transform physical notebook images into structured markdown notes using Claude's vision API. Perfect for building a second brain workflow with Obsidian or other note-taking systems.

## Features

- **Intelligent tag generation**: Automatically generates contextual Obsidian-compatible tags from your handwritten notes
- **Two-stage extraction**: First generates tags, then uses them as context for more accurate content extraction
- **Image optimization**: Automatic resizing, compression, and optional grayscale conversion to reduce API costs
- **Template-based output**: Customizable markdown templates designed for second brain workflows
- **Custom prompts**: Different extraction strategies for various note types (bullet points, detailed notes, etc.)
- **Custom source metadata**: Specify your own source description for better note organization
- **Test-driven development**: Comprehensive pytest suite with 73% test coverage

## Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation

1. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd notebook-parser
   uv sync
   ```

3. **Configure your API key**:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your Anthropic API key
   # ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

## Quick Start

### Basic Usage

Parse a notebook image with intelligent tag generation:

```bash
# With tag-based extraction (recommended)
uv run notebook-parser parse -i notebook.jpg --model claude --tags
```

This will:
1. Generate contextual Obsidian-compatible tags from your notes
2. Use those tags to extract content more accurately
3. Create a markdown file at `results/notebook.md`

### Common Usage Patterns

```bash
# Specify custom output location
uv run notebook-parser parse -i notebook.jpg -o notes/lecture-01.md --model claude --tags

# Add custom source metadata for better organization
uv run notebook-parser parse -i notebook.jpg --model claude --tags --source "CS101 Lecture 3"

# Save tokens with grayscale conversion (~3x reduction)
uv run notebook-parser parse -i notebook.jpg --model claude --tags --grayscale

# Use without tag generation (faster, but less accurate)
uv run notebook-parser parse -i notebook.jpg --model claude
```

### Quick Text Extraction

For quick OCR without template formatting:

```bash
notebook-parser read notebook.jpg
```

**Note**: All commands use Claude Sonnet 4.5, the latest vision model as of January 2026. If no output path is specified, files are saved to the `results/` directory with the same name as the input file.

## Usage

### Parse Command

```bash
notebook-parser parse [OPTIONS]
```

**Required:**
- `-i, --input PATH`: Input image file

**Output:**
- `-o, --output PATH`: Output markdown file (default: `results/<input-name>.md`)

**Model:**
- `--model claude`: Use Claude Sonnet 4.5 vision API (required)
- `--api-key TEXT`: Anthropic API key (or set `ANTHROPIC_API_KEY` environment variable)

**Tag Generation (Recommended):**
- `--tags`: Enable two-stage extraction with tag generation for better accuracy

**Image Optimization:**
- `--optimize/--no-optimize`: Optimize image for vision API (default: enabled)
- `--grayscale`: Convert to grayscale to reduce token usage (~3x savings)

**Template & Prompts:**
- `-t, --template PATH`: Custom template file (default: `templates/bullet-points-template.md`)
- `-p, --prompt TEXT`: Prompt name without .txt extension (e.g., 'bullet-points', 'clean-bullet-points')

**Metadata:**
- `-s, --source TEXT`: Custom source description for better note organization (default: image filename)

### Read Command

Quick text extraction without template formatting:

```bash
notebook-parser read <image-file>
```

Uses local TrOCR model for basic OCR. Useful for quick text extraction without the full template processing.

## Examples

### Tag-based extraction (recommended)
```bash
uv run notebook-parser parse -i lecture-notes.jpg --model claude --tags
# Generates contextual tags first, then uses them for improved extraction
# Output: results/lecture-notes.md
```

### Build your second brain workflow
```bash
# Organize notes with custom source metadata
uv run notebook-parser parse -i page1.jpg --model claude --tags --source "Design Patterns Book - Chapter 3"

# Save to your Obsidian vault
uv run notebook-parser parse -i page1.jpg -o ~/Documents/Obsidian/Inbox/page1.md --model claude --tags

# Batch process multiple pages with custom naming
uv run notebook-parser parse -i lecture-day1.jpg --model claude --tags --source "Python Course - Day 1"
uv run notebook-parser parse -i lecture-day2.jpg --model claude --tags --source "Python Course - Day 2"
```

### Cost optimization
```bash
# Use grayscale to reduce token usage (~3x savings)
uv run notebook-parser parse -i notes.jpg --model claude --tags --grayscale

# Disable optimization to use original image quality (higher cost but better recognition)
uv run notebook-parser parse -i notes.jpg --model claude --tags --no-optimize
```

### Custom templates and prompts
```bash
# Use alternative template for different note structure
uv run notebook-parser parse -i notes.jpg --model claude --template templates/note-template.md

# Use custom extraction prompt
uv run notebook-parser parse -i notes.jpg --model claude --prompt clean-bullet-points
```

## Output Format

All generated notes are Obsidian-compatible markdown files optimized for second brain workflows.

### Default Template (Bullet Points)

The default template (`templates/bullet-points-template.md`) creates clean, organized notes:

```markdown
**Title**: Deep Learning Basics
**Source**: CS230 Lecture 1
**Date**: 2026-01-15
**Tags**: #deep-learning #neural-networks #notes #handwritten
**Status**: #RawNotes

## Key Points

- Neural networks consist of interconnected layers of neurons
- Activation functions introduce non-linearity (ReLU, sigmoid, tanh)
- Backpropagation is used to train the network by adjusting weights
- ...
```

**When using `--tags`:**
- AI generates contextual Obsidian-compatible tags (e.g., `#machine-learning`, `#python`)
- Tags are added alongside default tags (`#notes`, `#handwritten`)
- Improves note discoverability in your second brain system

### Alternative: Note Template

The note template (`templates/note-template.md`) provides space for reflection:

```markdown
**Title**: <extracted-title>
**Source**: <custom-source-or-filename>
**Date**: <current-date>
**Tags**: #notes #handwritten
**Status**: #RawNotes

## Key Idea

<extracted-content>

## Why It Matters

*To be filled manually*

## How I Might Use It

*To be filled manually*
```

Use with: `--template templates/note-template.md`

This template follows the Zettelkasten/second brain principle of processing information in multiple passes.

## Custom Prompts

Prompts are stored in the `prompts/` directory and guide how the AI extracts text from your images.

### Available Prompts

- **bullet-points** (`prompts/bullet-points.txt`): Basic extraction as bullet points, handling arrows and schemas
- **clean-bullet-points** (`prompts/clean-bullet-points.txt`): Advanced extraction with interpretation, error correction, and cleaner output (recommended)
- **generate-tags** (`prompts/generate-tags.txt`): Generates Obsidian-compatible tags for the note (used automatically with `--tags`)
- **bullet-points-with-tags** (`prompts/bullet-points-with-tags.txt`): Context-aware extraction using generated tags (used automatically with `--tags`)

**Note**: When using the `--tags` flag, the system automatically uses `generate-tags` and `bullet-points-with-tags` prompts in a two-step process for improved accuracy.

### Creating Custom Prompts

1. Create a new `.txt` file in the `prompts/` directory
2. Write your extraction instructions
3. Use it with: `--prompt your-prompt-name` (without .txt extension)

Example prompt structure:
```
These are handwritten notes, they may contain arrows and schemas too. Transform it to bullet points.
```

## Image Optimization

By default, images are optimized for Claude's vision API to balance quality and cost:

- **Automatic resizing**: Images resized to max 1568px (optimal for Claude)
- **Compression**: JPEG quality set to 85 (balances quality and file size)
- **Grayscale option**: Use `--grayscale` to reduce token usage by ~3x

**When to disable optimization** (`--no-optimize`):
- Faint handwriting that needs maximum contrast
- Complex diagrams with fine details
- Color-coded notes where grayscale loses important information

## Development

### Running Tests

```bash
uv run pytest -v
```

### Test Coverage

```bash
uv run pytest --cov=src
```

## Second Brain Integration

This tool is designed to fit seamlessly into your second brain workflow:

### Obsidian Integration

1. **Direct vault integration**: Point output to your Obsidian vault's inbox
   ```bash
   uv run notebook-parser parse -i notes.jpg -o ~/Obsidian/Inbox/notes.md --model claude --tags
   ```

2. **Tag-based organization**: Generated tags are Obsidian-compatible (e.g., `#machine-learning`, `#python`)

3. **Metadata fields**: Notes include structured metadata (Title, Source, Date, Status) for easy filtering

4. **Status workflow**: Default status is `#RawNotes` - update to `#Processed` after reviewing

### Recommended Workflow

1. **Capture**: Take photos of your handwritten notes
2. **Process**: Run notebook-parser with `--tags` to generate structured markdown
3. **Review**: Read the generated note and verify accuracy
4. **Enhance**: Add your own insights, connections, and reflections
5. **Link**: Create connections to other notes in your system
6. **Tag update**: Change status from `#RawNotes` to `#Processed`

## Troubleshooting

### API Key Issues

**Error: "Authentication error" or "Invalid API key"**
- Verify your API key is set correctly in `.env` or as an environment variable
- Check the key has proper permissions at [console.anthropic.com](https://console.anthropic.com/)
- Ensure there are no extra spaces or newlines in the `.env` file

**Error: "API key not found"**
```bash
# Check if the API key is loaded
cat .env

# Or set it directly for testing
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
uv run notebook-parser parse -i test.jpg --model claude
```

### Extraction Quality Issues

**Poor handwriting recognition:**
- Ensure good lighting and focus when photographing notes
- Try disabling optimization: `--no-optimize`
- Avoid using `--grayscale` if handwriting is faint

**Missing or incorrect content:**
- Use `--tags` flag for better context-aware extraction
- Try a different prompt: `--prompt clean-bullet-points`
- Check that the image is clear and readable

**Wrong language or encoding:**
- Verify the image doesn't have extreme rotation or distortion
- Ensure text is horizontal and properly framed

### File and Path Issues

**Error: "File not found"**
- Use absolute paths or ensure you're in the correct directory
- Check file permissions

**Error: "Template not found"**
- Verify template path is correct
- Use default template by omitting `--template` flag

## Future Improvements

- **Local model support**: Ollama integration for fully private, offline processing
- **Batch processing**: Process multiple images in one command
- **Interactive mode**: Review and edit extractions before saving
- **Custom model selection**: Support for different Claude models
- **Benchmark suite**: Compare extraction accuracy across prompts and settings
- **Higher test coverage**: Expand pytest suite beyond current 73%