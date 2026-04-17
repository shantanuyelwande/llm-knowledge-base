import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)


class SimpleSearchEngine:
    """Simple yet effective search engine for the wiki"""

    def __init__(self, wiki_dir: Path, embeddings_service=None):
        self.wiki_dir = wiki_dir
        self.embeddings_service = embeddings_service
        self.index = self._build_index()
        self.backlinks_index: Dict[str, List[str]] = {}  # { topic: [referencing_articles] }
    
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
        """Search the wiki with keyword matching, reference count weighting, and optional semantic scoring"""
        query_words = self._extract_words(query)
        scored_files = {}

        # Keyword matching
        for word in query_words:
            if word in self.index:
                for file_path in self.index[word]:
                    scored_files[file_path] = scored_files.get(file_path, 0) + 1

        # Build results with connection strength weighting
        results = []
        for path, word_hits in scored_files.items():
            keyword_score = word_hits / len(query_words) if query_words else 0

            # Add reference count weighting
            file_stem = Path(path).stem
            ref_count = len(self.backlinks_index.get(file_stem, []))
            ref_score = min(ref_count / 10.0, 0.5)  # Cap contribution at 0.5

            # Composite relevance: weighted combination
            relevance = keyword_score + ref_score

            # Optional semantic reranking
            semantic_score = 0.0
            if self.embeddings_service and query_words:
                try:
                    semantic_score = self._compute_semantic_score(query, path)
                    # Update composite: 0.6 keyword + 0.2 reference + 0.2 semantic
                    relevance = 0.6 * keyword_score + 0.2 * ref_score + 0.2 * semantic_score
                except Exception as e:
                    logger.warning(f"Semantic scoring failed for {path}: {e}")

            results.append({
                "path": path,
                "relevance": relevance,
                "keyword_score": keyword_score,
                "reference_count": ref_count,
                "semantic_score": semantic_score,
                "content_preview": self._get_preview(path),
            })

        # Sort by relevance and limit
        results = sorted(results, key=lambda x: x["relevance"], reverse=True)[:limit]

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

    def set_backlinks(self, backlinks: Dict[str, List[str]]):
        """Inject backlinks index for reference-count weighting"""
        self.backlinks_index = backlinks

    def _compute_semantic_score(self, query: str, file_path: str) -> float:
        """Compute semantic similarity score between query and document"""
        if not self.embeddings_service:
            return 0.0

        try:
            # Embed query
            query_embedding = self.embeddings_service.embed_text(query)

            # Embed first 512 chars of document
            content = Path(file_path).read_text(encoding="utf-8")
            doc_text = content[:512] if len(content) > 512 else content
            doc_embedding = self.embeddings_service.embed_text(doc_text)

            # Compute cosine similarity
            similarity = self.embeddings_service.similarity(query_embedding, doc_embedding)
            return min(max(similarity, 0.0), 1.0)  # Clamp to [0, 1]
        except Exception as e:
            logger.debug(f"Semantic scoring error: {e}")
            return 0.0

    def refresh(self):
        """Rebuild the index"""
        self.index = self._build_index()
