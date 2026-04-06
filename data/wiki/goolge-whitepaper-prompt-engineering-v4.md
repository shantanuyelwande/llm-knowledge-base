---
title: Goolge-whitepaper_Prompt Engineering_v4
source_file: Goolge-whitepaper_Prompt Engineering_v4.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:23:44.311588
raw_file_updated: 2026-04-05T20:23:44.311588
version: 1
sources:
  - file: Goolge-whitepaper_Prompt Engineering_v4.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:23:44.311588
tags: []
related_topics: []
backlinked_by: []
---
# Prompt Engineering

## Summary

**Prompt Engineering** is the process of designing and optimizing text inputs (prompts) to guide [[Large Language Models]] (LLMs) to produce accurate, relevant, and high-quality outputs. It involves iterative refinement of prompts, configuration of model parameters, and application of specialized techniques to achieve desired results across various natural language processing tasks.

---

## Introduction

Prompt engineering is a fundamental skill in working with modern [[Generative AI]] systems. While anyone can write a prompt, crafting effective prompts that consistently produce high-quality outputs requires understanding how [[Large Language Models]] work, mastering various prompting techniques, and applying established best practices.

The efficacy of a prompt depends on multiple factors: the model selected, its training data, model configurations, word choice, writing style, tone, structure, and contextual information. Because of these variables, prompt engineering is inherently an iterative process requiring continuous testing, refinement, and documentation.

---

## How LLMs Work

[[Large Language Models]] function as prediction engines. The model takes sequential text as input and predicts what the next [[Token]] should be, based on patterns learned during training. This process repeats iteratively, with each previously predicted token added to the sequence to predict the following token.

When you write a prompt, you are setting up the LLM to predict the correct sequence of tokens. The next token prediction is based on the relationship between previous tokens and what the model has learned during training.

---

## LLM Output Configuration

Once you select a model, you must configure its output parameters. These settings control how the LLM generates responses and significantly impact both quality and cost.

### Output Length

The number of tokens to generate is a critical configuration setting. Generating more tokens requires more computation, leading to:
- Higher energy consumption
- Potentially slower response times
- Increased costs

Reducing output length does not make the LLM more concise in style; it simply causes the model to stop generating tokens once the limit is reached. For tasks requiring short outputs, you must engineer your prompt accordingly.

Output length restrictions are especially important for techniques like [[ReAct]], where the LLM may emit useless tokens after the desired response.

### Sampling Controls

LLMs do not formally predict a single token. Instead, they predict probabilities for each token in their vocabulary, then sample from these probabilities to select the next token. Three primary configuration settings control this process:

#### Temperature

Temperature controls the degree of randomness in token selection:

- **Low temperature (near 0)**: More deterministic responses; the highest probability token is consistently selected. Ideal for tasks requiring factual accuracy.
- **High temperature**: More diverse and creative results; all tokens become increasingly likely to be selected.
- **Temperature of 0**: Greedy decoding—always selects the highest probability token (though ties may be broken randomly).

Temperature in [[Gemini]] models works similarly to the softmax function in machine learning, with low temperatures emphasizing a single preferred output and high temperatures accommodating wider ranges of acceptable outputs.

#### Top-K and Top-P Sampling

**Top-K sampling** restricts the next token to come from the K most likely tokens:
- Higher top-K: More creative and varied output
- Lower top-K: More restrained and factual output
- Top-K of 1: Equivalent to greedy decoding

**Top-P sampling** (also called nucleus sampling) selects tokens whose cumulative probability does not exceed a threshold P:
- Values range from 0 (greedy decoding) to 1 (all tokens in vocabulary)
- Provides dynamic vocabulary restriction based on probability distribution

### Putting It All Together

When multiple sampling settings are available (temperature, top-K, and top-P), they interact as follows:

1. Tokens meeting both top-K and top-P criteria are identified as candidates
2. Temperature is applied to sample from these candidates
3. If only top-K or top-P is available, that single setting is used
4. If temperature is unavailable, candidates are randomly selected

**Extreme settings override other parameters:**
- Temperature of 0: top-K and top-P become irrelevant
- Extremely high temperature (10+): Temperature becomes irrelevant
- Top-K of 1: Temperature and top-P become irrelevant
- Top-P of 0 or 1: May override other settings depending on implementation

**Recommended starting points:**
- **Coherent, slightly creative**: Temperature 0.2, Top-P 0.95, Top-K 30
- **Highly creative**: Temperature 0.9, Top-P 0.99, Top-K 40
- **Deterministic**: Temperature 0.1, Top-P 0.9, Top-K 20
- **Single correct answer** (math, factual): Temperature 0

---

## Prompting Techniques

LLMs are trained to follow instructions and understand large amounts of data. However, they are not perfect. Specific techniques that leverage how LLMs work can significantly improve output quality.

### Zero-Shot Prompting

**Zero-shot prompting** is the simplest prompting technique. It provides only a task description and text for the model to work with, without any examples. The name derives from "zero examples."

Example use cases:
- Text classification
- Question answering
- Simple instruction following

Zero-shot works when the task is straightforward and the model has sufficient training data on similar tasks.

### One-Shot and Few-Shot Prompting

When zero-shot prompting is insufficient, providing examples significantly improves performance.

**One-shot prompting** provides a single example, allowing the model to imitate the pattern to complete the task.

**Few-shot prompting** provides multiple examples, typically three to five, showing the model a clear pattern to follow. The number of examples needed depends on:
- Task complexity
- Example quality
- Model capabilities

**Best practices for few-shot examples:**
- Use relevant, diverse, high-quality examples
- Include edge cases (unusual but valid inputs)
- Write examples clearly without errors
- For classification tasks, mix up the order of response classes to avoid overfitting

### System, Contextual, and Role Prompting

These three techniques guide how LLMs generate text by providing different types of context:

#### System Prompting

**System prompting** sets the overall context and purpose for the model. It defines the "big picture" of what the model should do (e.g., translating languages, classifying reviews). System prompts are useful for:
- Generating output meeting specific requirements
- Returning structured formats (JSON, XML)
- Controlling safety and toxicity
- Defining output constraints

Example: "Classify movie reviews as positive, neutral or negative. Only return the label in uppercase."

#### Role Prompting

**Role prompting** assigns a specific character or identity for the model to adopt. This helps generate responses consistent with that role and its associated knowledge and behavior.

Examples of effective roles:
- Book editor
- Travel guide
- Technical expert
- Kindergarten teacher

**Effective style modifiers:**
- Confrontational
- Descriptive
- Direct
- Formal
- Humorous
- Influential
- Informal
- Inspirational
- Persuasive

Role prompting adds personality and frames the output style and voice to match specific expectations.

#### Contextual Prompting

**Contextual prompting** provides specific details or background information relevant to the current task. It helps the model understand nuances and tailor responses accordingly. Context is highly specific to the current task and dynamic in nature.

Example: "You are writing for a blog about retro 80's arcade video games."

### Step-Back Prompting

**Step-back prompting** improves performance by prompting the LLM to first consider a general question related to the specific task, then using that answer to inform the specific task prompt.

Process:
1. Ask a general question related to broader principles
2. Use the answer as context for the specific task
3. Apply the general knowledge to solve the specific problem

Benefits:
- Activates relevant background knowledge
- Encourages critical thinking
- Generates more accurate and insightful responses
- Helps mitigate biases by focusing on general principles

### Chain of Thought (CoT)

**Chain of Thought prompting** improves reasoning capabilities by generating intermediate reasoning steps before providing the final answer. Instead of jumping directly to conclusions, the model explains its thinking process.

**Advantages:**
- Low-effort and highly effective
- Works with off-the-shelf models (no fine-tuning needed)
- Provides interpretability—you can see the reasoning steps
- Improves robustness across different model versions
- Helps identify errors in reasoning

**Disadvantages:**
- Increases output tokens, raising costs and latency
- More computation required

**Types of Chain of Thought:**
- **Zero-shot CoT**: Simply add "Let's think step by step" to the prompt
- **Few-shot CoT**: Provide examples showing step-by-step reasoning

**Best