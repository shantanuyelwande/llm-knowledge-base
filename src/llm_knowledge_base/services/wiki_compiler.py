import logging
from pathlib import Path
from typing import Optional
from datetime import datetime
import urllib.parse

try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

from .metadata_tracker import MetadataTracker
from .change_logger import ChangeLogger

logger = logging.getLogger(__name__)


class WikiCompiler:
    """Compiles raw documents into a structured wiki with LLM assistance"""
    
    def __init__(self, raw_dir: Path, wiki_dir: Path, llm_client):
        self.raw_dir = raw_dir
        self.wiki_dir = wiki_dir
        self.llm_client = llm_client
        self.wiki_dir.mkdir(parents=True, exist_ok=True)

        # Initialize metadata tracker
        metadata_dir = self.wiki_dir.parent / ".metadata"
        self.metadata_tracker = MetadataTracker(self.wiki_dir, metadata_dir)

        # Initialize change logger
        self.change_logger = ChangeLogger(self.wiki_dir)
    
    def compile_document(
        self,
        source_path: str,
        title: Optional[str] = None,
    ) -> str:
        """Compile a single document into wiki format"""
        source_file = self.raw_dir / source_path
        
        if not source_file.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")
        
        # Extract content based on file type
        if source_file.suffix.lower() == ".pdf":
            if not PDF_SUPPORT:
                raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
            try:
                content = self._extract_pdf_text(source_file)
            except Exception as e:
                logger.error(f"Error extracting PDF {source_file}: {e}")
                raise
        else:
            try:
                content = source_file.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Error reading source file {source_file}: {e}")
                raise
        
        # Use LLM to process and summarize
        title = title or source_file.stem
        wiki_content = self._generate_wiki_entry(content, title, source_path)
        
        # Save to wiki directory
        wiki_file = self._get_wiki_path(title)
        wiki_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and needs update
        is_update = wiki_file.exists()
        
        # Add metadata frontmatter
        frontmatter = self.metadata_tracker.generate_frontmatter(title, source_path, content)
        full_content = frontmatter + wiki_content
        
        wiki_file.write_text(full_content, encoding="utf-8")

        action = "Updated" if is_update else "Compiled"
        logger.info(f"{action} {source_path} -> {wiki_file}")

        # Log the ingestion
        action_type = "update" if is_update else "ingest"
        self.change_logger.log_ingest(title, source_path, action_type)

        # Save updated index
        self.save_index()

        return str(wiki_file)
    
    def _generate_wiki_entry(self, content: str, title: str, source: str) -> str:
        """Generate a wiki entry using LLM"""
        prompt = f"""Convert this source material into a well-structured wiki article.

Title: {title}
Source: {source}

Content to convert:
{content}

Please create a markdown wiki entry that:
1. Starts with a clear heading and introduction
2. Uses markdown formatting with proper hierarchy
3. Includes a summary section at the top
4. Identifies key concepts that should link to other articles
5. Adds metadata at the end (tags, related topics, source)
6. Uses clear, encyclopedic language

Return only the complete markdown content."""
        
        system_prompt = """You are an expert at creating clear, well-organized wiki articles. 
You transform raw research materials, articles, and documents into coherent, interconnected wiki entries.
Use proper markdown formatting. Include backlinks using [[topic]] notation for related concepts."""
        
        wiki_content = self.llm_client.generate(
            prompt=prompt,
            system=system_prompt,
            max_tokens=2048,
        )
        
        return wiki_content
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF file"""
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page_num, page in enumerate(reader.pages):
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Failed to extract PDF: {e}")
            raise
    
    def _get_wiki_path(self, title: str) -> Path:
        """Convert title to wiki file path"""
        # Simple slug generation
        slug = title.lower().replace(" ", "-").replace("_", "-")
        # Remove invalid characters
        slug = "".join(c if c.isalnum() or c in "-" else "" for c in slug)
        return self.wiki_dir / f"{slug}.md"
    
    def compile_all(self) -> int:
        """Compile all documents in raw directory"""
        if not self.raw_dir.exists():
            logger.warning(f"Raw data directory not found: {self.raw_dir}")
            return 0

        # Support markdown, text, HTML, and PDF files
        supported_extensions = [".md", ".txt", ".html"]
        if PDF_SUPPORT:
            supported_extensions.append(".pdf")

        count = 0
        for file_path in self.raw_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    self.compile_document(str(file_path.relative_to(self.raw_dir)))
                    count += 1
                except Exception as e:
                    logger.error(f"Error compiling {file_path}: {e}")

        # Apply forward links after all compilation
        self.apply_forward_links()

        return count
    
    def generate_index(self) -> str:
        """Generate an index/table of contents for the wiki"""
        wiki_files = sorted(self.wiki_dir.rglob("*.md"))

        if not wiki_files:
            return "# Wiki Index\n\nNo articles yet."

        # Generate index structure
        index_content = "# Wiki Index\n\n"
        index_content += f"Last updated: {datetime.now().isoformat()}\n\n"

        # Organize by directory
        by_dir = {}
        for file_path in wiki_files:
            rel_path = file_path.relative_to(self.wiki_dir)
            dir_name = str(rel_path.parent) if rel_path.parent != Path(".") else "Root"

            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(file_path)

        for dir_name in sorted(by_dir.keys()):
            if dir_name != "Root":
                index_content += f"\n## {dir_name}\n\n"
            else:
                index_content += "\n## Articles\n\n"

            for file_path in sorted(by_dir[dir_name]):
                # Extract title from frontmatter or first heading
                title = self._extract_title_for_index(file_path)

                rel_link = file_path.relative_to(self.wiki_dir)
                index_content += f"- [{title}]({rel_link})\n"

        return index_content

    def _extract_title_for_index(self, file_path: Path) -> str:
        """Extract title from article for index (from frontmatter or first heading)"""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Try to get title from frontmatter
            if content.startswith("---"):
                end = content.find("\n---\n", 4)
                if end > 0:
                    frontmatter = content[4:end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("title:"):
                            return line.replace("title:", "").strip()
                    # Frontmatter exists but no title, look for first heading after
                    body = content[end + 5:]
                else:
                    body = content
            else:
                body = content

            # Find first heading in body
            for line in body.split("\n"):
                if line.startswith("#"):
                    return line.replace("#", "").strip()

            # Fallback to filename
            return file_path.stem
        except:
            return file_path.stem

    def save_index(self) -> Path:
        """Generate and save index to index.md"""
        index_content = self.generate_index()
        index_file = self.wiki_dir / "index.md"
        index_file.write_text(index_content, encoding="utf-8")
        logger.info(f"Saved index to {index_file}")
        return index_file
    
    def generate_backlinks_index(self) -> dict:
        """Generate backlinks between articles"""
        backlinks = {}

        for file_path in self.wiki_dir.rglob("*.md"):
            content = file_path.read_text(encoding="utf-8")
            # Extract [[topic]] references
            import re
            links = re.findall(r'\[\[([^\]|]+)', content)

            for link in links:
                if link not in backlinks:
                    backlinks[link] = []
                backlinks[link].append(str(file_path.relative_to(self.wiki_dir)))

        return backlinks

    def apply_forward_links(self) -> dict:
        """Apply forward links: write 'Referenced by' sections into linked articles"""
        import re
        backlinks = self.generate_backlinks_index()

        updated = []
        broken_links = []

        for target_topic, referencing_articles in backlinks.items():
            # Resolve target topic to a wiki file path
            target_file = self._get_wiki_path(target_topic)

            if not target_file.exists():
                broken_links.append(target_topic)
                continue

            # Read target file content
            content = target_file.read_text(encoding="utf-8")

            # Remove existing "Referenced by" section if present
            content = re.sub(r'\n## Referenced by\n.*?(?=\n##|\Z)', '', content, flags=re.DOTALL)

            # Build new "Referenced by" section
            referenced_by_section = "\n## Referenced by\n\n"
            for article_path in sorted(referencing_articles):
                article_name = Path(article_path).stem
                referenced_by_section += f"- [[{article_name}]]\n"

            # Write updated content
            updated_content = content.rstrip() + referenced_by_section
            target_file.write_text(updated_content, encoding="utf-8")
            updated.append(target_topic)
            logger.info(f"Applied forward links to {target_topic} ({len(referencing_articles)} references)")

        # Log forward links operation
        self.change_logger.log_forward_links(len(updated), len(broken_links))

        # Save updated index after forward links applied
        self.save_index()

        return {
            "updated": updated,
            "broken_links": broken_links,
            "total_updated": len(updated),
            "total_broken": len(broken_links),
        }
