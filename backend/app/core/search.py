import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)


class SimpleSearchEngine:
    """Simple yet effective search engine for the wiki"""
    
    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir
        self.index = self._build_index()
    
    def _build_index(self) -> Dict[str, List[str]]:
        """Build a simple word-to-files index"""
        index = {}
        
        if not self.wiki_dir.exists():
            return index
        
        for md_file in self.wiki_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                words = self._extract_words(content)
                
                for word in set(words):
                    if word not in index:
                        index[word] = []
                    index[word].append(str(md_file))
            except Exception as e:
                logger.error(f"Error indexing {md_file}: {e}")
        
        return index
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract and normalize words from text"""
        words = []
        for word in text.lower().split():
            # Simple word extraction (remove punctuation)
            clean_word = "".join(c for c in word if c.isalnum())
            if len(clean_word) > 2:  # Skip very short words
                words.append(clean_word)
        return words
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search the wiki"""
        query_words = self._extract_words(query)
        scored_files = {}
        
        for word in query_words:
            if word in self.index:
                for file_path in self.index[word]:
                    scored_files[file_path] = scored_files.get(file_path, 0) + 1
        
        # Sort by score and limit
        results = [
            {
                "path": path,
                "relevance": score / len(query_words) if query_words else 0,
                "content_preview": self._get_preview(path),
            }
            for path, score in sorted(
                scored_files.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
        ]
        
        return results
    
    def _get_preview(self, file_path: str, char_limit: int = 200) -> str:
        """Get a preview of file content"""
        try:
            content = Path(file_path).read_text(encoding="utf-8")
            # Get first paragraph
            preview = content.split("\n\n")[0]
            if len(preview) > char_limit:
                preview = preview[:char_limit] + "..."
            return preview
        except Exception as e:
            logger.error(f"Error getting preview for {file_path}: {e}")
            return ""
    
    def refresh(self):
        """Rebuild the index"""
        self.index = self._build_index()
