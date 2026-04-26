---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-26T05:17:43.814107
raw_file_updated: 2026-04-26T05:17:43.814107
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-26T05:17:43.814107
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores the integration of [[Modal]] infrastructure with [[OpenAI Agents SDK]] to build sophisticated autonomous agent systems. It demonstrates how to construct a scalable agent harness that progresses from basic implementation to a parallel, GPU-accelerated research platform capable of handling complex tasks like the OpenAI Parameter Golf challenge.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable autonomous agent systems. Rather than relying solely on off-the-shelf solutions like Codex or Claude Code, organizations can now construct their own internal agentic systems tailored to specific needs. This article demonstrates how to integrate the OpenAI Agents SDK with [[Modal]] sandboxes to create powerful, scalable agent harnesses.

The integration allows agents to execute code safely in isolated environments while leveraging [[GPU]] resources for computationally intensive tasks. The example uses OpenAI's Parameter Golf challenge—a task requiring agents to optimize machine learning models within strict parameter constraints—to demonstrate the system's capabilities.

## Core Concepts

### Agents and Harnesses

An [[Agent]] is fundamentally a loop that executes an [[Large Language Model]] (LLM) running tools (functions) to accomplish tasks. The collection of tools, state management, and contextual systems built around the core agent loop is called a "Harness."

The harness represents the product engineering layer where developers customize agent behavior, memory management, and tool availability for specific use cases.

### Basic Agent Implementation

The simplest coding agent includes an `exec(command)` function that allows the LLM to invoke arbitrary shell commands. While straightforward, this approach poses significant security risks with malicious prompts or low-quality models and is not recommended for production use.

## Security and Isolation

### Sandbox Execution

[[Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. By moving agent execution into sandboxes, the LLM operates within a confined environment rather than on the host system, dramatically improving security.

The OpenAI Agents SDK provides:
- **SandboxAgent**: A superset of the base Agent class with preloaded sandbox tools
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client interface for remote sandbox interaction

### GPU Integration

[[Modal]] enables agents to request [[GPU]] resources for their sandboxes through `ModalSandboxClientOptions`, allowing computationally intensive tasks like model training to execute efficiently on specialized hardware.

## Advanced Harness Architecture

### Memory Management with Sessions

By default, agents are stateless. The [[Session]] object solves this limitation by accumulating context across multiple agent runs, enabling multi-turn conversations and maintaining state across agent instances.

**Challenge**: Unlimited memory accumulation leads to [[context rot]]—degradation of response quality as context windows grow too large.

**Solution**: Implement intelligent context management and periodic resets to prevent context bloat.

### Orchestrator and Subagent Pattern

To enable long-horizon work while managing context efficiently, the system implements a two-tier architecture:

- **Orchestrator Agent**: Maintains high-level memory and task planning; only accumulates strategic context
- **Subagents**: Spawn with fresh context windows for focused, short-burst tasks; context is discarded after completion

The orchestrator invokes subagents through an `invoke_subagent` tool, receiving only task summaries rather than implementation details.

### Asynchronous Parallel Execution

Rather than blocking the orchestrator while awaiting subagent completion, a [[SubAgentPool]] manages multiple parallel subagents:

- Stores active subagents as key-value pairs
- Uses `asyncio.Future` objects for non-blocking task invocation
- Provides tools for the orchestrator to selectively wait for specific work threads
- Implements [[Hooks]] to track active tools in each subagent
- Includes `set_status` tool for periodic orchestrator updates without exiting

### Resource Management with Quotas

To prevent unbounded resource consumption from parallel GPU subagents, quota systems limit the maximum number of expensive resources (e.g., 8x H100 GPUs) in simultaneous use.

### Filesystem Snapshots

[[Filesystem Snapshots]] address two critical challenges:

1. **Deduplication**: Freeze sandbox state at known checkpoints, allowing new subagents to branch from these points rather than repeating setup work
2. **Context Offloading**: Use the filesystem as implicit memory—artifacts and code state from prior agents remain available to future agents without explicit context inclusion

This enables efficient progression of work: orchestrator directs progress, snapshots filesystem state, then spawns fresh subagents into that snapshot with minimal instructions.

### Skills Subsystem

A pluggable [[Skills]] system allows agents to selectively opt into specialized context and instructions. Rather than hardcoding task-specific prompts into the core harness, skills enable general-purpose harnesses to be extended for specific challenges like Parameter Golf.

## Practical Example: MNIST Training

The article demonstrates agent capability through progressively complex MNIST training tasks:

1. **Basic Implementation**: Simple one-shot prompt to train an image model on MNIST
2. **Parallel Training**: Orchestrator spawns three parallel subagents to train using different ML frameworks (PyTorch, TensorFlow, JAX)
3. **Optimized Training**: Uses filesystem snapshots and skills to efficiently parallelize Parameter Golf research across GPU resources

## Architecture Summary

The complete harness architecture combines:

```
Orchestrator Agent (High-level planning, Memory)
    ↓
Subagent Pool (Parallel execution, Fresh contexts)
    ├─ Subagent 1 (GPU Sandbox)
    ├─ Subagent 2 (GPU Sandbox)
    └─ Subagent N (GPU Sandbox)

Supporting Systems:
- Sessions (Memory accumulation)
- Hooks (Execution tracking)
- Filesystem Snapshots (State checkpoints)
- Skills (Task specialization)
- Quotas (Resource limits)
```

## Key Benefits

- **Composability**: Systems layer cleanly on top of base agent loops
- **Scalability**: Parallel execution across multiple GPU resources
- **Context Efficiency**: Memory management prevents degradation at scale
- **Security**: Isolated sandbox execution prevents host system compromise
- **Flexibility**: General-purpose harness extensible through skills and capabilities
- **Cost Control**: Quota systems manage expensive GPU resource consumption

## Implementation Resources

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example), providing reference code for all concepts discussed.

## Related Technologies

- [[OpenAI API]]: Powers the LLM backbone of agents
- [[Modal Platform]]: Provides serverless infrastructure and sandbox execution
- [[Large Language Models]]: Core intelligence driving agent decision-making
- [[Containerization]]: Underlying technology for sandbox isolation
- [[GPU Computing]]: Enables efficient training and inference

## See Also

- [[OpenAI Agents SDK]]
- [[Modal Sandboxes]]
- [[Asynchronous Programming]]
- [[Context Management in LLMs]]
- [[Parameter Golf Challenge]]
- [[Orchestration Patterns]]

---

**Metadata**

- **Source**: Modal Engineering Blog
- **Author**: Erik Dunteman
- **Date Published**: April 15, 2026
- **Read Time**: 8 minutes
- **Tags**: `#agents` `#openai` `#modal` `#gpu-computing` `#orchestration` `#sandboxes` `#llm` `#python`
- **Related Topics**: [[Agent Orchestration]], [[Sandbox Computing]], [[Parallel Processing]], [[LLM Engineering]], [[Cloud Infrastructure]]
- **External Links**: [OpenAI Agents SDK Launch](https://openai.com/index/the-next-evolution-of-the-agents-sdk/), [Modal Platform](https://modal.com), [Parameter Golf Challenge](https://openai.com/index/parameter-golf/)