---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-12T05:44:31.612161
raw_file_updated: 2026-05-12T05:44:31.612161
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-12T05:44:31.612161
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a practical approach to creating scalable, parallelized agent systems that can execute complex tasks like the [[Parameter Golf]] challenge, progressing from basic implementations to sophisticated multi-agent architectures with memory management, context optimization, and resource quotas.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and automation tasks. Rather than relying solely on off-the-shelf solutions like Codex or Claude Code, organizations can now build their own internal agent harnesses tailored to specific needs. This article demonstrates how to combine the OpenAI Agents SDK with [[Modal]]'s computing infrastructure to create powerful, parallelizable agent systems.

## Core Concepts

### What is an Agent Harness?

An agent harness is the complete system surrounding the core [[agent loop]]. It consists of:

- The base [[LLM]] running tool invocations
- A set of [[tools]] (functions) available to the agent
- State management and context
- Additional capabilities and safety measures

The harness is entirely customizable and can be extended with new features to suit specific task requirements.

### Basic Coding Agent

The simplest coding agent implementation includes:

1. An `Agent` class that functions as a loop with an [[LLM]]
2. Tool functions that the agent can invoke
3. An `exec(command)` function for executing shell commands

**Important Security Note:** While simple, allowing arbitrary command execution is unsafe and not recommended for production use without proper isolation.

## Improving Security with Sandboxes

### Sandbox Isolation

[[Sandbox|Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. By running agent commands within a sandbox, the LLM operates within a confined environment rather than on the host system.

The OpenAI Agents SDK provides:

- **`SandboxAgent`**: A superset of `Agent` with preloaded tools for remote sandbox management
- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: The client interface to remote sandboxes

### Capabilities and GPU Integration

Sandbox tools are stateful, bound to specific `ModalSandboxSession` instances. The SDK uses a **Capability** system to bind tool sets to sandbox instances.

[[Modal]] uniquely allows attaching [[GPU|GPUs]] to sandboxes via `ModalSandboxClientOptions`, enabling compute-intensive tasks like model training to run directly within the agent environment.

## Building the Ultimate Harness

### Adding Memory with Sessions

By default, agents are stateless. The **Session** system solves this by:

- Accumulating conversation context across multiple agent runs
- Persisting memory across different user prompts
- Enabling multi-turn interactions

**Challenge:** As memory accumulates indefinitely, [[context management]] becomes critical to prevent [[context rot]] and token waste.

### Orchestrator and Subagent Architecture

For long-horizon tasks, agents are split into two roles:

**Orchestrator Agent:**
- Maintains high-level task memory
- Makes strategic decisions
- Invokes subagents for focused work
- Stays concerned with overall progress

**Subagents:**
- Execute focused, short-burst tasks
- Have fresh context windows and independent sessions
- Report summaries back to orchestrator
- Keep orchestrator context lean

This architecture prevents context bloat by isolating implementation details in subagent sessions that are discarded after task completion.

### Asynchronous Subagent Pools

Rather than blocking the orchestrator during subagent execution:

1. **SubAgentPool**: A key-value collection of active subagents
2. **Async Futures**: Subagent invocations return `asyncio.Future` objects
3. **Non-blocking Operations**: Orchestrator can spawn multiple parallel workers

The orchestrator tracks subagent status through:

- **Hooks**: Monitor currently active tools in each subagent
- **set_status tool**: Allows subagents to provide periodic updates
- **list_subagents tool**: Gives orchestrator visibility into parallel work

### Resource Management with Quotas

Quotas prevent unbounded resource consumption:

- Limit maximum number of concurrent [[GPU]] subagents
- Control expensive compute operations
- Prevent cost overruns from parallel task spawning

### Filesystem Snapshots for Context Deduplication

**Problem:** Subagents starting from base sandboxes waste time on repeated setup work (dependency installation, repository cloning).

**Solution:** Filesystem snapshots freeze sandbox state into reusable images:

- Snapshot an active sandbox after setup completion
- Spawn new subagents from snapshot rather than base image
- Preserve on-disk artifacts and working state
- Reduce setup overhead and token consumption

**Implicit Memory:** Filesystems serve as implicit memory when accessed via shell tools, allowing future agents to access prior work without explicit context inclusion.

### Skills Subsystem

A pluggable skills system allows:

- Selective opt-in to specialized prompts and context
- Keeping the core harness general-purpose
- Task-specific guidance without hardcoding
- Extensible capability loading

## Complete System Architecture

The final harness combines all components:

1. **Orchestrator agent** with memory sessions for high-level planning
2. **Async subagent pool** for parallel execution
3. **Sandbox isolation** with GPU support for secure computation
4. **Filesystem snapshots** for context deduplication and checkpoint branching
5. **Resource quotas** for cost and resource control
6. **Skills plugins** for task-specific guidance

This architecture enables:

- Parallel autonomous research across multiple GPU workers
- Lean context management preventing token waste
- Long-horizon task execution with memory persistence
- Efficient resource utilization through checkpointing

## Practical Example: Parameter Golf

The [[Parameter Golf]] challenge prompts participants to achieve intelligence thresholds with minimal model parameters. The described harness can:

- Spawn parallel subagents exploring different ML frameworks
- Train models on [[GPU|GPUs]] with different optimization strategies
- Checkpoint successful configurations for branching
- Coordinate research across multiple experimental threads

## Key Takeaways

1. **Composability**: Agent harnesses are built by composing systems atop base agent loops
2. **Context is Currency**: Memory and context management are critical for long-running agents
3. **Parallelization**: Async subagent pools enable massive throughput improvements
4. **Infrastructure Matters**: [[Modal]]'s sandbox and GPU support makes complex systems practical
5. **Flexibility**: The OpenAI Agents SDK provides building blocks for custom solutions

## Getting Started

- Review the [complete project code](https://github.com/modal-labs/openai-agents-python-example)
- Sign up for [[Modal]] to access sandbox and GPU infrastructure
- Start with basic agents and progressively add harness features
- Reference the OpenAI Agents SDK documentation for detailed API usage

---

## Metadata

**Source:** Modal Engineering Blog  
**Published:** April 15, 2026  
**Author:** Erik Dunteman  
**Read Time:** 8 minutes

**Tags:** 
- [[AI agents]]
- [[OpenAI Agents SDK]]
- [[Modal infrastructure]]
- [[LLM engineering]]
- [[Multi-agent systems]]
- [[GPU computing]]
- [[Agent orchestration]]

**Related Topics:**
- [[Agentic AI systems]]
- [[Sandbox environments]]
- [[Context management in LLMs]]
- [[Asynchronous task execution]]
- [[Distributed computing]]
- [[Model training infrastructure]]
- [[Parameter Golf challenge]]

**External Resources:**
- [OpenAI Agents SDK Launch](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [Modal Platform](https://modal.com)
- [Example Repository](https://github.com/modal-labs/openai-agents-python-example)