---
title: I am sharing _Context Engineering  for AI Agents_ with you
source_file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:48:04.646958
raw_file_updated: 2026-04-24T18:48:04.646958
version: 1
sources:
  - file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:48:04.646958
tags: []
related_topics: []
backlinked_by: []
---
# Context Engineering for AI Agents

## Summary

**Context Engineering for AI Agents** is a systematic approach to managing the limited context window of [[Large Language Models]] (LLMs) when building [[AI Agents]]. Drawing parallels to operating system RAM management, context engineering encompasses strategies for writing, selecting, compressing, and isolating context to optimize agent performance, reduce token usage, and prevent performance degradation in long-running tasks.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Context Engineering Strategies](#context-engineering-strategies)
4. [Implementation with LangGraph and LangSmith](#implementation-with-langgraph-and-langsmith)
5. [Challenges and Solutions](#challenges-and-solutions)
6. [Conclusion](#conclusion)

---

## Introduction

### The LLM as Operating System

As articulated by Andrej Karpathy, [[Large Language Models]] function as a new kind of operating system, where:

- The LLM itself operates as the CPU
- The [[context window]] serves as the model's working memory, analogous to RAM
- Context engineering plays the role of an OS curator, determining what information fits into the available capacity

Just as operating systems must carefully manage RAM allocation, AI engineers must strategically manage what context is available to the LLM at any given time.

### Types of Context

Context engineering encompasses three primary types of information that require management:

1. **Instructions** - Prompts, memories, [[few-shot examples]], tool descriptions
2. **Knowledge** - Facts, historical information, domain-specific data
3. **Tools** - Feedback from [[tool calling]] operations

---

## Core Concepts

### Why Context Engineering Matters

As the complexity of [[AI Agents]] has grown, context engineering has emerged as a critical discipline. Major AI organizations recognize its importance:

- **Cognition**: Context engineering is "effectively the #1 job of engineers building AI agents"
- **Anthropic**: Context from tool calls accumulates over multiple agent turns, requiring careful management strategies

### The Problem: Context Degradation

Long-running agent tasks accumulate tokens that can cause several performance problems, identified by Drew Breunig:

| Problem | Description |
|---------|-------------|
| **Context Poisoning** | Hallucinations become embedded in the context, corrupting future decisions |
| **Context Distraction** | Excessive context overwhelms the model's reasoning |
| **Context Confusion** | Superfluous information causes incorrect responses |
| **Context Clash** | Conflicting information in context leads to contradictory outputs |

These issues can result in:
- Exceeding context window limits
- Increased costs and latency
- Degraded agent performance
- Token waste in long-running conversations (potentially spanning hundreds of turns)

---

## Context Engineering Strategies

### 1. Write Context

**Write context** means saving information outside the context window to help an agent perform a task, preserving it for future use.

#### Scratchpads

Scratchpads function as an agent's note-taking system, allowing agents to persist information during task execution:

- **Concept**: Save information outside the context window so it remains available to the agent
- **Implementation**: Can be implemented as a tool that writes to a file, or as a field in a runtime state object
- **Example**: Anthropic's multi-agent researcher uses scratchpads to save its approach and planning, ensuring critical information isn't lost when the context window exceeds capacity

Scratchpads are particularly valuable within a single session or thread.

#### Memories

Memories extend the scratchpad concept across multiple sessions, allowing agents to learn and retain information over time:

- **Reflexion**: Introduced reflection following each agent turn, with agents reusing self-generated memories
- **Generative Agents**: Created memories synthesized periodically from collections of past feedback
- **Production Examples**: ChatGPT, Cursor, and Windsurf all feature auto-generated long-term memories that persist across sessions based on user-agent interactions

### 2. Select Context

**Select context** means pulling relevant information into the context window to help an agent perform a task.

#### Scratchpad Selection

The mechanism for retrieving scratchpad context depends on implementation:

- **Tool-based**: Agents retrieve scratchpad content via tool calls
- **State-based**: Developers can selectively expose specific state fields to the LLM at each step, providing fine-grained control

#### Memory Selection

When agents maintain large memory collections, selection becomes critical. Different memory types serve different purposes:

- **Episodic Memories**: Few-shot examples demonstrating desired behavior
- **Procedural Memories**: Instructions that steer agent behavior
- **Semantic Memories**: Facts and task-relevant context

**Selection Challenges:**

- Many code agents use narrow file sets that are always included (e.g., CLAUDE.md, rules files)
- Larger semantic memory collections require more sophisticated retrieval
- **Embeddings** and [[knowledge graphs]] are commonly used for memory indexing
- Selection errors can occur: Simon Willison reported ChatGPT unexpectedly injecting his location from memory into generated images

#### Tool Selection

Agents can become overloaded when provided with too many tools, especially when tool descriptions overlap and cause confusion:

- **Solution**: Apply [[Retrieval Augmented Generation]] (RAG) to tool descriptions
- **Results**: Recent papers show 3-fold improvement in tool selection accuracy when using RAG-based filtering

#### Knowledge Selection via RAG

[[Retrieval Augmented Generation]] is a central context engineering challenge, particularly in code agents operating at production scale:

**Challenges identified by Windsurf:**
- Indexing code ≠ context retrieval
- Embedding search becomes unreliable as codebases grow
- Multiple retrieval techniques are necessary: grep/file search, [[knowledge graph]]-based retrieval, and re-ranking steps

### 3. Compress Context

**Compress context** by retaining only the tokens required to perform a task, reducing overall token consumption.

#### Context Summarization

Summarization distills token-heavy interactions into concise summaries:

- **Trajectory Summarization**: Claude Code runs "auto-compact" when exceeding 95% of context window, summarizing the full history of user-agent interactions
- **Strategies**: Recursive or hierarchical summarization can be applied across agent trajectories
- **Targeted Summarization**: Can be applied to specific points in agent design:
  - Post-processing token-heavy tool calls (e.g., search results)
  - Summarizing at agent-agent boundaries during knowledge hand-offs
- **Challenges**: Capturing specific events or decisions requires careful implementation; Cognition uses fine-tuned models for this purpose

#### Context Trimming

Trimming filters or "prunes" context rather than summarizing it:

- **Hard-coded Heuristics**: Remove older messages from conversation history
- **Trained Pruners**: Provence is an example of a trained context pruner for [[Question-Answering]]
- **Advantage**: Often simpler than summarization but may lose important details

### 4. Isolate Context

**Isolate context** by splitting it across different components or agents to help manage overall token consumption.

#### Multi-Agent Architecture

One of the most effective isolation strategies is distributing tasks across multiple specialized agents:

- **Separation of Concerns**: Each agent handles specific sub-tasks with its own tools, instructions, and context window
- **Example**: OpenAI Swarm library was motivated by this principle
- **Performance**: Anthropic's multi-agent researcher demonstrated that many agents with isolated contexts outperformed single-agent approaches, because each subagent's context window can be allocated to narrower, more focused sub-tasks
- **Parallel Execution**: Subagents can operate in parallel, exploring different aspects of a problem simultaneously
- **Trade-offs**: 
  - Can use up to 15× more tokens than single-agent chat (per Anthropic)
  - Requires careful prompt engineering to coordinate sub-agent work
  - Demands sophisticated coordination mechanisms

#### Context Isolation with Environments

[[HuggingFace]]'s deep researcher demonstrates an alternative isolation approach:

- **Traditional Approach**: Tool calling APIs return JSON objects that are passed to tools, with results returned to the LLM
- **CodeAgent Approach**: Agents output executable code that runs in a sandbox environment
- **Benefit**: Token-heavy objects (images, audio, large data structures) can be isolated from the LLM in the environment
- **Return Values**: Selected context from tool calls is passed back to the LLM as needed

#### State-Based Isolation

An agent's runtime state object provides another isolation mechanism:

- **Schema Design**: Define a state object with multiple fields for different types of information
- **Selective Exposure**: Only expose certain fields (e.g., messages) to the LLM at each turn
- **Deferred Access**: