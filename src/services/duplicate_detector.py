import logging
from pathlib import Path
from typing import List, Dict, Optional
import json

try:
    from sentence_transformers import util, SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

from .metadata_tracker import MetadataTracker

logger = logging.getLogger(__name__)


class DuplicateDetector:
    """Detects and manages duplicate content in wiki"""
    
    def __init__(self, wiki_dir: Path, metadata_dir: Path, use_embeddings: bool = True):
        self.wiki_dir = wiki_dir
        self.metadata_tracker = MetadataTracker(wiki_dir, metadata_dir)
        self.use_embeddings = use_embeddings and EMBEDDINGS_AVAILABLE
        
        if self.use_embeddings:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Embeddings model loaded for duplicate detection")
            except Exception as e:
                logger.warning(f"Could not load embeddings model: {e}. Falling back to title-based detection.")
                self.use_embeddings = False
    
    def extract_title_from_article(self, wiki_file: Path) -> str:
        """Extract title from wiki article (from frontmatter or first heading)"""
        frontmatter = self.metadata_tracker.get_frontmatter_from_article(wiki_file)
        if frontmatter and "title" in frontmatter:
            return frontmatter["title"].lower()
        
        content = wiki_file.read_text(encoding="utf-8")
        # Skip frontmatter
        if content.startswith("---"):
            end = content.find("\n---\n", 4)
            if end > 0:
                content = content[end + 5:]
        
        # Find first heading
        for line in content.split("\n"):
            if line.startswith("#"):
                return line.replace("#", "").strip().lower()
        
        return wiki_file.stem.lower()
    
    def find_duplicates_by_title(self, similarity_threshold: float = 0.8) -> List[Dict]:
        """Find potential duplicates using title similarity"""
        titles = {}
        
        for wiki_file in self.wiki_dir.rglob("*.md"):
            title = self.extract_title_from_article(wiki_file)
            if title not in titles:
                titles[title] = []
            titles[title].append(wiki_file)
        
        duplicates = [{"title": title, "files": files} for title, files in titles.items() if len(files) > 1]
        return duplicates
    
    def find_duplicates_by_embedding(self, similarity_threshold: float = 0.75) -> List[Dict]:
        """Find potential duplicates using semantic similarity"""
        if not self.use_embeddings:
            logger.warning("Embeddings not available. Use find_duplicates_by_title instead.")
            return []
        
        # Get all wiki files
        wiki_files = list(self.wiki_dir.rglob("*.md"))
        if len(wiki_files) < 2:
            return []
        
        # Extract titles for embedding
        titles = [self.extract_title_from_article(f) for f in wiki_files]
        
        # Encode titles
        try:
            embeddings = self.model.encode(titles, convert_to_tensor=True)
        except Exception as e:
            logger.error(f"Error encoding titles: {e}")
            return []
        
        # Compute similarity matrix
        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
        
        # Find pairs with high similarity
        duplicates = []
        seen_pairs = set()
        
        for i in range(len(wiki_files)):
            for j in range(i + 1, len(wiki_files)):
                sim_score = similarity_matrix[i][j].item()
                
                if sim_score >= similarity_threshold:
                    pair = (min(i, j), max(i, j))
                    if pair not in seen_pairs:
                        duplicates.append({
                            "similarity": round(sim_score, 3),
                            "file1": str(wiki_files[i].relative_to(self.wiki_dir)),
                            "file2": str(wiki_files[j].relative_to(self.wiki_dir)),
                            "title1": titles[i],
                            "title2": titles[j],
                        })
                        seen_pairs.add(pair)
        
        return duplicates
    
    def find_duplicates(self, method: str = "hybrid") -> List[Dict]:
        """Find duplicates using specified method"""
        if method == "title":
            return self.find_duplicates_by_title()
        elif method == "embedding":
            return self.find_duplicates_by_embedding()
        elif method == "hybrid":
            # Try embeddings first, fall back to title
            if self.use_embeddings:
                return self.find_duplicates_by_embedding()
            else:
                return self.find_duplicates_by_title()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def generate_duplicate_report(self, output_file: Path) -> None:
        """Generate a report of all potential duplicates"""
        duplicates = self.find_duplicates()
        
        report = {
            "total_duplicates": len(duplicates),
            "method": "hybrid",
            "duplicates": duplicates,
        }
        
        output_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
        logger.info(f"Generated duplicate report: {output_file} ({len(duplicates)} potential duplicates)")
