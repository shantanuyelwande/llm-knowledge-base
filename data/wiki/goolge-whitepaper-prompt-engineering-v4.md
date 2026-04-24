---
title: Goolge-whitepaper_Prompt Engineering_v4
source_file: Goolge-whitepaper_Prompt Engineering_v4.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:57:28.420307
raw_file_updated: 2026-04-24T18:57:28.420307
version: 1
sources:
  - file: Goolge-whitepaper_Prompt Engineering_v4.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:57:28.420307
tags: []
related_topics: []
backlinked_by: []
---
# Prompt Engineering

## Summary

**Prompt Engineering** is the process of designing and optimizing high-quality prompts that guide [[Large Language Models]] (LLMs) to produce accurate, relevant outputs. It involves iteratively crafting prompts, configuring model parameters, and applying specialized techniques to achieve desired results across various natural language processing tasks. The field combines practical experimentation with established methodologies to help users, regardless of technical background, effectively communicate with AI systems.

---

## Introduction

[[Prompt engineering]] is the art and science of crafting effective inputs for [[large language models]]. While anyone can write a prompt, creating prompts that reliably produce desired outputs requires understanding how LLMs work, the various configuration options available, and established prompting techniques.

The efficacy of a prompt depends on multiple factors:
- The specific [[LLM]] model being used
- The model's [[training data]]
- Model [[configuration]] settings (temperature, sampling parameters)
- Word choice, style, and tone
- Structural organization
- Contextual information provided

Prompt engineering is fundamentally an **iterative process**. Inadequate prompts can lead to ambiguous or inaccurate responses, while well-crafted prompts unlock the model's ability to provide meaningful output.

---

## How Large Language Models Work

To understand prompt engineering, it's essential to grasp how LLMs function. LLMs operate as **prediction engines** that work sequentially:

1. The model receives text input (a prompt)
2. It predicts the next [[token]] based on statistical relationships learned during [[training]]
3. The predicted token is added to the sequence
4. This process repeats to generate complete responses

When you write a prompt, you're essentially setting up the LLM to predict the correct sequence of tokens. Your goal is to provide enough context and direction that the model's predictions align with your intended output.

---

## LLM Output Configuration

Before crafting prompts, you must configure the model's output parameters. These settings control how the model generates responses and significantly impact results.

### Output Length

The **max token limit** controls how many tokens the model will generate in a response.

**Considerations:**
- More tokens require more computation, leading to higher energy consumption and costs
- Slower response times with longer outputs
- Reducing output length doesn't make responses more concise—it simply stops generation at a limit
- For techniques like [[ReAct]], output length control is especially important to prevent useless token generation

**Best Practice:** Match your token limit to your task requirements. Include output length specifications in your prompt when necessary.

### Sampling Controls

LLMs don't predict single tokens deterministically. Instead, they generate probability distributions across their vocabulary and sample from these distributions. Three primary configuration settings control this process:

#### Temperature

**Temperature** controls the randomness in token selection:

- **Low temperature (0-0.3):** More deterministic, focused responses. Temperature of 0 uses [[greedy decoding]], always selecting the highest probability token
- **High temperature (0.7-1.0):** More diverse, creative, potentially unexpected results
- **Very high temperature (>1):** Nearly random output

**Use Cases:**
- Low temperature: Factual tasks, mathematical problems, consistent classifications
- High temperature: Creative writing, brainstorming, diverse output generation

**Analogy:** Temperature functions similarly to the [[softmax]] function in machine learning—low values emphasize a single preferred outcome, while high values distribute probability across more options.

#### Top-K and Top-P Sampling

These techniques restrict token selection to high-probability candidates:

**Top-K Sampling:**
- Selects from the K most likely tokens
- Higher K = more creative and varied output
- Lower K = more restricted and factual output
- K=1 is equivalent to greedy decoding

**Top-P (Nucleus) Sampling:**
- Selects tokens whose cumulative probability doesn't exceed P
- P ranges from 0 (greedy) to 1 (all tokens)
- More flexible than Top-K, adapts to different probability distributions

**Selection Strategy:** Experiment with both methods to determine which produces better results for your specific task.

### Putting It All Together

When multiple sampling settings are available (as in [[Vertex AI Studio]]), they interact in a specific order:

1. Tokens meeting both Top-K AND Top-P criteria are identified
2. Temperature is applied to sample from these filtered tokens
3. At extreme settings, one parameter can override others:
   - Temperature = 0: Top-K and Top-P become irrelevant
   - Temperature > 1: Temperature becomes irrelevant
   - Top-K = 1: Temperature and Top-P become irrelevant
   - Top-P = 0: Only most probable token qualifies

**Recommended Starting Points:**

| Use Case | Temperature | Top-P | Top-K |
|----------|-------------|-------|-------|
| Balanced (coherent but creative) | 0.2 | 0.95 | 30 |
| Highly creative | 0.9 | 0.99 | 40 |
| Factual/constrained | 0.1 | 0.9 | 20 |
| Deterministic (single correct answer) | 0 | - | - |

**Important Note:** Greater freedom in sampling settings (higher temperature, top-K, top-P, and output tokens) may result in less relevant generated text.

---

## Prompting Techniques

LLMs are trained to follow instructions on large datasets, enabling them to understand prompts and generate responses. However, specific techniques that leverage how LLMs work dramatically improve output quality.

### Zero-Shot Prompting

**Zero-shot** prompting is the simplest technique. It provides only a task description and input text, with no examples (hence "zero-shot").

**Structure:**
- Task description
- Input to process
- Expected output format

**Example:** "Classify the following movie review as POSITIVE, NEUTRAL, or NEGATIVE. Review: [text]. Sentiment:"

**When to use:** Simple, straightforward tasks where the model's training provides sufficient context.

**Limitations:** May fail on complex or nuanced tasks.

### One-Shot and Few-Shot Prompting

When zero-shot prompting doesn't work, providing examples dramatically improves results.

**One-Shot Prompting:**
- Provides a single example
- Model learns by imitation

**Few-Shot Prompting:**
- Provides multiple examples (typically 3-5)
- Shows a pattern the model should follow
- More effective than one-shot for complex tasks

**Guidelines for Examples:**
- Use 3-5 examples as a starting point (more for complex tasks)
- Ensure examples are relevant, high-quality, and well-written
- Include [[edge cases]]—unusual inputs the model should handle
- Avoid small mistakes in examples; they confuse the model

**Benefits:**
- Guides output structure and format
- Establishes desired patterns
- Improves consistency

### System, Contextual, and Role Prompting

These three techniques guide how LLMs generate text by establishing different types of context:

#### System Prompting

**System prompting** sets the overall context and purpose for the model.

**Characteristics:**
- Defines the "big picture" of what the model should do
- Provides additional instructions on output format
- Specifies constraints or requirements

**Use Cases:**
- Returning output in specific formats (JSON, XML)
- Enforcing safety and respectful tone
- Ensuring consistent style
- Generating structured data

**Example:** "Classify movie reviews as POSITIVE, NEUTRAL, or NEGATIVE. Return only the label in uppercase."

**Benefits:**
- Forces structured output, limiting [[hallucinations]]
- Enables data processing in real-world applications
- Allows sorted output (useful for datetime objects)

#### Role Prompting

**Role prompting** assigns a specific character or identity to the model.

**Approach:**
- Assign a role: "You are a travel guide," "You are a kindergarten teacher," "You are a code reviewer"
- Provide role-specific prompts
- Model generates responses consistent with the assigned role

**Benefits:**
- Generates more relevant and informative output
- Establishes tone, style, and focused expertise
- Improves quality, relevance, and effectiveness

**Style Options:**
Confrontational, Descriptive, Direct, Formal, Humorous, Influential, Informal, Inspirational, Persuasive

**Example:** "Act as a travel guide. Suggest 3 places to visit in Amsterdam in a humorous style."

#### Contextual Prompting

**Contextual prompting** provides specific details and background information relevant to the current task.

**Approach:**
- Include relevant context upfront
- Help the model understand nuances
- Enable tailored responses

**Benefits:**
- Faster comprehension of requests
- More accurate and relevant responses
- Enables dynamic,