---
title: Agentic_Ai_Problem_Set_Release_12
source_file: Agentic_Ai_Problem_Set_Release_12.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T21:13:34.010141
raw_file_updated: 2026-04-05T21:13:34.010141
version: 1
sources:
  - file: Agentic_Ai_Problem_Set_Release_12.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T21:13:34.010141
tags: []
related_topics: []
backlinked_by: []
---
# Agentic AI Problem Set Release 12

## Overview

The **Agentic AI Problem Set Release 12** is an educational resource developed by Prof. Tom Yeh in collaboration with Ofer Mendelevitch (Vectara) to teach the 20 core concepts of [[Agentic AI]] that gained prominence in 2025. The problem set employs a problem-driven, think-first pedagogical approach sponsored by AI by Hand ✍.

## Design Philosophy

The problem set is structured around five key principles:

1. **Problem-Driven**: Each concept begins with a real-world problem statement that motivated the idea
2. **Think-First**: Multiple-choice questions encourage independent reasoning before revealing answers
3. **Solution-Oriented**: Each answer explains how the concept addresses the stated problem
4. **Industry Insights**: Real-world perspectives from industry practitioners complement academic theory
5. **Practical Application**: Focus on production-grade implementation challenges and practical considerations

## The 20 Core Agentic AI Concepts

### Reasoning and Planning

- **[[LLM Agent]]** — Uses an LLM's general reasoning ability to follow instructions and generalize to new tasks
- **[[Chain of Thought]]** — Encourages step-by-step reasoning to produce deeper, clearer answers instead of shallow replies
- **[[Reason-and-Act (ReAct)]]** — Makes agents reason explicitly before taking actions to ensure transparent decision-making
- **[[Tree of Thought]]** — Generates and evaluates multiple reasoning branches in parallel to explore alternative possibilities
- **[[Graph of Thought]]** — Links and reuses insights across reasoning branches to support non-linear reasoning and connect disparate ideas

### Action and Tool Integration

- **[[Tool Use]]** — Lets agents take real actions instead of just explaining steps
- **[[Function Calling]]** — Ensures tool calls are structured and machine-executable with proper argument validation
- **[[Delegation]]** — Hands off work to tools or sub-agents to avoid bottlenecks and distribute workload
- **[[Orchestration]]** — Coordinates tools, results, and execution steps to keep them in sync

### Feedback and Improvement

- **[[Agent Loop]]** — Adds continuous feedback so agents can observe outcomes and adjust subsequent actions
- **[[Reflection]]** — Allows agents to review mistakes and correct themselves before trying again
- **[[Critic]]** — Provides preference signals to judge which outputs are better and guide iterative improvement

### Planning and Execution

- **[[Plan-and-Execute]]** — Separates planning from execution for structured, organized task completion

### Memory Systems

- **[[Episodic Memory]]** — Stores short-term events and recent actions that agents can reference to avoid repetition
- **[[Semantic Memory]]** — Stores long-term knowledge and distilled lessons so expertise carries over across interactions

### Information Retrieval and Grounding

- **[[Context Selection]]** — Chooses only relevant information for the prompt to keep it focused and compact
- **[[RAG (Retrieval-Augmented Generation)]]** — Grounds reasoning in external data by retrieving and incorporating user documents
- **[[Graph RAG]]** — Reasons over relationships between retrieved documents rather than treating them as isolated chunks

### Infrastructure and Governance

- **[[Model Control Protocol (MCP)]]** — Standardizes secure, auditable access to tools and data across all agent interactions
- **[[Safety Guardrails]]** — Enforces boundaries for safe, governed agent behavior with clear limits and rules

## Problem-Solution Mapping

| # | Problem | Solution |
|---|---------|----------|
| 1 | Agents blindly move forward without feedback | [[Agent Loop]] |
| 2 | Agents cannot connect insights across branches | [[Graph of Thought]] |
| 3 | Agents struggle to keep tools and steps in sync | [[Orchestration]] |
| 4 | Agents access tools inconsistently | [[Model Control Protocol]] |
| 5 | Agents cannot reason over document relationships | [[Graph RAG]] |
| 6 | Agents cannot generalize to new instructions | [[LLM Agent]] |
| 7 | Agents cross unknown boundaries | [[Safety Guardrails]] |
| 8 | Agents produce correct outputs without preference | [[Critic]] |
| 9 | Agents improvise instead of planning | [[Plan-and-Execute]] |
| 10 | Agents cannot use user data for reasoning | [[RAG]] |
| 11 | Model selects tool but produces invalid call | [[Function Calling]] |
| 12 | Agents repeat the same wrong answer | [[Reflection]] |
| 13 | Agents act with no reasoning | [[Reason-and-Act]] |
| 14 | Agents give shallow replies | [[Chain of Thought]] |
| 15 | Agents grab too much irrelevant text | [[Context Selection]] |
| 16 | Agents cannot build persistent expertise | [[Semantic Memory]] |
| 17 | Agents tell but cannot execute | [[Tool Use]] |
| 18 | Agents forget recent events | [[Episodic Memory]] |
| 19 | Agents bottleneck work by doing it alone | [[Delegation]] |
| 20 | Agents never explore alternative branches | [[Tree of Thought]] |

## Key Industry Insights

### Production-Grade Implementation
> "Most agents today are simple tool loops — but making them production-grade is the real challenge"

The gap between functional prototypes and production-ready systems requires careful attention to orchestration, state management, and reliability.

### Governance and Infrastructure Challenges
> "45% of enterprises will struggle to operationalize agentic prototypes due to governance and infrastructure gaps."

Organizations face significant challenges in translating successful proofs-of-concept into deployed systems, particularly around safety, compliance, and infrastructure requirements.

### Complexity Beyond Reasoning
> "The hard part of agents isn't the reasoning — it's everything around it: sessions, tools, state, safety, and scale."

While reasoning capabilities are well-developed, the surrounding infrastructure—session management, tool integration, state persistence, safety mechanisms, and scalability—represents the true engineering challenge.

### Need for Integrated Solutions
> "Piecemeal Agentic AI solutions take months to implement — and twice as long to stabilize. Enterprises need an end-to-end Agent Operating System designed to avoid common AI pitfalls."

Fragmented approaches to building agentic systems lead to extended development and stabilization timelines. Integrated, purpose-built platforms can significantly reduce time-to-value.

## Pedagogical Approach

The problem set uses a structured learning methodology:

1. **Problem Statement** (odd-numbered pages): Presents a concrete challenge agents face
2. **Multiple Choice Question**: Offers four possible solutions, encouraging learners to think critically
3. **Answer and Explanation** (even-numbered pages): Reveals the correct concept and explains how it solves the problem
4. **Industry Context**: Interspersed insights from practitioners provide real-world validation and additional perspective

This approach ensures learners understand not just *what* each concept is, but *why* it matters and *when* to apply it.

## Related Topics

- [[Artificial Intelligence]]
- [[Large Language Models]]
- [[AI Safety]]
- [[Prompt Engineering]]
- [[Knowledge Graphs]]
- [[Information Retrieval]]
- [[Multi-Agent Systems]]

## Metadata

**Source**: Agentic AI Problem Set Release 12  
**Authors**: Prof. Tom Yeh, Ofer Mendelevitch  
**Sponsor**: AI by Hand ✍  
**Year**: 2025  
**Focus**: 20 Core Agentic AI Concepts  
**Contributor Affiliation**: Vectara  

**Tags**: `agentic-ai` `problem-set` `education` `llm-agents` `ai-systems` `tool-use` `memory-systems` `safety` `orchestration` `production-ai`

**Related Resources**:
- Hands-On RAG for Production (O'Reilly) by Ofer Mendelevitch
- AI by Hand initiative