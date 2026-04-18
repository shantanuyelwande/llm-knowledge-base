---
title: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you
source_file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:02:39.824732
raw_file_updated: 2026-04-17T21:02:39.824732
version: 1
sources:
  - file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:02:39.824732
tags: []
related_topics: []
backlinked_by: []
---
# LLM Hallucinations: Practical Reduction Techniques

## Summary

**LLM Hallucinations** are instances where [[Large Language Models|language models]] generate plausible-sounding but factually incorrect or fabricated information. This article outlines seven practical techniques to reduce hallucination in LLM outputs, ranging from simple prompting strategies to sophisticated multi-step reasoning and verification approaches. These methods form the foundation of modern [[AI Safety|safe AI systems]] and are implemented by major technology companies.

---

## Table of Contents

1. [Overview](#overview)
2. [Technique 1: Prompting](#technique-1-prompting)
3. [Technique 2: Reasoning](#technique-2-reasoning)
4. [Technique 3: Retrieval Augmented Generation](#technique-3-retrieval-augmented-generation)
5. [Technique 4: ReAct (Reason + Act)](#technique-4-react-reason--act)
6. [Technique 5: Tree of Reviews](#technique-5-tree-of-reviews)
7. [Technique 6: Reflexion](#technique-6-reflexion)
8. [Technique 7: Chain-of-Verification](#technique-7-chain-of-verification)
9. [Bonus: Constitutional AI](#bonus-constitutional-ai)
10. [See Also](#see-also)

---

## Overview

[[LLM Hallucinations|Hallucinations]] represent a fundamental challenge in deploying [[Large Language Models|language models]] for critical applications. Modern approaches to mitigating hallucinations leverage the inherent properties of LLMs—their tendency to follow instructions, their capacity to emulate reasoning, and their ability to interact with external tools and knowledge sources.

The techniques described here range from simple to complex:
- **Simple techniques** modify how we prompt the model
- **Intermediate techniques** enhance the model's internal reasoning process
- **Advanced techniques** combine reasoning with external verification and iterative refinement

---

## Technique 1: Prompting

### Description

The simplest and most accessible technique for reducing hallucinations leverages the **sycophantic nature** of most LLMs—their tendency to follow instructions and adhere to stated constraints. By explicitly instructing models to abstain from hallucination, we can significantly improve output reliability.

### Implementation Strategies

**Strict context adherence:**
```
"Answer only from context; otherwise, say I don't know."
```

**Explicit permission boundaries:**
```
"Summarize warranty strictly from docs; do not infer perks."
```

### Real-World Usage

This technique is employed by major technology companies, including:
- [[Apple Intelligence]]
- [[Grok]] (Grok 4)

### Advantages

- ✓ Simple to implement
- ✓ No additional infrastructure required
- ✓ Effective for preventing obvious fabrications
- ✓ Works across different LLM architectures

### Limitations

- ✗ Requires careful prompt engineering
- ✗ May not prevent subtle hallucinations
- ✗ Effectiveness varies by model

---

## Technique 2: Reasoning

### Description

While [[Large Language Models|LLMs]] do not possess true reasoning capability in the human sense, they can **emulate structured reasoning** when explicitly prompted to do so. This technique forces models to generate intermediate steps and logical checks before providing a final answer, making the reasoning process transparent and auditable.

### How It Works

Rather than jumping directly to conclusions, the model:
1. Identifies sub-questions
2. Retrieves supporting evidence
3. Draws conclusions based on evidence

### Example: Tesla Model S Warranty Query

**Step 1: Identify sub-questions**
- What does Tesla's warranty cover for the Model S?
- Does the warranty include roadside assistance?
- Does the warranty cover maintenance?

**Step 2: Retrieve evidence**
- Battery and drive unit coverage: 8 years or 150,000 miles
- General repairs: 4 years or 50,000 miles
- Roadside assistance: Included for warranty duration
- Maintenance: Not covered; owner's responsibility

**Step 3: Conclude and verify**
- Warranty covers battery, drive unit, and general repairs
- Roadside assistance is included
- Maintenance is excluded

### Advantages

- ✓ Makes the model's thought process transparent
- ✓ Easier to audit and verify intermediate steps
- ✓ Reduces logic gaps and premature conclusions
- ✓ Scales with model size and training data

### Related Techniques

This approach forms the foundation for:
- [[Chain of Thought|Chain-of-Thought (CoT)]]
- [[ReAct|Reason + Act (ReAct)]]
- Modern "Thinking" or "Reasoning" modes in advanced LLMs

---

## Technique 3: Retrieval Augmented Generation

### Description

**Retrieval Augmented Generation (RAG)** enhances LLM outputs by grounding responses in external knowledge sources. Rather than relying solely on the model's training data, RAG retrieves relevant documents or information and uses them as context for generation, significantly reducing hallucinations.

### How It Works

1. User query is received
2. Relevant external sources are retrieved
3. Retrieved sources are provided as context
4. Model generates answer grounded in retrieved information
5. Sources are cited for veracity

### Real-World Examples

**Perplexity AI**
- Functions as "RAG over the entire internet"
- Uses webpages as sources
- Cites sources for verification

**Google Notebook LM**
- Allows upload of custom documents (PDFs, etc.)
- Supports imports from Google Drive and YouTube
- Grounds responses in user-provided sources

### Advantages

- ✓ Grounds responses in verified information
- ✓ Provides source attribution
- ✓ Reduces reliance on training data alone
- ✓ Allows customization with domain-specific knowledge

### Limitations

- ✗ Requires access to knowledge sources
- ✗ Quality depends on source quality
- ✗ May not find relevant information for all queries

---

## Technique 4: ReAct (Reason + Act)

### Description

**ReAct** (Reason + Act) unifies internal reasoning with external tool use, enabling LLMs to iteratively think about problems and take actions to gather information. This approach inspired the modern wave of [[Agentic AI|tool-using AI agents]].

### Historical Context

Before the seminal ReAct paper by Yao et al. (2022), LLM reasoning focused exclusively on internal methods ([[Chain of Thought|CoT]]), with tool use being ad-hoc and disconnected from reasoning.

### How It Works

The model operates in an execution loop where each iteration involves:

1. **Reasoning**: Generate thoughts about the problem
2. **Acting**: Call external tools based on reasoning
3. **Observing**: Receive feedback from tool execution
4. **Repeating**: Continue until task completion

### Available Tools

External tools can include:
- Weather APIs
- Web search
- Database queries
- Calculation engines
- Custom domain-specific APIs

### Advantages

- ✓ Combines thinking with action
- ✓ Reduces hallucinations through verification
- ✓ Enables dynamic problem-solving
- ✓ Foundation for modern [[Agentic AI|agentic systems]]

### Impact

ReAct's approach to unified reasoning and action is now reflected in the majority of contemporary LLM implementations.

---

## Technique 5: Tree of Reviews

### Description

**Tree of Reviews (ToR)** represents an advanced synthesis of previous techniques, combining elements of [[#Technique 2: Reasoning|reasoning]], [[#Technique 3: Retrieval Augmented Generation|RAG]], and [[#Technique 4: ReAct (Reason + Act)|ReAct]] into a comprehensive framework for generating reliable LLM outputs.

### Problem with Linear Reasoning

Standard [[#Technique 4: ReAct (Reason + Act)|ReAct]] follows a linear pattern:
- Generate single reasoning → Act on it → Observe → Repeat

**The issue**: If the LLM generates incorrect reasoning at any step, subsequent actions are based on flawed logic, causing a "domino effect" that compounds errors and leads to hallucinations.

### Solution: Tree-Based Reasoning

Instead of a single reasoning path, ToR generates **multiple candidate reasoning paths** and selects the best one:

1. **Generate multiple candidate paths**: Create several possible reasoning approaches
2. **Review each path**: Evaluate candidates using the LLM
3. **Label candidates**: Assign one of three labels to each path
4. **Combine evidence**: Use accepted paths for final answer

###