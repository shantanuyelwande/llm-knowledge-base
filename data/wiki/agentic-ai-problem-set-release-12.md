---
title: Agentic_Ai_Problem_Set_Release_12
source_file: Agentic_Ai_Problem_Set_Release_12.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:28:06.264597
raw_file_updated: 2026-04-17T20:28:06.264597
version: 1
sources:
  - file: Agentic_Ai_Problem_Set_Release_12.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:28:06.264597
tags: []
related_topics: []
backlinked_by: []
---
# Agentic AI Problem Set Release 12

## Overview

**Agentic AI Problem Set Release 12** is an educational resource developed by Prof. Tom Yeh in collaboration with Ofer Mendelevitch that presents 20 core concepts in [[Agentic AI]] through a problem-driven learning methodology. Sponsored by AI by Hand, this problem set was designed to help students understand key agentic AI terminology and concepts that became prominent in 2025.

## Design Philosophy

The problem set follows four core principles:

1. **Problem-Driven**: Each concept begins with a real-world problem statement that motivated the idea
2. **Think-First**: Multiple-choice questions encourage active thinking before revealing answers
3. **Solution-Focused**: Clear explanations show how each term addresses the stated problem
4. **Industry-Informed**: Real-world perspectives from production AI systems complement academic theory

## The 20 Core Agentic AI Concepts

### Reasoning and Planning

#### [[LLM Agent]]
An agent that leverages an LLM's general reasoning ability to follow instructions flexibly. Solves the problem of agents unable to generalize to new instructions by enabling reasoning-based task adaptation rather than reliance on fixed rules.

#### [[Reason-and-Act]] (ReAct)
A framework that makes agents reason explicitly before taking actions. Addresses the problem of agents acting without clear reasoning by ensuring every action has a visible chain of thought behind it.

#### [[Chain of Thought]]
A technique that encourages step-by-step reasoning instead of shallow, direct answers. Prevents agents from skipping important steps by having them "think out loud," producing deeper and more accurate responses.

#### [[Tree of Thought]]
Enables agents to explore multiple reasoning branches in parallel and compare them. Solves the problem of agents sticking to a single line of thinking by generating and evaluating alternative possibilities.

#### [[Graph of Thought]]
Allows agents to link and reuse insights across multiple reasoning branches to support non-linear reasoning. Addresses the problem of agents unable to connect insights across different branches of analysis.

#### [[Plan-and-Execute]]
Separates planning from execution for structured task completion. Fixes the problem of agents improvising without structure by requiring them to outline a clear plan before execution.

### Memory Systems

#### [[Episodic Memory]]
Stores short-term events and recent actions that agents can reference. Solves the problem of agents forgetting what happened recently by maintaining a record of recent interactions and attempts.

#### [[Semantic Memory]]
Stores long-term knowledge and distilled lessons so expertise carries over across interactions. Addresses the problem of agents starting from scratch by enabling persistent knowledge accumulation.

### Tool Integration and Execution

#### [[Tool Use]]
Allows agents to take real actions instead of merely explaining steps. Solves the problem of agents that only provide instructions by enabling direct task execution through tool calls.

#### [[Function Calling]]
Ensures tool calls are structured and machine-executable. Addresses the problem of agents selecting the right tool but failing to emit valid, executable function calls by requiring strict schema compliance.

#### [[Orchestration]]
Coordinates tools, results, and execution steps to keep them synchronized. Fixes the problem of agents struggling to coordinate multiple tools and intermediate results.

#### [[Delegation]]
Hands off work to other tools or sub-agents to avoid bottlenecks. Solves the problem of agents bottlenecking by doing all work alone, enabling parallel task execution.

### Information Retrieval and Context

#### [[RAG]] (Retrieval-Augmented Generation)
Grounds agent reasoning in external data by retrieving relevant documents. Addresses the problem of agents unable to use user data by enabling direct incorporation of external information.

#### [[Graph RAG]]
Reasons over relationships between retrieved documents rather than treating them as isolated chunks. Solves the problem of agents missing connections between documents by building and reasoning over a graph of relationships.

#### [[Context Selection]]
Deliberately chooses only relevant information for the prompt instead of loading entire documents. Addresses the problem of agents grabbing too much irrelevant text by filtering information intelligently.

### Feedback and Improvement

#### [[Agent Loop]]
Adds continuous feedback so agents can observe outcomes and adjust subsequent actions. Solves the problem of agents blindly moving forward without feedback by creating an iterative observation-adjustment cycle.

#### [[Reflection]]
Allows agents to review mistakes and correct themselves before trying again. Addresses the problem of agents repeating the same wrong answer by enabling self-correction.

#### [[Critic]]
Provides preference signals to judge which outputs are better. Fixes the problem of agents producing correct outputs with no sense of preference by evaluating outputs against goals and quality criteria.

### Safety and Governance

#### [[Safety Guardrails]]
Enforces boundaries for safe, governed agent behavior. Solves the problem of agents crossing boundaries they didn't know existed by defining clear rules and limits.

#### [[Model Control Protocol]] (MCP)
Standardizes secure, auditable access to tools and data. Addresses the problem of agents accessing tools inconsistently by providing one clear, permissioned protocol for all actions.

## Industry Insights

### On Production Challenges

> "Most agents today are simple tool loops — but making them production-grade is the real challenge"
> 
> — Ofer Mendelevitch, Head of Developer Relations at Vectara

### On Implementation Complexity

> "The hard part of agents isn't the reasoning — it's everything around it: sessions, tools, state, safety, and scale."
> 
> — Ofer Mendelevitch, Head of Developer Relations at Vectara

### On Enterprise Adoption

> "45% of enterprises will struggle to operationalize agentic prototypes due to governance and infrastructure gaps."
> 
> — Ofer Mendelevitch, Head of Developer Relations at Vectara

### On System Architecture

> "Piecemeal Agentic AI solutions take months to implement — and twice as long to stabilize. Enterprises need an end-to-end Agent Operating System designed to avoid common AI pitfalls."
> 
> — Ofer Mendelevitch, Head of Developer Relations at Vectara

## Learning Methodology

The problem set uses a consistent structure for each concept:

1. **Problem Statement**: Identifies a real challenge in agent behavior
2. **Multiple Choice Question**: Presents four possible solutions
3. **Answer and Explanation**: Reveals the correct concept and explains how it solves the problem
4. **Industry Context**: Provides practical insights from production systems

## Authors and Contributors

- **Prof. Tom Yeh**: Primary developer and academic perspective
- **Ofer Mendelevitch**: Industry collaboration, production insights, author of *Hands-On RAG for Production* (O'Reilly)

## Related Concepts

- [[Artificial Intelligence]]
- [[Large Language Models]]
- [[AI Agents]]
- [[Natural Language Processing]]
- [[Machine Learning Operations]]
- [[AI Safety]]
- [[Knowledge Graphs]]

---

## Metadata

**Source**: Agentic AI Problem Set Release 12  
**Authors**: Prof. Tom Yeh, Ofer Mendelevitch  
**Sponsor**: AI by Hand  
**Topic Area**: [[Agentic AI]], [[AI Education]], [[AI Systems Design]]  
**Key Concepts**: 20 core agentic AI terms  
**Audience**: Students, AI practitioners, enterprise architects  
**Focus**: Problem-driven learning, production-ready AI systems  
**Related Tags**: `agentic-ai`, `llm-agents`, `ai-systems`, `problem-solving`, `educational-resource`