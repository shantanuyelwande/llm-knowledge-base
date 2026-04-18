---
title: Goolge-whitepaper_Prompt Engineering_v4
source_file: Goolge-whitepaper_Prompt Engineering_v4.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:19:08.871316
raw_file_updated: 2026-04-17T20:19:08.871316
version: 1
sources:
  - file: Goolge-whitepaper_Prompt Engineering_v4.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:19:08.871316
tags: []
related_topics: []
backlinked_by: []
---
# Prompt Engineering

## Summary

Prompt engineering is the process of designing and optimizing text inputs (prompts) to guide [[Large Language Models]] (LLMs) to produce accurate, relevant, and high-quality outputs. It involves iterative refinement of prompts, configuration of model parameters, and application of specialized techniques to achieve desired results across various natural language processing tasks.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Fundamentals](#fundamentals)
3. [LLM Output Configuration](#llm-output-configuration)
4. [Prompting Techniques](#prompting-techniques)
5. [Code Prompting](#code-prompting)
6. [Best Practices](#best-practices)
7. [Related Topics](#related-topics)

---

## Introduction

Prompt engineering is the art and science of crafting effective inputs for [[Large Language Models]]. Unlike traditional programming, which requires explicit instructions, prompt engineering works with the probabilistic nature of LLMs to guide them toward desired outputs.

### Why Prompt Engineering Matters

Everyone can write a prompt, but crafting the most effective prompt requires understanding multiple factors:

- The specific [[Language Model]] being used
- The model's training data and capabilities
- Model configuration settings ([[Temperature]], [[Top-K]], [[Top-P]])
- Word choice, style, and tone
- Prompt structure and context
- The iterative nature of prompt development

Inadequate prompts can lead to ambiguous, inaccurate responses and hinder the model's ability to provide meaningful output. Prompt engineering is fundamentally an **iterative process** requiring experimentation and refinement.

### Applicable Tasks

Prompt engineering can be applied to numerous natural language processing and generation tasks:

- [[Text Summarization]]
- [[Information Extraction]]
- [[Question Answering]]
- [[Text Classification]]
- Language and code translation
- Code generation and documentation
- Reasoning and problem-solving

---

## Fundamentals

### How LLMs Work

To understand prompt engineering, it's essential to grasp how [[Large Language Models]] operate:

1. LLMs are **prediction engines** that take sequential text as input
2. They predict the next token (word or subword) based on training data
3. The prediction is based on relationships between previous tokens and patterns learned during training
4. This process repeats iteratively, with each predicted token added to the sequence

When writing a prompt, you are essentially **setting up the LLM to predict the right sequence of tokens**. Effective prompt engineering optimizes this token prediction process by:

- Structuring prompts for clarity
- Providing relevant context
- Including examples when appropriate
- Adjusting model configurations

### Model Selection

Prompt engineering begins with choosing an appropriate model. Different models may require different prompting approaches:

- [[Gemini]] (Google's models)
- GPT (OpenAI)
- Claude (Anthropic)
- Open source models (Gemma, LLaMA)

Prompts may need optimization for specific models regardless of which platform or service you use.

---

## LLM Output Configuration

Beyond the prompt itself, LLMs come with various configuration options that control output quality and characteristics. Effective prompt engineering requires setting these configurations optimally for your task.

### Output Length

**Token limit** is an important configuration setting that determines how many tokens the model generates in a response.

**Considerations:**

- More tokens require more computation, leading to:
  - Higher energy consumption
  - Slower response times
  - Higher costs
- Reducing output length doesn't make the model more concise—it simply stops generation at the limit
- For tasks requiring short outputs, you may need to engineer your prompt accordingly
- Particularly important for techniques like [[ReAct]], where the model may emit useless tokens after the desired response

### Sampling Controls

LLMs don't formally predict a single token; instead, they predict **probabilities** for each token in their vocabulary. Sampling controls determine how these probabilities are processed to select the output token.

#### Temperature

[[Temperature]] controls the degree of randomness in token selection:

- **Temperature = 0** (greedy decoding): Deterministic—always selects the highest probability token
  - Best for tasks with single correct answers (math, factual retrieval)
  - May produce identical outputs
- **Low temperatures** (0.1-0.3): More deterministic, consistent results
  - Suitable for [[Text Classification]], factual tasks
- **High temperatures** (0.7-1.0): More random and creative output
  - Suitable for creative writing, brainstorming
- **Very high temperatures** (>1.0): All tokens become equally likely

Temperature works similarly to the softmax function in machine learning, where low values emphasize a single preferred outcome with high certainty, while high values distribute probability more evenly.

#### Top-K and Top-P

Both [[Top-K]] and [[Top-P]] (nucleus sampling) restrict the predicted next token to come from high-probability candidates, controlling randomness and diversity:

**Top-K Sampling:**
- Selects from the top K most likely tokens
- Higher K = more creative, varied output
- Lower K = more restive, factual output
- K=1 is equivalent to greedy decoding

**Top-P Sampling (Nucleus Sampling):**
- Selects tokens whose cumulative probability doesn't exceed value P
- P ranges from 0 (greedy decoding) to 1 (all vocabulary)
- More flexible than Top-K for controlling diversity

**Best Practice:** Experiment with both methods to find which produces better results for your specific task.

### Putting It All Together

Configuration settings interact with each other. Understanding their combined effect is crucial:

**Processing Order (in Vertex Studio):**
1. Tokens meeting both Top-K and Top-P criteria become candidates
2. Temperature is applied to sample from these candidates
3. If only one setting is available, behavior adapts accordingly

**Extreme Settings:**

When one configuration reaches extreme values, it can override others:

| Setting | Extreme Value | Effect |
|---------|---------------|--------|
| Temperature | 0 | Top-K and Top-P become irrelevant; highest probability token always selected |
| Temperature | Very high (>1) | Temperature becomes irrelevant; random sampling from Top-K/Top-P candidates |
| Top-K | 1 | Only one token passes criteria; temperature and Top-P irrelevant |
| Top-K | Vocabulary size | All tokens with nonzero probability pass; none filtered out |
| Top-P | 0 or very small | Only most probable token qualifies; temperature and Top-K irrelevant |
| Top-P | 1 | All tokens with nonzero probability pass; none filtered out |

**Recommended Starting Points:**

- **Balanced creativity:** Temperature 0.2, Top-P 0.95, Top-K 30
- **High creativity:** Temperature 0.9, Top-P 0.99, Top-K 40
- **Low creativity:** Temperature 0.1, Top-P 0.9, Top-K 20
- **Deterministic (single correct answer):** Temperature 0

**Note:** Greater freedom in settings (higher temperature, Top-K, Top-P, and output tokens) may result in less relevant text.

---

## Prompting Techniques

### Zero-Shot Prompting

[[Zero-Shot Prompting]] is the simplest prompting approach. It provides only a task description and input text without examples.

**Characteristics:**
- No examples provided (hence "zero-shot")
- Works for straightforward tasks
- Input can be a question, story beginning, or instructions

**Example Use Case:** Classifying a movie review as positive, neutral, or negative with just a single instruction.

**When to use:** For simple, well-defined tasks where the model has sufficient training data.

### One-Shot and Few-Shot Prompting

[[Few-Shot Prompting]] provides examples within the prompt to guide the model's output.

**One-Shot Prompting:**
- Provides a single example
- Model learns from one demonstration

**Few-Shot Prompting:**
- Provides multiple examples (typically 3-5)
- Shows a pattern the model should follow
- Increases likelihood of pattern adherence

**Guidelines:**

- Choose examples relevant to your task
- Ensure examples are diverse, high-quality, and well-written
- Include edge cases for robust handling
- Number of examples depends on:
  - Task complexity
  - Example quality
  - Model capabilities
  - Input length limitations

**Best Practice:** Use at least 3-5 examples for few-shot prompting, adjusting based on task complexity.

### System, Contextual, and Role Prompting

These three techniques guide LLM output by establishing context and perspective:

#### System Prompting

[[System Prompting]] sets the overall context and purpose for the model. It defines the "