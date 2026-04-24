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
    
    def _extract_tags_from_content(self, content: str) -> list:
        """Extract tags from article frontmatter with robust delimiter and quoting support"""
        try:
            content_stripped = content.lstrip()
            if not content_stripped.startswith("---"):
                return []
            
            # Find the closing '---' on its own line
            lines = content.splitlines()
            end_idx = -1
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    end_idx = i
                    break
            
            if end_idx == -1:
                return []
                
            frontmatter = "\n".join(lines[0:end_idx])
            for line in frontmatter.splitlines():
                line = line.strip()
                if line.lower().startswith("tags:"):
                    tags_part = line[5:].strip()
                    # Remove brackets if present: [tag1, tag2] -> tag1, tag2
                    tags_part = tags_part.strip("[]")
                    # Split by comma, strip whitespace and surrounding quotes
                    tags = [t.strip().strip("'\"") for t in tags_part.split(",") if t.strip()]
                    return tags
        except Exception as e:
            logger.debug(f"Tag extraction failed: {e}")
        return []

    def _extract_source_info(self, content: str) -> dict:
        """Extract source_file and source_url from article frontmatter"""
        source_info = {}
        try:
            if content.startswith("---"):
                end = content.find("\n---\n", 4)
                if end > 0:
                    frontmatter = content[4:end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("source_file:"):
                            source_info["file"] = line.split(":", 1)[1].strip()
                        elif line.startswith("source_url:"):
                            url = line.split(":", 1)[1].strip()
                            source_info["url"] = url
        except:
            pass
        return source_info

    def _extract_article_summary(self, content: str) -> str:
        """Extract clean article summary (first non-heading paragraph)"""
        try:
            if content.startswith("---"):
                end = content.find("\n---\n", 4)
                if end > 0:
                    body = content[end + 5:]
                else:
                    body = content
            else:
                body = content

            for line in body.split("\n"):
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("["):
                    clean = line.replace("**", "").replace("*", "").replace("[[", "").replace("]]", "")
                    return clean[:150] + ("..." if len(clean) > 150 else "")
        except:
            pass
        return "Knowledge base article"

    def _build_search_index(self, articles: List[Dict[str, Any]]) -> str:
        """Build searchable JSON index for client-side search"""
        index = []
        for article in articles:
            tags = self._extract_tags_from_content(article['content'])
            source_info = article.get('source_info', {})

            index.append({
                "id": article["id"],
                "title": article["title"],
                "summary": article.get('summary', ''),
                "content": article["content"][:500],
                "tags": tags,
                "source_url": source_info.get('url', ''),
                "source_file": source_info.get('file', ''),
                "word_count": article["word_count"]
            })

        return json.dumps(index)

    def export_html(self, articles: List[Dict[str, Any]] = None) -> Path:
        """Export as interactive accordion HTML with categories and a core concept hub"""
        if articles is None:
            articles = self.collect_wiki_articles()

        output_file = self.output_dir / "knowledge.html"
        try:
            # Extract clean article summaries and source info
            for article in articles:
                article['summary'] = self._extract_article_summary(article['content'])
                article['source_info'] = self._extract_source_info(article['content'])

            # Group articles by primary tag only (to condense categories)
            articles_by_tag = {}
            uncategorized = []

            for article in articles:
                tags = self._extract_tags_from_content(article['content'])
                if tags:
                    primary_tag = tags[0]
                    if primary_tag not in articles_by_tag:
                        articles_by_tag[primary_tag] = []
                    articles_by_tag[primary_tag].append(article)
                else:
                    uncategorized.append(article)

            # Build accordion HTML sections
            accordion_html = ""
            for tag in sorted(articles_by_tag.keys()):
                article_count = len(articles_by_tag[tag])
                accordion_html += f'<div class="accordion-item">\n'
                accordion_html += f'  <button class="accordion-header" onclick="toggleAccordion(this)"><span>📚 {tag}</span><span class="category-count">{article_count}</span><span class="toggle-icon">▼</span></button>\n'
                accordion_html += f'  <div class="accordion-content">\n'

                for article in sorted(articles_by_tag[tag], key=lambda x: x["title"]):
                    accordion_html += f'    <div class="article-card"><h4>{article["title"]}</h4>'
                    accordion_html += f'<p class="summary">{article["summary"]}</p>'

                    # Add source info if available
                    source_info = article.get('source_info', {})
                    source_text = ""
                    if source_info.get('url'):
                        source_text = f'🔗 <a href="{source_info["url"]}" target="_blank" rel="noopener">Source</a>'
                    elif source_info.get('file'):
                        source_text = f'📑 {source_info["file"]}'
                    meta_text = f'📄 {article["word_count"]} words'
                    if source_text:
                        meta_text = f'{source_text} • {meta_text}'

                    accordion_html += f'<p class="meta">{meta_text}</p></div>\n'

                accordion_html += f'  </div>\n</div>\n'

            # Add uncategorized if any
            if uncategorized:
                accordion_html += f'<div class="accordion-item"><button class="accordion-header" onclick="toggleAccordion(this)"><span>📋 Uncategorized</span><span class="category-count">{len(uncategorized)}</span><span class="toggle-icon">▼</span></button>'
                accordion_html += f'<div class="accordion-content">\n'
                for article in sorted(uncategorized, key=lambda x: x["title"]):
                    source_info = article.get('source_info', {})
                    source_text = ""
                    if source_info.get('url'):
                        source_text = f'🔗 <a href="{source_info["url"]}" target="_blank" rel="noopener">Source</a> • '
                    elif source_info.get('file'):
                        source_text = f'📑 {source_info["file"]} • '
                    accordion_html += f'<div class="article-card"><h4>{article["title"]}</h4><p class="meta">{source_text}📄 {article["word_count"]} words</p></div>\n'
                accordion_html += f'</div></div>\n'

            # Build search index
            search_index = self._build_search_index(articles)

            # Build HTML
            html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Knowledge Base</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; color: #2c3e50; background: #f5f7fa; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{ background: white; border-radius: 12px; padding: 40px; margin-bottom: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 12px; color: #667eea; font-weight: 700; }}
        .header p {{ color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 20px; }}
        .stat {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 10px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2); }}
        .stat-number {{ font-size: 2.2em; font-weight: 700; margin-bottom: 8px; }}
        .stat-label {{ font-size: 0.95em; opacity: 0.9; }}
        .accordion-item {{ background: white; border-radius: 10px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.07); overflow: hidden; transition: box-shadow 0.3s ease; }}
        .accordion-item:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .accordion-header {{ width: 100%; padding: 18px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; cursor: pointer; font-size: 1.05em; font-weight: 600; display: flex; justify-content: space-between; align-items: center; gap: 12px; transition: all 0.3s ease; }}
        .accordion-header:hover {{ padding-left: 28px; }}
        .category-count {{ background: rgba(255,255,255,0.25); padding: 2px 8px; border-radius: 12px; font-size: 0.85em; font-weight: 500; }}
        .toggle-icon {{ font-size: 0.8em; transition: transform 0.3s ease; }}
        .accordion-item.active .toggle-icon {{ transform: rotate(180deg); }}
        .accordion-content {{ max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }}
        .accordion-item.active .accordion-content {{ max-height: 8000px; padding: 24px; }}
        .article-card {{ background: #f8fafb; padding: 18px; margin-bottom: 14px; border-radius: 8px; border-left: 3px solid #667eea; transition: all 0.2s ease; }}
        .article-card:hover {{ background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.06); transform: translateX(4px); }}
        .article-card h4 {{ color: #2c3e50; margin-bottom: 8px; font-size: 1.02em; font-weight: 600; }}
        .summary {{ color: #555; font-size: 0.95em; line-height: 1.5; margin-bottom: 8px; }}
        .meta {{ color: #999; font-size: 0.85em; }}
        .footer {{ text-align: center; color: #7f8c8d; margin-top: 50px; padding: 20px; font-size: 0.9em; }}
        .search-box {{ background: white; padding: 20px; margin-bottom: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .search-input {{ width: 100%; padding: 12px 16px; font-size: 1em; border: 2px solid #e0e0e0; border-radius: 8px; transition: border-color 0.3s ease; }}
        .search-input:focus {{ outline: none; border-color: #667eea; }}
        .search-results {{ display: none; margin-bottom: 30px; }}
        .search-results.active {{ display: block; }}
        .search-results-header {{ color: #667eea; font-weight: 600; margin-bottom: 15px; }}
        .search-result-item {{ background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .search-result-item h4 {{ color: #2c3e50; margin-bottom: 5px; }}
        .search-result-snippet {{ color: #666; font-size: 0.9em; margin-bottom: 8px; }}
        .search-result-meta {{ color: #999; font-size: 0.85em; }}
        .search-result-tags {{ margin-top: 5px; }}
        .tag {{ display: inline-block; background: #f0f0f0; padding: 2px 8px; border-radius: 4px; margin-right: 5px; font-size: 0.8em; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Knowledge Base</h1>
            <p>Organized, categorized knowledge</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{len(articles)}</div>
                    <div class="stat-label">Articles</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{sum(a['word_count'] for a in articles)}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(articles_by_tag)}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
        </div>

        <div class="search-box">
            <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search articles... (type to search)">
        </div>

        <div class="search-results" id="searchResults">
            <div class="search-results-header" id="resultsHeader"></div>
            <div id="resultsList"></div>
        </div>

        <div class="categories-section" id="categoriesSection">
            {accordion_html}
        </div>
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    <script>
        // Search index embedded in page
        const searchIndex = {search_index};

        // Toggle accordion
        function toggleAccordion(button) {{ button.parentElement.classList.toggle('active'); }}

        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const resultsHeader = document.getElementById('resultsHeader');
        const resultsList = document.getElementById('resultsList');
        const categoriesSection = document.getElementById('categoriesSection');

        function performSearch(query) {{
            if (!query.trim()) {{
                searchResults.classList.remove('active');
                categoriesSection.classList.add('active');
                return;
            }}

            query = query.toLowerCase();
            const results = searchIndex.filter(article => {{
                const title = article.title.toLowerCase();
                const summary = article.summary.toLowerCase();
                const tags = article.tags.map(t => t.toLowerCase()).join(' ');
                const content = article.content.toLowerCase();
                return title.includes(query) || summary.includes(query) || tags.includes(query) || content.includes(query);
            }});

            // Display results
            searchResults.classList.add('active');
            categoriesSection.classList.remove('active');

            resultsHeader.textContent = results.length + ' result' + (results.length !== 1 ? 's' : '') + ' found';
            resultsList.innerHTML = results.map(article => {{
                const sourceHtml = article.source_url
                    ? `🔗 <a href="${{article.source_url}}" target="_blank" rel="noopener">Source URL</a>`
                    : article.source_file ? `📑 ${{article.source_file}}` : '';
                return `
                    <div class="search-result-item">
                        <h4>${{article.title}}</h4>
                        <p class="search-result-snippet">${{article.summary}}</p>
                        <div class="search-result-meta">
                            📄 ${{article.word_count}} words
                            ${{sourceHtml ? ' • ' + sourceHtml : ''}}
                        </div>
                        ${{article.tags.length > 0 ? `<div class="search-result-tags">${{article.tags.map(t => `<span class="tag">${{t}}</span>`).join('')}}</div>` : ''}}
                    </div>
                `;
            }}).join('');
        }}

        searchInput.addEventListener('input', (e) => {{
            performSearch(e.target.value);
        }});

        // Initialize with categories showing
        document.querySelector('.accordion-item')?.classList.add('active');
    </script>
</body>
</html>"""
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            logger.info(f"✓ Exported to accordion HTML: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error exporting HTML: {e}")
            raise


    def export_html_old(self, articles: List[Dict[str, Any]] = None) -> Path:
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
