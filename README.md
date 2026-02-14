# Rossete — Educational Content Generation MCP Server

**Rossete** is a Model Context Protocol (MCP) server that automates the creation of educational content (lectures, laboratory work, practical work) for university and college instructors. It uses **template-based architecture** with modular block generators to ensure consistent formatting and pedagogical quality. Powered by **Groq API** for ultra-fast content generation.

## Overview

### Problem Solved
Creating educational materials with proper formatting and pedagogical structure is time-consuming. Each institution has specific requirements for document structure, formatting, and content quality. Rossete automates this while maintaining flexibility through customizable templates.

### Key Features
- 🎯 **Template-Based Generation** — Define document structure once, generate infinite variations
- 🧩 **Modular Block System** — Each block type has its own specialized generation algorithm
- 📚 **Built-in Templates** — Standard templates for lectures, lab work, and practical work
- 🔧 **Customizable** — Create custom templates and block types
- 📄 **Multiple Export Formats** — Generate DOCX, PDF, and Markdown
- ⚡ **Groq Integration** — Ultra-fast LLM inference with Groq API for quick content generation
- 🔌 **MCP Protocol** — Integrates with Claude.ai and other MCP-compatible tools

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Rossete MCP Server (fastMCP)            │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │   Template Registry                      │   │
│  │   • lecture_standard_v1                  │   │
│  │   • lab_work_standard_v1                 │   │
│  │   • practical_work_standard_v1           │   │
│  │   • Custom user templates                │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                               │
│  ┌──────────────────────────────────────────┐   │
│  │   Block Type Registry                    │   │
│  │   • title_page                           │   │
│  │   • introduction                         │   │
│  │   • main_content                         │   │
│  │   • key_takeaways                        │   │
│  │   • references                           │   │
│  │   • practical_task                       │   │
│  │   • [+ 10 more types]                    │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                               │
│  ┌──────────────────────────────────────────┐   │
│  │   Groq Integration Layer                 │   │
│  │   • GroqClient wrapper                   │   │
│  │   • Model: mixtral-8x7b-32768            │   │
│  │   • Ultra-fast inference                 │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                               │
│  ┌──────────────────────────────────────────┐   │
│  │   Block Generation Engines               │   │
│  │   • IntroductionBlockGenerator           │   │
│  │   • MainContentBlockGenerator            │   │
│  │   • KeyTakeawaysBlockGenerator           │   │
│  │   • ReferencesBlockGenerator             │   │
│  │   • [Custom generators]                  │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                               │
│  ┌──────────────────────────────────────────┐   │
│  │   Document Assembler & Formatter         │   │
│  │   • Collects blocks in order             │   │
│  │   • Applies styling (fonts, spacing)     │   │
│  │   • Generates TOC, page numbers          │   │
│  └──────────────────────────────────────────┘   │
│                  ↓                               │
│  ┌──────────────────────────────────────────┐   │
│  │   Export Module                          │   │
│  │   • DOCX (python-docx)                   │   │
│  │   • PDF (pandoc)                         │   │
│  │   • Markdown                             │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.9+
- pip
- Groq API key (get from https://console.groq.com)
- pandoc (for PDF export, optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rossete.git
cd rossete

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key
```

### Configuration

Create `.env` file:
```env
GROQ_API_KEY=gsk_...
GROQ_MODEL=mixtral-8x7b-32768
ROSSETE_STORAGE_PATH=./generated_documents
ROSSETE_TEMPLATES_PATH=./templates
ROSSETE_LOG_LEVEL=INFO
```

### Run the Server

```bash
python -m rossete.server
```

The server will start on `stdio` mode (suitable for MCP protocol).

## Usage

### From Claude.ai

Once connected as an MCP server in Claude.ai, you can use Rossete like this:

```
User: "Rossete, generate a lecture on State Management in Flutter. 
Use the standard lecture template, intermediate level, 90 minutes, 
for the PMU-21 group. Include code snippets."

Rossete:
1. Loads lecture_standard_v1 template
2. Generates each block via Groq API (⚡ ultra-fast):
   - TitlePage: Formats metadata
   - Introduction: Groq-generated intro with objectives
   - MainContent: Detailed explanation with code examples
   - KeyTakeaways: Summary of key concepts
   - References: GOST-formatted bibliography
3. Assembles document with proper formatting
4. Exports to DOCX format
5. Returns: lecture_state_management_flutter.docx
```

### Programmatic Usage

```python
from rossete.generator import DocumentGenerator

# Initialize generator with Groq
generator = DocumentGenerator(
    api_key="your-groq-api-key",
    model="mixtral-8x7b-32768"
)

# Generate a lecture
result = generator.generate_document(
    template_id="lecture_standard_v1",
    topic="State Management в Flutter",
    level="intermediate",
    parameters={
        "duration_minutes": 90,
        "group": "ПМС-21",
        "year": 2025,
        "include_code_snippets": True,
        "language": "ru"
    }
)

print(result["output_file"])  # lecture_state_management_flutter.docx
print(result["generation_time"])  # ~8-15 seconds with Groq
```

## Project Structure

```
rossete/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── rossete/
│   ├── __init__.py
│   ├── server.py                 # fastMCP server entry point
│   ├── config.py                 # Configuration management
│   │
│   ├── templates/                # Template definitions
│   │   ├── __init__.py
│   │   ├── registry.py           # Template registry and loader
│   │   ├── lecture/
│   │   │   └── lecture_standard_v1.json
│   │   ├── lab_work/
│   │   │   └── lab_work_standard_v1.json
│   │   └── practical_work/
│   │       └── practical_work_standard_v1.json
│   │
│   ├── blocks/                   # Block type definitions and generators
│   │   ├── __init__.py
│   │   ├── types.py              # BlockType enum and models
│   │   ├── base.py               # BaseBlockGenerator abstract class
│   │   │
│   │   ├── generators/           # Concrete block generators
│   │   │   ├── __init__.py
│   │   │   ├── title_page.py
│   │   │   ├── introduction.py
│   │   │   ├── main_content.py
│   │   │   ├── key_takeaways.py
│   │   │   ├── references.py
│   │   │   ├── appendix.py
│   │   │   ├── practical_task.py
│   │   │   ├── questions.py
│   │   │   ├── learning_outcomes.py
│   │   │   └── custom.py
│   │   │
│   │   └── registry.py           # Block generator registry
│   │
│   ├── generator/                # Main generation logic
│   │   ├── __init__.py
│   │   ├── document_generator.py # Main orchestrator
│   │   ├── block_engine.py       # Block generation engine
│   │   └── assembler.py          # Document assembly and formatting
│   │
│   ├── export/                   # Export formats
│   │   ├── __init__.py
│   │   ├── base.py               # BaseExporter
│   │   ├── docx_exporter.py      # DOCX export
│   │   ├── pdf_exporter.py       # PDF export (via pandoc)
│   │   └── markdown_exporter.py  # Markdown export
│   │
│   ├── storage/                  # Document storage and retrieval
│   │   ├── __init__.py
│   │   ├── file_manager.py
│   │   └── metadata_store.py
│   │
│   ├── ai/                       # Groq API integration
│   │   ├── __init__.py
│   │   └── groq_client.py        # Groq API wrapper
│   │
│   └── tools/                    # MCP Tools definitions
│       ├── __init__.py
│       ├── document_tools.py     # generate_document, etc.
│       ├── template_tools.py     # list_templates, etc.
│       ├── block_tools.py        # list_block_types, etc.
│       └── export_tools.py       # export_document, etc.
│
├── tests/
│   ├── __init__.py
│   ├── test_templates.py
│   ├── test_block_generators.py
│   ├── test_document_generator.py
│   └── test_exporters.py
│
└── docs/
    ├── architecture.md
    ├── adding_block_types.md
    ├── creating_templates.md
    └── groq_integration.md
```

## Available Tools

### Document Generation

**`generate_document`**
- Generates complete document based on template and topic
- Parameters: `template_id`, `topic`, `level`, `parameters`
- Returns: Generated document with metadata

**`list_templates`**
- Lists all available templates
- Optional filter by document type
- Returns: Template metadata

**`get_template`**
- Retrieves full template definition
- Parameters: `template_id`
- Returns: Complete template structure

**`create_custom_template`**
- Creates new custom template
- Parameters: `name`, `document_type`, `blocks`, `formatting`
- Returns: New template ID

### Block Types

**`list_block_types`**
- Lists all available block types
- Returns: Description, parameters, and generation time for each type

**`get_block_type`**
- Gets details about specific block type
- Parameters: `block_type`
- Returns: Full block type definition

### Export

**`export_document`**
- Exports generated document to different format
- Parameters: `document_id`, `format` (docx/pdf/markdown)
- Returns: File path and metadata

## Block Types Reference

| Block Type | Purpose | Generation Method | Parameters |
|---|---|---|---|
| `title_page` | Cover page | Format metadata | `show_date`, `show_group`, `show_course` |
| `introduction` | Introduction | Groq AI | `include_objectives`, `include_key_questions` |
| `table_of_contents` | Table of contents | Auto-generated | — |
| `main_content` | Main lecture content | Groq AI | `include_code_snippets`, `depth` |
| `key_takeaways` | Key conclusions | Groq AI | `format` (bullets/paragraphs) |
| `references` | Bibliography | Groq AI | `style` (gost/apa/chicago) |
| `appendix` | Additional materials | Collected from others | `include_code`, `include_tables` |
| `practical_task` | Practical exercises | Groq AI | `count`, `complexity` |
| `questions` | Quiz/control questions | Groq AI | `count`, `difficulty` |
| `learning_outcomes` | Competencies | Groq AI | — |

## Examples

### Example 1: Generate Standard Lecture

```python
from rossete.generator import DocumentGenerator

generator = DocumentGenerator()

result = generator.generate_document(
    template_id="lecture_standard_v1",
    topic="Dart Language Fundamentals",
    level="beginner",
    parameters={
        "duration_minutes": 60,
        "group": "ПМС-21",
        "include_code_snippets": True,
        "language": "ru"
    }
)

print(f"Generated in {result['generation_time']:.1f}s")  # ~10s with Groq
```

### Example 2: Generate Lab Work

```python
result = generator.generate_document(
    template_id="lab_work_standard_v1",
    topic="Flutter State Management with Provider",
    level="intermediate",
    parameters={
        "work_number": 3,
        "duration_hours": 2,
        "group": "ПМС-21",
        "include_questions_for_preparation": True
    }
)
```

### Example 3: Create Custom Template

```python
custom_template = {
    "name": "Minimalist Lecture",
    "document_type": "lecture",
    "blocks": [
        {"order": 1, "block_type": "title_page", "required": True},
        {"order": 2, "block_type": "introduction", "required": True},
        {"order": 3, "block_type": "main_content", "required": True},
        {"order": 4, "block_type": "key_takeaways", "required": True}
    ]
}

template_id = generator.create_custom_template(custom_template)
```

## Groq Integration Details

### Why Groq?

- **⚡ Ultra-Fast Inference** — 10-15x faster than traditional LLMs
- **💰 Cost-Effective** — Lower latency means lower operational costs
- **🔄 Streaming Support** — Real-time content generation feedback
- **🌐 Global Network** — Reliable API with 99.9% uptime
- **📊 Better for Education** — Perfect for generating educational content quickly

### Supported Models

**Default: `mixtral-8x7b-32768`**
- 32K context window
- Excellent for educational content
- Fast token generation

Other available models:
- `llama2-70b-4096` — Larger model for complex topics
- `llama2-7b-2048` — Faster for simple content

Switch models by updating `GROQ_MODEL` in `.env`:
```env
GROQ_MODEL=llama2-70b-4096
```

### GroqClient Wrapper

```python
# rossete/ai/groq_client.py

from groq import Groq

class GroqClient:
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        self.client = Groq(api_key=api_key)
        self.model = model
    
    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate content using Groq API"""
        message = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            max_tokens=max_tokens,
            temperature=0.7
        )
        return message.choices[0].message.content
```

## Extending Rossete

### Adding a New Block Type

1. **Create block generator class:**

```python
# rossete/blocks/generators/custom.py

from rossete.blocks.base import BaseBlockGenerator
from rossete.ai.groq_client import groq_client

class CustomBlockGenerator(BaseBlockGenerator):
    """Custom block generator for special content"""
    
    block_type = "custom_block"
    required_inputs = ["topic", "level"]
    
    @staticmethod
    async def generate(
        topic: str,
        level: str,
        parameters: dict
    ) -> str:
        """Generate custom block content via Groq"""
        
        prompt = f"""
        Generate custom content for topic: {topic}
        Level: {level}
        Additional parameters: {parameters}
        """
        
        return await groq_client.generate(prompt)
```

2. **Register in block registry:**

```python
# rossete/blocks/registry.py

from .generators.custom import CustomBlockGenerator

BLOCK_GENERATORS = {
    # ... existing generators
    "custom_block": CustomBlockGenerator,
}
```

3. **Use in templates:**

```json
{
  "blocks": [
    {
      "order": 3,
      "block_type": "custom_block",
      "required": true,
      "parameters": {}
    }
  ]
}
```

### Creating Custom Template

1. Create JSON file in `rossete/templates/` directory
2. Follow the template schema
3. Reference in generation calls

## API Reference

### DocumentGenerator

```python
class DocumentGenerator:
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768")
    
    async def generate_document(
        template_id: str,
        topic: str,
        level: str,
        parameters: dict
    ) -> Dict[str, Any]
    
    async def create_custom_template(
        template_config: dict
    ) -> str
    
    async def list_templates(document_type: str = None) -> List[Dict]
    
    async def get_template(template_id: str) -> Dict[str, Any]
    
    async def export_document(
        document_id: str,
        format: str = "docx"
    ) -> str
```

## Configuration

### Environment Variables

```env
# Required
GROQ_API_KEY=gsk_...

# Optional
GROQ_MODEL=mixtral-8x7b-32768
ROSSETE_STORAGE_PATH=./generated_documents
ROSSETE_TEMPLATES_PATH=./templates
ROSSETE_LOG_LEVEL=INFO
ROSSETE_MAX_WORKERS=5
GROQ_TIMEOUT=60
```

### Formatting Standards

Default formatting (configurable per template):
- Font: Times New Roman
- Font Size: 12pt
- Line Spacing: 1.5
- Margins: Left 20mm, Right 15mm, Top 15mm, Bottom 15mm
- Page Numbers: Bottom right
- Encoding: UTF-8

## Performance

- **Average Generation Time**: 8-15 seconds per document (with Groq)
- **Token Throughput**: 20-40 tokens/second
- **Supported Document Length**: Up to 8,000 tokens per block
- **Concurrent Requests**: 5 (configurable)
- **Caching**: 24-hour TTL for identical requests

### Performance vs Other Solutions

| Solution | Generation Time | Cost |
|---|---|---|
| Rossete + Groq | ~12s | Low ⭐ |
| Claude API | ~20-30s | Medium |
| GPT-4 | ~30-45s | High |
| Local LLM | Variable | Free (but slow) |

## Limitations

- Currently supports Russian and English content
- DOCX export is primary; PDF requires pandoc
- Maximum 10 blocks per document
- Groq context window: 32K tokens (for mixtral-8x7b-32768)
- Rate limits based on Groq plan

## Requirements

```
fastmcp==0.1.0
groq==0.9.0
python-docx==0.8.11
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

## Contributing

Contributions are welcome! Areas for contribution:
- New block generators
- New template designs
- Export format improvements
- Documentation
- Tests

See `docs/CONTRIBUTING.md` for guidelines.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- 📧 Email: support@rossete.dev
- 🐛 Bug reports: https://github.com/yourusername/rossete/issues
- 💬 Discussions: https://github.com/yourusername/rossete/discussions

## Changelog

### v0.1.0 (Initial Release)
- ✅ Core template system
- ✅ Standard block generators
- ✅ DOCX export
- ✅ Groq API integration (mixtral-8x7b-32768)
- ✅ MCP integration with fastMCP
- ✅ Basic documentation

### Planned (v0.2.0)
- PDF export without pandoc dependency
- Interactive template editor
- Block generation history and version control
- Multi-language support improvements
- Support for more Groq models

## Acknowledgments

Built with:
- [fastMCP](https://github.com/anthropics/mcp/tree/main/python/fastmcp) - Anthropic's MCP framework
- [Groq API](https://groq.com/) - Ultra-fast LLM inference
- [python-docx](https://python-docx.readthedocs.io/) - DOCX generation

---

**Made with ❤️ for educators, powered by ⚡ Groq**
