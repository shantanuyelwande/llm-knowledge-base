import logging
from typing import List
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class EmbeddingsService:
    """Generate and manage embeddings for semantic search using sentence-transformers"""
    
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.enabled = True
            logger.info("✓ Embeddings service initialized with all-MiniLM-L6-v2")
        except ImportError:
            self.enabled = False
            logger.warning("⚠ sentence-transformers not installed. Embeddings disabled. Run: pip install sentence-transformers")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not self.enabled:
            return []
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not self.enabled or not texts:
            return [[] for _ in texts]
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return [e.tolist() if hasattr(e, 'tolist') else list(e) for e in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [[] for _ in texts]
    
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        if not embedding1 or not embedding2:
            return 0.0
        try:
            from sentence_transformers.util import cos_sim
            import torch
            sim = cos_sim(torch.tensor([embedding1]), torch.tensor([embedding2]))
            return float(sim[0][0])
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
