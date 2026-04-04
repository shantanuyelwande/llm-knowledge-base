# Performance optimizations for search at scale

## Current Search Implementation

The system uses a simple word-indexed search that's effective for ~100-500 articles. Here's how to optimize for larger wikis.

### For Wikis > 1000 Articles

**Option 1: Database Indexing (Recommended)**

```python
# backend/app/core/advanced_search.py

import sqlite3
from pathlib import Path

class DatabaseSearchIndex:
    def __init__(self, db_path: str = "wiki_index.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE,
                title TEXT,
                content TEXT,
                indexed_at TIMESTAMP
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS word_index (
                id INTEGER PRIMARY KEY,
                word TEXT,
                doc_id INTEGER,
                frequency INTEGER,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            )
        """)
        
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_word ON word_index(word)")
        self.conn.commit()
    
    def index_document(self, path: str, content: str):
        # Index logic here
        pass
```

**Option 2: Embedding-Based Search**

For semantic search on large wikis:

```python
# backend/app/core/semantic_search.py

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class SemanticSearchIndex:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.documents = []
        self.vectors = None
    
    def index_documents(self, docs: List[str]):
        self.documents = docs
        self.vectors = self.vectorizer.fit_transform(docs)
    
    def search(self, query: str, k: int = 10):
        query_vector = self.vectorizer.transform([query])
        scores = (query_vector * self.vectors.T).toarray()[0]
        top_k = np.argsort(scores)[-k:][::-1]
        return top_k, scores[top_k]
```

### Caching Strategies

```python
# backend/app/core/cache.py

from functools import lru_cache
from typing import Tuple
import hashlib

class SearchCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, query: str) -> Optional[List[dict]]:
        hash_key = hashlib.md5(query.encode()).hexdigest()
        return self.cache.get(hash_key)
    
    def set(self, query: str, results: List[dict]):
        if len(self.cache) >= self.max_size:
            # Remove oldest entries
            self.cache.pop(next(iter(self.cache)))
        
        hash_key = hashlib.md5(query.encode()).hexdigest()
        self.cache[hash_key] = results
```

### Incremental Indexing

```python
# backend/app/services/incremental_index.py

import watchfiles
from pathlib import Path

class IncrementalIndexer:
    def __init__(self, wiki_dir: Path, search_index):
        self.wiki_dir = wiki_dir
        self.search_index = search_index
    
    async def watch_and_index(self):
        async for changes in watchfiles.awatch(self.wiki_dir):
            for change_type, file_path in changes:
                if file_path.endswith('.md'):
                    await self.reindex_document(file_path)
    
    async def reindex_document(self, file_path: str):
        content = Path(file_path).read_text()
        self.search_index.update_document(file_path, content)
```

## Recommendations by Wiki Size

| Wiki Size | Implementation | Performance |
|-----------|----------------|-------------|
| < 100 articles | Current simple search | ✓ Fast |
| 100-500 articles | Current simple search | ✓ Good |
| 500-2000 articles | Add database indexing | ✓ Fast |
| 2000+ articles | Embedding-based + cache | ✓ Excellent |

## Future: Fine-Tuning

Once your wiki reaches 50K+ words:

```python
# backend/app/services/finetuning.py

class WikiFineTuner:
    def prepare_dataset(self, wiki_dir: Path):
        """Prepare wiki content for model fine-tuning"""
        # Convert to supervised dataset format
        # Use Claude to generate Q&A pairs
        # Create JSONL for fine-tuning
        pass
    
    def finetune(self):
        """Fine-tune model on wiki data"""
        # Use Anthropic's batch API or fine-tuning endpoints
        # Reduces token usage and improves accuracy
        pass
```

This approach makes the model "aware" of your knowledge base at weights level, bypassing context window limitations.
