---
title: Goolge-whitepaper_Prompt Engineering_v4
source_file: Goolge-whitepaper_Prompt Engineering_v4.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:57:58.560548
raw_file_updated: 2026-04-17T20:57:58.560548
version: 1
sources:
  - file: Goolge-whitepaper_Prompt Engineering_v4.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:57:58.560548
tags: []
related_topics: []
backlinked_by: []
---
# Prompt Engineering

## Summary

Prompt engineering is the process of designing and optimizing text inputs to guide [[Large Language Models]] (LLMs) to produce accurate, relevant, and high-quality outputs. It is an iterative discipline that involves crafting effective prompts, configuring model parameters, and applying specialized techniques to achieve desired results across various natural language processing tasks.

---

## Overview

Prompt engineering is the art and science of designing high-quality prompts that guide [[LLMs]] to produce accurate outputs. This process involves tinkering to find the best prompt, optimizing prompt length, and evaluating a prompt's writing style and structure in relation to the specific task. Unlike traditional software engineering, prompt engineering does not require specialized technical expertise—anyone can write a prompt, though crafting effective ones requires understanding how language models work and applying proven techniques.

### Core Concept

An [[LLM]] is fundamentally a prediction engine that processes sequential text as input and predicts what the following token should be, based on patterns learned during training. When you write a prompt, you are attempting to set up the LLM to predict the right sequence of tokens. The effectiveness of a prompt depends on multiple factors:

- The model selected and its training data
- Model configuration settings (temperature, sampling parameters)
- Word choice, style, and tone
- Prompt structure and organization
- Contextual information provided
- Task-specific requirements

---

## LLM Output Configuration

Before crafting prompts, it is essential to understand and configure the model's output parameters. These settings control how the model generates responses and significantly impact both quality and cost.

### Output Length

Output length refers to the maximum number of [[tokens]] the model will generate in a response. This is a critical configuration because:

- **Resource Impact**: Generating more tokens requires greater computational resources, leading to higher energy consumption, slower response times, and increased costs
- **Truncation Behavior**: Reducing output length does not make the model more concise; it simply causes the model to stop generating tokens once the limit is reached
- **Prompt Engineering Necessity**: When short outputs are required, the prompt itself must be engineered to accommodate this constraint

Output length restrictions are particularly important for certain prompting techniques like [[ReAct]], where the model may continue generating unnecessary tokens after the desired response.

### Sampling Controls

LLMs do not select a single token deterministically. Instead, they generate probability distributions across their vocabulary, with each token assigned a probability. These probabilities are then sampled to determine the actual output token. Three primary configuration settings control this sampling process:

#### Temperature

Temperature controls the degree of randomness in token selection:

- **Low Temperature (0.1-0.3)**: Produces more deterministic, focused, and factual outputs. A temperature of 0 (greedy decoding) always selects the highest probability token, though ties may be broken randomly
- **High Temperature (0.7-1.0)**: Generates more diverse, creative, and unexpected results
- **Extreme Values**: As temperature approaches infinity, all tokens become equally likely

Temperature functions similarly to the softmax function in machine learning—low temperatures emphasize a single preferred output with high certainty, while higher temperatures distribute probability across a wider range of options.

#### Top-K and Top-P Sampling

**Top-K sampling** restricts token selection to the K most likely tokens from the model's probability distribution:
- Higher top-K values produce more creative and varied output
- Lower top-K values produce more restive and factual output
- Top-K of 1 is equivalent to greedy decoding

**Top-P sampling** (also called nucleus sampling) selects tokens whose cumulative probability does not exceed a threshold value P:
- Values range from 0 (greedy decoding) to 1 (all tokens in vocabulary)
- Provides more flexible control than top-K by adapting to the probability distribution shape

### Configuration Interaction and Best Practices

When multiple sampling settings are available (as in Vertex AI Studio), they interact in a specific order:

1. Tokens meeting both top-K and top-P criteria are identified as candidates
2. Temperature is applied to sample from these candidates
3. If temperature is set to 0, top-K and top-P become irrelevant (deterministic selection)
4. If temperature is extremely high, temperature becomes irrelevant and candidates are randomly selected

**Recommended Starting Points:**
- **Balanced Coherence**: Temperature 0.2, top-P 0.95, top-K 30
- **Creative Results**: Temperature 0.9, top-P 0.99, top-K 40
- **Factual/Deterministic**: Temperature 0.1, top-P 0.9, top-K 20
- **Single Correct Answer** (math, logic): Temperature 0

---

## Core Prompting Techniques

### Zero-Shot Prompting

Zero-shot prompting is the simplest prompting approach, providing only a task description and input text without any examples. The term "zero-shot" refers to the absence of demonstrations.

**Characteristics:**
- No examples provided to the model
- Relies entirely on the model's pre-training knowledge
- Quick to implement but may produce less consistent results
- Suitable for straightforward tasks

**Example Use Case:** Classifying movie reviews as positive, neutral, or negative with a single instruction

**When to Use:** Basic tasks where the model's training data provides sufficient context

### One-Shot and Few-Shot Prompting

Few-shot prompting involves providing examples within the prompt to help the model understand the desired output pattern.

**One-Shot Prompting:** Provides a single example for the model to imitate

**Few-Shot Prompting:** Provides multiple examples (typically 3-5) to establish a clear pattern

**Benefits:**
- Dramatically improves accuracy on complex tasks
- Helps establish desired output structure and format
- Guides the model toward specific patterns and styles
- Particularly effective for classification and structured output tasks

**Best Practices:**
- Use relevant, high-quality examples
- Include diverse examples covering different scenarios
- Add edge cases to improve robustness
- Mix up the order of response classes in classification tasks
- Ensure examples are well-written with no errors that could confuse the model

**Number of Examples:** Generally 3-5 examples for most tasks, though more complex tasks may require additional examples. Consider input length limitations of your model.

### System, Contextual, and Role Prompting

These three complementary techniques provide different types of guidance to shape model behavior:

#### System Prompting

System prompting sets the overall context and purpose for the language model, defining the "big picture" of what the model should accomplish.

**Characteristics:**
- Specifies fundamental capabilities and overarching purpose
- Provides instructions on output format and structure
- Useful for ensuring consistent behavior across multiple prompts
- Can enforce safety and toxicity guidelines

**Applications:**
- Specifying output format (JSON, XML, structured text)
- Setting tone and style requirements
- Defining behavioral constraints and values
- Limiting hallucinations through structured output requirements

**Example:** "Return valid JSON with sentiment field and movie name field" ensures structured, parseable output

#### Role Prompting

Role prompting assigns a specific character or identity for the model to adopt, helping it generate contextually appropriate responses.

**Characteristics:**
- Frames the model's output style and voice
- Adds a layer of specificity and personality
- Leverages the model's training knowledge about specific roles
- Effective for creative and specialized tasks

**Applicable Styles:**
Confrontational, Descriptive, Direct, Formal, Humorous, Influential, Informal, Inspirational, Persuasive

**Example:** "Act as a travel guide" primes the model to provide travel-specific knowledge and recommendations

#### Contextual Prompting

Contextual prompting provides specific details and background information relevant to the current task, helping the model understand nuances and tailor responses accordingly.

**Characteristics:**
- Supplies immediate, task-specific information
- Highly dynamic and input-dependent
- Helps the model understand the specific context
- Improves relevance and accuracy of responses

**Example:** "You are writing for a blog about retro 80's arcade video games" provides context that shapes all subsequent suggestions

### Step-Back Prompting

Step-back prompting improves LLM performance by first prompting the model to consider general principles related to a task, then using that answer to inform the specific task solution.

**Process:**
1. Ask a general question related to the specific task
2. Feed the answer to that general question into a subsequent prompt
3. Use the general knowledge to solve the specific problem

**Benefits:**
- Activates relevant background knowledge before solving specific problems
- Encourages critical thinking and novel application of knowledge
- Helps mitigate biases by focusing on general principles
- Produces more accurate and insightful responses

**Example:** Before writing a video game level storyline, first identify 5 engaging themes, then use those themes to create a more compelling storyline

### Chain of Thought (Co