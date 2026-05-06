---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-06T05:35:31.781336
raw_file_updated: 2026-05-06T05:35:31.781336
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-06T05:35:31.781336
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progressive approach to creating agent harnesses, starting from basic coding agents and scaling up to parallel, GPU-accelerated systems capable of handling complex research tasks like OpenAI's Parameter Golf challenge.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building custom agentic systems. Unlike off-the-shelf solutions such as Codex and Claude Code, this SDK provides the foundational building blocks necessary for organizations to develop their own specialized agent harnesses. When combined with [[Modal's Sandboxes]], the SDK enables secure, scalable, and powerful agent systems that can leverage distributed computing resources, including GPUs.

This guide demonstrates how to construct a production-ready agent harness from the ground up, using [[Parameter Golf]] as a practical example of parallel agent research.

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop that pairs a [[Large Language Model]] (LLM) with a set of callable tools (functions). The agent iteratively:

1. Receives context or instructions
2. Invokes appropriate tools based on LLM decisions
3. Processes tool outputs
4. Continues until task completion

The collection of tools and supporting infrastructure surrounding this core loop is called a **Harness**.

### The Agent Harness

A harness encompasses all the architectural decisions and infrastructure that enable an agent to function effectively for specific tasks. This includes:

- Tool definitions and capabilities
- Context management systems
- Memory and session handling
- Resource allocation
- Error handling and safety measures

## Building Progression

### Stage 1: Basic Coding Agent

The simplest implementation uses an `Agent` with an `exec(command)` function that allows arbitrary shell command execution. While functional, this approach presents significant security risks and is unsuitable for production use.

```python
# Pseudocode for basic agent
agent = Agent(tools=[exec_command])
agent.run("write and execute code")
```

**Limitations:**
- Executes commands directly on the host system
- No isolation or security boundaries
- Vulnerable to prompt injection attacks

### Stage 2: Sandboxed Execution

The OpenAI Agents SDK provides a `SandboxAgent` class that isolates agent execution in remote environments. [[Modal Sandboxes]] provide:

- **Isolation**: Linux environments running on VMs or hardened containers
- **Safety**: Commands execute in isolated contexts, not on the host
- **Resource Control**: Ability to attach GPUs and manage computational resources
- **State Management**: Persistent filesystem and environment state

Key components include:

- **SandboxAgent**: Extends the base Agent with sandbox integration
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client for managing remote sandbox instances
- **Capabilities**: Bindings of tool sets to specific sandbox instances

#### GPU Attachment

Modal enables GPU attachment to sandboxes via `ModalSandboxClientOptions`, allowing agents to leverage accelerated computing for training and inference tasks.

### Stage 3: Memory and Sessions

By default, agents are stateless. Each run operates independently without access to previous interactions. [[Sessions]] solve this problem by:

- Accumulating conversation history across multiple agent runs
- Maintaining context across different agent instances
- Enabling multi-turn interactions with persistent memory

**Trade-offs:**
- Introduces [[context rot]] as memory accumulates indefinitely
- Requires active context management to prevent token bloat
- Necessitates strategic memory pruning and reset mechanisms

### Stage 4: Orchestrator and Subagent Architecture

For long-horizon tasks, a single agent becomes token-heavy as it explores codebases and processes extensive stdout/stderr. The solution employs a **two-tier architecture**:

#### Orchestrator Agent
- Maintains high-level task memory and planning
- Manages overall task progression
- Has limited direct access to execution environments
- Focuses on strategic decision-making

#### Subagents
- Spawned by the orchestrator for focused, short-duration tasks
- Operate with fresh context windows and isolated Sessions
- Complete specific work items and return summaries
- Context is discarded after task completion

**Benefits:**
- Prevents context bloat in the main orchestrator
- Enables focused, efficient task execution
- Maintains clear separation of concerns

### Stage 5: Asynchronous Parallel Execution

Rather than blocking the orchestrator while subagents work, a **SubAgentPool** manages multiple concurrent subagents:

- Stores active subagents as key-value pairs
- Uses `asyncio.Future` for non-blocking execution
- Allows orchestrator to spawn multiple parallel research threads
- Enables massive throughput increases for parallel experiments

#### Monitoring Parallel Work

Two mechanisms provide visibility into subagent activity:

1. **Hooks**: Track the current active tool for each subagent
2. **set_status Tool**: Allows subagents to provide periodic status updates without exiting

The orchestrator accesses this information via a `list_subagents` tool that displays active work.

### Stage 6: Resource Management with Quotas

Asynchronous execution introduces the risk of unbounded resource consumption. A **quota system** prevents excessive GPU spending by:

- Limiting the maximum number of concurrent expensive resources (e.g., 8x H100 GPUs)
- Enforcing hard caps on parallel execution
- Preventing runaway cost scenarios

### Stage 7: Filesystem Snapshots for Checkpoint Management

When spawning multiple subagents from base sandboxes, each wastes computational resources on identical setup work:

- Repository cloning
- Dependency installation
- Environment configuration

**Filesystem Snapshots** address this by:

1. **Freezing State**: Capturing a sandbox's complete filesystem state as an immutable snapshot
2. **Branching Work**: Spawning new subagents from known checkpoints rather than base images
3. **Context Offloading**: Using the filesystem as implicit memory, reducing Session context bloat
4. **Artifact Persistence**: Making prior work artifacts available to future agents automatically

This approach transforms the filesystem into a form of implicit, on-disk memory that survives across agent generations.

### Stage 8: Skills Subsystem

The final architectural component adds **pluggable skills** that allow the orchestrator to selectively enable specialized knowledge:

- Keeps the core harness general-purpose
- Enables task-specific optimizations without modifying base code
- Allows the orchestrator to opt-in to domain-specific context
- Supports specialization for challenges like [[Parameter Golf]]

## Practical Example: Parameter Golf

[[Parameter Golf]] is OpenAI's challenge to achieve baseline intelligence thresholds with minimal model parameters. The complete harness enables:

- **Parallel Exploration**: Multiple subagents simultaneously testing different ML frameworks and approaches
- **Checkpoint Branching**: Creating snapshots after successful configurations for future work
- **Autonomous Research**: Orchestrator directing research without manual intervention
- **GPU Acceleration**: Each subagent equipped with GPU resources for model training

### Execution Pattern

```
Orchestrator receives Parameter Golf task
  ↓
Spawns 3 parallel subagents (PyTorch, TensorFlow, JAX)
  ↓
Each subagent creates filesystem snapshot after setup
  ↓
Subagents train models in parallel on GPUs
  ↓
Orchestrator monitors progress via list_subagents
  ↓
Successful approaches trigger new subagent branches from snapshots
  ↓
Results aggregated by orchestrator
```

## Key Architectural Principles

### Composition Over Monoliths

The harness demonstrates that complex agentic systems emerge from composing simple, well-defined components:

- Base agent loops provide core functionality
- Each architectural layer adds specific capabilities
- Components remain loosely coupled and independently testable

### Context as a Precious Resource

Managing context effectively requires:

- Separating long-horizon memory (orchestrator Sessions) from short-term work (subagent Sessions)
- Offloading memory to filesystems when possible
- Aggressively pruning unnecessary context
- Snapshotting state at logical checkpoints

### Security Through Isolation

[[Sandboxes]] provide multiple layers of protection:

- Computational isolation prevents code escape
- Resource limits prevent denial-of-service
- Immutable snapshots prevent state corruption
- Stateless execution allows safe parallelization

## Related Technologies and Concepts

- [[Modal]] - Serverless cloud platform providing Sandboxes and GPU infrastructure
- [[OpenAI API]] - Underlying LLM powering the agent decision-making
- [[Async/Await Patterns]] - Enables non-blocking parallel subagent execution
- [[Container Orchestration]] - Manages the underlying infrastructure
- [[Context Windows]] - Fundamental LLM limitation driving architectural