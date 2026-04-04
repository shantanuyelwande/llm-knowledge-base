# Development Guide

## Project Structure

```
llm-knowledge-base/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Settings management
│   │   │   ├── llm.py             # Claude API client
│   │   │   └── search.py          # Simple search engine
│   │   ├── services/
│   │   │   ├── wiki_compiler.py   # Document compilation
│   │   │   ├── qa_system.py       # Question answering
│   │   │   └── output_renderer.py # Result formatting
│   │   └── api/
│   │       └── routes.py          # FastAPI endpoints
│   └── main.py           # Entry point
├── cli/
│   └── main.py           # Typer CLI commands
├── frontend/
│   └── index.html        # Web UI
└── data/
    ├── raw/              # Source documents
    ├── wiki/             # Compiled articles
    └── output/           # Query results
```

## Development Setup

1. **Clone and setup**
```bash
cd llm-knowledge-base
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Create .env**
```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY
```

3. **Initialize**
```bash
cd cli
python main.py init
```

## Running Locally

### Terminal 1: Backend API
```bash
cd backend
python main.py  # Runs on http://localhost:8000
```

### Terminal 2: Frontend
```bash
cd frontend
python -m http.server 5000  # Runs on http://localhost:5000
```

### Terminal 3: CLI
```bash
cd cli
python main.py --help
```

## Adding New Features

### Adding a New API Endpoint

1. Add the endpoint to `backend/app/api/routes.py`
2. Use the existing services (wiki_compiler, qa_system, etc.)
3. Define request/response models with Pydantic
4. Test with `curl` or the frontend

Example:
```python
@app.post("/my-feature")
async def my_feature(request: MyRequest):
    # Implementation
    return {"status": "success", "data": ...}
```

### Adding a New CLI Command

1. Add command to `cli/main.py`
2. Use Typer decorators for arguments and options
3. Use existing services
4. Format output with Rich console

Example:
```python
@app.command()
def my_command(
    arg: str = typer.Argument(..., help="Required argument"),
    opt: str = typer.Option("default", help="Optional option")
):
    """Command description"""
    # Implementation
    console.print("[green]Success![/green]")
```

### Adding a New Service

1. Create module in `backend/app/services/`
2. Import required dependencies
3. Use LLMClient from `core/llm.py`
4. Document with docstrings

## Testing

### Manual Testing

1. **Compile documents**
```bash
cd cli
python main.py compile-all
```

2. **Search the wiki**
```bash
python main.py search "machine learning"
```

3. **Query the knowledge base**
```bash
python main.py query "What is machine learning?"
```

4. **Test via API**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "limit": 10}'
```

## Performance Tips

1. **Search Optimization**: Consider adding pagination or caching for large wikis
2. **LLM Calls**: Implement caching to avoid redundant API calls
3. **Large Documents**: Process in chunks for better performance
4. **Backlink Generation**: Use async processing for large wikis

## Extension Ideas

- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Embedding-based semantic search
- [ ] Automatic gap detection
- [ ] Article quality scoring
- [ ] Multi-language support
- [ ] Export to different formats (PDF, EPUB)
- [ ] Real-time collaboration
- [ ] Integration with Obsidian
- [ ] Web scraper for data ingestion
- [ ] Fine-tuning on wiki data

## Configuration

Key settings in `.env`:

- `ANTHROPIC_API_KEY`: Required, get from console.anthropic.com
- `MODEL`: LLM model (default: claude-3-sonnet-20240229)
- `MAX_TOKENS`: Response length (default: 4096)
- `TEMPERATURE`: Creativity (0-1, default: 0.7)
- `RAW_DATA_DIR`: Raw documents location
- `WIKI_DIR`: Compiled wiki location
- `OUTPUT_DIR`: Query results location

## Troubleshooting

### API Not Responding
- Check if backend is running: `ps aux | grep main.py`
- Check port 8000 is not in use: `lsof -i :8000`
- Check `.env` has valid ANTHROPIC_API_KEY

### No Search Results
- Ensure documents are compiled: `python main.py compile-all`
- Check wiki directory has .md files
- Try a simpler search query

### LLM Errors
- Check API key is valid
- Check rate limits aren't exceeded
- Check internet connection

## Code Style

- Use type hints in all functions
- Document classes and functions with docstrings
- Use descriptive variable names
- Add logging for important operations

## Contributing

1. Create a feature branch
2. Make your changes with clear commits
3. Test manually
4. Update README if needed
5. Submit PR with description
