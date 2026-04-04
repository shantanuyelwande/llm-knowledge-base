import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from .metadata_tracker import MetadataTracker

logger = logging.getLogger(__name__)


class WikiMerger:
    """Handles merging of duplicate wiki articles"""
    
    def __init__(self, wiki_dir: Path, metadata_dir: Path):
        self.wiki_dir = wiki_dir
        self.metadata_tracker = MetadataTracker(wiki_dir, metadata_dir)
    
    def merge_articles(
        self,
        source_file: Path,
        target_file: Path,
        strategy: str = "append"
    ) -> bool:
        """
        Merge one wiki article into another
        
        Args:
            source_file: Article to merge FROM (will be archived)
            target_file: Article to merge INTO (will be updated)
            strategy: "append" (add at end), "prepend" (add at top), or "section" (create separate section)
        
        Returns:
            True if successful
        """
        if not source_file.exists() or not target_file.exists():
            logger.error(f"Files must exist: {source_file} and {target_file}")
            return False
        
        source_content = source_file.read_text(encoding="utf-8")
        target_content = target_file.read_text(encoding="utf-8")
        
        # Extract bodies (remove frontmatter)
        source_body = self._extract_body(source_content)
        target_body = self._extract_body(target_content)
        
        # Extract frontmatters
        source_fm = self.metadata_tracker.get_frontmatter_from_article(source_file)
        target_fm = self.metadata_tracker.get_frontmatter_from_article(target_file)
        
        if not source_fm or not target_fm:
            logger.error("Both articles must have frontmatter metadata")
            return False
        
        # Create merged body
        if strategy == "append":
            merged_body = target_body + self._create_merge_separator(source_file, source_fm) + source_body
        elif strategy == "prepend":
            merged_body = source_body + self._create_merge_separator(source_file, source_fm) + target_body
        elif strategy == "section":
            # Create section headers for each source
            source_title = source_fm.get("title", source_file.stem)
            target_title = target_fm.get("title", target_file.stem)
            merged_body = f"## From {target_title}\n\n{target_body}\n\n## From {source_title}\n\n{source_body}"
        else:
            logger.error(f"Unknown merge strategy: {strategy}")
            return False
        
        # Update target frontmatter
        updated_fm = self._merge_frontmatters(source_fm, target_fm, source_file)
        
        # Write merged content
        merged_content = updated_fm + merged_body
        target_file.write_text(merged_content, encoding="utf-8")
        
        # Archive source file
        archive_path = self.wiki_dir / ".archives" / f"{source_file.stem}.{datetime.now().isoformat()}.md"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_text(source_content, encoding="utf-8")
        
        # Remove source file (mark for deletion)
        # Note: in production, you might want to Git rm this
        logger.info(f"Merged {source_file.name} into {target_file.name}")
        logger.info(f"Archived original to {archive_path}")
        
        return True
    
    def _extract_body(self, content: str) -> str:
        """Extract article body (everything after frontmatter)"""
        if content.startswith("---"):
            end = content.find("\n---\n", 4)
            if end > 0:
                return content[end + 5:]
        return content
    
    def _extract_frontmatter(self, content: str) -> str:
        """Extract frontmatter block"""
        if content.startswith("---"):
            end = content.find("\n---\n", 4)
            if end > 0:
                return content[:end + 5]
        return "---\n---\n"
    
    def _create_merge_separator(self, source_file: Path, source_fm: dict) -> str:
        """Create a separator marking merged content"""
        source_title = source_fm.get("title", source_file.stem)
        source_file_ref = source_fm.get("source_file", "unknown")
        timestamp = datetime.now().isoformat()
        
        separator = f"""
---

> **Merged from:** {source_title}  
> **Original source:** {source_file_ref}  
> **Merged at:** {timestamp}

---

"""
        return separator
    
    def _merge_frontmatters(self, source_fm: dict, target_fm: dict, source_file: Path) -> str:
        """Merge two frontmatter blocks"""
        # Keep target title as primary
        title = target_fm.get("title", "Unknown")
        version = int(target_fm.get("version", 1)) + 1
        
        # Combine sources list
        sources = self._combine_sources(source_fm, target_fm)
        
        # Combine tags
        target_tags = target_fm.get("tags", "[]")
        source_tags = source_fm.get("tags", "[]")
        combined_tags = list(set([target_tags, source_tags]))
        
        timestamp = datetime.now().isoformat()
        
        frontmatter = f"""---
title: {title}
source_file: {target_fm.get('source_file', 'merged')}
source_hash: merged
compiled_at: {timestamp}
raw_file_updated: {timestamp}
version: {version}
sources:
"""
        
        for src in sources:
            frontmatter += f"  - file: {src['file']}\n"
            frontmatter += f"    hash: {src['hash']}\n"
            frontmatter += f"    added_at: {src['added_at']}\n"
        
        frontmatter += f"""tags: {combined_tags}
related_topics: []
merged_sources:
  - file: {source_file.name}
    merged_at: {timestamp}
---
"""
        
        return frontmatter
    
    def _combine_sources(self, source_fm: dict, target_fm: dict) -> list:
        """Combine source tracking lists"""
        sources = []
        
        # Add target sources
        if "sources" in target_fm:
            # Parse sources if string
            sources.append({
                "file": target_fm.get("source_file", "unknown"),
                "hash": target_fm.get("source_hash", "unknown"),
                "added_at": target_fm.get("compiled_at", "unknown"),
            })
        
        # Add source sources
        sources.append({
            "file": source_fm.get("source_file", "unknown"),
            "hash": source_fm.get("source_hash", "unknown"),
            "added_at": source_fm.get("compiled_at", "unknown"),
        })
        
        # Remove duplicates
        unique_sources = {}
        for src in sources:
            key = f"{src['file']}:{src['hash']}"
            if key not in unique_sources:
                unique_sources[key] = src
        
        return list(unique_sources.values())
