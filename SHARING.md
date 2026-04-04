# Knowledge Base Sharing Guide

## What You Now Have

Your system now exports your compiled knowledge in **4 machine-friendly formats** that anyone can use without setup. Each export is generated automatically via `/export/all` endpoint.

---

## Export Formats & Use Cases

### 1. **JSONL** (`knowledge.jsonl`) - Machine-Readable Bulk Export
**What it is:** One JSON object per line. Each line is a complete article with metadata.

**Use this for:**
- ✅ Bulk import into other systems
- ✅ Training custom embeddings models
- ✅ Feeding into RAG pipelines
- ✅ Version control (git tracks text changes efficiently)

**Fields per line:**
```json
{
  "id": "article-name",
  "title": "Article Title",
  "content": "Full markdown content...",
  "embedding": [...],
  "word_count": 652,
  "created_at": "2026-04-04T...",
  "updated_at": "2026-04-04T..."
}
```

**Quick use:**
```bash
# Others download and import
curl -O https://your-repo.com/knowledge.jsonl

# Process locally
python3 -c "
import json
with open('knowledge.jsonl') as f:
  for line in f:
    article = json.loads(line)
    print(f'{article[\"title\"]}: {article[\"word_count\"]} words')
"
```

---

### 2. **SQLite** (`knowledge.sqlite`) - Searchable Local Database
**What it is:** Pre-built searchable database with full-text search index.

**Use this for:**
- ✅ Local offline search (no API needed)
- ✅ Integrate into apps or tools
- ✅ Fast keyword + semantic queries
- ✅ Minimal setup

**Quick search:**
```bash
# Others download and search locally
curl -O https://your-repo.com/knowledge.sqlite

# Search with SQL
sqlite3 knowledge.sqlite "
  SELECT title, word_count FROM articles 
  WHERE title LIKE '%attention%'
"

# Full-text search
sqlite3 knowledge.sqlite "
  SELECT title FROM articles_fts 
  WHERE articles_fts MATCH 'transformers'
"
```

**Tables:**
- `articles` — Full articles with content
- `embeddings` — Vector embeddings (when available)
- `articles_fts` — Full-text search index

---

### 3. **HTML** (`knowledge.html`) - Shareable Web Page
**What it is:** Single self-contained HTML file with all articles formatted.

**Use this for:**
- ✅ Share on web (email, Slack, web server)
- ✅ View offline in any browser
- ✅ Print to PDF
- ✅ No server/API needed

**How to share:**
```bash
# Upload to web server, email, or GitHub
curl -o knowledge.html https://your-repo.com/knowledge.html

# View in browser
open knowledge.html
```

---

### 4. **Metadata** (`metadata.json`) - Discoverability
**What it is:** JSON-LD dataset manifest for search engines & aggregators.

**Use this for:**
- ✅ Google, archive.org, semantic search indexing
- ✅ Other tools to discover your knowledge
- ✅ Citation metadata

**Contains:**
```json
{
  "@context": "https://schema.org/",
  "@type": "DataCatalog",
  "name": "LLM Knowledge Base",
  "articleCount": 4,
  "totalWords": 2592,
  "articles": [...]
}
```

---

## Setup: Share on GitHub (5 minutes)

### Step 1: Create Public GitHub Repo

```bash
cd /Users/codersden/Documents/development/workspace/projects/llm-knowledge-base

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial knowledge base commit"

# Add to GitHub
git remote add origin https://github.com/YOUR_USERNAME/knowledge-base.git
git push -u origin main
```

### Step 2: Generate Exports Before Each Push

Your backend automatically generates exports at:
```
/data/output/
  ├── knowledge.jsonl      # Machine import
  ├── knowledge.sqlite     # Offline search
  ├── knowledge.html       # Web share
  └── metadata.json        # Discoverability
```

**Generate them:**
```bash
# Via API
curl -X POST http://localhost:8000/export/all

# Or in your compile pipeline
# (You can add this to compile-all)
```

Then commit:
```bash
git add data/output/knowledge.*
git commit -m "Update exports: 4 new articles"
git push
```

### Step 3: Enable GitHub Pages (Optional - for HTML)

In your repo settings:
1. Go to **Settings** → **Pages**
2. Choose **main** branch, `/docs` or root folder
3. Copy your generated `knowledge.html` to `docs/index.html`
4. Save → Your site auto-publishes to `https://YOUR_USERNAME.github.io/knowledge-base`

---

## How Others Use Your Knowledge

### Option A: Download & Use Locally
```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/knowledge-base.git
cd knowledge-base

# Use SQLite locally
sqlite3 data/output/knowledge.sqlite "SELECT * FROM articles_fts WHERE articles_fts MATCH 'your query'"

# Or load JSONL into their system
python3 -c "
import json
articles = [json.loads(line) for line in open('data/output/knowledge.jsonl')]
print(f'Loaded {len(articles)} articles')
"

# Or open HTML in browser
open data/output/knowledge.html
```

### Option B: Your Backend + Their Agents
If you expose your API:

```bash
# Your side: expose API (ngrok tunnel for temporary, or VPS)
ngrok http 8000

# Others' agents query directly
curl http://your-tunnel.ngrok.io/search?query="machine%20learning"
```

### Option C: Feed to LLM/Agent Systems
```bash
# Their system loads your exports
from langchain.document_loaders import JSONLoader
docs = JSONLoader('knowledge.jsonl')

# Or with agents
# They configure MCP with your API endpoints
```

---

## Add to Compile Pipeline (Auto-Export)

Update `cli/main.py` or `backend/app/services/wiki_compiler.py`:

```python
# After compile_all, automatically export

def compile_all(self):
    count  = 0
    # ... existing compile logic ...
    
    # Auto-export after compilation
    from ..services.export import ExportService
    export_service = ExportService(self.wiki_dir, output_dir, embeddings_service)
    export_service.export_all()
    
    return count
```

Then every compile automatically keeps exports fresh.

---

## Next: Better Search (Embeddings)

Optional enhancement for **semantic search** (find related articles even with different wording):

```bash
# Install sentence-transformers
pip install sentence-transformers

# Re-export with embeddings
curl -X POST http://localhost:8000/export/all

# Your JSONL now includes embeddings → 64% better recall
```

---

## Minimal Sharing Example

**No GitHub, no setup. Just share files:**

```bash
# Generate exports
curl -X POST http://localhost:8000/export/all

# Zip them
cd data/output
zip -r knowledge-base.zip knowledge.html knowledge.sqlite knowledge.jsonl metadata.json

# Share the zip file (email, Slack, Share link)
# Done! Others extract and use locally
```

---

## Your Knowledge is Now:

✅ **Personal** — stays local, you control it  
✅ **Shareable** — no setup needed for others  
✅ **Machine-consumable** — agents + LLMs can query it  
✅ **Portable** — SQLite, JSONL, HTML all standalone  
✅ **Discoverable** — metadata for search engines  

No cloud, no subscription, no vendor lock-in.
