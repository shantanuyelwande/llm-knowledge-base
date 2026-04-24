---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T05:00:14.163484
raw_file_updated: 2026-04-24T05:00:14.163484
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T05:00:14.163484
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]]'s serverless computing platform. It demonstrates a progression from basic coding agents to sophisticated parallel agent systems, using [[Parameter Golf]] as a practical example. The guide covers essential patterns including sandboxing, memory management, async execution, and resource quotas.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in agent development, providing building blocks for teams to construct custom agentic systems. When combined with [[Modal]]'s computing infrastructure, it enables scalable, efficient agent harnesses capable of handling complex tasks like automated code generation and machine learning experimentation.

This article documents the journey from a simple local agent to a production-ready parallel agent orchestration system, suitable for real-world applications like those built by companies such as [[Ramp]].

## Core Concepts

### What is an Agent?

An [[agent]] in this context is fundamentally a for-loop with an [[Large Language Model|LLM]] executing [[tools]] (functions) toward task completion. The collection of tools, state management, and supporting infrastructure built around the core agent loop is called a "harness."

### Basic Coding Agent

The simplest implementation provides an agent with an `exec(command)` function to run arbitrary shell commands. While functional, this approach presents significant security risks and is not recommended for production use without isolation mechanisms.

## Building the Agent Harness

### Stage 1: Local Execution

The initial approach uses the [[OpenAI Agents SDK]] to create a basic agent with shell command execution capabilities. This serves as a foundation but lacks isolation and safety features necessary for production deployment.

### Stage 2: Sandbox Isolation

[[Modal Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. Integration with sandboxes provides:

- **Security**: The LLM operates within an isolated environment rather than on the host system
- **Environment Control**: Consistent, reproducible execution environments
- **GPU Access**: Ability to attach GPUs for computationally intensive tasks via `ModalSandboxClientOptions`

The [[OpenAI Agents SDK]] provides:
- `SandboxAgent` class: Extends the base agent with sandbox integration
- `ShellTool` class: Adds guardrails to command execution
- `ModalSandboxSession`: Client interface to remote sandboxes
- `Capability` pattern: Binds tool sets to specific sandbox instances

#### Example: MNIST Training

A one-shot prompt can direct the sandboxed agent to train an image model on the MNIST dataset end-to-end, demonstrating the agent's capability to handle complex machine learning tasks autonomously.

### Stage 3: Memory and Sessions

By default, agents are stateless—each invocation operates without knowledge of previous interactions. [[Sessions]] solve this by:

- Accumulating context across multiple agent runs
- Preserving conversation history
- Enabling multi-turn interactions
- Persisting state across agent instances

**Challenge**: [[Context rot]] emerges as memory accumulates indefinitely, requiring intelligent context management and pruning strategies.

### Stage 4: Orchestration with Subagents

To enable long-horizon tasks while managing token consumption, the architecture splits into two agent types:

- **Orchestrator Agent**: Main chat agent accumulating task-level memory
- **Subagent**: Fresh context window for focused, time-limited tasks

The orchestrator uses an `invoke_subagent` tool to delegate work, receiving summaries rather than implementation details. This pattern:

- Keeps orchestrator context lean and focused
- Enables parallel exploration of multiple approaches
- Allows subagent sessions to be discarded after task completion

### Stage 5: Asynchronous Parallel Execution

Rather than blocking the orchestrator during subagent execution, a [[SubAgentPool]] enables concurrent task management:

- **Key-value store** of active subagents
- **asyncio.Future** for non-blocking subagent invocation
- **Hooks system** for tracking active tools in each subagent
- **Status updates** allowing subagents to report progress without exiting

The orchestrator gains visibility through:
- `set_status` tool for periodic subagent updates
- `list_subagents` tool displaying active work and progress
- Hook-based monitoring of current tool execution

### Stage 6: Resource Quotas

With unbounded async task spawning capability, cost control becomes critical. A quota system limits concurrent expensive resources (e.g., 8x H100 GPUs), preventing runaway costs while maintaining parallelism.

#### Parallel MNIST Example

The orchestrator can spawn three parallel subagents to train MNIST using different ML frameworks (PyTorch, TensorFlow, JAX) simultaneously, coordinating the parallel work without blocking.

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshots]] freeze sandbox state into reusable checkpoints, enabling:

- **Deduplication**: Subagents branch from snapshots rather than reinstalling dependencies
- **Context Management**: Filesystems act as implicit memory, storing artifacts for future agents
- **Efficiency**: Significant time savings on setup and initialization
- **Implicit Memory**: On-disk state available to all future agents without explicit context inclusion

This pattern is particularly valuable for multi-step tasks where intermediate states represent valuable checkpoints.

### Stage 8: Skills Subsystem

A pluggable skills system allows agents to opt into domain-specific knowledge:

- **General-purpose harness**: Remains flexible and reusable
- **Selective context**: Agents load only relevant skills
- **Modular prompting**: Domain expertise encapsulated as skills plugins

This enables the orchestrator to efficiently tackle specialized challenges like [[Parameter Golf]] without embedding task-specific logic in the core harness.

## Parameter Golf Use Case

[[Parameter Golf]] is an OpenAI challenge to achieve baseline intelligence thresholds with minimal model parameters. The complete harness enables:

- Parallel exploration across multiple approaches
- Autonomous research and experimentation
- GPU-accelerated training and evaluation
- Context-efficient long-horizon task execution
- Checkpoint-based work resumption

## Key Architectural Patterns

### Context Management

Strategies for preventing context bloat:
- Session-based memory accumulation
- Subagent context isolation
- Filesystem-based implicit memory
- Periodic context pruning and summarization

### Parallelism

Enabling concurrent execution:
- Async subagent invocation with futures
- Subagent pool management
- Resource quota enforcement
- Status monitoring without blocking

### Isolation and Safety

Security and reliability mechanisms:
- Sandboxed execution environments
- Tool guardrails (ShellTool)
- Quota enforcement
- Capability-based access control

## Implementation Details

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

Key implementation notes:
- Orchestrators require "encouragement" to avoid premature exit before async tasks complete
- Future work could include "self thought" tools for productive orchestrator planning
- Filesystem snapshots require careful management of checkpoint timing

## Getting Started

To build with Modal and the OpenAI Agents SDK:

1. Sign up for [[Modal]] account
2. Access $30 in free monthly compute credits
3. Reference the complete example repository
4. Implement patterns progressively based on requirements

## Related Technologies

- [[OpenAI Agents SDK]]: Core agent framework
- [[Modal]]: Serverless computing platform
- [[Modal Sandboxes]]: Isolated execution environments
- [[Large Language Models]]: Agent reasoning engines
- [[Parameter Golf]]: Example challenge domain

## Key Takeaways

The primary insight is that agent systems are composable: starting with basic agent loops, developers can progressively add capabilities—isolation, memory, parallelism, and domain knowledge—to build production-grade systems suited to specific tasks.

The [[OpenAI Agents SDK]] combined with [[Modal]]'s infrastructure provides the necessary building blocks for teams to construct sophisticated internal tools equivalent to commercial offerings, while maintaining full control and customization.

---

## Metadata

**Source**: Modal Blog - Building with Modal and the OpenAI Agents SDK  
**Author**: Erik Dunteman, Member of Technical Staff at Modal  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  
**Category**: Engineering, AI/ML, Agent Systems

**Tags**: #agents #openai #modal #llm #sandboxes #parallel-computing #gpu #orchestration #coding-agents #parameter-golf

**Related Topics**:
- [[AI Agent Architecture]]
- [[Serverless Computing]]
- [[Prompt Engineering]]
- [[Distributed Systems]]
- [[Machine Learning Infrastructure]]
- [[Ramp Engineering Case Study]]

**External Resources**:
- [OpenAI Agents SDK Launch](https://openai.com/index/the-next-evolution-of