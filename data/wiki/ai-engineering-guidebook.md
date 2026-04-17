---
title: AI Engineering Guidebook
source_file: AI Engineering Guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:30:36.583990
raw_file_updated: 2026-04-05T20:30:36.583990
version: 1
sources:
  - file: AI Engineering Guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:30:36.583990
tags: ["AI Engineering", "Large Language Models", "Production Deployment", "System Design", "AI Operations"]
related_topics: []
backlinked_by: []

---
# AI Engineering Guidebook

## Summary

The AI Engineering Guidebook is a comprehensive resource covering the complete lifecycle of building production-grade AI systems. It provides practical guidance on [[Large Language Models]], [[Retrieval-Augmented Generation]], [[Fine-tuning]], [[AI Agents]], and deployment strategies. The guidebook emphasizes that successful AI engineering requires not just model capability, but systematic orchestration of context, careful evaluation, and robust deployment infrastructure.

## Overview

AI engineering has evolved from simple prompt-based interactions to complex, multi-component systems requiring careful design and optimization. This guidebook covers the essential patterns, techniques, and tools needed to build reliable, scalable AI applications in production environments.

The core philosophy is straightforward: **context quality matters more than model capability**. As models improve, the bottleneck shifts from the model itself to the systems and infrastructure surrounding it.

## Core Topics

### [[Large Language Models]] (LLMs)

#### What is an LLM?

A [[Large Language Model]] is a [[Transformer]]-based neural network trained on massive text corpora to predict the next token in a sequence. Through this process, it acquires the ability to understand, generate, and reason with human language.

LLMs work by:
- Breaking text into small units called [[tokens]]
- Predicting the next token based on previous tokens
- Repeating this process to generate complete responses
- Learning from patterns across billions of parameters

#### Why LLMs Matter

Before LLMs, AI systems were task-specific:
- A translation system handled only translation
- A summarizer knew only summarization
- Each new problem required a new model

LLMs changed this paradigm by learning general language structure across millions of domains. A single model can now answer questions, write code, analyze text, and more—without explicit programming for each task.

#### What Makes an LLM "Large"?

Scale determines capability:
- **Number of parameters**: Billions to trillions of learned values
- **Training data**: Massive text corpora (books, articles, code, conversations)
- **Compute**: Distributed training across thousands of GPUs

Larger models exhibit emergent capabilities:
- Follow detailed instructions
- Perform multi-step reasoning
- Solve novel problems
- Generalize across domains

#### How LLMs Are Built

**Core Components:**

1. **[[Transformer]] Architecture**: The foundation of modern LLMs, enabling models to attend to all tokens simultaneously and identify relationships across long sequences.

2. **[[Tokenization]]**: Breaking text into manageable units (words, subwords, or punctuation) that the model can process.

3. **Transformer Layers**: Stacked layers that refine understanding by comparing tokens and updating their representations.

4. **[[Positional Encoding]]**: Adding information about token order, since Transformers don't inherently understand sequence position.

5. **Parameters**: Billions of learned values stored in weight matrices that capture patterns from training data.

6. **[[Distributed Training]]**: Splitting the model and data across multiple GPUs to handle massive scale efficiently.

#### Training LLMs from Scratch

LLM training follows a four-stage pipeline:

**Stage 1: Pre-training**
- Train on massive corpora to predict the next token
- Model learns grammar, facts, reasoning patterns
- Result: A model that continues text but isn't conversational

**Stage 2: Instruction Fine-tuning**
- Train on instruction-response pairs
- Model learns to follow prompts and format replies
- Result: A conversational assistant

**Stage 3: Preference Fine-tuning (RLHF)**
- Use human feedback to rate model responses
- Train a reward model to predict human preferences
- Update the LLM using [[Reinforcement Learning with Human Feedback]]
- Result: Better alignment with human values

**Stage 4: Reasoning Fine-tuning**
- For tasks with verifiable correct answers (math, logic)
- Use correctness as the reward signal
- Techniques like [[GRPO]] (Group Relative Policy Optimization)
- Result: Improved reasoning capabilities

#### How LLMs Generate Text

LLMs generate text through [[conditional probability]]:

Given previous tokens, the model calculates the probability of each possible next token and selects based on a strategy.

**Temperature Parameter**: Controls randomness
- Low temperature (~0): Deterministic, repetitive output
- High temperature (0.7-1.0): Creative, diverse output

**Generation Strategies**:

1. **Greedy Decoding**: Always pick the highest probability token
   - Fast but repetitive

2. **Multinomial Sampling**: Sample from the probability distribution
   - Diverse but potentially incoherent

3. **Beam Search**: Explore multiple promising paths
   - Balances quality and diversity
   - Used in machine translation

4. **Contrastive Search**: Penalize similar tokens
   - Prevents repetition while maintaining coherence

#### LLM Generation Parameters

Seven key parameters control output:

1. **Max Tokens**: Hard cap on response length
2. **Temperature**: Controls randomness (0-1)
3. **Top-k**: Sample from top k most probable tokens
4. **Top-p (Nucleus Sampling)**: Sample from tokens covering p% of probability mass
5. **Frequency Penalty**: Reduces reusing frequent tokens
6. **Presence Penalty**: Encourages novel tokens
7. **Stop Sequences**: Custom tokens that halt generation

#### Knowledge Distillation

Smaller models can learn from larger ones through [[Knowledge Distillation]]:

- **Soft-label distillation**: Student learns teacher's probability distributions
- **Hard-label distillation**: Student learns from teacher's final outputs
- **Co-distillation**: Teacher and student learn together

This enables efficient smaller models (like Llama Scout) trained from larger ones (Llama Behemoth).

#### Running LLMs Locally

Four approaches for local deployment:

1. **[[Ollama]]**: Simple CLI tool with one-command setup
2. **[[LMStudio]]**: Desktop app with ChatGPT-like interface
3. **[[vLLM]]**: Fast inference library with OpenAI-compatible API
4. **[[LlamaCPP]]**: Minimal setup with good performance

#### [[Mixture of Experts]] (MoE)

Alternative to traditional Transformers for scaling:

- Uses multiple "expert" feed-forward networks
- Only activates subset of experts per token
- Keeps parameter count large but compute efficient
- Router network learns which experts to select

**Challenges**:
- Expert imbalance (some experts train more than others)
- Uneven token distribution
- Requires sophisticated inference engines

### [[Prompt Engineering]]

#### What is Prompt Engineering?

[[Prompt Engineering]] is the practice of crafting instructions to guide LLM behavior. It's the fastest, lowest-effort way to improve model outputs without changing weights.

Good prompts help models:
- Think step-by-step
- Follow constraints
- Stay focused
- Avoid shallow answers

#### Three Prompting Techniques for Reasoning

**1. Chain of Thought (CoT)**
- Ask the model to reason step-by-step before answering
- Simple but effective
- Often improves accuracy on complex tasks

**2. Self-Consistency (Majority Voting)**
- Generate multiple reasoning paths
- Select the most common final answer
- More robust than single-path reasoning
- Doesn't evaluate reasoning quality, only consistency

**3. Tree of Thoughts (ToT)**
- Explore multiple reasoning directions at each step
- Evaluate which paths are most promising
- More compute-intensive but significantly better results
- Like a search algorithm over reasoning space

#### Attentive Reasoning Queries (ARQ)

A structured approach to maintain control over long conversations:

- Instead of free-form reasoning, guide through explicit domain-specific questions
- Encode reasoning steps as JSON schema fields
- Ensures critical instructions remain aligned mid-conversation
- Makes decisions auditable and verifiable

Success rate: 90.2% (vs 86.1% for CoT, 81.5% for direct response)

#### [[Verbalized Sampling]]

Recovers output diversity lost during [[Reinforcement Learning with Human Feedback]]:

- Post-training alignment causes "mode collapse" (narrow, predictable responses)
- Ask model to verbalize probability distribution instead of single response
- Taps into diverse knowledge learned during pre-training
- Training-free method requiring only prompt modification

Results: 1.6-2.1x diversity increase while maintaining quality

#### [[JSON Prompting]]

Structure outputs for consistency:

- Natural language is powerful but vague
- JSON forces explicit field definitions
- Eliminates hallucinations and inconsistencies
- Models trained on structured data (APIs, web) respond precisely

Alternatives: XML (Claude), Markdown also work—structure matters more than syntax.

### [[Fine-tuning]]

#### What is Fine-tuning?