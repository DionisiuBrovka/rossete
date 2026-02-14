# Rossete

**Rossete** is an MCP server that automates creation of educational content (lectures, lab work, practical work) for universities. It uses template-based generation with Groq API for ultra-fast LLM inference.

## Features

- **Template-Based Generation** — Predefined structures for lectures, lab work, and practical work
- **Modular Block System** — 15+ specialized block types (title page, introduction, main content, key takeaways, references, etc.)
- **Multiple Export Formats** — DOCX, PDF (via pandoc), Markdown
- **Groq Integration** — Ultra-fast content generation (8-15 seconds per document)
- **MCP Protocol** — Works with Claude.ai and other MCP-compatible tools
- **Customizable** — Create custom templates and block types

## Quick Start

### Prerequisites

- Python 3.9+
- Groq API key (get from https://console.groq.com)
- pandoc (optional, for PDF export)

### Installation

```bash
git clone https://github.com/yourusername/rossete.git
cd rossete

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

`.env` file:
```env
GROQ_API_KEY=gsk_...
GROQ_MODEL=mixtral-8x7b-32768
ROSSETE_STORAGE_PATH=./generated_documents
ROSSETE_TEMPLATES_PATH=./templates
```

### Run

```bash
python -m rossete.server
```

## Usage

### With Claude.ai

Use Rossete as an MCP server to generate educational documents directly from Claude.

### Programmatic Usage

```python
from rossete.generator import DocumentGenerator

generator = DocumentGenerator(
    api_key="your-groq-api-key",
    model="mixtral-8x7b-32768"
)

result = generator.generate_document(
    template_id="lecture_standard_v1",
    topic="State Management in Flutter",
    level="intermediate",
    parameters={
        "duration_minutes": 90,
        "group": "PMU-21",
        "include_code_snippets": True,
        "language": "en"
    }
)

print(result["output_file"])  # Generated DOCX file
```

## Available Tools

**`generate_document`** — Generate document from template
- Parameters: `template_id`, `topic`, `level`, `parameters`

**`list_templates`** — List available templates

**`list_block_types`** — Show available block types

**`export_document`** — Export to different format (docx/pdf/markdown)

**`create_custom_template`** — Create custom template

## Block Types

| Block Type | Purpose |
|---|---|
| `title_page` | Cover page |
| `introduction` | Introduction with objectives |
| `main_content` | Main lecture content |
| `key_takeaways` | Summary of concepts |
| `references` | Bibliography |
| `practical_task` | Exercises |
| `questions` | Quiz questions |
| `learning_outcomes` | Competencies |
| `appendix` | Additional materials |

## Project Structure

```
rossete/
├── rossete/
│   ├── server.py              # MCP server
│   ├── config.py              # Configuration
│   ├── templates/             # Template definitions
│   ├── blocks/                # Block generators
│   ├── generator/             # Document generation logic
│   ├── export/                # Export formats (DOCX, PDF, Markdown)
│   ├── storage/               # File storage
│   ├── ai/                    # Groq API wrapper
│   └── tools/                 # MCP tools
├── tests/
├── requirements.txt
└── README.md
```

## Configuration

### Environment Variables

```env
GROQ_API_KEY=gsk_...              # Required
GROQ_MODEL=mixtral-8x7b-32768     # Optional
ROSSETE_STORAGE_PATH=./documents  # Optional
ROSSETE_TEMPLATES_PATH=./templates # Optional
ROSSETE_LOG_LEVEL=INFO            # Optional
```

## Performance

- **Generation Time**: 8-15 seconds per document
- **Max Document Size**: 10 blocks, 8,000 tokens per block
- **Concurrent Requests**: 5 (configurable)

## Limitations

- Supports Russian and English content
- DOCX is primary export format; PDF requires pandoc
- Max 10 blocks per document
- Groq context window: 32K tokens

## License

MIT License

## Support

- 📧 Email: support@rossete.dev
- 🐛 Issues: https://github.com/yourusername/rossete/issues
- 💬 Discussions: https://github.com/yourusername/rossete/discussions
