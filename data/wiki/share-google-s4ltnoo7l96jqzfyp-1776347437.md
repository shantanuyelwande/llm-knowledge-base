---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-10T06:30:42.578846
raw_file_updated: 2026-06-10T06:30:42.578846
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-10T06:30:42.578846
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

A comprehensive guide to constructing sophisticated AI agent systems using [[Modal]] infrastructure and [[OpenAI Agents SDK]]. This article demonstrates how to progressively build a production-ready agent harness—starting from a basic coding agent and advancing to a parallel, GPU-accelerated system capable of autonomous research tasks. The approach emphasizes security, scalability, and context management through practical implementation patterns.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and autonomous task execution. While off-the-shelf solutions like Codex and Claude Code exist, many organizations seek to build proprietary agent systems tailored to their specific needs—similar to how [[Ramp]] constructed background coding agents responsible for over half of their pull requests.

This article explores how to integrate the OpenAI Agents SDK with [[Modal]] Sandboxes to create scalable, parallelizable agent harnesses. The example uses OpenAI's [[Parameter Golf]] challenge as a practical demonstration of the system's capabilities.

---

## Core Concepts

### What is an Agent Harness?

An **agent harness** is the complete system surrounding a core agent loop, including:
- Available [[tools]] (functions the agent can invoke)
- State management
- Memory systems
- Security boundaries
- Execution environments

The harness represents the programmable layer where developers can add capabilities, controls, and optimizations specific to their use case.

### Agent Architecture

An `Agent` fundamentally operates as a loop:
1. Receives context/instructions
2. Invokes available [[tools]] to make progress
3. Iterates until task completion

---

## Building Blocks

### Stage 1: Basic Coding Agent

The simplest implementation provides an agent with an `exec(command)` function to run arbitrary shell commands. While functional, this approach poses significant security risks with untrusted prompts or unreliable models.

**Key limitation:** Executes directly on the host system with full privileges.

### Stage 2: Sandbox Isolation

[[Sandboxes]] are isolated Linux environments running on VMs or security-hardened containers. The OpenAI Agents SDK provides:

- **`SandboxAgent`**: Extends the base `Agent` class with sandbox-specific tools
- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: Client interface to remote sandbox instances

#### Capabilities Framework

Tools are grouped into **Capabilities**—sets of tools bound to specific sandbox instances. This enables:
- Stateful tool management
- Multi-tool coordination
- Instance-specific configurations

#### GPU Attachment

[[Modal]] uniquely supports GPU attachment to sandboxes via `ModalSandboxClientOptions`, enabling compute-intensive tasks like model training directly within agent execution.

### Stage 3: Memory and Sessions

By default, agents are stateless. The `Session` object solves this by:
- Accumulating context across multiple agent runs
- Maintaining conversation history
- Persisting state across agent instances

**Challenge introduced:** [[Context rot]]—the degradation of memory quality as context accumulates indefinitely.

#### Context Management Solutions

- **Selective memory retention**: Only preserve essential information
- **Memory summarization**: Compress historical context
- **Context resetting**: Clear memory at logical boundaries

### Stage 4: Orchestration with Subagents

Long-horizon tasks require architectural changes. A two-tier system separates concerns:

#### Orchestrator Agent
- Maintains high-level task memory
- Makes strategic decisions
- Manages subagent lifecycle
- Remains unconcerned with implementation details

#### Subagents
- Execute focused, short-duration tasks
- Receive fresh context windows
- Provide summaries back to orchestrator
- Have their sessions discarded after completion

**Benefit:** Keeps orchestrator context lean while enabling specialized work delegation.

### Stage 5: Asynchronous Parallelization

Rather than blocking on subagent completion, the system implements:

#### SubAgentPool
A key-value store of active subagents enabling:
- Concurrent task execution
- Orchestrator non-blocking operation
- Selective waiting on specific work threads

#### Visibility Tools
- **`Hooks`**: Track current active tool for each subagent
- **`set_status` tool**: Allow subagents to report progress without exiting
- **`list_subagents` tool**: Provide orchestrator visibility into parallel work

### Stage 6: Resource Management with Quotas

GPU resources are expensive and finite. A quota system prevents unbounded resource consumption by:
- Limiting concurrent GPU subagent instances
- Enforcing maximum resource allocation
- Preventing runaway parallel execution

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshots]] freeze sandbox state at specific moments, enabling:

#### Deduplication
- Avoid repeated setup work across subagents
- Reduce GPU time spent on dependency installation
- Checkpoint progress at known points

#### Implicit Memory
- Sandboxes maintain stateful filesystems as implicit memory
- Artifacts from prior agents remain available
- Future agents can branch from known checkpoints without explicit context inclusion

**Advantage:** Offload memory management from [[Session]] state to persistent filesystem storage.

### Stage 8: Skills Subsystem

A **Skills** plugin system allows agents to selectively opt-into domain-specific knowledge:
- Keeps harness general-purpose
- Enables task-specific prompting
- Supports modular capability addition
- Reduces core harness complexity

---

## Implementation Patterns

### Training Example: MNIST

A complete end-to-end example trains an image model on the MNIST dataset:
1. Sandbox receives task description
2. Agent writes training code
3. Executes in sandbox environment
4. Returns trained model and results

This demonstrates the basic agent-sandbox integration working correctly.

### Parallel Research Example: Parameter Golf

The Parameter Golf challenge—cramming intelligence into minimal parameters—demonstrates the full harness:

1. **Orchestrator** receives challenge description
2. **Spawns parallel subagents** for different approaches (frameworks, techniques)
3. **Each subagent** works independently on GPU
4. **Snapshots** progress at key milestones
5. **Branches new work** from snapshots
6. **Skills** guide orchestrator toward effective research patterns
7. **Results** aggregate back to orchestrator

**Outcome:** Autonomous, parallelized research across multiple GPU-accelerated subagents.

---

## Key Design Principles

### Progressive Complexity
- Start with minimal, unsafe implementations
- Incrementally add security, scalability, and sophistication
- Each layer builds on previous foundations

### Composability
- Systems are built by composing smaller components
- Each addition (memory, parallelization, snapshots) is independently useful
- Combinations create emergent capabilities

### Context Efficiency
- Orchestrator memory remains focused on high-level concerns
- Implementation details delegated to subagents
- Filesystem serves as implicit, persistent memory
- Explicit sessions complement rather than replace filesystem storage

### Resource Consciousness
- Quotas prevent runaway resource consumption
- Snapshots eliminate redundant computation
- Asynchronous execution maximizes GPU utilization
- Task parallelization improves throughput

---

## Related Technologies

- [[Modal Sandboxes]]: Isolated execution environments
- [[OpenAI API]]: Language model backend
- [[asyncio]]: Asynchronous task management
- [[GPU computing]]: Hardware acceleration for training
- [[Parameter Golf]]: Efficiency optimization challenge

---

## Practical Considerations

### Security
- Sandboxes isolate agent execution from host systems
- `ShellTool` adds guardrails to command execution
- Quotas prevent resource exhaustion attacks

### Scalability
- Asynchronous subagents enable massive parallelization
- Filesystem snapshots reduce per-agent setup overhead
- Quota systems maintain predictable resource consumption

### Maintainability
- Skills system keeps harness general-purpose
- Clear separation between orchestrator and subagent concerns
- Modular capability design supports future extensions

---

## Getting Started

The complete example project is available at: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

To run the Parameter Golf implementation:
```
# See repository for complete setup instructions
```

[[Modal]] provides $30 in free monthly compute credits for new users.

---

## Metadata

**Source:** Modal Engineering Blog  
**Date:** April 15, 2026  
**Author:** Erik Dunteman, Member of Technical Staff  
**Read Time:** 8 minutes  

**Tags:** `#agents` `#openai` `#modal` `#llm` `#gpu` `#parallelization` `#sandboxes` `#ai-infrastructure`

**Related Topics:** 