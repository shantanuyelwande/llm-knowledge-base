---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-08T04:58:43.499339
raw_file_updated: 2026-05-08T04:58:43.499339
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-08T04:58:43.499339
tags: []
related_topics: []
backlinked_by: []
---
# Building Agents with Modal and OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] for scalable, GPU-backed execution. It demonstrates a progressive approach from basic coding agents to sophisticated multi-agent orchestration systems capable of parallel task execution and context management.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding tasks, research, and automation. When combined with [[Modal]]'s [[Sandbox|sandboxes]] and GPU infrastructure, developers can create powerful, scalable agent harnesses that rival purpose-built solutions while maintaining full control over customization.

This integration is particularly relevant for organizations like [[Ramp]] that have successfully deployed internal coding agents responsible for substantial portions of their pull request generation.

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop structure where a [[Large Language Model]] (LLM) executes [[Tool|tools]] (functions) to accomplish tasks. The collection of tools, state management, and surrounding infrastructure is called a "Harness."

### The Agent Harness

A harness represents the complete system architecture surrounding the core agent loop. It includes:

- Tool definitions and capabilities
- State and memory management
- Context control mechanisms
- Integration with external services
- Monitoring and observability

## Building Blocks: From Basic to Advanced

### 1. Basic Coding Agent

The simplest agent implementation uses an `exec()` function to run arbitrary shell commands. While functional, this approach presents significant security risks and is not recommended for production use.

**Key limitation:** Exposes the host system to potentially malicious LLM-generated commands.

### 2. Sandboxed Execution

[[Modal Sandbox|Sandboxes]] provide isolated Linux environments built on VMs or security-hardened containers. By running agent commands within sandboxes, the LLM operates within a confined environment rather than directly on the host system.

**Key features:**
- `SandboxAgent` class for remote sandbox management
- `ShellTool` class with built-in guardrails
- `ModalSandboxSession` client for sandbox communication
- GPU attachment capabilities via `ModalSandboxClientOptions`

### 3. Memory and Sessions

By default, agents are stateless. The [[Session]] concept solves this limitation by accumulating context across multiple agent runs and user interactions.

**Challenge introduced:** [[Context Rot]] - the degradation of context quality as memory accumulates indefinitely, requiring active context management strategies.

### 4. Orchestrator-Subagent Architecture

To manage long-horizon tasks and prevent context bloat, agents are split into two roles:

- **Orchestrator:** Main chat agent maintaining memory for entire task
- **Subagent:** Fresh context window spawned for focused, short-duration tasks

The orchestrator uses an `invoke_subagent` tool to delegate work, receiving summaries rather than implementation details.

**Benefit:** Tight context management with high-level task focus in the orchestrator while subagents handle implementation details.

### 5. Asynchronous Parallel Execution

Rather than blocking orchestrator execution, a [[SubAgentPool]] manages multiple parallel subagents using `asyncio.Future` objects.

**Implementation details:**
- Key-value store of active subagents
- Modified `invoke_subagent` tool storing futures
- Tools for selective waiting on specific work threads
- [[Hook|Hooks]] for tracking active tools per subagent
- `set_status` tool for periodic status updates without exiting

**Requirement:** Special handling to prevent orchestrator premature exit before async tasks complete.

### 6. GPU Resource Management

With async parallelization, agents can spawn unbounded GPU-intensive subagents. A quota system constrains resource usage, ensuring fixed limits on expensive GPU allocations (e.g., 8x H100s).

### 7. Filesystem Snapshots

Subagents starting from base sandboxes waste GPU time on redundant setup (repository pulls, dependency installation). [[Filesystem Snapshot|Filesystem snapshots]] freeze sandbox state into reusable images.

**Dual benefits:**
1. **Performance:** Fresh subagents branch from known checkpoints
2. **Context Management:** Filesystems serve as implicit memory, offloading context requirements

**Two implementation approaches:**
- **Explicit:** Writing skills/memory files to filesystem
- **Implicit:** Pre-configured codebase state available to all future agents

### 8. Skills Subsystem

A pluggable system allowing agents to selectively opt-into specialized context and prompting strategies without embedding task-specific logic in the core harness.

**Advantage:** Maintains harness generality while enabling specialized behavior for specific challenges like [[Parameter Golf]].

## Practical Example: Parameter Golf Research

The [[Parameter Golf]] challenge tasks participants with achieving baseline intelligence thresholds with minimal model parameters. The described agent harness tackles this by:

1. Spawning multiple parallel subagents for different ML frameworks
2. Leveraging GPU compute for training and experimentation
3. Snapshotting successful states for branch-and-explore workflows
4. Managing orchestrator context to prevent token bloat
5. Using skills to guide research direction

**Result:** Autonomous parallel research across multiple approaches without overwhelming the orchestrator's context window.

## Key Architectural Patterns

### Context Management Strategy

```
Primary Context (Session) → High-level task memory
Implicit Context (Filesystem) → Artifacts and codebase state
Subagent Context → Fresh windows for focused work
```

### Parallelization Pattern

```
Orchestrator (blocking-resistant)
├── Subagent Pool (async workers)
│   ├── Worker 1 (GPU-enabled)
│   ├── Worker 2 (GPU-enabled)
│   └── Worker N (GPU-enabled)
└── Status monitoring via hooks and set_status
```

## Related Technologies and Concepts

- [[Modal]] - Serverless compute platform for agents
- [[OpenAI Agents SDK]] - Framework for building agent systems
- [[Sandbox|Sandboxes]] - Isolated execution environments
- [[Large Language Model]] - Core reasoning engine
- [[Parameter Golf]] - Efficiency optimization challenge
- [[Ramp]] - Real-world implementation example

## Advantages of This Approach

1. **Composability:** Systems built from modular components
2. **Scalability:** Parallel execution across distributed sandboxes
3. **Safety:** Isolated execution prevents host compromise
4. **Customization:** Full control over harness design
5. **Resource Efficiency:** GPU quotas and filesystem snapshots optimize costs
6. **Context Control:** Multiple strategies prevent token waste

## Implementation Resources

- **Complete Example Repository:** [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Platform:** [Modal.com](https://modal.com)
- **Documentation:** [Modal Docs](/docs)
- **Getting Started:** $30 free monthly compute credits available

## See Also

- [[AI Agent Architecture]]
- [[Serverless Computing]]
- [[GPU Computing]]
- [[LLM Context Management]]
- [[Distributed Systems]]
- [[Agentic Workflows]]

---

## Metadata

**Source:** [Modal Blog - Building with Modal and the OpenAI Agents SDK](https://share.google/S4lTnOo7l96jQZFyP)

**Published:** April 15, 2026

**Author:** Erik Dunteman (Modal Technical Staff)

**Article Type:** Technical Guide / Tutorial

**Topics:** 
- [[Artificial Intelligence]]
- [[Agent Systems]]
- [[Cloud Computing]]
- [[GPU Computing]]
- [[Distributed Systems]]
- [[Software Architecture]]

**Related Articles:**
- How Ramp Built a Full-Context Background Coding Agent on Modal
- OpenAI Agents SDK Launch
- Parameter Golf Challenge

**Reading Time:** 8 minutes