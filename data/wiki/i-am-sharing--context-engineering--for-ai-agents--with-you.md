---
title: I am sharing _Context Engineering  for AI Agents_ with you
source_file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:49:07.895890
raw_file_updated: 2026-04-17T20:49:07.895890
version: 1
sources:
  - file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:49:07.895890
tags: []
related_topics: []
backlinked_by: []
---
# Context Engineering for AI Agents

## Summary

**Context Engineering for AI Agents** is a systematic approach to managing the limited context window of Large Language Models (LLMs) when building AI agent applications. Drawing from Andrej Karpathy's analogy of LLMs as operating systems, context engineering applies across multiple context types including instructions, knowledge, and tool feedback. As AI agents become increasingly sophisticated with long-running tasks and complex tool interactions, effective context management has emerged as a critical engineering discipline for optimizing performance, cost, and reliability.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Context Engineering for Agents](#context-engineering-for-agents)
3. [Core Strategies](#core-strategies)
   - [Write Context](#write-context)
   - [Select Context](#select-context)
   - [Compress Context](#compress-context)
   - [Isolate Context](#isolate-context)
4. [Implementation with LangSmith and LangGraph](#implementation-with-langsmith-and-langgraph)
5. [Conclusion](#conclusion)

---

## Introduction

### The LLM as Operating System

According to Andrej Karpathy, [[Large Language Models|LLMs]] function as a new kind of operating system where:

- The **LLM** acts as the CPU
- The **context window** serves as the RAM (working memory)
- **Context engineering** plays the role of an OS curator, determining what information fits into the model's working memory

Just as operating systems must carefully manage limited RAM capacity, developers building [[AI Agent|AI agents]] must strategically manage the limited context window to handle various sources of information.

### Types of Context

Context engineering applies across three primary context types:

- **Instructions** – prompts, memories, few-shot examples, tool descriptions
- **Knowledge** – facts, semantic information, stored memories
- **Tools** – feedback from tool calls and external system interactions

---

## Context Engineering for Agents

### The Challenge of Long-Running Tasks

As [[AI Agent|agents]] have become more sophisticated with improved reasoning and [[Tool Calling|tool calling]] capabilities, they increasingly handle long-running tasks that interleave multiple LLM invocations with tool calls. While this enables complex problem-solving, it creates significant challenges:

- **Context Window Overflow** – Extended interactions exceed available context capacity
- **Cost and Latency Escalation** – Accumulating tokens dramatically increase computational costs
- **Performance Degradation** – Longer context can paradoxically reduce agent effectiveness

### Context-Related Performance Problems

Drew Breunig identified four specific ways that longer context degrades agent performance:

| Problem | Description |
|---------|-------------|
| **Context Poisoning** | Hallucinations that make their way into the context window |
| **Context Distraction** | Context so voluminous it overwhelms the LLM's training |
| **Context Confusion** | Superfluous context that influences responses unexpectedly |
| **Context Clash** | Conflicting information within the context window |

### Industry Recognition

Both [[Cognition]] and [[Anthropic]] have identified context engineering as fundamental to agent development:

- Cognition emphasizes that context engineering is "effectively the #1 job of engineers building AI agents"
- Anthropic notes that context from tool calls accumulates over hundreds of agent turns, requiring careful management strategies

---

## Core Strategies

Context engineering strategies are organized into four primary buckets: write, select, compress, and isolate.

### Write Context

Writing context means **saving information outside the context window** to help agents perform tasks.

#### Scratchpads

[[Scratchpad|Scratchpads]] enable agents to take notes and persist information during task execution, mirroring how humans solve complex problems by taking notes for future reference.

**Implementation approaches:**
- Tool-based: A tool that writes to persistent storage (files, databases)
- State-based: A field in the agent's runtime state object that persists during the session

**Example:** Anthropic's multi-agent researcher uses scratchpads to save its initial plan to memory before the context window reaches capacity, ensuring the strategic approach persists even as context accumulates.

#### Memories

While scratchpads support single-session persistence, agents often benefit from cross-session memory. Modern approaches include:

- **Reflexion** – Self-generated memories created through reflection after each agent turn
- **Generative Agents** – Memories synthesized periodically from collections of past feedback
- **Production implementations** – ChatGPT, Cursor, and Windsurf all implement auto-generated long-term memories based on user-agent interactions

### Select Context

Selecting context means **pulling relevant information into the context window** to assist agent task execution.

#### Scratchpad Selection

The mechanism for scratchpad retrieval depends on implementation:

- **Tool-based scratchpads** – Agents make tool calls to read relevant sections
- **State-based scratchpads** – Developers expose specific state fields to the LLM at each turn, providing fine-grained control

#### Memory Selection

When agents maintain larger memory collections, intelligent selection becomes critical. Three memory types commonly require selection:

- **Episodic Memories** – Few-shot examples demonstrating desired behavior
- **Procedural Memories** – Instructions to guide agent behavior
- **Semantic Memories** – Task-relevant facts and relationships

**Selection Approaches:**

1. **Static Selection** – Popular code agents (Claude Code, Cursor, Windsurf) use fixed files:
   - CLAUDE.md for instructions and examples
   - Rules files for procedural guidance

2. **Dynamic Selection with Embeddings** – For larger semantic memory collections, [[Embedding|embeddings]] and [[Knowledge Graph|knowledge graphs]] enable relevance-based retrieval

**Challenges:** Memory selection remains difficult at scale. Simon Willison demonstrated unexpected behavior when ChatGPT unexpectedly injected location data from memories into generated images, illustrating risks of uncontrolled memory retrieval.

#### Tool Selection

Agents can become overloaded when provided excessive tool options, especially when tool descriptions overlap. [[Retrieval-Augmented Generation|RAG]] applied to tool descriptions can improve selection accuracy by up to 3-fold by fetching only relevant tools.

#### Knowledge Retrieval

[[RAG|Retrieval-Augmented Generation]] represents a central context engineering challenge in large-scale applications. Code agents demonstrate production-scale RAG complexity:

- **Indexing challenges** – Simple embedding search becomes unreliable as codebases grow
- **Hybrid retrieval** – Effective systems combine multiple techniques:
  - Grep and file-based search
  - Knowledge graph-based retrieval
  - Re-ranking steps to order context by relevance
  - AST parsing for semantically meaningful code chunking

### Compress Context

Compressing context means **retaining only tokens essential** for task performance.

#### Context Summarization

Agent interactions spanning hundreds of turns generate substantial token overhead. Summarization strategies include:

- **Auto-compaction** – Claude Code automatically summarizes full interaction trajectories when exceeding 95% of context window capacity
- **Hierarchical Summarization** – Recursive or tree-based approaches to distill information across agent trajectories
- **Targeted Summarization** – Applied at specific architectural points:
  - Post-processing token-heavy tool calls (e.g., search results)
  - Agent-to-agent boundaries during knowledge handoff

**Implementation Considerations:** Effective summarization requires capturing critical events and decisions. Cognition employs fine-tuned models for this task, indicating the complexity involved.

#### Context Trimming

While summarization uses LLMs to distill relevant information, trimming uses heuristic-based filtering:

- **Hard-coded heuristics** – Removing older messages from conversation history
- **Trained pruners** – Systems like Provence use machine learning to intelligently prune context for question-answering tasks

### Isolate Context

Isolating context means **splitting information** across architectural components to help agents perform tasks.

#### Multi-Agent Architecture

One of the most effective isolation strategies distributes context across multiple specialized agents:

**Benefits:**
- **Separation of Concerns** – Each agent focuses on specific sub-tasks with dedicated tools and instructions
- **Context Efficiency** – Subagent context windows allocate resources to narrow domains more effectively than single-agent approaches
- **Performance Gains** – Anthropic's multi-agent researcher demonstrated that multiple agents with isolated contexts outperformed single-agent systems

**Challenges:**
- **Token Overhead** – Multi-agent systems can use up to 15× more tokens than single-agent chat
- **Coordination Complexity** – Requires careful prompt engineering for sub-agent planning and coordination

#### Context Isolation with Environments

Alternative isolation approaches use sandboxed execution environments:

**HuggingFace Code Agent Example:**
- Agents output code containing desired tool calls
- Code executes in isolated sandbox environments
- Selected results pass