---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:47:53.047061
raw_file_updated: 2026-05-01T05:47:53.047061
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:47:53.047061
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|agent]] harnesses using the [[OpenAI Agents SDK]] in combination with [[Modal]], a cloud computing platform. It demonstrates progressive enhancement of a basic coding agent through the addition of sandboxed execution environments, memory management, parallel processing, and GPU acceleration to create sophisticated autonomous research systems.

## Overview

The [[OpenAI Agents SDK]] provides developers with foundational building blocks for creating agent systems capable of handling complex tasks such as coding, research, and parameter optimization. When integrated with [[Modal]]'s [[sandbox|sandboxes]] and GPU infrastructure, these agents can be scaled to perform parallel work across multiple computational resources.

This guide walks through building a complete agent harness from first principles, using [[OpenAI]]'s [[Parameter Golf]] challenge as a practical example—a task requiring agents to discover efficient machine learning approaches within strict parameter constraints.

## Core Concepts

### What is an Agent Harness?

An agent harness is the complete system surrounding an agent's core loop. It encompasses:

- **The Agent Loop**: A for-loop structure where an [[large language model|LLM]] iteratively invokes [[tool|tools]] (functions) to accomplish tasks
- **Tools**: Functions available to the agent for executing actions
- **State Management**: Context and memory systems
- **Capabilities**: Bound sets of tools attached to specific agent instances

The harness is where customization occurs—it's the product engineering layer that determines what an agent can do and how effectively it operates.

## Building Blocks: From Basic to Advanced

### Stage 1: Basic Coding Agent

The simplest agent implementation includes an `exec(command)` function allowing the agent to execute arbitrary shell commands. While functional, this approach presents significant security risks and is not recommended for production use.

**Key limitation**: The agent has direct access to the host system, creating potential security vulnerabilities.

### Stage 2: Sandboxed Execution

[[Modal Sandbox|Sandboxes]] are isolated [[Linux]] environments built on virtual machines or security-hardened containers. Moving agent execution into sandboxes provides:

- **Isolation**: The agent operates within a contained environment rather than on the host system
- **Safety**: Malicious or errant commands cannot affect the underlying infrastructure
- **Resource Control**: Computational resources can be allocated and limited

#### SandboxAgent and Capabilities

The OpenAI Agents SDK provides specialized classes for sandbox integration:

- **SandboxAgent**: An extension of the base Agent class with preloaded tools for remote sandbox interaction
- **ShellTool**: Adds guardrails to shell command execution
- **ModalSandboxSession**: Client for managing remote sandbox connections
- **Capability**: A binding mechanism for associating tools with specific sandbox instances

#### GPU Acceleration

[[Modal]] allows attachment of [[GPU|GPUs]] to sandboxes via `ModalSandboxClientOptions`, enabling resource-intensive tasks like model training to run with hardware acceleration.

### Stage 3: Memory and Sessions

By default, agents are stateless—each invocation receives input and returns output without retaining context from previous interactions.

[[Session|Sessions]] solve this problem by:

- Accumulating conversation history across multiple agent runs
- Maintaining context windows across different agent instances
- Enabling multi-turn interactions with coherent memory

**Challenge**: Unlimited context accumulation leads to [[context rot]]—degradation in agent performance as context grows too large. This requires active context management and strategic memory reset.

### Stage 4: Hierarchical Agent Architecture

Long-horizon tasks overwhelm single agents due to token consumption during code exploration and environment interaction. The solution is a hierarchical structure:

#### Orchestrator Agent

- Maintains high-level task memory
- Coordinates overall workflow
- Delegates focused work to subagents
- Has access to a `invoke_subagent` tool

#### Subagents

- Receive fresh context windows and clean [[Session|sessions]]
- Execute specific, focused tasks
- Return summaries rather than verbose logs
- Have their session memory discarded after completion

This architecture keeps the orchestrator's context lean while enabling focused work on specific problems.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking orchestrator execution while waiting for subagent completion, a **SubAgentPool** enables parallel work:

- **Async Operations**: Subagent invocations return `asyncio.Future` objects
- **Worker Pool Pattern**: Multiple subagents run concurrently
- **Status Monitoring**: Tools allow the orchestrator to:
  - List active subagents via `list_subagents`
  - Check current tool execution via hooks
  - Receive status updates without full task completion via `set_status`

This design allows the orchestrator to spawn multiple parallel research threads while maintaining awareness of progress.

### Stage 6: Resource Quota Management

With async subagent spawning, agents could theoretically create unlimited GPU instances, resulting in uncontrolled costs. A quota system enforces limits:

- Fixed maximum number of expensive resources (e.g., 8x [[H100]] GPUs)
- Prevents unbounded resource consumption
- Enables safe autonomous operation

### Stage 7: Filesystem Snapshots

As agents work across multiple subagent instances, repeated setup tasks (repository cloning, dependency installation) waste computational resources and GPU time.

**Filesystem Snapshots** address this by:

- Freezing a sandbox's filesystem state to a reusable ID
- Allowing new subagents to start from known checkpoints
- Reducing redundant setup work
- Serving as implicit memory—artifacts persist on disk for future agents

#### Filesystem as Memory

Beyond time savings, filesystems provide distributed memory:

- Explicit: Writing skill files and memory artifacts
- Implicit: Maintaining a working codebase state that agents can understand without explicit context

Fresh subagents can resume work from snapshots with minimal instructions, understanding context from the filesystem state rather than verbose session history.

### Stage 8: Skills Subsystem

General-purpose harnesses can incorporate task-specific knowledge through a **Skills** plugin system:

- Agents selectively opt into contextual information
- Task-specific prompting remains modular
- Harness stays general-purpose while supporting specialized tasks
- Skills can be composed and combined as needed

## Practical Example: Parameter Golf Research

The complete harness enables autonomous, parallel research on the [[OpenAI]] [[Parameter Golf]] challenge:

1. **Orchestrator** receives the challenge description
2. **Subagents** spawn in parallel, each exploring different approaches (different ML frameworks, architectures, etc.)
3. **Snapshots** capture progress points, allowing branching from successful states
4. **Skills** provide domain-specific guidance about the challenge
5. **GPUs** accelerate model training across all parallel threads
6. **Quotas** prevent unbounded resource consumption

The system can autonomously discover and train new state-of-the-art efficient models without human intervention.

## Key Design Principles

### Composability

Systems can be built by composing layers of functionality on top of base agent loops. Each addition (memory, parallelism, snapshots, skills) is independent and can be combined as needed.

### Context Management

Keeping context lean is essential for long-horizon work. This is achieved through:

- Hierarchical agent structures (orchestrator + subagents)
- Session memory boundaries
- Filesystem-based implicit memory
- Strategic context pruning

### Isolation and Safety

[[Sandbox|Sandboxes]] provide security boundaries, allowing agents to operate autonomously without risking host system integrity.

### Resource Efficiency

Multiple mechanisms prevent waste:

- Filesystem snapshots eliminate redundant setup
- Parallel execution maximizes GPU utilization
- Quotas prevent runaway resource consumption
- Hierarchical architecture reduces token consumption

## Implementation Resources

The complete example project is available at: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

### Getting Started

To build with these technologies:

1. Sign up for [[Modal]] and receive $30 in free compute credits
2. Review the complete example repository
3. Adapt the patterns to your specific use case
4. Deploy using Modal's infrastructure

## Related Concepts

- [[OpenAI Agents SDK]]: The foundational SDK for building agents
- [[Modal]]: Cloud computing platform providing sandboxes and GPUs
- [[Sandbox|Sandboxes]]: Isolated execution environments
- [[LLM|Large Language Models]]: The reasoning engine powering agents
- [[Tool Use]]: Function calling and tool invocation patterns
- [[Agent Orchestration]]: Coordinating multiple agents
- [[Parameter Golf]]: OpenAI's efficiency optimization challenge
- [[Context Rot]]: Degradation of agent performance with excessive context
- [[Ramp]]: Real-world example of background coding agents in production

---

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman (Member of Technical Staff