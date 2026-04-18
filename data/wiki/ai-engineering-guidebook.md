---
title: AI Engineering Guidebook
source_file: AI Engineering Guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:04:07.199082
raw_file_updated: 2026-04-17T21:04:07.199082
version: 1
sources:
  - file: AI Engineering Guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:04:07.199082
tags: []
related_topics: []
backlinked_by: []
---
# AI Engineering: System Design Patterns for LLMs, RAG, and Agents

## Summary

AI Engineering is a comprehensive discipline focused on designing, building, and deploying intelligent systems powered by large language models (LLMs). It encompasses the complete lifecycle from model selection and fine-tuning through [[Retrieval-Augmented Generation|RAG]], agent design, optimization, evaluation, and production deployment. This guidebook covers system design patterns, architectural decisions, and practical implementation strategies for creating robust, scalable AI applications.

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Key Components](#key-components)
4. [Development Lifecycle](#development-lifecycle)
5. [Advanced Topics](#advanced-topics)
6. [Deployment and Operations](#deployment-and-operations)

---

## Overview

AI Engineering represents a shift from traditional machine learning development toward building practical, production-grade systems that leverage the capabilities of large language models. Unlike pure data science, which focuses on statistical analysis and model training, AI Engineering emphasizes:

- **System design** over isolated models
- **Practical constraints** (latency, cost, reliability) over raw accuracy
- **User-centric architecture** over benchmark performance
- **Operational excellence** over theoretical optimality

The field emerged because deploying LLMs requires solving unique challenges that don't exist in traditional ML: managing variable-length outputs, handling context windows, optimizing token generation, and orchestrating complex multi-step workflows.

---

## Core Concepts

### Large Language Models (LLMs)

[[Large Language Models|LLMs]] are [[Transformer]]-based neural networks trained on massive text corpora to predict the next token in a sequence. Through this process, they acquire the ability to understand, generate, and reason with human language.

**Key characteristics:**

- **Foundation**: Trained on diverse internet-scale text data (books, articles, code, conversations)
- **Mechanism**: Predict the next token by calculating conditional probabilities based on previous tokens
- **Scale**: Measured by parameter count (billions to trillions), training data size, and computational resources
- **Emergence**: Larger models develop unexpected capabilities like reasoning, multi-step planning, and tool use

**What makes an LLM "large":**

The "large" in LLM refers to three dimensions:
- **Number of parameters**: Billions or trillions of learned values
- **Training data**: Massive corpora spanning multiple domains
- **Compute**: Enormous computational resources (distributed across many GPUs)

These dimensions directly correlate with model capabilities. Larger models demonstrate better instruction-following, multi-step reasoning, and generalization to unseen tasks.

### How LLMs Generate Text

LLMs generate text through an autoregressive process where each token is predicted based on all previous tokens. The process relies on **conditional probability**: given the context so far, what is the most likely next token?

**The generation process:**

1. Encode input text into tokens
2. Pass through transformer layers to get probability distribution over vocabulary
3. Sample or select next token according to generation strategy
4. Append to context and repeat

**Temperature and randomness:**

- **Low temperature** (~0): Deterministic, greedy selection of highest probability tokens
- **High temperature** (0.7-1.0): More random sampling, increased diversity and creativity
- **Temperature tuning**: Critical for balancing coherence with diversity

### 7 LLM Generation Parameters

Fine-grained control over LLM output comes through generation parameters:

1. **Max tokens**: Hard cap on output length
2. **Temperature**: Controls randomness in sampling
3. **Top-k**: Restrict sampling to k most probable tokens
4. **Top-p (nucleus sampling)**: Sample from smallest set of tokens covering cumulative probability p
5. **Frequency penalty**: Reduce likelihood of repeated tokens
6. **Presence penalty**: Encourage novel tokens not yet in output
7. **Stop sequences**: Custom tokens that halt generation

### 4 LLM Text Generation Strategies

Different decoding strategies produce different output characteristics:

1. **Greedy**: Always select highest probability token (fast, repetitive)
2. **Multinomial sampling**: Sample from probability distribution (diverse, less coherent)
3. **Beam search**: Keep top-k partial sequences, explore tree of possibilities (better global optimization)
4. **Contrastive search**: Balance probability and diversity to prevent repetition loops

---

## Key Components

### Training LLMs from Scratch

The standard training pipeline involves four stages:

#### 1. Pre-training

- **Objective**: Learn language fundamentals on massive corpora
- **Data**: Internet-scale text (books, articles, code, conversations)
- **Task**: Next-token prediction on unlabeled data
- **Result**: Model understands grammar, facts, reasoning patterns, but isn't conversational

#### 2. Instruction Fine-tuning (IFT)

- **Objective**: Teach the model to follow instructions and respond conversationally
- **Data**: Instruction-response pairs (can be synthetic or human-created)
- **Task**: Supervised fine-tuning to match expected outputs
- **Result**: Model can answer questions, summarize, write code, etc.

#### 3. Preference Fine-tuning (PFT) / RLHF

- **Objective**: Align model outputs with human preferences
- **Data**: Human feedback on response pairs ("which response is better?")
- **Algorithm**: [[RLHF|Reinforcement Learning with Human Feedback]] using PPO
- **Result**: Model learns nuanced alignment without explicit "correct" answers

#### 4. Reasoning Fine-tuning

- **Objective**: Improve performance on tasks with verifiable correct answers
- **Data**: Problems with ground-truth solutions (math, logic, code)
- **Signal**: Automatic reward based on correctness, not human judgment
- **Method**: [[GRPO|Group Relative Policy Optimization]] or similar RL algorithms
- **Result**: Specialized reasoning capabilities for specific domains

### Prompt Engineering

[[Prompt Engineering]] is the practice of designing inputs to guide LLM behavior without modifying model weights. It's the fastest, lowest-effort way to improve outputs.

**3 prompting techniques for reasoning:**

1. **Chain of Thought (CoT)**: Ask model to reason step-by-step before answering
2. **Self-Consistency**: Generate multiple reasoning paths, select most common answer
3. **Tree of Thoughts (ToT)**: Explore multiple reasoning branches at each step, evaluate paths

**Bonus: Attentive Reasoning Queries (ARQ)**

Instead of free-form reasoning, guide models through explicit domain-specific questions encoded in JSON schemas. This maintains alignment and creates auditable reasoning steps.

**JSON Prompting**

Structured JSON outputs eliminate ambiguity and ensure consistent formatting. Models are trained on massive amounts of structured API data, so they respond with precision when given JSON schema.

### Fine-tuning Techniques

Traditional full-model fine-tuning is impractical for LLMs due to memory and computational costs. Instead, efficient techniques reduce trainable parameters while preserving performance:

#### 1. LoRA (Low-Rank Adaptation)

Decompose weight update matrices into low-rank factors A and B, training only these small matrices instead of full weights. Reduces trainable parameters by 99%+ while maintaining performance.

#### 2. LoRA-FA (Frozen-A)

Freeze matrix A, train only matrix B to reduce activation memory requirements.

#### 3. VeRA (Vector-based Rank Adaptation)

Share frozen random matrices across layers, train only small layer-specific scaling vectors.

#### 4. Delta-LoRA

Update weight matrices by adding deltas between consecutive training steps' low-rank products.

#### 5. LoRA+

Use higher learning rate for matrix B than matrix A for more optimal convergence.

**Other variants**: QLoRA (quantized), DoRA (weight-decomposed), LoRA-drop (selective layer application)

### Generating Fine-tuning Datasets

**Instruction Fine-tuning Dataset (IFT)** requires instruction-response pairs. These can be generated synthetically using frameworks like [[Distilabel]]:

1. Start with seed instructions
2. Generate multiple responses using different LLMs
3. Use a judge LLM to rank responses
4. Pair best response with instruction
5. Result: Synthetic dataset for fine-tuning

### SFT vs RFT

- **Supervised Fine-Tuning (SFT)**: Train on static labeled dataset of prompt-completion pairs
- **Reinforcement Fine-Tuning (RFT)**: Use online rewards to train from model-generated outputs

Choose based on:
- Have labeled data? → SFT
- Task verifiable but no labels? → RFT (e.g., GRPO for math)
- Task requires human judgment? → RLHF