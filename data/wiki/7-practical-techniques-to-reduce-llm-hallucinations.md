---
title: 7 Practical Techniques to Reduce LLM Hallucinations
source_file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:29:10.365349
raw_file_updated: 2026-04-05T20:29:10.365349
version: 1
sources:
  - file: I am sharing _7 Practical Techniques to Reduce LLM Hallucinations_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:29:10.365349
tags: ["LLM Hallucinations", "Prompt Engineering", "Retrieval Augmented Generation", "Model Reliability", "AI Safety"]
related_topics: []
backlinked_by: []

---
# LLM Hallucinations: Practical Reduction Techniques

## Overview

**LLM Hallucinations** refer to instances where [[Large Language Models]] generate plausible-sounding but factually incorrect or fabricated information. This article explores seven practical techniques for reducing hallucinations in LLM outputs, ranging from simple prompting strategies to sophisticated multi-stage verification processes.

## Summary

Hallucinations are a fundamental challenge in [[Large Language Models]]. This guide presents seven evidence-based techniques for mitigation:

1. **[[Prompting]]** - Explicit instruction to abstain from hallucinations
2. **[[Reasoning]]** - Forcing structured intermediate steps
3. **[[Retrieval Augmented Generation]]** (RAG) - Grounding responses in retrieved documents
4. **[[ReAct]]** (Reason + Act) - Combining reasoning with tool use
5. **[[Tree of Reviews]]** (ToR) - Multi-path reasoning with evaluation
6. **[[Reflexion]]** - Self-critique and iterative revision
7. **[[Chain-of-Verification]]** (CoVe) - Checklist-based answer validation

---

## Technique 1: Prompting

### Definition

Prompting leverages the [[sycophantic nature]] of LLMs—their tendency to comply with explicit instructions—to encourage models to abstain from hallucinations.

### Implementation

Effective prompting strategies include:

- **Strict context adherence**: "Answer only from context; otherwise, say I don't know."
- **Explicit boundaries**: "Summarize warranty strictly from docs; do not infer perks."

### Notable Applications

This technique is employed by major technology companies, including [[Apple Intelligence]] and [[Grok 4]], demonstrating its effectiveness at scale.

### Advantages

- Simple to implement
- Requires no architectural changes
- Immediately applicable to existing systems

---

## Technique 2: Reasoning

### Definition

Reasoning techniques force LLMs to generate structured, intermediate steps before producing final answers. While LLMs do not "think" or "reason" in the human sense, larger models with more training data can effectively emulate reasoning processes.

### Mechanism

The approach involves:

1. **Identifying sub-questions** - Breaking down the query into constituent parts
2. **Retrieving evidence** - Gathering factual information for each sub-question
3. **Concluding** - Synthesizing evidence into structured answers

### Example Workflow

For a query about Tesla Model S warranty:

- Sub-question: "What does Tesla's warranty cover for the Model S?"
- Evidence: "Battery and drive unit coverage for 8 years or 150,000 miles"
- Conclusion: Structured bullet points grounded in retrieved information

### Benefits

- Reduces logical gaps and non-sequiturs
- Makes the model's "thought process" auditable
- Provides transparency in decision-making
- Forms the foundation for advanced techniques like [[Chain of Thought]] and [[ReAct]]

### Related Techniques

This approach underlies techniques such as:
- [[Chain of Thought]] (CoT)
- [[Reason + Act]] (ReAct)
- "Reasoning" or "Thinking" modes in modern LLMs

---

## Technique 3: Retrieval Augmented Generation

### Definition

**Retrieval Augmented Generation (RAG)** grounds LLM responses in external, retrieved documents or data sources rather than relying solely on the model's training data.

### How It Works

RAG systems:

1. Retrieve relevant documents or passages from a knowledge base
2. Pass retrieved context to the LLM
3. Generate responses based on the provided sources
4. Cite sources for veracity and traceability

### Real-World Examples

- **[[Perplexity AI]]**: A search engine implementing RAG over the entire internet, citing webpages as sources
- **[[Google Notebook LM]]**: Allows users to upload documents (PDFs, Google Drive files, YouTube videos) as sources for grounded responses

### Advantages

- Grounds responses in verifiable sources
- Reduces reliance on model training data alone
- Enables citation and fact-checking
- Scales to specialized knowledge bases

### Limitations

- Dependent on quality of retrieved documents
- Cannot retrieve information not in the knowledge base

---

## Technique 4: ReAct (Reason + Act)

### Definition

**ReAct** (Reason + Act) unifies two capabilities: internal reasoning with external tool use. It executes LLMs in a dynamic loop where each iteration generates either reasoning or an action (tool call).

### Historical Significance

The ReAct framework, introduced by Yao et al. (2022), marked a paradigm shift in LLM design. Prior to this, [[Chain of Thought]] focused exclusively on internal reasoning, while tool use was ad-hoc. ReAct systematically integrated both approaches.

### Mechanism

The execution loop operates as follows:

1. **Generate reasoning**: The model produces internal reasoning
2. **Act on reasoning**: The model calls an external tool (API, web search, calculator, etc.)
3. **Observe outcome**: The model receives results from the tool
4. **Iterate**: Steps 1-3 repeat until task completion

### Supported Tools

- Weather APIs
- Web search engines
- Database queries
- Mathematical calculators
- Custom domain-specific tools

### Impact

ReAct inspired the current wave of [[Agentic AI]] systems and tool-use patterns in modern LLMs.

---

## Technique 5: Tree of Reviews (ToR)

### Definition

**Tree of Reviews (ToR)** synthesizes [[Reasoning]], [[RAG]], and [[ReAct]] into a comprehensive framework that generates multiple candidate reasoning paths and evaluates them systematically.

### Problem with Linear Reasoning

Standard [[ReAct]] follows a linear reasoning-to-action sequence:

- At each step, a single reasoning is generated
- The model acts based on that reasoning
- If the reasoning is flawed, subsequent actions compound the error
- This creates a "domino effect" leading to hallucinations

### ToR Solution: Multi-Path Reasoning

Rather than a single chain, ToR constructs a **tree of reasoning paths**:

1. **Generate multiple candidate paths**: The model produces several possible reasoning approaches
2. **Review each path**: An evaluator LLM assesses each candidate
3. **Label outcomes**: Each path receives one of three labels:
   - **ACCEPT** → Add to evidence pool
   - **SEARCH** → Refine query and expand branch further
   - **REJECT** → Prune branch

### Process

The iterative process continues until:
- Sufficient evidence is accumulated
- Branches are exhausted or pruned
- Accepted evidence is combined for the final answer

### Advantages

- Prevents single-path errors from cascading
- Explores multiple solution approaches
- Provides comprehensive evidence synthesis
- More robust than linear reasoning chains

---

## Technique 6: Reflexion (Self-Critique & Revise)

### Definition

**Reflexion** is an iterative process where LLMs generate outputs, critique them, and reflect on the critique. The reflection is stored as feedback and passed to the next iteration, modeling a [[Reinforcement Learning]] loop.

### Architecture

The Reflexion process involves three LLM roles:

1. **Actor (LM)**: Generates actions (answers, code, solutions) using current input and past reflections
2. **Evaluator (LM)**: Reviews the trajectory and provides internal or external feedback
3. **Self-Reflector (LM)**: Converts feedback into actionable lessons ("what went wrong, what to try next")

### Memory Systems

- **Trajectory (Short-term Memory)**: Stores steps and outcomes of the current attempt
- **Experience (Long-term Memory)**: Saves reflections for future improvement

### Execution Flow

```
Actor → Evaluator → Self-reflection → Memory → Actor (iterate until success)
```

### Key Features

- Feedback loop mimics human learning
- Reflections accumulate as experience over iterations
- Environment provides observations and rewards
- Process continues until task success

### Advantages

- Systematic error correction
- Accumulates learning across iterations
- Transparent feedback mechanisms
- Models human revision processes

---

## Technique 7: Chain-of-Verification (CoVe)

### Definition

**Chain-of-Verification (CoVe)** is a two-stage process where the model first generates an answer, then creates a verification checklist to evaluate the answer's completeness and accuracy.

### Process

1. **Generate answer**: The model produces an initial response
2. **Create checklist**: The model generates verification questions covering all requirements
3. **Evaluate**: The checklist items are used to assess answer quality
4. **Revise**: If checklist items fail, the model uses failures to improve the answer

###