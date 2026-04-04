import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class MetadataTracker:
    """Tracks source file changes, versions, and wiki metadata"""
    
    def __init__(self, wiki_dir: Path, metadata_dir: Path):
        self.wiki_dir = wiki_dir
        self.metadata_dir = metadata_dir
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file content"""
        if not file_path.exists():
            return "0" * 64
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def generate_frontmatter(
        self,
        title: str,
        source_file: str,
        source_content: str,
    ) -> str:
        """Generate YAML frontmatter for wiki article"""
        source_hash = self.compute_file_hash(Path(source_file))
        current_time = datetime.now().isoformat()
        
        frontmatter = f"""---
title: {title}
source_file: {source_file}
source_hash: {source_hash}
compiled_at: {current_time}
raw_file_updated: {current_time}
version: 1
sources:
  - file: {source_file}
    hash: {source_hash}
    added_at: {current_time}
tags: []
related_topics: []
---
"""
        return frontmatter
    
    def get_frontmatter_from_article(self, wiki_file: Path) -> Optional[Dict]:
        """Extract frontmatter from wiki article"""
        if not wiki_file.exists():
            return None
        
        content = wiki_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        
        try:
            # Find end of frontmatter
            end_marker = content.find("\n---\n", 4)
            if end_marker == -1:
                return None
            
            frontmatter_str = content[4:end_marker]
            frontmatter = {}
            
            for line in frontmatter_str.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
            
            return frontmatter
        except Exception as e:
            logger.error(f"Error parsing frontmatter from {wiki_file}: {e}")
            return None
    
    def check_if_source_updated(self, wiki_file: Path, source_file: Path) -> bool:
        """Check if raw source file has been updated since last compilation"""
        if not wiki_file.exists() or not source_file.exists():
            return True
        
        frontmatter = self.get_frontmatter_from_article(wiki_file)
        if not frontmatter:
            return True  # No metadata = assume updated
        
        old_hash = frontmatter.get("source_hash", "")
        new_hash = self.compute_file_hash(source_file)
        
        return old_hash != new_hash
    
    def update_frontmatter_on_recompile(
        self,
        wiki_file: Path,
        source_file: str,
        source_path: Path,
    ) -> None:
        """Update frontmatter when recompiling an article"""
        if not wiki_file.exists():
            return
        
        content = wiki_file.read_text(encoding="utf-8")
        frontmatter = self.get_frontmatter_from_article(wiki_file)
        
        if not frontmatter:
            return
        
        # Increment version
        version = int(frontmatter.get("version", "1")) + 1
        new_hash = self.compute_file_hash(source_path)
        current_time = datetime.now().isoformat()
        
        # Update timestamps
        new_frontmatter = f"""---
title: {frontmatter.get('title', 'Unknown')}
source_file: {source_file}
source_hash: {new_hash}
compiled_at: {current_time}
raw_file_updated: {current_time}
version: {version}
sources:
"""
        
        # Keep source history
        existing_sources = frontmatter.get("sources", [])
        if isinstance(existing_sources, str):
            # Parse from YAML list format if needed
            new_frontmatter += f"  - file: {source_file}\n    hash: {new_hash}\n    updated_at: {current_time}\n"
        
        new_frontmatter += f"""tags: {frontmatter.get('tags', '[]')}
related_topics: {frontmatter.get('related_topics', '[]')}
---
"""
        
        # Extract body (everything after frontmatter)
        body = content[content.find("\n---\n", 4) + 5:] if "\n---\n" in content[4:] else ""
        
        wiki_file.write_text(new_frontmatter + body, encoding="utf-8")
        logger.info(f"Updated frontmatter for {wiki_file}: version {version}")
    
    def get_stale_articles(self) -> List[Dict]:
        """Find wiki articles where source files have been updated"""
        stale = []
        
        for wiki_file in self.wiki_dir.rglob("*.md"):
            frontmatter = self.get_frontmatter_from_article(wiki_file)
            if not frontmatter:
                continue
            
            source_file = frontmatter.get("source_file")
            if not source_file:
                continue
            
            source_path = Path(source_file)
            if source_path.exists() and self.check_if_source_updated(wiki_file, source_path):
                stale.append({
                    "wiki_file": str(wiki_file.relative_to(self.wiki_dir)),
                    "source_file": source_file,
                    "version": int(frontmatter.get("version", 1)),
                    "compiled_at": frontmatter.get("compiled_at"),
                })
        
        return stale
    
    def export_metadata_log(self, output_file: Path) -> None:
        """Export metadata tracking log"""
        metadata_entries = []
        
        for wiki_file in self.wiki_dir.rglob("*.md"):
            frontmatter = self.get_frontmatter_from_article(wiki_file)
            if frontmatter:
                metadata_entries.append({
                    "wiki_file": str(wiki_file.relative_to(self.wiki_dir)),
                    **frontmatter
                })
        
        output_file.write_text(json.dumps(metadata_entries, indent=2), encoding="utf-8")
        logger.info(f"Exported metadata log to {output_file}")
