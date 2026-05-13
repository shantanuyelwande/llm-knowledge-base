---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-13T05:55:15.147864
raw_file_updated: 2026-05-13T05:55:15.147864
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-13T05:55:15.147864
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article describes how to build custom AI agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] sandboxes. It demonstrates progressive complexity from a basic coding agent to a sophisticated parallel research harness capable of autonomously running experiments on GPUs, using the [[Parameter Golf]] challenge as a practical example.

---

## Introduction

The [[OpenAI Agents SDK]] provides foundational building blocks for creating custom agentic systems. When integrated with [[Modal]]'s sandbox infrastructure, developers can build scalable, parallel agent systems with GPU acceleration. This approach enables organizations to create internal tools similar to those deployed by companies like [[Ramp]], which uses background coding agents to generate over half of its pull requests.

## Core Concepts

### What is an Agent?

An **Agent** is fundamentally a for-loop with a [[Large Language Model]] (LLM) running [[tools]] (functions) to achieve task completion. The supporting infrastructure built around this core loop is called a **Harness** - the collection of tools, state management, and capabilities that give agents context and resources.

### The Agent Harness

A harness is the product engineering layer around agent loops, completely within the programmer's control. It provides:
- Context and state management
- Tool definitions and constraints
- Resource allocation (compute, memory, GPUs)
- Communication patterns between agents

## Building Progression

### Stage 1: Basic Coding Agent

The simplest agent implementation uses an `exec(command)` function as a tool, allowing the LLM to run arbitrary shell commands. While functional, this approach poses significant security risks with malicious prompts or lower-quality models.

**Key limitation:** Runs on the host machine with full system access.

### Stage 2: Sandbox Isolation

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. The OpenAI Agents SDK provides:

- **`SandboxAgent`**: Extends the base `Agent` class with preloaded tools for remote sandbox interaction
- **`ShellTool`**: Adds guardrails to shell command execution
- **`ModalSandboxSession`**: Client for managing remote sandbox communication

#### Capabilities and GPU Attachment

Tools become **stateful** when bound to a specific `ModalSandboxSession` instance. Capabilities define ways to bind tool sets to sandbox instances. [[GPU]] resources can be requested using `ModalSandboxClientOptions`, enabling compute-intensive tasks like machine learning model training.

### Stage 3: Memory and Sessions

By default, agents are stateless. **[[Sessions]]** solve this by:
- Accumulating conversation context across multiple agent runs
- Persisting memory across different agent instances
- Enabling multi-turn interactions with context preservation

**Challenge introduced:** [[Context Rot]] - as memory accumulates indefinitely, context management becomes critical to prevent context bloat.

### Stage 4: Orchestration with Subagents

Long-horizon tasks require splitting work across multiple agents:

- **Orchestrator Agent**: Main chat agent maintaining high-level memory and task context
- **Subagents**: Spawn with fresh context windows for focused, short-burst tasks
- **`invoke_subagent` Tool**: Allows orchestrator to delegate work while maintaining lean context

**Pattern:** Task description → Subagent execution → Summary response → Context cleanup

### Stage 5: Async Parallel Execution

**`SubAgentPool`**: A key-value data structure managing multiple concurrent subagents. Enables:

- Non-blocking orchestrator operations
- Parallel experiment throughput
- Asynchronous task management via `asyncio.Future`

#### Visibility and Control

- **[[Hooks]]**: Track current active tools for each subagent
- **`set_status` Tool**: Allows subagents to provide status updates without full context switching
- **`list_subagents` Tool**: Gives orchestrator visibility into active work

### Stage 6: Resource Quotas

With unbounded async capabilities, GPU costs can spiral. A **quota system** limits expensive resource usage (e.g., fixed number of H100 GPUs in simultaneous use).

### Stage 7: Filesystem Snapshots

**Challenge:** Subagents waste GPU time on redundant setup (dependency installation, repository cloning).

**Solution:** [[Filesystem Snapshots]] freeze active sandbox state into persistent IDs, allowing future subagents to branch from known checkpoints.

**Benefits:**
- Eliminates duplicate setup work
- Provides implicit memory via filesystem state
- Allows subagents to resume work without explicit context injection
- Offloads memory management from token-limited sessions

### Stage 8: Skills Subsystem

A **Skills** plugin system allows the orchestrator to selectively opt-in to specialized context and prompting strategies without cluttering the core harness. This keeps the harness general-purpose while enabling task-specific optimization.

## Practical Example: Parameter Golf Research

[[Parameter Golf]] is an OpenAI challenge to achieve baseline intelligence thresholds with minimal model parameters. The complete harness enables:

1. **Parallel execution**: Multiple subagents simultaneously exploring different ML frameworks
2. **GPU acceleration**: Each subagent runs on dedicated GPU resources
3. **Checkpoint recovery**: Filesystem snapshots allow branching from successful states
4. **Autonomous research**: Skills subsystem guides orchestrator through specialized prompting
5. **Resource efficiency**: Quotas prevent runaway GPU consumption

## Key Design Patterns

### Context Management

- **Hot context**: Session memory for active decision-making
- **Cold context**: Filesystem state as implicit memory
- **Memory offloading**: Use sandboxes as stateful compute environments

### Scalability Architecture

```
Orchestrator (Main thread)
├── Subagent Pool (Async workers)
│   ├── Worker 1 (Fresh context)
│   ├── Worker 2 (Fresh context)
│   └── Worker N (Fresh context)
└── Filesystem Snapshots (Shared checkpoints)
```

### Tool Hierarchy

- **Orchestrator tools**: High-level planning, subagent management, status monitoring
- **Subagent tools**: Shell execution, code modification, status reporting
- **Sandbox tools**: Resource-constrained execution with guardrails

## Implementation Considerations

### Security

- Isolate LLM execution in sandboxes rather than host machines
- Use `ShellTool` guardrails instead of raw `exec()`
- Implement quota systems to prevent resource exhaustion

### Performance

- Use filesystem snapshots to eliminate redundant work
- Implement async patterns to maximize parallelism
- Keep orchestrator context lean through summarization

### Maintainability

- Use capabilities to organize tool sets logically
- Implement skills as plugins for task-specific logic
- Leverage hooks for observability and debugging

## Integration with Modal

[[Modal]] provides:

- **Sandbox infrastructure**: Isolated environments for safe agent execution
- **GPU resources**: Attach H100s and other accelerators to sandboxes
- **Scalability**: Spin up and tear down compute resources on-demand
- **Cost efficiency**: Pay only for active compute with free tier credits ($30/month)

## Related Technologies

- [[OpenAI Agents SDK]]: Base framework for agent construction
- [[Large Language Models]]: The reasoning engine for agents
- [[Reinforcement Learning from Human Feedback]]: Improves agent behavior
- [[Tool Use]]: Enables agents to interact with external systems
- [[Prompt Engineering]]: Guides agent behavior through instructions

## Conclusion

Building sophisticated agent systems requires thoughtful composition of multiple patterns: isolation, memory management, parallelization, and resource control. The OpenAI Agents SDK provides the building blocks, while Modal's sandbox infrastructure provides the execution environment. Together, they enable developers to create production-grade autonomous research systems.

The progression from basic to advanced harnesses demonstrates that complexity emerges through incremental feature addition, each solving specific challenges (security, memory, parallelism, cost). This modular approach allows teams to build customized agent systems tailored to their specific needs.

---

## Metadata

**Source:** Modal Engineering Blog  
**Author:** Erik Dunteman (Member of Technical Staff, Modal)  
**Published:** April 15, 2026  
**Read time:** 8 minutes  
**Repository:** [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

### Tags

`#agents` `#llm` `#openai` `#modal` `#sandboxes` `#gpu` `#parallelization` `#agent-orchestration` `#autonomous-systems` `#infrastructure`

### Related Articles

- [[OpenAI Agents SDK Overview]]
- [[Modal Sandboxes Guide]]
- [[GPU Acceleration for Machine Learning]]
- [[How Ramp Built Background Coding Agents]]
- [[Agent Orchestration Patterns]]
- [[