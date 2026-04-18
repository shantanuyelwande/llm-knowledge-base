---
title: I am sharing _Context Engineering  for AI Agents_ with you
source_file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:10:24.276523
raw_file_updated: 2026-04-17T20:10:24.276523
version: 1
sources:
  - file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:10:24.276523
tags: []
related_topics: []
backlinked_by: []
---
# Context Engineering for AI Agents

## Summary

**Context Engineering for AI Agents** is a comprehensive framework for managing the limited context window of [[Large Language Models|LLMs]] in agent-based systems. Drawing from Andrej Karpathy's analogy of LLMs as operating systems, context engineering parallels how operating systems manage RAM. This discipline encompasses four primary strategies: **writing** context outside the window, **selecting** relevant context for retrieval, **compressing** context to essential tokens, and **isolating** context across multiple agents or environments. As AI agents become increasingly sophisticated and long-running, context engineering has emerged as the critical engineering challenge for building effective agent systems.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Fundamentals of Context Engineering](#fundamentals-of-context-engineering)
3. [Write Context Strategy](#write-context-strategy)
4. [Select Context Strategy](#select-context-strategy)
5. [Compress Context Strategy](#compress-context-strategy)
6. [Isolate Context Strategy](#isolate-context-strategy)
7. [Implementation with LangGraph and LangSmith](#implementation-with-langgraph-and-langsmith)
8. [Conclusion](#conclusion)

---

## Introduction

### The LLM as Operating System

As articulated by Andrej Karpathy, [[Large Language Models|LLMs]] function as a new kind of operating system. In this analogy:

- The **LLM** itself acts as the CPU
- The **context window** serves as the RAM, functioning as the model's working memory
- **Context engineering** plays the role of an operating system's memory management layer

Just as RAM has limited capacity, the [[Context Window|LLM context window]] has finite capacity to handle various sources of context. Context engineering provides the curation mechanism to determine what fits into this constrained space.

### Types of Context to Manage

Context engineering applies across three primary context types:

- **Instructions**: [[Prompt Engineering|Prompts]], memories, [[Few-shot Learning|few-shot examples]], [[Tool Description|tool descriptions]], and other directional information
- **Knowledge**: Facts, stored memories, and domain-specific information
- **Tools**: Feedback from [[Tool Calling|tool calls]] and external system interactions

---

## Fundamentals of Context Engineering

### The Agent Challenge

With growing sophistication in [[Reasoning|reasoning]] and [[Tool Calling|tool calling]] capabilities, [[AI Agent|AI agents]] have become increasingly popular. However, agents present unique context challenges:

- Agents **interleave** [[Large Language Models|LLM]] invocations with tool calls for long-running tasks
- Feedback from tool calls accumulates over multiple agent turns
- Long-running tasks can rapidly consume tokens, causing multiple problems:
  - Exceeding context window limits
  - Ballooning costs and latency
  - Degrading agent performance

### Context-Related Performance Problems

Drew Breunig identified four specific ways that longer context degrades agent performance:

| Problem | Description |
|---------|-------------|
| **Context Poisoning** | Hallucinations that make their way into the context, corrupting subsequent reasoning |
| **Context Distraction** | Context that overwhelms the model's training-based priors and decision-making |
| **Context Confusion** | Superfluous information that influences responses in unintended ways |
| **Context Clash** | Conflicting or contradictory information within the context |

### Industry Recognition

Both Cognition and Anthropic have identified context engineering as critical:

- **Cognition**: Context engineering is "effectively the #1 job of engineers building AI agents"
- **Anthropic**: Agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies

---

## Write Context Strategy

**Writing context** means saving information outside the context window to help an agent perform a task. This enables agents to persist information for future reference without consuming valuable context window space.

### Scratchpads

[[Scratchpad|Scratchpads]] implement a note-taking approach analogous to how humans solve complex tasks. The concept involves saving information outside the context window so it remains available to the agent.

**Implementation approaches:**
- **Tool-based**: Agents call a tool that writes to a file or external storage
- **State-based**: Information persists in a runtime state object during the session

**Example**: Anthropic's multi-agent researcher uses scratchpads to save its task approach and planning. When the context window approaches 200,000 tokens and risks truncation, the scratchpad preserves the plan for continued reference.

### Memories

While scratchpads support task-level persistence within a session, [[Memory|memories]] enable agents to retain information across multiple sessions and interactions.

**Key developments:**
- **Reflexion**: Introduced reflection following each agent turn, with self-generated memories for reuse
- **Generative Agents**: Created memories synthesized periodically from collections of past agent feedback
- **Production implementations**: ChatGPT, Cursor, and Windsurf all feature auto-generated long-term memories that persist across sessions based on user-agent interactions

---

## Select Context Strategy

**Selecting context** means pulling relevant information into the context window to help an agent perform a task. This requires mechanisms to identify and retrieve the most pertinent information.

### Selecting from Scratchpads

The mechanism for selecting scratchpad context depends on implementation:

- **Tool-based scratchpads**: Agents read them via tool calls
- **State-based scratchpads**: Developers can expose specific state fields to the agent at each step, providing fine-grained control

### Selecting from Memories

Agents with memory storage require selection mechanisms to identify relevant memories. Selection serves multiple purposes:

- **Episodic memories** (few-shot examples): Demonstrate desired behavior
- **Procedural memories** (instructions): Steer agent behavior
- **Semantic memories** (facts): Provide task-relevant context

**Selection approaches:**

1. **Static selection**: Many agents use narrow, predefined sets of files always pulled into context
   - Claude Code uses `CLAUDE.md`
   - Cursor and Windsurf use rules files

2. **Dynamic selection**: For larger memory collections, more sophisticated approaches are needed
   - **Embeddings-based retrieval**: Convert memories to embeddings and use semantic search
   - **Knowledge graphs**: Structure memories as graphs for relationship-aware retrieval
   - **Hybrid approaches**: ChatGPT demonstrates large-scale selection from user-specific memory collections

**Selection challenges**: Memory retrieval can be unpredictable. Simon Willison shared an example where ChatGPT unexpectedly injected his location (retrieved from memories) into a requested image, causing users to feel the context window "no longer belonged to them."

### Selecting Tools

Agents using many tools can become overloaded, particularly when tool descriptions overlap and cause model confusion.

**Solution**: Apply [[Retrieval Augmented Generation|RAG]] (retrieval augmented generation) to tool descriptions to fetch only the most relevant tools for a given task. Recent research shows this approach improves tool selection accuracy by 3-fold.

### Selecting Knowledge

[[Retrieval Augmented Generation|RAG]] is central to context engineering and particularly critical in code agents operating at large scale.

**Challenges in large-scale RAG** (as identified by Varun from Windsurf):

- Indexing code ≠ context retrieval
- Simple embedding search becomes unreliable as codebases grow
- Effective approaches require combinations of:
  - Semantic chunking via AST (Abstract Syntax Tree) parsing
  - Grep/file search for exact matching
  - Knowledge graph-based retrieval
  - Re-ranking steps to order results by relevance

---

## Compress Context Strategy

**Compressing context** involves retaining only the tokens required to perform a task, reducing overall token consumption without sacrificing capability.

### Context Summarization

Agent interactions spanning hundreds of turns with token-heavy tool calls benefit from summarization approaches.

**Example**: Claude Code implements "auto-compact," which triggers when the context window exceeds 95% capacity. The system summarizes the full trajectory of user-agent interactions using strategies such as:

- Recursive summarization
- Hierarchical summarization

**Strategic application points:**

1. **Trajectory-level**: Summarize entire agent interaction histories
2. **Tool-level**: Post-process token-heavy tool calls (e.g., search results)
3. **Agent-boundary-level**: Reduce tokens during knowledge handoff between agents

**Implementation complexity**: Cognition uses fine-tuned models for summarization, underscoring the sophistication required when specific events or decisions must be captured.

### Context Trimming

Whereas summarization distills context using [[Large Language Models|LLMs]], **trimming** uses heuristics to filter or "prune" context.

**Approaches:**
- **Hard-coded heuristics**: Remove older messages from conversation