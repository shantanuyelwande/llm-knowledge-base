# LLM Knowledge Base

Transform your research materials into an intelligent, queryable knowledge base powered by Claude AI.

## 🎯 Features

- **Data Ingestion**: Index raw documents (articles, papers, repos, datasets)
- **Wiki Compilation**: Automatically convert raw documents into structured wiki articles using LLM
- **Intelligent Search**: BM25 word-based + optional semantic embeddings (sentence-transformers)
- **Q&A System**: Ask complex questions and get research-based answers
- **Wiki Linking**: Automatic backlinks and article connections
- **Duplicate Detection**: Find and merge duplicate articles; auto-detect via title similarity or embeddings
- **Update Tracking**: Detect when source files change; track versions and compilation history
- **Multi-Format Exports**: Export knowledge base as JSONL, SQLite, HTML, JSON-LD. See [SHARING.md](SHARING.md)
- **Shareable Knowledge**: Portable exports enable sharing without cloud infrastructure
- **CLI & Web UI**: Command-line tools and web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone and navigate to the project**
```bash
cd llm-knowledge-base
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

5. **Initialize the knowledge base**
```bash
cd cli
python main.py init
```

## 📖 Usage Guide

### Using the CLI

The CLI provides commands for all knowledge base operations:

```bash
cd cli
python main.py --help
```

**Key Commands:**

- `init` - Initialize knowledge base directories
- `compile [SOURCE_PATH]` - Compile a raw document into wiki format
- `compile-all` - Compile all raw documents
- `search [QUERY]` - Search the wiki
- `query [QUESTION]` - Ask a question against the knowledge base
- `summarize [TOPIC]` - Summarize a topic
- `health` - Check system status
- `lint --find-duplicates` - Find potential duplicate articles
- `lint --find-stale` - Find articles with outdated sources
- `merge SOURCE TARGET` - Merge two articles

**Examples:**

```bash
# Initialize
python main.py init

# Add raw documents to data/raw/ directory, then compile
python main.py compile research/ai-papers.md --title "AI Research Papers"
python main.py compile-all

# Search and query
python main.py search "machine learning"
python main.py query "What are the key concepts in machine learning?"
python main.py summarize "neural networks"

# Maintenance
python main.py health
python main.py lint --find-duplicates      # Find overlapping articles
python main.py lint --find-stale           # Find articles with outdated sources
python main.py merge neural-networks.md deep-learning.md --strategy append
```

### Using the Web UI

1. **Start the backend API**
```bash
cd backend
python main.py
# API will be available at http://localhost:8000
```

2. **Open the frontend**
Open [frontend/index.html](frontend/index.html) in your browser or serve it:
```bash
cd frontend
# Using Python 3
python -m http.server 5000
# Then visit http://localhost:5000
```

**Web UI Features:**
- Search documents and articles
- Ask questions with various output formats
- Compile and manage documents
- Generate wiki index and summaries
- View system statistics

## 📁 Directory Structure

```
llm-knowledge-base/
├── backend/              # FastAPI backend server
│   ├── app/
│   │   ├── core/        # Configuration and utilities
│   │   ├── services/    # Business logic (wiki, search, QA)
│   │   └── api/         # API endpoints
│   └── main.py          # FastAPI entry point
├── cli/                 # Command-line interface
│   └── main.py          # Typer CLI commands
├── frontend/            # Web UI (HTML/JS)
│   └── index.html       # Single-page application
├── data/                # Data storage
│   ├── raw/             # Raw source documents
│   ├── wiki/            # Compiled wiki articles
│   └── output/          # Query results and reports
├── requirements.txt     # Python dependencies
├── .env.example         # Environment configuration template
└── README.md           # This file
```

## 🔧 Architecture

### Components

1. **LLM Client** (`backend/app/core/llm.py`)
   - Interfaces with Anthropic's Claude API
   - Text generation and streaming

2. **Wiki Compiler** (`backend/app/services/wiki_compiler.py`)
   - Converts raw documents into structured markdown
   - Generates wiki index and backlinks
   - Adds YAML frontmatter with metadata

3. **Metadata Tracker** (`backend/app/services/metadata_tracker.py`)
   - Tracks source file hashes (SHA256) and timestamps
   - Detects when raw files have been updated
   - Manages version counter for each article

4. **Duplicate Detector** (`backend/app/services/duplicate_detector.py`)
   - Title-based similarity (always available)
   - Optional semantic embeddings (sentence-transformers)
   - Generates duplicate reports

5. **Wiki Merger** (`backend/app/services/wiki_merger.py`)
   - Merges two articles with three strategies: append, prepend, section
   - Archives original articles before deletion
   - Updates metadata to track merged sources

6. **Search Engine** (`backend/app/core/search.py`)
   - BM25 word-based indexing
   - Relevance scoring

7. **Embeddings Service** (`backend/app/services/embeddings.py`) *(Optional)*
   - Semantic search using sentence-transformers
   - Graceful fallback if not installed

8. **Q&A System** (`backend/app/services/qa_system.py`)
   - Retrieves relevant context from wiki
   - Generates answers using LLM

9. **Export Service** (`backend/app/services/export.py`)
   - JSONL, SQLite, HTML, JSON-LD exports
   - Full-text search indexing

10. **Output Renderer** (`backend/app/services/output_renderer.py`)
    - Saves results in multiple formats
    - Generates HTML from markdown

### Data Flow

```
Raw Data (raw/)
    ↓
[Wiki Compiler] ← LLM processes & formats
    ↓
[Metadata Tracker] ← Source hash + timestamp
    ↓
Structured Wiki (wiki/) with YAML frontmatter
    ↓
┌─ Maintenance Layer ─────────────────────────┐
│  • Duplicate Detector (find overlaps)       │
│  • Update Detector (find stale articles)    │
│  • Wiki Merger (merge duplicates)           │
│  • Git tracking (version history)           │
└─────────────────────────────────────────────┘
    ↓
[BM25 Search] ← [Embeddings (optional)]
    ↓
[Q&A System] → Answer + Sources
    ↓
[Export Service] → 4 formats
    ├→ JSONL (training)
    ├→ SQLite (offline)
    ├→ HTML (web)
    └→ Metadata (discovery)
```

## 🎓 Example Use Cases

### Personal Research Wiki
1. Add research papers, articles, and notes to `data/raw/`
2. Compile all documents: `python main.py compile-all`
3. Ask questions: `python main.py query "What are the key findings about LLMs?"`
4. Outputs are saved as markdown files you can review in Obsidian

### Documentation Generator
1. Organize source docs in `data/raw/`
2. Generate web-friendly HTML output
3. Use API to create programmatic documentation workflows

### Knowledge Synthesis
1. Load multiple sources on a topic
2. Use `summarize` to identify patterns
3. Use `query` to discover connections
4. Let LLM fill in gaps from external web search

## � Maintenance & Data Consistency

### Tracking Updates
Each wiki article is saved with metadata (YAML frontmatter) containing:
- `source_hash`: SHA256 of original raw file
- `version`: Compilation count (increments on update)
- `compiled_at`: Last compilation timestamp

To detect stale articles:
```bash
python main.py lint --find-stale
```

Then recompile to update:
```bash
python main.py compile-all
```

### Finding & Merging Duplicates
Find articles with overlapping content:
```bash
python main.py lint --find-duplicates
```

Merge two articles (source → target):
```bash
python main.py merge neural-networks.md deep-learning.md --strategy append
```

**Strategies:**
- `append`: Add merged content at end
- `prepend`: Add merged content at top
- `section`: Create separate "From X" sections

Original article is archived to `.archives/` and tracked in metadata.

### Frontmatter Example
```yaml
---
title: Neural Networks
source_file: data/raw/ai-basics.md
source_hash: abc123def456...
compiled_at: 2026-04-04T10:30:00
raw_file_updated: 2026-04-04T10:30:00
version: 2
sources:
  - file: data/raw/ai-basics.md
    hash: abc123...
    added_at: 2026-04-04T10:30:00
tags: []
related_topics: []
---
```

## �🔌 API Reference

**Base URL:** `http://localhost:8000`

### Wiki Operations

#### POST `/wiki/compile`
Compile a single document into wiki format.
```json
{
  "source_path": "research/paper.md",
  "title": "My Paper Title"
}
```

#### POST `/wiki/compile-all`
Compile all raw documents into wiki.

#### GET `/wiki/index`
Get wiki table of contents.

#### GET `/wiki/backlinks`
Get article backlinks for cross-reference mapping.

#### POST `/wiki/refresh`
Refresh wiki compilation.

### Search & Q&A

#### POST `/search`
Search the wiki with BM25 indexing.
```json
{
  "query": "machine learning",
  "limit": 10
}
```

#### POST `/qa/query`
Ask a question against the knowledge base.
```json
{
  "question": "What is the most important concept?",
  "max_sources": 5,
  "output_format": "markdown"
}
```

#### POST `/qa/summarize`
Generate a summary on a topic.
```json
{
  "topic": "neural networks"
}
```

### Export Operations

#### POST `/export/jsonl`
Export knowledge base as JSONL (1 article per line).
- **Use case**: Training data, AI model fine-tuning, bulk import
- **Output**: `knowledge.jsonl` in `/data/output/`

#### POST `/export/sqlite`
Export as SQLite with full-text search indexing.
- **Use case**: Offline search, portable database, application integration
- **Output**: `knowledge.sqlite` (indexed, ~176 KB)

#### POST `/export/html`
Export as self-contained HTML webpage.
- **Use case**: Web sharing, static hosting, GitHub Pages
- **Output**: `knowledge.html` (standalone, no dependencies)

#### POST `/export/metadata`
Export as JSON-LD structured metadata.
- **Use case**: SEO, search engine discoverability, linked data
- **Output**: `metadata.json` (JSON-LD schema)

#### POST `/export/all`
Export in all 4 formats simultaneously.
- **Output**: All formats in `/data/output/`

### System

#### GET `/health`
Health check and system statistics.
Returns wiki size, article count, recent operations.

## ⚙️ Configuration

Edit `.env` to customize:

```
ANTHROPIC_API_KEY=sk-...           # Your Claude API key (required)
MODEL=claude-3-sonnet-20240229     # LLM model to use
MAX_TOKENS=4096                    # Max response length
TEMPERATURE=0.7                    # Response creativity (0-1)
```

### Optional Dependencies

**Semantic Search (Embeddings)** — Install for better search recall:
```bash
pip install sentence-transformers torch transformers
```

If not installed, the system gracefully falls back to BM25 search (still effective for most use cases).

## 🤔 FAQ

**Q: How do I add web articles to my knowledge base?**
A: Use the Obsidian Web Clipper to save articles as markdown to your `data/raw/` directory, then run `compile-all`.

**Q: Can I use a different LLM provider?**
A: Currently configured for Anthropic's Claude. Modify `backend/app/core/llm.py` to support other providers.

**Q: How do I handle duplicate articles?**
A: Run `lint --find-duplicates` to find overlaps, then merge with `merge source.md target.md`. Originals are archived.

**Q: How do I know if a wiki article is outdated?**
A: Run `lint --find-stale` to find articles whose source files have been updated. Recompile with `compile-all`.

**Q: What's the difference between BM25 and embeddings search?**
A: BM25 is keyword-based (fast, no setup). Embeddings provide semantic search (better for concepts). Embeddings optional.

**Q: How do I share my knowledge base?**
A: Use `/export/all` to generate 4 formats (JSONL, SQLite, HTML, metadata). See [SHARING.md](SHARING.md) for sharing workflows.

**Q: Can I visualize connections between articles?**
A: The backlinks feature maps article connections. Could build a graph visualization with this data.

## 📝 License

MIT

## 🙋 Contributing

Contributions welcome! This is an open system - feel free to extend it with new features, better search algorithms, or additional output formats.

## � Related Reading

- [DUPLICATE_DETECTION.md](DUPLICATE_DETECTION.md) — Detailed guide on duplicate detection, merging, and update tracking
- [SHARING.md](SHARING.md) — Guide to exporting and sharing your knowledge base
- [Karpathy's LLM Wiki Pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Conceptual foundation for this architecture
- [DEVELOPMENT.md](DEVELOPMENT.md) — Technical setup and troubleshooting

## 💡 Future Ideas

- ✅ **Multi-format exports** (JSONL, SQLite, HTML, metadata) — *Implemented*
- ✅ **Optional semantic search** (embeddings) — *Implemented*  
- ✅ **Duplicate detection & merging** — *Implemented*
- ✅ **Update tracking** (file hashes, versions) — *Implemented*
- Git integration for version history (easy with `data/wiki/.git`)
- Auto-merge on duplicate detection
- LLM-powered conflict resolution
- Multi-way merge support
- Graph visualization of article connections
