---
title: AI Engineering Guidebook
source_file: AI Engineering Guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:25:16.103173
raw_file_updated: 2026-04-17T20:25:16.103173
version: 1
sources:
  - file: AI Engineering Guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:25:16.103173
tags: []
related_topics: []
backlinked_by: []
---
# AI Engineering Guidebook

## Summary

The **AI Engineering Guidebook** is a comprehensive 2025 guide covering the architecture, design patterns, and practical implementation of modern AI systems. It provides detailed coverage of [[Large Language Models]], [[Retrieval-Augmented Generation]], [[AI Agents]], [[Model Fine-tuning]], and production deployment strategies for building scalable, reliable AI applications.

---

## Overview

The AI Engineering Guidebook is an open-source resource created by Akshay Pachaar and Avi Chawla from DailyDoseofDS.com. It serves as a practical manual for building production-grade AI systems using [[LLMs]], agents, and [[Retrieval-Augmented Generation]] (RAG) architectures. The guide emphasizes system design patterns, implementation details, and real-world deployment considerations rather than theoretical foundations alone.

The total reading time is approximately 20 hours, though readers are encouraged to use the included assessment tool (https://bit.ly/ai-engg-assessment) to identify the most relevant chapters for their expertise level.

---

## Core Topics

### 1. Large Language Models (LLMs)

[[LLMs]] form the foundation of modern AI systems. The guidebook covers:

- **What is an LLM**: LLMs are [[Transformer]]-based neural networks trained on massive text corpora to predict the next [[Token]] in a sequence. Through this process, they acquire the ability to understand, generate, and reason with human language.

- **Building LLMs**: The architecture includes:
  - [[Tokenization]] - breaking text into manageable units
  - [[Transformer Layers]] - stacked neural network layers that refine understanding
  - [[Positional Encoding]] - providing sequence order information
  - [[Distributed Training]] - parallel processing across multiple GPUs

- **Training LLMs**: A four-stage process:
  1. **Pre-training** - learning from massive corpora to predict next tokens
  2. **Instruction Fine-tuning** - training on instruction-response pairs for conversational ability
  3. **Preference Fine-tuning (PFT)** - using [[RLHF]] to align with human preferences
  4. **Reasoning Fine-tuning** - optimizing for tasks with verifiable correct answers

- **How LLMs Work**: LLMs generate text through [[Conditional Probability]] estimation. They calculate the probability distribution over possible next tokens given previous context, then sample from this distribution. [[Temperature]] controls randomness in generation.

- **Generation Parameters**: Seven key controls:
  - [[Max Tokens]] - output length limit
  - [[Temperature]] - randomness level
  - [[Top-K Sampling]] - restricts to top K probable tokens
  - [[Top-P Sampling]] - nucleus sampling with cumulative probability threshold
  - [[Frequency Penalty]] - reduces token repetition
  - [[Presence Penalty]] - encourages novel tokens
  - [[Stop Sequences]] - custom termination tokens

- **Text Generation Strategies**:
  - [[Greedy Decoding]] - selects highest probability token
  - [[Multinomial Sampling]] - samples from probability distribution
  - [[Beam Search]] - explores multiple paths to maximize sequence probability
  - [[Contrastive Search]] - balances fluency with diversity
  - [[SLED]] - leverages logits across all layers for factual accuracy

- **Distillation**: Training smaller models using larger ones:
  - [[Soft-label Distillation]] - matching probability distributions
  - [[Hard-label Distillation]] - matching final token outputs
  - [[Co-distillation]] - training teacher and student simultaneously

- **Running LLMs Locally**: Tools include [[Ollama]], [[LMStudio]], [[vLLM]], and [[LlamaCPP]]

- **Mixture of Experts (MoE)**: Alternative architecture using specialized "experts" that activate selectively, enabling larger capacity with lower compute costs

### 2. Prompt Engineering

[[Prompt Engineering]] is the steering wheel for LLMs - small adjustments completely shift output direction without changing model weights.

- **3 Prompting Techniques for Reasoning**:
  - [[Chain of Thought]] - nudging models to reason step-by-step
  - [[Self-Consistency]] - majority voting over multiple reasoning paths
  - [[Tree of Thoughts]] - exploring multiple reasoning branches and selecting optimal paths
  - [[ARQ]] (Attentive Reasoning Queries) - guided domain-specific reasoning through structured JSON queries

- **Verbalized Sampling**: Training-free technique to recover diversity lost during [[RLHF]] alignment by prompting models to verbalize probability distributions

- **JSON Prompting**: Structured output format that leverages LLM training on APIs and web data, ensuring consistent, predictable results

### 3. Fine-tuning

[[Fine-tuning]] adapts pre-trained models to specific tasks. Traditional approaches are infeasible for LLMs due to their massive parameter counts.

- **Issues with Traditional Fine-tuning**: 
  - GPT-3's 175B parameters require 350GB of memory
  - Scales poorly for multiple users
  - Storage and infrastructure costs become prohibitive

- **5 LLM Fine-tuning Techniques**:
  1. [[LoRA]] (Low-Rank Adaptation) - adds trainable low-rank matrices alongside frozen weights
  2. [[LoRA-FA]] - freezes matrix A, updates only matrix B
  3. [[VeRA]] - uses frozen random shared matrices, trains only scaling vectors
  4. [[Delta-LoRA]] - updates weight differences between training steps
  5. [[LoRA+]] - applies higher learning rate to matrix B

- **Advanced Variants**:
  - [[LoRA-drop]] - removes LoRA from low-impact layers
  - [[QLoRA]] - combines LoRA with quantization for memory efficiency
  - [[DoRA]] - decomposes weights into magnitude and direction

- **Instruction Fine-tuning Dataset Generation**: Using [[Distilabel]] framework to create synthetic instruction-response pairs via LLM collaboration

- **SFT vs RFT**:
  - [[SFT]] (Supervised Fine-tuning) - uses static labeled data
  - [[RFT]] (Reinforcement Fine-tuning) - uses online reward signals without labels

- **GRPO Implementation**: [[Group Relative Policy Optimization]] for reasoning-focused fine-tuning using deterministic reward functions

### 4. Retrieval-Augmented Generation (RAG)

[[RAG]] enables LLMs to access external knowledge without retraining, solving the knowledge cutoff problem.

- **Core Components**:
  - [[Vector Databases]] - store unstructured data as embeddings
  - [[Embeddings]] - numerical representations capturing semantic meaning
  - [[Similarity Search]] - finding relevant context via approximate nearest neighbor search

- **RAG Workflow** (8 steps):
  1. Chunk external documents
  2. Generate embeddings using embedding models
  3. Store in vector database with metadata
  4. Embed user query with same model
  5. Retrieve k most similar chunks
  6. Re-rank chunks using cross-encoders
  7. Combine with original query for LLM
  8. Generate final response

- **5 Chunking Strategies**:
  1. [[Fixed-size Chunking]] - uniform segments with overlap
  2. [[Semantic Chunking]] - groups by semantic similarity
  3. [[Recursive Chunking]] - hierarchical subdivision
  4. [[Document Structure-based Chunking]] - respects document hierarchy
  5. [[LLM-based Chunking]] - uses LLM to identify meaningful chunks

- **RAG Decision Framework**: Choose based on:
  - External knowledge requirement
  - Model adaptation needed
  - Vocabulary/style changes

- **8 RAG Architectures**:
  1. [[Naive RAG]] - pure vector similarity
  2. [[Multimodal RAG]] - handles multiple data types
  3. [[HyDE]] - generates hypothetical answers before retrieval
  4. [[Corrective RAG]] - validates against trusted sources
  5. [[Graph RAG]] - converts content to knowledge graphs
  6. [[Hybrid RAG]] - combines dense and graph retrieval
  7. [[Adaptive RAG]] - dynamically decides retrieval needs
  8. [[Agentic RAG]] - uses agents for planning and reasoning

- **Advanced Techniques**:
  - [[Agentic RAG]] - agents decide if, what, and where to retrieve
  - [[HyDE]] - improves retrieval by generating hypothetical documents
  - [[REFRAG]] - compresses and filters context at vector level
  - [[CAG]] (Cache-Aug