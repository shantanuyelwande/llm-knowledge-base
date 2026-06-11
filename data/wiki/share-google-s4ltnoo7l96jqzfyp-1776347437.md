---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-11T06:54:17.165842
raw_file_updated: 2026-06-11T06:54:17.165842
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-11T06:54:17.165842
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent]] systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] serverless computing platform. It demonstrates a progressive approach to building agent harnesses, starting from basic coding agents and evolving into a sophisticated parallel system capable of managing multiple autonomous agents with GPU resources, memory management, and context optimization.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in agent development, providing building blocks for teams to construct their own agentic systems. When combined with [[Modal Sandboxes]], developers can create powerful agent harnesses that leverage cloud computing resources at scale.

This guide walks through building a general-purpose coding harness capable of tackling complex tasks like OpenAI's [[Parameter Golf]] challenge, with the ability to parallelize work across multiple GPU-equipped subagents.

## Core Concepts

### What is an Agent Harness?

An **agent harness** is the collection of tools, state management, and infrastructure built around a core [[agent loop]]. The harness provides:

- **Tools**: Functions the agent can invoke to accomplish tasks
- **State**: Memory and context for multi-turn interactions
- **Environment**: The execution environment (local, sandboxed, or distributed)

### Basic Agent Architecture

At its simplest, an `Agent` is a for-loop with an [[LLM]] running tools to task completion:

```python
Agent → Tool Invocation → Task Completion
```

The most basic coding agent includes an `exec(command)` function allowing arbitrary shell command execution, though this approach presents significant security risks.

## Progressive Development Approach

### Stage 1: Basic Coding Agent

The simplest implementation uses an LLM with shell execution capabilities:

- **Pros**: Simple, straightforward implementation
- **Cons**: Security risks, no isolation, unsafe for production

### Stage 2: Sandbox Isolation

Moving agents into [[Modal Sandboxes]] provides:

- **Isolated Linux environments** built on VMs or security-hardened containers
- **ShellTool** class with built-in guardrails
- **GPU attachment** capability via `ModalSandboxClientOptions`
- **ModalSandboxSession** client management

The `SandboxAgent` class provides preloaded tools for remote sandbox interaction, with **Capabilities** binding tool sets to specific sandbox instances.

### Stage 3: Memory and Sessions

By default, agents are stateless. [[Sessions]] solve this by:

- Accumulating conversation context across multiple runs
- Maintaining state across agent instances
- Enabling multi-turn interactions with persistent memory

**Challenge**: Managing [[context rot]] as memory accumulates indefinitely.

### Stage 4: Orchestration with Subagents

For long-horizon work, agents are split into two types:

**Orchestrator Agent**:
- Maintains high-level memory and planning
- Manages task decomposition
- Spawns and monitors subagents

**Subagents**:
- Execute focused, short-duration tasks
- Work with fresh context windows
- Report summaries back to orchestrator

This separation keeps orchestrator context tight while enabling specialized task execution.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking orchestrator operations, a **SubAgentPool** manages multiple concurrent subagents:

- **Key-value mapping** of active subagents
- **asyncio.Future** objects for non-blocking task management
- **Hooks** to track active tools in each subagent
- **set_status** tool for progress updates without exiting

Tools exposed to orchestrator:
- `invoke_subagent`: Spawn new parallel agents
- `list_subagents`: Monitor active subagent status
- `wait_for_subagent`: Block on specific task completion

### Stage 6: Resource Management with Quotas

GPU cost control is implemented through quota systems:

- Fixed limits on expensive resource allocation
- Prevents unbounded spawning of GPU subagents
- Ensures predictable infrastructure costs

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshots]] optimize repeated work:

- **Deduplication**: Avoid redundant setup across subagents
- **Checkpointing**: Freeze sandbox state for later branching
- **Implicit memory**: Filesystem state acts as persistent context
- **Context offloading**: Reduce session memory pressure

Subagents can branch from known checkpoints rather than starting from base images, dramatically reducing setup time and context bloat.

### Stage 8: Skills Subsystem

A pluggable skills architecture enables:

- **Selective context opt-in** via skill plugins
- **Task-specific prompting** without core harness modification
- **Generalized harness design** with specialized capabilities

## Implementation Example: Parameter Golf

The article demonstrates these concepts through OpenAI's [[Parameter Golf]] challenge—cramming intelligence into minimal model parameters.

### Parallel Training Architecture

```
Orchestrator Agent
├── Subagent Pool (Async)
│   ├── Subagent 1 (Framework A + GPU)
│   ├── Subagent 2 (Framework B + GPU)
│   └── Subagent 3 (Framework C + GPU)
└── Filesystem Snapshots (Checkpoints)
```

The orchestrator naturally parallelizes work across different ML frameworks, with each subagent:
- Training independently on GPU resources
- Discovering efficiency optimizations
- Reporting progress back to orchestrator
- Sharing filesystem snapshots for checkpoint resumption

## Key Technical Patterns

### Context Management

Multiple strategies keep context lean:

1. **Session-based memory** in orchestrator only
2. **Filesystem-based memory** in sandbox state
3. **Snapshot-based branching** to discard intermediate context
4. **Hook-based monitoring** for status tracking

### Scalability Mechanisms

- **Async/await patterns** for non-blocking operations
- **Worker pools** for managing concurrent agents
- **Quota systems** for resource constraints
- **Snapshot branching** for efficient task resumption

### Security & Isolation

- **Sandboxed execution** prevents host compromise
- **ShellTool guardrails** add safety to commands
- **Isolated sessions** prevent cross-contamination
- **Resource quotas** prevent denial-of-service

## Related Technologies

- [[OpenAI Agents SDK]]: Core agent framework
- [[Modal]]: Serverless compute platform
- [[Modal Sandboxes]]: Isolated execution environments
- [[LLM]]: Language models powering agent reasoning
- [[Parameter Golf]]: Efficiency optimization challenge
- [[Ramp]]: Example company using background coding agents

## Practical Considerations

### When to Use This Architecture

- Complex multi-step coding tasks
- Parallel experimentation and research
- Long-horizon autonomous work
- GPU-intensive workloads requiring parallelization
- Tasks requiring persistent state across operations

### Common Challenges

- **Context bloat**: Mitigated through snapshots and selective memory
- **Orchestrator blocking**: Solved with async subagent pools
- **Redundant setup**: Addressed via filesystem snapshots
- **Unbounded costs**: Controlled with quota systems
- **Agent coherence**: Maintained through session-based memory

## Getting Started

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

To begin:

1. Set up a [[Modal]] account (includes $30 free compute credits)
2. Clone the example repository
3. Configure OpenAI API credentials
4. Run the Parameter Golf example
5. Customize the harness for your specific use case

## Key Takeaway

Agent systems can be composed incrementally from base agent loops, adding features progressively:

```
Basic Agent → Sandboxing → Memory → Orchestration → Parallelization → 
Snapshots → Skills → Production System
```

Each layer adds capability while maintaining composability, allowing developers to build sophisticated autonomous systems tailored to specific domains and constraints.

---

## Metadata

**Source**: Modal Blog - Engineering  
**Author**: Erik Dunteman (@erikdunteman), Member of Technical Staff  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  
**Original Source**: https://share.google/S4lTnOo7l96jQZFyP

### Tags

- [[AI Agents]]
- [[Agent Architecture]]
- [[OpenAI]]
- [[Modal]]
- [[Sandboxes]]
- [[GPU Computing]]
- [[Parallel Processing]]
- [[LLM Applications]]
- [[System Design]]
- [[Cloud Computing]]

### Related Topics

- [[AI Agent Design Patterns]]
- [[Distributed Computing]]
- [[Context Management in LLMs]]
- [[GPU Resource Allocation]]
- [[Serverless Computing]]
- [[