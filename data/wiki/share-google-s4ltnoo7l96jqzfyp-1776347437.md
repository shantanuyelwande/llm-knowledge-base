---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-02T06:48:18.018909
raw_file_updated: 2026-06-02T06:48:18.018909
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-02T06:48:18.018909
tags: []
related_topics: []
backlinked_by: []
---
# Building Agents with Modal and OpenAI Agents SDK

## Summary

This article describes how to build custom AI agent harnesses using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progression from basic [[Coding Agents|coding agents]] to sophisticated parallel agent systems capable of managing multiple GPU-accelerated subagents, with applications like OpenAI's Parameter Golf challenge. The approach emphasizes composition of features like [[Sandboxes]], memory management, and asynchronous task distribution to create scalable agentic systems.

## Overview

The [[OpenAI Agents SDK]] represents a new approach to building internal agent systems. Rather than relying on off-the-shelf solutions like Codex or Claude Code, organizations can now construct customized agent harnesses tailored to their specific needs. [[Modal]] provides the infrastructure foundation through [[Sandboxes|sandbox]] environments and GPU resources that enable these agents to execute code safely and at scale.

This architecture is inspired by real-world implementations like [[Ramp]]'s [[Background Coding Agents|background coding agent]] system, which now generates over half of their pull requests autonomously.

## Core Concepts

### What is an Agent Harness?

An agent harness is the complete system surrounding a core [[Agent]] loop. It includes:

- **Tools**: Functions the agent can invoke
- **Context**: Information available to the agent
- **State Management**: Memory and session handling
- **Orchestration**: Coordination of multiple agents
- **Safety Measures**: Guardrails and resource limits

The harness is entirely under programmer control, making it a form of product engineering around the base agent loop.

### Basic Agent Architecture

A minimal [[Coding Agents|coding agent]] at its core is a loop where an [[Large Language Model|LLM]] executes [[Tools|tools]] (functions) until task completion. The simplest example includes an `exec(command)` function for running shell commands.

**Warning**: Basic local execution is unsafe and not recommended for production use without proper security measures.

## Building Progressively Safer Systems

### Stage 1: Local Execution

The simplest approach executes commands directly on the host system:

```python
# Minimal unsafe agent with direct shell access
agent = Agent(tools=[exec_tool])
```

While straightforward, this approach presents significant security risks with malicious prompts or unreliable models.

### Stage 2: Sandboxed Execution

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. The [[OpenAI Agents SDK]] provides:

- **SandboxAgent**: A specialized agent class for remote sandbox execution
- **ShellTool**: A tool wrapper with additional guardrails
- **ModalSandboxSession**: Client for managing remote sandboxes

This approach makes the LLM operate within an isolated environment rather than accessing the host system directly.

#### GPU Integration

[[Modal]] allows attaching [[GPU|GPUs]] to sandboxes via `ModalSandboxClientOptions`, enabling resource-intensive operations like model training on dedicated hardware.

#### Capabilities Pattern

Sandbox tools are stateful and bound to specific `ModalSandboxSession` instances. The [[Capabilities]] pattern binds sets of tools to a session instance.

## Advanced Harness Features

### Memory Management with Sessions

By default, [[Agent|agents]] are stateless. The [[OpenAI Agents SDK]] provides **Sessions** to:

- Accumulate context across multiple agent runs
- Preserve conversation history
- Enable multi-turn interactions

However, accumulating memory indefinitely creates challenges:

- **Context Bloat**: Memory grows without bounds
- **Context Rot**: Older information becomes less relevant
- **Token Efficiency**: Larger context windows consume more tokens

### Orchestrator Pattern

For long-horizon tasks, a single agent becomes inefficient due to token overhead from code exploration and debugging output. The solution is a two-tier architecture:

**Orchestrator Agent**:
- Maintains high-level task memory
- Manages overall strategy
- Has limited direct code execution
- Delegates focused work to subagents

**Subagents**:
- Receive specific task descriptions
- Work with fresh context windows
- Return summaries of completed work
- Have their session memory discarded after task completion

This design keeps orchestrator context lean while enabling longer-horizon work through delegation.

### Asynchronous Parallel Execution

Rather than blocking on subagent execution, the orchestrator can manage multiple parallel subagents using a **SubAgentPool**:

- Stores active subagents as key-value pairs
- Uses `asyncio.Future` for non-blocking execution
- Provides tools for selective waiting on specific work threads
- Enables massive parallelization of independent tasks

#### Visibility and Monitoring

Parallel execution requires visibility into subagent status:

- **Hooks**: Track current active tools for each subagent
- **set_status Tool**: Allows subagents to provide status updates
- **list_subagents Tool**: Shows orchestrator current state of all parallel work

### Resource Management with Quotas

Asynchronous execution can lead to unbounded resource consumption. Quotas limit expensive resources:

- Prevent spawning unlimited GPU subagents
- Ensure fixed limits on concurrent resource use
- Example: Maximum of 8x H100 GPUs in simultaneous use

### Filesystem Snapshots

As tasks progress, intermediate states become valuable checkpoints. **Filesystem Snapshots** freeze a sandbox session into a reusable image:

**Benefits**:
- **Deduplication**: Future subagents start from known checkpoints, avoiding repeated setup
- **Context Management**: Filesystems serve as implicit memory, offloading from token limits
- **Branching**: Enable multiple subagents to fork from the same checkpoint

This approach allows subagents to avoid redundant work like repository cloning and dependency installation.

### Skills Subsystem

Rather than hardcoding task-specific prompts into the core harness, a **Skills** plugin system allows:

- Selective opt-in to contextual information
- Task-specific guidance without harness modifications
- Maintainability of general-purpose orchestration logic

Example: Parameter Golf-specific skills provide domain knowledge to the orchestrator without coupling it to that specific challenge.

## Practical Example: Parameter Golf

[[Parameter Golf]] is OpenAI's challenge to achieve intelligence thresholds with minimal model parameters. The complete harness can:

1. **Parse Requirements**: Understand the Parameter Golf challenge
2. **Spawn Parallel Work**: Create multiple subagents exploring different approaches
3. **Manage Checkpoints**: Snapshot progress and branch from known states
4. **Train Models**: Execute GPU-accelerated training in isolated sandboxes
5. **Coordinate Results**: Aggregate findings from parallel experiments

Example invocation:
```
"Train MNIST using three different backends (PyTorch, TensorFlow, JAX) 
in parallel and compare efficiency"
```

The orchestrator naturally spawns three parallel subagents, each tackling a different framework simultaneously.

## Key Design Principles

### Composition Over Monoliths

Build complex systems by composing simple, modular features around a base agent loop rather than creating monolithic agents.

### Context Efficiency

Keep primary orchestrator context lean by:
- Delegating detailed work to subagents
- Using filesystem snapshots for implicit memory
- Discarding subagent session memory after task completion

### Safety Through Isolation

Use [[Sandboxes]] to isolate agent execution from host systems, with additional guardrails via tools like `ShellTool`.

### Scalability Through Parallelism

Enable massive throughput by:
- Supporting asynchronous subagent execution
- Using worker pools for resource management
- Implementing quota systems for expensive resources

## Implementation Details

### Session and Memory Management

Sessions accumulate context but require careful management to prevent unbounded growth. Strategies include:

- Explicit context reset between major phases
- Summarization of completed work
- Filesystem-based storage for artifacts

### Orchestrator "Encouragement"

Orchestrators may exit prematurely before async tasks complete. The current solution involves "encouragement" patterns in prompting, though future implementations might use dedicated "self-thought" tools.

## Related Technologies

- [[OpenAI Agents SDK]]: Core framework for agent construction
- [[Modal]]: Infrastructure platform providing [[Sandboxes]] and [[GPU]] resources
- [[LLM|Large Language Models]]: The reasoning engine driving agent behavior
- [[Tools]]: Functions agents can invoke to interact with systems
- [[Background Coding Agents]]: Real-world implementation by [[Ramp]]

## Getting Started

The complete project code is available at [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example).

To begin:

1. Sign up for [[Modal]] (includes $30/month free compute credits)
2. Clone the example repository
3. Follow the documentation at [Modal Docs](/docs