# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd llm-knowledge-base
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY
# Get one from: https://console.anthropic.com
```

### 3. Initialize and Create Examples
```bash
# Initialize directories
cd cli
python main.py init

# Go back and create example documents
cd ..
python create_examples.py
```

### 4. Start the System
```bash
# Option 1: Use startup script
chmod +x start.sh
./start.sh

# Option 2: Manual startup
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - Frontend (separate terminal)
cd frontend && python -m http.server 5000
```

### 5. Access the System

- **Web UI**: Open [http://localhost:5000](http://localhost:5000) in your browser
- **API Docs**: Visit [http://localhost:8000/docs](http://localhost:8000/docs)
- **CLI**: Use commands like:
  ```bash
  cd cli
  python main.py search "machine learning"
  python main.py query "What is machine learning?"
  python main.py compile-all
  ```

## Common Tasks

### Add Your Own Research

1. Save articles to `data/raw/` (as .md, .txt, or .html)
2. Compile them:
   ```bash
   cd cli
   python main.py compile-all
   ```
3. Access via search or API

### Ask Questions

```bash
cd cli
python main.py query "Your question here?"
```

Results are saved to `data/output/` as markdown files.

### Search the Knowledge Base

```bash
cd cli
python main.py search "search terms" --limit 20
```

### Generate Summary

```bash
cd cli
python main.py summarize "topic name"
```

## Using the Web UI

1. **Search Tab**: Find articles in your wiki
2. **Query Tab**: Ask questions and get AI-generated answers
3. **Wiki Management**: Compile documents, generate indexes
4. **System Status**: View statistics and health

## Troubleshooting

**"ANTHROPIC_API_KEY not set"**
- Check your `.env` file
- Make sure ANTHROPIC_API_KEY is set correctly
- Get an API key from [console.anthropic.com](https://console.anthropic.com)

**"No search results"**
- Make sure documents are compiled: `python main.py compile-all`
- Check that files exist in `data/wiki/`

**"Backend not responding"**
- Make sure backend is running: `python backend/main.py`
- Check port 8000 is not in use
- Wait 2-3 seconds after starting the backend

## Next Steps

1. Add your research materials to `data/raw/`
2. Experiment with queries and searches
3. Check `DEVELOPMENT.md` for more advanced features
4. Read `README.md` for complete documentation

## API Quick Reference

**Health Check**
```bash
curl http://localhost:8000/health
```

**Search**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "limit": 10}'
```

**Query**
```bash
curl -X POST http://localhost:8000/qa/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?", "max_sources": 5, "output_format": "markdown"}'
```

**Generate Summary**
```bash
curl -X POST http://localhost:8000/qa/summarize \
  -H "Content-Type: application/json" \
  -d '{"query": "Machine Learning", "limit": 10}'
```

## Getting Help

- Check the README.md for full documentation
- Review DEVELOPMENT.md for architecture details
- Check logs in terminal output for errors
- Verify your ANTHROPIC_API_KEY is valid

Happy researching! 🚀
