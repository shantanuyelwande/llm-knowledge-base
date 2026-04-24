---
title: AI Engineering Guidebook
source_file: AI Engineering Guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:04:06.796999
raw_file_updated: 2026-04-24T19:04:06.796999
version: 1
sources:
  - file: AI Engineering Guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:04:06.796999
tags: []
related_topics: []
backlinked_by: []
---
# AI Engineering: System Design Patterns for LLMs, RAG, and Agents

## Summary

This comprehensive guide covers the complete landscape of AI engineering, from foundational [[Large Language Models]] (LLMs) through [[Retrieval-Augmented Generation]] (RAG), [[Fine-tuning]] techniques, [[AI Agents]], and production deployment. It addresses the practical challenges of building, optimizing, evaluating, and operating AI systems at scale.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Large Language Models](#large-language-models)
3. [Prompt Engineering](#prompt-engineering)
4. [Fine-tuning](#fine-tuning)
5. [Retrieval-Augmented Generation](#retrieval-augmented-generation)
6. [Context Engineering](#context-engineering)
7. [AI Agents](#ai-agents)
8. [Model Context Protocol](#model-context-protocol)
9. [LLM Optimization](#llm-optimization)
10. [LLM Evaluation](#llm-evaluation)
11. [LLM Deployment](#llm-deployment)
12. [LLM Observability](#llm-observability)

---

## Introduction

AI Engineering represents a fundamental shift in how we build intelligent systems. Rather than developing task-specific models for each problem, modern AI engineering leverages large pre-trained models and adapts them through a combination of [[Prompt Engineering]], [[Fine-tuning]], and [[Retrieval-Augmented Generation]].

The core philosophy is pragmatic: optimize for real-world constraints including latency, cost, memory, and reliability—not just accuracy. This guide provides both conceptual understanding and practical implementation patterns used in production systems.

---

## Large Language Models

### What is an LLM?

A [[Large Language Model]] (LLM) is a [[Transformer]]-based neural network trained on massive text corpora to predict the next [[Token]] in a sequence. Through this process, it acquires the ability to understand, generate, and reason with human language.

**Key insight**: LLMs work by predicting one token at a time. When you ask "What is the capital of France?", the model calculates conditional probabilities for each possible next word and selects the most likely one, repeating this process until generating a complete answer.

### The Evolution from Task-Specific to General Models

Before LLMs, AI systems were fragmented:
- Translation systems handled only translation
- Summarizers knew only summarization
- Sentiment classifiers recognized only sentiment

Each new problem required a new model and pipeline. LLMs changed this by learning the general structure of language across millions of domains, enabling a single model to perform many tasks without explicit programming for each one.

### What Makes an LLM "Large"?

The "large" in LLM refers to three dimensions:

1. **Number of parameters**: Billions or trillions of learnable weights
2. **Training data scale**: Massive corpora spanning diverse domains
3. **Compute resources**: Significant computational investment during training

As models scaled across these dimensions, a clear capability shift emerged: larger models began following detailed instructions, performing multi-step reasoning, and solving novel problems. This wasn't from adding new rules but from the model learning deeper relationships in language.

### LLM Architecture

#### Core Components

**[[Transformer]]**: The foundational architecture that allows models to attend to all input tokens simultaneously and identify which parts of text are most relevant to each other.

**[[Tokenization]]**: Text is broken into tokens (words, subwords, or punctuation) and mapped to numerical representations. This keeps vocabulary manageable while handling any language input.

**Transformer Layers**: Multiple layers stacked on top of each other, where each layer refines understanding by comparing tokens, attending to important parts, and updating representations.

**[[Positional Encoding]]**: Since Transformers don't naturally understand token order, positional encodings provide sequence information, enabling interpretation of ordered structures like sentences and code.

**Parameters**: Billions of learnable values that store patterns learned from text and form the basis for language understanding and generation.

**[[Distributed Training]]**: Due to model size, training occurs across many GPUs in parallel, with parameters, computations, and data distributed for efficiency.

### Training an LLM from Scratch

LLM development follows four stages:

#### Stage 1: Pre-training

The model learns language fundamentals by training on massive corpora to predict the next token. It absorbs grammar, world facts, and reasoning patterns. However, pre-trained models simply continue text—they're not conversational.

#### Stage 2: Instruction Fine-tuning (IFT)

The model learns to follow prompts by training on instruction-response pairs. This enables it to:
- Answer questions
- Summarize content
- Write code
- Follow specific formatting

At this point, the model has consumed the internet's raw knowledge, and human-labeled instruction data becomes the limiting factor.

#### Stage 3: Preference Fine-tuning (PFT)

Using [[Reinforcement Learning with Human Feedback]] (RLHF), the model learns to align with human preferences. Users indicate which response they prefer, creating preference data. A [[Reward Model]] predicts human preference, and the LLM is updated using [[Proximal Policy Optimization]] (PPO) to align with humans even when no single "correct" answer exists.

#### Stage 4: Reasoning Fine-tuning

For tasks with verifiable correct answers (math, logic), the model generates answers and receives rewards based on correctness. This [[Reinforcement Learning with Verifiable Rewards]] approach uses techniques like [[GRPO]] (Group Relative Policy Optimization) to sharpen reasoning capabilities.

### How LLMs Work: Conditional Probability

LLMs operate on [[Conditional Probability]]—given the words that have come before, what is the most likely next word?

The model calculates probabilities for each possible next token and selects the one with highest probability. Repeating this process generates complete responses.

**The creativity problem**: Always picking the highest probability word produces repetitive, dull outputs. This is where [[Temperature]] comes in.

#### Temperature and Sampling

Instead of always selecting the most likely token, the model can "sample" from the probability distribution:

- **Low temperature** (~0): Probabilities concentrate around the most likely token, producing nearly deterministic outputs
- **High temperature** (0.7–1.0): Probabilities become more uniform, producing diverse and creative outputs

### LLM Generation Parameters

Seven key parameters control text generation:

1. **Max tokens**: Hard cap on response length. Too low causes truncation; too high wastes compute.

2. **Temperature**: Controls randomness. Low for factual tasks (QA, chatbots); high for creative tasks (brainstorming).

3. **Top-k**: Restricts sampling to the k most probable tokens. Prevents both random outputs and excessive repetition.

4. **Top-p (nucleus sampling)**: Samples from the smallest set of tokens covering cumulative probability p. More adaptive than top-k.

5. **Frequency penalty**: Reduces likelihood of reusing tokens that appeared frequently. Useful for avoiding redundancy.

6. **Presence penalty**: Encourages new tokens not yet seen. Pushes for diversity in exploratory generation.

7. **Stop sequences**: Custom tokens that halt generation immediately. Critical for structured outputs like JSON.

**Bonus - Min-p sampling**: Dynamically adjusts based on model confidence. If the top token has 60% probability, few options remain. If 20%, many pass the threshold. Automatically balances coherence and diversity.

### Text Generation Strategies

Four main approaches to selecting tokens:

#### 1. Greedy Strategy

Always choose the highest probability token. Simple but produces repetitive outputs.

#### 2. Multinomial Sampling

Sample from the full probability distribution. Introduces diversity but can be incoherent.

#### 3. Beam Search

Maintains top-k partial sequences and explores alternatives. Approximates global sequence probability maximization. Widely used in machine translation where correctness matters more than creativity.

#### 4. Contrastive Search

Balances fluency with diversity by penalizing tokens too similar to previously generated text. Especially effective for longer generations like stories.

**Bonus - SLED (Self-Logits Evolution Decoding)**: Instead of using only the final layer's logits, examines how logits evolve across all layers. Each layer contributes its own prediction, and SLED nudges final logits toward layer-wise consensus. Requires no retraining and produces more factual outputs.

### Training LLMs Using Other LLMs

Modern LLMs are increasingly trained using knowledge from other LLMs through [[Distillation]]:

- Llama 4 Scout and Maverick were trained using Llama 4 Behemoth
- Gemma 2 and 3 were trained using Google's Gemini

Distillation occurs at two stages: