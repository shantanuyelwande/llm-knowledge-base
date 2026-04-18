---
title: rag AI Engineer System Design 8nterviee
source_file: rag AI Engineer System Design 8nterviee.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:26:55.042735
raw_file_updated: 2026-04-17T20:26:55.042735
version: 1
sources:
  - file: rag AI Engineer System Design 8nterviee.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:26:55.042735
tags: []
related_topics: []
backlinked_by: []
---
# AI Engineer System Design Interview Guide: RAG & LLM Systems

## Summary

This comprehensive interview preparation guide covers Retrieval-Augmented Generation (RAG), [[Large Language Model]] system design, and production AI infrastructure. Authored by Lamhot Siagian, it provides foundational concepts through advanced production-level design patterns, with emphasis on [[retrieval quality]], [[hallucination reduction]], [[evaluation metrics]], and enterprise-scale deployment considerations.

---

## Table of Contents

1. [[#overview|Overview]]
2. [[#rag-fundamentals|RAG Fundamentals]]
3. [[#advanced-retrieval-design|Advanced Retrieval Design]]
4. [[#production-architecture|Production Architecture]]
5. [[#evaluation-and-metrics|Evaluation and Metrics]]
6. [[#hallucination-and-reliability|Hallucination and Reliability]]
7. [[#performance-and-scaling|Performance and Scaling]]
8. [[#data-pipeline-and-ingestion|Data Pipeline and Ingestion]]
9. [[#security-and-enterprise-rag|Security and Enterprise RAG]]
10. [[#agentic-rag|Agentic RAG]]
11. [[#prompt-engineering-for-rag|Prompt Engineering for RAG]]
12. [[#observability-and-monitoring|Observability and Monitoring]]
13. [[#deployment-and-llmops|Deployment and LLMOps]]
14. [[#inference-optimization|Inference Optimization]]

---

## Overview

This guide is designed for senior-level AI engineering interviews, with particular focus on [[RAG]] system design and production deployment. The 2026 edition expands coverage to include:

- End-to-end RAG architecture and framework selection
- [[Hallucination]] mitigation strategies
- [[Evaluation frameworks]] for retrieval and generation
- [[LLM inference optimization]] and [[KV cache]] management
- [[Multi-tenant]] security and access control
- [[Observability]] and monitoring for production systems
- [[Agentic workflows]] and tool orchestration

The material progresses from foundational concepts through production-level design reasoning, with each chapter containing core concepts followed by interview-style questions with sample answers.

---

## RAG Fundamentals

### Core Concept: What is RAG?

[[Retrieval-Augmented Generation]] combines information retrieval with [[language model]] generation. Rather than relying solely on a model's parametric knowledge, RAG systems retrieve relevant documents and use them as context for generating answers.

### RAG vs Fine-tuning vs Long-context LLMs

| Approach | Best For | Limitations |
|----------|----------|-------------|
| **RAG** | Dynamic knowledge, grounding, citations | Retrieval latency, pipeline complexity |
| **Fine-tuning** | Style, tone, task format, domain-specific behavior | Expensive, cannot update knowledge easily |
| **Long-context LLMs** | Short-lived context (200K tokens) | Cost, slow, no fresh knowledge |

**Decision framework:**
- Use RAG when knowledge changes frequently, citations are required, or data is too large to fine-tune
- Use fine-tuning for behavioral adaptation and style transfer
- Use long-context when context is static and self-contained

### Embeddings: Dense vs Sparse vs Hybrid

#### Dense Embeddings
Neural networks map text to continuous vectors (typically 384–1536 dimensions). Examples: [[text-embedding-3-large]], [[BGE]], [[E5]]. Strengths: semantic understanding, synonym handling. Weaknesses: expensive to compute, struggle with rare terms.

#### Sparse Embeddings
Term-frequency representations like [[BM25]] and [[TF-IDF]]. Strengths: exact keyword matching, interpretable, fast. Weaknesses: no semantic understanding.

#### Hybrid Embeddings
Combine dense and sparse via [[Reciprocal Rank Fusion]] (RRF). Achieves best precision and recall by leveraging both semantic and lexical signals.

### Chunking Strategies

- **Fixed-size**: Split at N characters with overlap. Simple and predictable but risks mid-sentence splits.
- **Recursive character**: Split on priority order (`["\n\n", "\n", ". "]`). Best default strategy.
- **Semantic**: Embed sentences; split where similarity drops. Produces coherent chunks but slower.
- **Document-aware**: Parse Markdown/HTML structure; keep sections intact.
- **Parent-child**: Small chunks for retrieval, large parent chunks returned for context. Balances precision and context.

### Vector Databases

| Database | Strengths | Index Type | Use Case |
|----------|-----------|-----------|----------|
| **FAISS** | In-memory, very fast | HNSW, IVF | Research, single node |
| **Pinecone** | Managed, serverless | Proprietary | SaaS, low ops |
| **Chroma** | Easy local development | HNSW | Prototypes |
| **Weaviate** | Hybrid search native | HNSW + BM25 | Production enterprise |
| **Qdrant** | Fast, Rust-native | HNSW | High throughput |
| **pgvector** | PostgreSQL extension | IVFFlat | Existing PG users |

### Similarity Search: Cosine vs Dot Product

**Cosine Similarity**: $\text{cosine}(a, b) = \frac{a \cdot b}{|a||b|}$

Measures angle only; removes magnitude bias. Use when vectors are not normalized.

**Dot Product**: $a \cdot b$

Measures both direction and magnitude. Equivalent to cosine similarity when vectors are L2-normalized, but faster.

**Practical guidance**: Normalize all embeddings at index time; then use dot product.

### When RAG Fails

1. **Retrieval failure**: Wrong chunks returned; answer not in index
2. **Chunk size mismatch**: Answer spans multiple chunks; none sufficient alone
3. **Semantic gap**: Query language differs from document language
4. **Multi-hop reasoning**: Answer requires combining facts across many documents
5. **Temporal issues**: Index is stale; retrieved documents outdated
6. **LLM ignores context**: Model uses parametric knowledge instead of retrieved context

**Fix strategy**: Evaluate [[retrieval metrics]] and [[generation metrics]] separately. If recall is low, fix chunking and embeddings. If [[faithfulness]] is low despite good retrieval, fix the prompt.

### Embedding Model Selection

Key factors affecting retrieval quality:

- **Dimensionality**: Higher dims (1536 vs 384) more expressive but slower and costlier
- **Training data**: General-purpose vs domain-trained models
- **Pooling strategy**: CLS token, mean pooling, weighted mean
- **Max context length**: Some models cap at 512 tokens

**Domain-specific approach:**
1. Start with text-embedding-3-large or BGE-large as baseline
2. Evaluate on domain test set using [[MTEB]] leaderboard metrics
3. If recall is poor, fine-tune on domain triplets (query, positive, hard negative)
4. Use [[matryoshka representation learning]] (MRL) embeddings for dimension flexibility

### Chunk Size Tuning

**Too small** (50–100 tokens):
- Chunks lack context; embeddings are noisy
- Answer may span multiple chunks
- Higher retrieval cost

**Too large** (2000+ tokens):
- Embedding averages over too much content
- Irrelevant content dilutes signal
- Larger context window needed in generation

**Tuning approach:**
1. Start at 512 tokens with 64-token overlap
2. Measure [[Context Precision@K]]
3. Grid-search on labeled eval set
4. Use parent-child chunking: 400-token child for retrieval, 1600-token parent for generation

---

## Advanced Retrieval Design

### Hybrid Retrieval: BM25 + Vector Search

Hybrid retrieval combines [[dense semantic search]] with [[sparse BM25]] keyword search, merged via [[Reciprocal Rank Fusion]]:

$$\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + r(d)}, \quad k = 60$$

**Implementation pattern:**
```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Sparse retriever (BM25)
bm25 = BM25Retriever.from_documents(docs)
bm25.k = 10

# Dense retriever (vector store)
dense