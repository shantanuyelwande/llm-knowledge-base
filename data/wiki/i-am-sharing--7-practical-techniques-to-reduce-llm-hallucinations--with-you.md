---
title: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you
source_file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:02:14.849848
raw_file_updated: 2026-04-24T19:02:14.849848
version: 1
sources:
  - file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:02:14.849848
tags: []
related_topics: []
backlinked_by: []
---
# LLM Hallucinations: Practical Reduction Techniques

## Summary

**LLM Hallucinations** are instances where [[Large Language Models]] generate plausible-sounding but factually incorrect or fabricated information. This article outlines seven practical techniques for reducing hallucinations in LLM applications, ranging from [[Prompting]] strategies to advanced methods like [[Tree of Thoughts]] and [[Reflexion]]. These techniques address the fundamental challenge of ensuring LLM outputs remain grounded in factual information and verifiable evidence.

---

## Overview

[[Large Language Models]] are powerful tools, but they suffer from a significant limitation: they can generate convincing-sounding but entirely false information. This phenomenon, known as hallucination, occurs because LLMs predict the next token based on patterns in training data rather than accessing or reasoning about ground truth.

This article presents seven practical techniques that have been successfully implemented by major technology companies and research institutions to mitigate hallucinations and improve output reliability.

---

## 1. Prompting

### Concept

[[Prompting]] leverages the sycophantic nature of most LLMs—their tendency to follow instructions and comply with user requests—to explicitly prevent hallucinations. By carefully crafting instructions, developers can guide models to abstain from generating ungrounded information.

### Practical Strategies

**Strict instructions to stick to context:**
- Example: "Answer only from context; otherwise, say I don't know."
- This creates a clear boundary between available information and speculation.

**Explicit allowances and restrictions:**
- Example: "Summarize warranty strictly from docs; do not infer perks."
- Clearly defines what operations are permitted and which are prohibited.

### Real-World Implementation

Major technology companies including [[Apple Intelligence]] and Grok 4 incorporate these prompting principles into their systems to reduce hallucinations at scale.

---

## 2. Reasoning

### Concept

While [[Large Language Models]] do not possess genuine reasoning capabilities in the human sense, they can emulate structured reasoning when prompted to generate intermediate steps before producing final answers. This technique forces the model to show its work, making errors more detectable.

### Mechanism

The approach involves instructing the LLM to:
1. Break down complex queries into sub-questions
2. Retrieve and cite evidence for each sub-question
3. Draw conclusions based on evidence
4. Provide final answers grounded in the reasoning chain

### Example Workflow

For a query about Tesla Model S warranties:

**Step 1: Identify sub-questions**
- What does Tesla's warranty cover for the Model S?
- Does the warranty include roadside assistance?
- Does the warranty cover maintenance?

**Step 2: Retrieve evidence**
- Battery and drive unit coverage: 8 years or 150,000 miles
- Basic vehicle warranty: 4 years or 50,000 miles
- Roadside assistance: Included for warranty duration
- Maintenance: Not covered; owner responsibility

**Step 3: Conclude with grounded claims**
- Warranty covers battery and drive unit for 8 years or 150,000 miles
- Basic vehicle warranty covers general repairs for 4 years or 50,000 miles
- Roadside assistance is included
- Maintenance is not covered

### Benefits

- **Auditability**: The model's "thought process" becomes transparent and verifiable
- **Error Detection**: Logical jumps or incorrect assumptions become visible
- **Foundation for Advanced Methods**: This technique underpins more sophisticated approaches like [[Chain of Thought]] and [[Reason + Act]].

---

## 3. Retrieval Augmented Generation (RAG)

### Concept

[[Retrieval Augmented Generation]] (RAG) grounds LLM responses in external, verifiable sources rather than relying solely on the model's training data. The system retrieves relevant documents or web pages and cites them as evidence for its claims.

### How RAG Works

1. User submits a query
2. System retrieves relevant documents from a knowledge base or the internet
3. LLM generates a response based on retrieved sources
4. Response includes citations linking to source material
5. Users can verify claims by consulting original sources

### Real-World Examples

**Perplexity AI:**
- Functions as a RAG system over the "entire internet"
- Retrieves webpages and cites them for veracity
- Provides transparent source attribution

**Google Notebook LM:**
- Allows users to upload documents, PDFs, or import from Google Drive and YouTube
- Grounds responses in user-provided sources
- Maintains document-level traceability

### Advantages

- **Verifiability**: Claims are directly traceable to sources
- **Currency**: Can access up-to-date information beyond training data
- **Transparency**: Users understand the evidence basis for responses

---

## 4. ReAct (Reason + Act)

### Concept

[[ReAct]] (Reason + Act) represents a paradigm shift in how [[Large Language Models]] handle hallucinations by unifying two previously separate approaches: internal reasoning and external tool use. Introduced by Yao et al. (2022), ReAct inspired the current wave of [[Agentic AI]] and tool-use capabilities.

### Key Innovation

Before ReAct, LLM reasoning focused exclusively on internal reasoning methods like [[Chain of Thought]], with tool use remaining ad-hoc and disconnected. ReAct unified these approaches into a coherent execution loop.

### Mechanism

The ReAct process operates as a dynamic execution loop:

1. **Reasoning Phase**: LLM generates internal reasoning or planning
2. **Action Phase**: LLM calls external tools based on its reasoning
3. **Observation Phase**: System receives results from tool execution
4. **Iteration**: Process repeats until task completion

### Available Tools

External tools can include:
- APIs (weather, web search, database queries)
- Calculators and computational engines
- Domain-specific services
- Real-time information sources

### Impact

ReAct's framework has become foundational to modern agentic AI systems, where models can dynamically decide between thinking and acting based on task requirements.

---

## 5. Tree of Thoughts (ToT)

### Concept

[[Tree of Thoughts]] (ToT) extends [[ReAct]] by addressing a critical limitation: the linear nature of single-path reasoning. While ReAct follows a single chain of reasoning and actions, ToT generates multiple possible reasoning paths and evaluates them as a tree structure, selecting the most promising branches.

### Problem Addressed

In linear ReAct processes:
- The LLM generates a single reasoning step
- It acts based on that reasoning
- If the reasoning is flawed, subsequent actions follow the wrong path
- This creates a "domino effect" leading to hallucinated or incorrect outputs

### Solution: Tree Structure

Instead of a single chain, ToT constructs a tree of candidate reasoning paths:

```
                    Initial Query
                         |
            ______________|__________
           /              |          \
      Path 1          Path 2      Path 3
       /  \            /  \         /  \
      A    B          C    D       E    F
```

### Evaluation Process

Each reasoning path (candidate path) receives one of three labels:

| Label | Action | Purpose |
|-------|--------|---------|
| **ACCEPT** | Add to evidence pool | Promising path continues |
| **SEARCH** | Refine query + expand branch | Path needs deeper exploration |
| **REJECT** | Prune branch | Path is unproductive |

### Final Answer Generation

- Accepted evidence from all viable paths is combined
- Final answer synthesizes insights from multiple reasoning branches
- Reduces risk of following a single flawed reasoning path

### Advantages

- **Robustness**: Multiple independent reasoning paths provide redundancy
- **Exploration**: Systematically explores solution space rather than committing early
- **Evidence Integration**: Combines insights from multiple perspectives

---

## 6. Reflexion (Self-Critique & Revise)

### Concept

[[Reflexion]] implements a self-improvement loop where an [[Large Language Model]] generates output, critiques its own work, and uses that critique to improve in subsequent iterations. The approach mirrors [[Reinforcement Learning]] principles but operates entirely through text-based feedback and reflection.

### Architecture

The Reflexion system employs LLMs in three distinct roles:

#### Actor (LM)
- **Role**: Generates primary output (answers, code, solutions)
- **Input**: Current query + past reflections from experience memory
- **Output**: Action or answer attempt

#### Evaluator (LM)
- **Role**: Reviews the actor's output (trajectory)
- **Function**: Provides both internal and external feedback
- **Output**: Structured evaluation of performance

#### Self-Reflector (LM)
- **Role**: Transforms feedback into actionable lessons
- **Function**: Converts evaluator feedback into concise