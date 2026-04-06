---
title: Context Engineering for AI Agents
source_file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:16:14.053910
raw_file_updated: 2026-04-05T20:16:14.053910
version: 1
sources:
  - file: I am sharing _Context Engineering  for AI Agents_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:16:14.053910
tags: []
related_topics: []
backlinked_by: []
---
# Context Engineering for AI Agents

## Summary

**Context Engineering for AI Agents** is a comprehensive framework for managing the limited context window of large language models (LLMs) in [[AI Agent]] applications. Drawing an analogy to operating systems managing RAM, context engineering applies strategies to write, select, compress, and isolate different types of context—including [[Prompt Engineering|instructions]], knowledge, and tool feedback—to optimize agent performance, reduce token consumption, and prevent context-related performance degradation.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Context Types](#context-types)
4. [Context Engineering Strategies](#context-engineering-strategies)
5. [Implementation with LangGraph and LangSmith](#implementation-with-langgraph-and-langsmith)
6. [Challenges and Solutions](#challenges-and-solutions)
7. [Conclusion](#conclusion)

---

## Introduction

### The Context Window as Working Memory

[[Large Language Model|LLMs]] function as a new kind of operating system, where the model itself acts as the CPU and its [[Context Window|context window]] serves as the working memory—analogous to RAM in traditional computers. Just as operating systems carefully manage what data fits into RAM, engineers building LLM applications must thoughtfully curate what information fits into the [[Context Window|context window]].

This practice, termed **context engineering**, has emerged as a critical discipline in [[AI Agent]] development. As noted by leading AI researchers, context engineering represents one of the most important responsibilities of engineers building production AI agents.

### Why Context Engineering Matters

The growing sophistication of [[AI Agent|agents]]—systems that interleave [[Large Language Model|LLM]] invocations with [[Tool Use|tool calls]] for long-running tasks—has highlighted the urgency of context management. Long-running agent tasks accumulate extensive feedback from tool calls, rapidly consuming tokens and creating numerous problems:

- **Increased costs and latency** from token consumption
- **Context window overflow** exceeding model capacity
- **Degraded agent performance** from accumulated context

---

## Core Concepts

### Context Poisoning

When hallucinations or inaccurate information become embedded in the context, they can propagate through subsequent agent reasoning steps, leading to compounded errors.

### Context Distraction

An overwhelming volume of context can cause the [[Large Language Model|LLM]] to lose focus on the core task, as the model struggles to distinguish signal from noise.

### Context Confusion

Superfluous or tangential information in the context can influence model outputs in unintended ways, steering responses away from optimal solutions.

### Context Clash

When different parts of the context contradict each other, the [[Large Language Model|LLM]] must resolve conflicting information, potentially leading to suboptimal decision-making.

---

## Context Types

Context engineering applies across multiple categories of information that agents must manage:

### Instructions

- [[Prompt Engineering|Prompts]] and system instructions
- [[Few-Shot Learning|Few-shot examples]]
- [[Tool Use|Tool descriptions]]
- Memory references
- Behavioral guidelines

### Knowledge

- Factual information
- Domain-specific data
- Historical context
- User profiles and preferences

### Tools

- [[Tool Use|Tool]] feedback and results
- Tool call outputs
- Error messages and exceptions
- Return values from external systems

---

## Context Engineering Strategies

Context engineering employs four primary strategies, each addressing different aspects of context management:

### Write Context

**Writing context** involves saving information outside the active context window to preserve it for future agent steps or sessions.

#### Scratchpads

[[Scratchpad|Scratchpads]] function as persistent note-taking mechanisms within an agent's workflow. Similar to how humans take notes while solving problems, agents can write information to scratchpads—implemented either as [[Tool Use|tool calls]] that write to files or as fields in the agent's runtime state object.

**Example**: Anthropic's multi-agent researcher saves its task plan to a scratchpad at the beginning of execution, ensuring the plan persists even if the context window reaches its 200,000-token limit.

#### Memories

While scratchpads support task-specific context within a session, **memories** enable agents to retain information across multiple sessions or conversations. This approach, inspired by concepts like [[Reflexion]] and [[Generative Agents]], allows agents to:

- Generate self-reflections after each turn
- Synthesize periodic memories from accumulated feedback
- Build long-term knowledge about users and tasks

Popular applications including [[ChatGPT]], [[Cursor (IDE)|Cursor]], and [[Windsurf]] implement auto-generated long-term memories that persist across user sessions.

### Select Context

**Selecting context** involves retrieving relevant information from storage and injecting it into the active context window when needed.

#### Scratchpad Selection

The mechanism for retrieving scratchpad information depends on implementation:
- **Tool-based scratchpads**: Agents call a read tool to access stored information
- **State-based scratchpads**: Developers selectively expose state fields to the [[Large Language Model|LLM]] at each step

#### Memory Selection

When agents maintain large collections of memories, intelligent selection becomes critical. Different memory types require different retrieval approaches:

- **Episodic memories** (examples): Selected to demonstrate desired behavior patterns
- **Procedural memories** (instructions): Retrieved to guide agent behavior
- **Semantic memories** (facts): Fetched for task-relevant contextual information

**Challenge**: While some agents use simple, fixed file sets (e.g., [[Claude Code|Claude Code's]] `CLAUDE.md`), larger memory collections require sophisticated retrieval. [[Embedding|Embeddings]] and [[Knowledge Graph|knowledge graphs]] are commonly employed for indexing, though imperfect memory selection can create privacy and user experience issues.

#### Tool Selection

Providing agents with too many [[Tool Use|tools]] causes performance degradation, particularly when tool descriptions overlap and create confusion. [[Retrieval Augmented Generation (RAG)|RAG]] techniques applied to tool descriptions can improve tool selection accuracy by up to 3-fold.

#### Knowledge Selection via RAG

[[Retrieval Augmented Generation (RAG)|RAG]] represents a significant context engineering challenge, particularly in code agents. Production implementations must address:

- Semantic code indexing using [[Abstract Syntax Tree (AST)|AST]] parsing
- Chunking along meaningful boundaries
- Combining multiple retrieval techniques (grep, file search, knowledge graphs)
- Re-ranking retrieved context by relevance

### Compress Context

**Compressing context** reduces token consumption by retaining only information essential for task completion.

#### Context Summarization

As agent interactions span hundreds of turns and accumulate token-heavy [[Tool Use|tool calls]], summarization becomes essential. [[Claude Code]] implements "auto-compact," automatically summarizing the full agent-user interaction trajectory when context usage exceeds 95%.

Summarization strategies include:
- **Recursive summarization**: Hierarchical compression across agent trajectories
- **Post-processing summarization**: Condensing outputs from specific [[Tool Use|tools]] (e.g., search results)
- **Boundary summarization**: Compressing context at agent-to-agent handoffs in multi-agent systems

**Challenge**: Capturing specific events or critical decisions during summarization requires careful design, sometimes necessitating fine-tuned models.

#### Context Trimming

Where summarization uses [[Large Language Model|LLMs]] to distill relevant information, **trimming** applies heuristic-based filtering:

- Hard-coded rules (e.g., removing older messages)
- Trained context pruning models (e.g., [[Provence]] for question-answering tasks)

### Isolate Context

**Isolating context** involves partitioning information across different agent components or execution environments to prevent interference and manage token usage more effectively.

#### Multi-Agent Architecture

One of the most effective isolation strategies involves splitting work across specialized sub-agents, each with:
- Dedicated context windows
- Specific [[Tool Use|tools]] and capabilities
- Focused responsibilities

**Advantages**: Anthropic's research demonstrated that multiple specialized agents often outperform single monolithic agents because each sub-agent's context window can be allocated to narrower, more focused tasks.

**Trade-offs**: Multi-agent approaches require:
- Higher token consumption (up to 15× more tokens than single-agent chat)
- Sophisticated [[Prompt Engineering|prompt engineering]] for task planning
- Careful coordination mechanisms between agents

#### Context Isolation with Environments

Rather than exposing all context to the [[Large Language Model|LLM]], agents can execute [[Tool Use|tool calls]] in isolated environments (sandboxes) and selectively pass back results.

**Example**: HuggingFace's CodeAgent outputs executable code that runs in a sandbox, with selected return values fed back to the [[Large Language Model|LLM]]. This approach excels at isolating token-heavy objects like images and audio files.

#### State-