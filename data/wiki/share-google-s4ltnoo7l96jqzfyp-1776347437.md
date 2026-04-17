---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-16T16:56:48.160009
raw_file_updated: 2026-04-16T16:56:48.160009
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-16T16:56:48.160009
tags: ["OpenAI Agents SDK", "Modal", "AI Agents", "Scalable Computing", "GPU Optimization"]
related_topics: []
backlinked_by: []

---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] for scalable computation. It demonstrates a progressive approach to agent development, starting from basic coding agents and evolving into a sophisticated system with parallel execution, memory management, and GPU resource optimization. The example uses OpenAI's [[Parameter Golf]] challenge to showcase real-world agent capabilities.

---

## Introduction

The launch of the [[OpenAI Agents SDK]] represents a significant advancement in building customizable agentic systems. Unlike off-the-shelf solutions such as Codex and Claude Code, this SDK provides developers with the building blocks to create powerful internal tools tailored to specific organizational needs. [[Modal]], a cloud platform for running code at scale, integrates seamlessly with this SDK to provide agents with isolated computing environments and access to GPUs.

This article documents the progression from a basic coding agent to a sophisticated parallel research harness capable of autonomously conducting complex experiments.

---

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop that combines a [[Large Language Model]] (LLM) with a set of executable tools. The agent repeatedly:
1. Receives context or a task
2. Decides which tools to invoke
3. Executes those tools
4. Processes results and continues until task completion

### What is a Harness?

A **harness** is the broader system surrounding the core agent loop, encompassing:
- Tool definitions and capabilities
- State management
- Context handling
- Integration layers
- Security boundaries

The harness is where developers exercise creative control to optimize agents for specific use cases.

---

## Building Blocks: Progressive Development

### Stage 1: Basic Coding Agent

The simplest agent implementation uses an `exec(command)` function as a tool, allowing the LLM to execute arbitrary shell commands. While straightforward, this approach poses significant security risks and is not recommended for production use.

**Key limitation:** The agent operates directly on the host system, creating potential security vulnerabilities.

### Stage 2: Sandboxed Execution

[[Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. Moving agent execution into sandboxes provides:

- **Security isolation**: The LLM interacts with a contained environment rather than the host system
- **Resource control**: Compute resources can be limited and monitored
- **Reproducibility**: Sandboxes can be snapshot and restored to known states

The [[OpenAI Agents SDK]] provides the `SandboxAgent` class, which comes preloaded with tools for managing remote sandboxes. The `ShellTool` class adds additional safety guardrails to command execution.

**Key concept:** [[Capability|Capabilities]] bind sets of tools to specific sandbox instances, creating stateful, isolated tool environments.

#### GPU-Accelerated Sandboxes

[[Modal]] uniquely supports GPU attachment to sandboxes via `ModalSandboxClientOptions`, enabling agents to run computationally intensive tasks like model training directly within their execution environment.

### Stage 3: Memory and Sessions

By default, agents are stateless—each run receives input and returns output without retaining conversation history. [[Session|Sessions]] solve this by:

- Accumulating context across multiple agent runs
- Maintaining conversation history
- Enabling multi-turn interactions

**Trade-off:** As memory accumulates, [[context rot]] becomes a concern, requiring active management to prevent context bloat.

### Stage 4: Hierarchical Agent Architecture

For long-horizon tasks, a single agent quickly exhausts its token budget. The solution is a two-tier architecture:

1. **Orchestrator Agent**: Maintains high-level task memory and planning
2. **Subagents**: Execute focused, short-duration tasks with fresh context windows

The orchestrator uses an `invoke_subagent` tool to spawn subagents for specific subtasks. Once complete, subagents return a summary, and their context is discarded, keeping the orchestrator's context lean.

**Benefit:** Enables work decomposition and prevents context bloat from implementation details.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking while subagents execute sequentially, a [[SubAgentPool]] manages multiple parallel subagents using `asyncio.Future` objects. This enables:

- **Higher throughput**: Multiple experiments run simultaneously
- **Better resource utilization**: GPUs remain active across multiple tasks
- **Scalability**: The orchestrator can manage dozens of parallel workers

**Implementation details:**
- [[Hook|Hooks]] track active tools for each subagent
- `set_status` tool allows subagents to provide status updates
- `list_subagents` tool gives the orchestrator visibility into worker state

### Stage 6: Resource Quotas

With unbounded async task spawning, GPU costs become uncontrolled. A **quota system** limits the number of expensive resources (e.g., 8x H100 GPUs) in use simultaneously, providing predictable cost management.

### Stage 7: Filesystem Snapshots

When multiple subagents start from identical base sandboxes, they redundantly perform the same setup work (repository cloning, dependency installation). **Filesystem snapshots** freeze a sandbox state into a reusable image, allowing future subagents to:

- Branch work from known checkpoints
- Avoid duplicate setup work
- Access artifacts from prior agents without explicit context inclusion

**Dual benefit:** Reduces wasted computation and provides implicit memory via the filesystem, offsetting context window limitations.

### Stage 8: Skills Subsystem

Rather than hardcoding task-specific prompts into the core harness, a **skills system** allows the orchestrator to selectively opt into contextual knowledge via plugins. This maintains harness generality while enabling specialization for specific challenges like [[Parameter Golf]].

---

## Complete Example: Parameter Golf Research

The article demonstrates these concepts through building an autonomous research harness for OpenAI's [[Parameter Golf]] challenge—optimizing model performance within strict parameter budgets.

### Architecture Overview

```
Orchestrator Agent
├── Maintains task memory
├── Spawns parallel subagents
├── Monitors progress via hooks and status updates
└── Manages filesystem snapshots as checkpoints

Subagent Pool (Parallel Workers)
├── Subagent 1: Framework A testing
├── Subagent 2: Framework B testing
└── Subagent 3: Framework C testing

Shared Resources
├── GPU quota (e.g., 8x H100s)
├── Filesystem snapshots
└── Skills plugins
```

### Workflow

1. Orchestrator receives Parameter Golf challenge context
2. Orchestrator spawns multiple subagents to explore different approaches
3. Each subagent:
   - Pulls the repository
   - Installs dependencies (or starts from a snapshot)
   - Trains models with different hyperparameters
   - Reports results back to orchestrator
4. Orchestrator reviews results and spawns new subagents based on findings
5. Process repeats until convergence or resource exhaustion

---

## Key Technical Insights

### Context Management

Effective agent harnesses require sophisticated context management:
- **Session state** maintains conversation history in memory
- **Filesystem state** provides implicit memory for code and artifacts
- **Snapshots** allow branching from known good states
- **Hooks** provide observability without context inclusion

### Parallelism vs. Context

There is a fundamental tension between:
- **Parallelism**: Running many subagents simultaneously maximizes throughput
- **Context efficiency**: Each subagent needs sufficient context to work effectively

The solution uses hierarchical decomposition where the orchestrator maintains high-level context while subagents handle implementation details.

### GPU Utilization

GPUs are expensive resources requiring careful management:
- Attach GPUs directly to sandboxes for agent use
- Implement quotas to prevent runaway spending
- Use filesystem snapshots to avoid redundant setup work
- Parallelize work to keep GPUs continuously utilized

---

## Implementation Resources

The complete, production-ready example code is available on GitHub: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

Key files demonstrate:
- Basic agent setup with sandboxes
- Session management for memory
- Orchestrator-subagent architecture
- Async pool implementation
- Filesystem snapshot usage
- Skills system integration

---

## Related Concepts

- [[OpenAI Agents SDK]]: The foundational framework
- [[Modal]]: Cloud platform for scalable computation
- [[Sandbox|Sandboxes]]: Isolated execution environments
- [[Large Language Model]]: The reasoning engine
- [[Parameter Golf]]: Example optimization challenge
- [[Context Window]]: Token budget limitations
- [[Async Programming]]: Parallel execution patterns
- [[GPU Computing]]: Accelerated workloads
- [[Ramp]] (case study): Real-