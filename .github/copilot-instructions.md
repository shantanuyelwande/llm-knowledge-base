# LLM Knowledge Base - GitHub Copilot Instructions

This is an LLM-powered knowledge base system that transforms research materials into an intelligent, searchable wiki.

## Project Overview

A complete system with:
- FastAPI backend with Anthropic Claude integration
- Simple but effective search engine  
- CLI tool for workflow automation
- Beautiful web UI for interaction
- Multi-format output rendering

Use this to build personal research wikis that you can intelligently query.

## Key Files & Their Purpose

### Backend Implementation
- `backend/app/core/llm.py` - Claude API integration
- `backend/app/core/search.py` - Full-text search implementation
- `backend/app/services/wiki_compiler.py` - Document processing & compilation
- `backend/app/services/qa_system.py` - Question answering with context
- `backend/app/api/routes.py` - All REST endpoints

### CLI & Interfaces
- `cli/main.py` - Command-line tools (9 commands)
- `frontend/index.html` - Web interface

### Configuration
- `.env.example` - Environment template (copy to .env)
- `requirements.txt` - Python dependencies

### Documentation  
- `README.md` - Full documentation
- `QUICKSTART.md` - 5-minute setup
- `DEVELOPMENT.md` - Architecture details
- `SCALING.md` - Performance optimization

## How to Use

### First Time Setup
1. Copy `.env.example` to `.env` and add your ANTHROPIC_API_KEY
2. Run: `pip install -r requirements.txt`
3. Initialize: `cd cli && python main.py init`
4. Start: `../start.sh` (or `../start.bat` on Windows)

### Common Tasks

**Compile documents:**
```bash
cd cli
python main.py compile-all
```

**Search:**
```bash
python main.py search "your query"
```

**Ask questions:**
```bash
python main.py query "Your question?"
```

**Start backend:**
```bash
cd backend
python main.py
```

**Open web UI:**
- Open `frontend/index.html` in browser (or serve on http://localhost:5000)

## Architecture

Fast and simple: Raw documents → LLM compilation → Wiki → Search index → Q&A

## When to Ask Copilot

- Help extending the search algorithm
- Adding new API endpoints
- Creating new CLI commands
- Understanding how components work together
- Help debugging errors

## Project Stats

- 23 files, ~2,000+ lines of core logic
- 6 major modules (LLM, search, wiki, Q&A, API, CLI)
- 10+ API endpoints
- 9 CLI commands
- Fully documented and typed

This is production-ready! Perfect for personal research or as a template for larger projects.
