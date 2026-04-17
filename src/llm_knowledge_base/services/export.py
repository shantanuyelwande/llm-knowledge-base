import logging
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ExportService:
    """Export knowledge base in multiple formats for sharing and reuse"""
    
    def __init__(self, wiki_dir: Path, output_dir: Path, embeddings_service=None):
        self.wiki_dir = wiki_dir
        self.output_dir = output_dir
        self.embeddings_service = embeddings_service
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_wiki_articles(self) -> List[Dict[str, Any]]:
        """Collect all wiki articles with metadata"""
        articles = []
        if not self.wiki_dir.exists():
            logger.warning(f"Wiki directory not found: {self.wiki_dir}")
            return articles
        
        for wiki_file in self.wiki_dir.glob("**/*.md"):
            try:
                content = wiki_file.read_text(encoding="utf-8")
                title = wiki_file.stem
                
                # Generate embedding if available
                embedding = []
                if self.embeddings_service and self.embeddings_service.enabled:
                    # Embed first 512 chars for speed
                    embedding = self.embeddings_service.embed_text(content[:512])
                
                articles.append({
                    "id": wiki_file.stem,
                    "title": title,
                    "path": str(wiki_file.relative_to(self.wiki_dir)),
                    "content": content,
                    "embedding": embedding,
                    "word_count": len(content.split()),
                    "created_at": datetime.fromtimestamp(wiki_file.stat().st_ctime).isoformat(),
                    "updated_at": datetime.fromtimestamp(wiki_file.stat().st_mtime).isoformat(),
                })
            except Exception as e:
                logger.error(f"Error processing wiki file {wiki_file}: {e}")
        
        logger.info(f"Collected {len(articles)} wiki articles")
        return articles
    
    def export_jsonl(self, articles: List[Dict[str, Any]] = None) -> Path:
        """Export knowledge base as JSONL (one JSON object per line)"""
        if articles is None:
            articles = self.collect_wiki_articles()
        
        output_file = self.output_dir / "knowledge.jsonl"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for article in articles:
                    f.write(json.dumps(article, ensure_ascii=False) + "\n")
            logger.info(f"✓ Exported {len(articles)} articles to {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting JSONL: {e}")
            raise
    
    def export_sqlite(self, articles: List[Dict[str, Any]] = None) -> Path:
        """Export knowledge base as searchable SQLite database"""
        if articles is None:
            articles = self.collect_wiki_articles()
        
        output_file = self.output_dir / "knowledge.sqlite"
        try:
            conn = sqlite3.connect(str(output_file))
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    path TEXT,
                    content TEXT NOT NULL,
                    word_count INTEGER,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id TEXT PRIMARY KEY,
                    embedding TEXT,
                    FOREIGN KEY (id) REFERENCES articles(id)
                )
            """)
            
            # Insert data
            for article in articles:
                cursor.execute(
                    """INSERT OR REPLACE INTO articles 
                       (id, title, path, content, word_count, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        article["id"],
                        article["title"],
                        article["path"],
                        article["content"],
                        article["word_count"],
                        article["created_at"],
                        article["updated_at"],
                    )
                )
                
                if article["embedding"]:
                    cursor.execute(
                        """INSERT OR REPLACE INTO embeddings (id, embedding)
                           VALUES (?, ?)""",
                        (article["id"], json.dumps(article["embedding"]))
                    )
            
            # Create full-text search index
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
                    title, content, tokenize = 'porter'
                )
            """)
            
            cursor.execute("""
                INSERT INTO articles_fts (title, content)
                SELECT title, content FROM articles
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"✓ Exported {len(articles)} articles to SQLite: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting SQLite: {e}")
            raise
    
    def export_metadata(self, articles: List[Dict[str, Any]] = None) -> Path:
        """Export dataset metadata (JSON-LD + CITATION.cff format)"""
        if articles is None:
            articles = self.collect_wiki_articles()
        
        output_file = self.output_dir / "metadata.json"
        try:
            metadata = {
                "@context": "https://schema.org/",
                "@type": "DataCatalog",
                "name": "LLM Knowledge Base",
                "description": "Personal knowledge base compiled from raw documents",
                "creator": {
                    "@type": "Person",
                    "name": "Knowledge Base Owner"
                },
                "datePublished": datetime.now().isoformat(),
                "articleCount": len(articles),
                "totalWords": sum(a["word_count"] for a in articles),
                "articles": [
                    {
                        "id": a["id"],
                        "title": a["title"],
                        "wordCount": a["word_count"],
                        "created": a["created_at"],
                        "updated": a["updated_at"],
                    }
                    for a in articles
                ]
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ Exported metadata to {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting metadata: {e}")
            raise
    
    def export_html(self, articles: List[Dict[str, Any]] = None) -> Path:
        """Export as single shareable HTML page"""
        if articles is None:
            articles = self.collect_wiki_articles()
        
        output_file = self.output_dir / "knowledge.html"
        try:
            try:
                import markdown
            except ImportError:
                markdown = None
            
            # Build HTML manually to avoid style string issues
            total_words = sum(a["word_count"] for a in articles)
            toc_items = "\n".join([f'            <li><a href="#{a["id"]}">{a["title"]}</a></li>' for a in articles])
            
            articles_html = ""
            for article in articles:
                articles_html += f'    <div class="article" id="{article["id"]}">\n'
                articles_html += f'        <h2>{article["title"]}</h2>\n'
                articles_html += f'        <div class="article-meta">Words: {article["word_count"]} | Updated: {article["updated_at"]}</div>\n'
                
                # Convert markdown to HTML if available, otherwise use pre tags
                if markdown:
                    try:
                        content_html = markdown.markdown(article["content"])
                    except Exception as e:
                        logger.warning(f"Could not convert markdown for {article['id']}: {e}")
                        content_html = f"<pre>{article['content']}</pre>"
                else:
                    content_html = f"<pre>{article['content']}</pre>"
                
                articles_html += f'        {content_html}\n'
                articles_html += '    </div>\n'
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Base</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2em; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .article {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #667eea; }}
        .article h2 {{ margin-top: 0; color: #667eea; }}
        .article-meta {{ font-size: 0.9em; color: #666; margin: 10px 0; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        pre {{ background: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        a {{ color: #667eea; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
        .toc {{ background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .toc h3 {{ margin-top: 0; }} .toc ul {{ list-style: none; padding: 0; }}
        .toc li {{ padding: 5px 0; }} .toc a {{ color: #667eea; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Knowledge Base</h1>
        <p>Personal knowledge compiled and shared • {len(articles)} articles • {total_words} words</p>
    </div>
    <div class="toc">
        <h3>Table of Contents</h3>
        <ul>
{toc_items}
        </ul>
    </div>
{articles_html}</body>
</html>"""
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            logger.info(f"✓ Exported to HTML: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting HTML: {e}")
            raise
    
    def export_all(self) -> Dict[str, Path]:
        """Export in all formats and return file paths"""
        articles = self.collect_wiki_articles()
        
        results = {
            "jsonl": self.export_jsonl(articles),
            "sqlite": self.export_sqlite(articles),
            "metadata": self.export_metadata(articles),
            "html": self.export_html(articles),
        }
        
        logger.info(f"✓ All exports complete: {', '.join(results.keys())}")
        return results
