---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-22T04:52:16.154330
raw_file_updated: 2026-04-22T04:52:16.154330
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-22T04:52:16.154330
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using [[Modal]] and the [[OpenAI Agents SDK]]. It demonstrates a progressive approach to creating agent harnesses, starting with basic coding agents and advancing to sophisticated parallel systems capable of managing multiple subagents with GPU resources, memory management, and context optimization.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in agent development, providing building blocks for teams to construct their own agentic systems. When combined with [[Modal]]'s [[Sandboxes]] and [[GPU]] infrastructure, developers can create powerful, scalable agent harnesses capable of handling complex, long-horizon tasks. This guide demonstrates how to build a general-purpose coding agent harness that can parallelize tasks across multiple subagents running on GPUs.

---

## Core Concepts

### What is an Agent Harness?

An agent harness is the complete system surrounding a core agent loop—the tools, state management, and context that enable an [[AI agent]] to accomplish complex tasks. The harness determines what capabilities the agent has access to and how it manages information across multiple runs.

### Basic Agent Architecture

At its foundation, an [[Agent]] is a for-loop with an [[Large Language Model|LLM]] running [[tools]] (functions) to task completion. The simplest implementation includes:

- An LLM making decisions
- A set of callable functions (tools)
- State management
- Loop control until task completion

The most basic coding agent might have an `exec(command)` function allowing arbitrary shell command execution, though this approach carries significant security risks.

---

## Progressive Development Approach

### Stage 1: Basic Local Agent

The simplest approach executes commands directly on the host system. While functional, this is unsafe and not recommended for production use due to security vulnerabilities.

```python
# Pseudocode: Basic agent with direct execution
agent = Agent(
    tools=[exec_command]
)
result = agent.run("perform a task")
```

### Stage 2: Sandboxed Execution

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. Moving agent execution into a sandbox provides:

- **Security isolation**: The LLM interacts with a sandbox, not the host system
- **Resource containment**: Prevents runaway processes from affecting the host
- **Environment control**: Consistent, reproducible execution environments

The [[OpenAI Agents SDK]] provides a `SandboxAgent` class with:

- Pre-loaded tools for remote sandbox interaction
- `ShellTool` class with additional guardrails
- `ModalSandboxSession` client for remote sandbox management
- **Capabilities** system for binding tools to sandbox instances

#### Adding GPU Support

[[Modal]] allows attaching [[GPU|GPUs]] to sandboxes via `ModalSandboxClientOptions`, enabling agents to run computationally intensive tasks like [[Machine Learning]] model training.

**Example**: Training MNIST with a one-shot prompt works out-of-the-box with a properly configured sandbox and GPU.

### Stage 3: Memory and Sessions

By default, agents are stateless—they don't retain information across multiple runs. [[Sessions]] solve this by:

- Accumulating context across multiple agent runs
- Maintaining conversation history
- Enabling multi-turn interactions

However, sessions introduce new challenges:

- **Context management**: Preventing unlimited context window growth
- **[[Context rot]]**: Degradation of older information as context accumulates
- **Token efficiency**: Managing costs as context grows

### Stage 4: Orchestrator and Subagent Architecture

For long-horizon work, a single agent becomes inefficient due to token overhead from code exploration and output inspection. The solution is a two-tier architecture:

#### Orchestrator Agent
- Maintains high-level memory of the entire task
- Makes strategic decisions
- Delegates work to subagents
- Concerns itself only with summaries and results

#### Subagents
- Fresh context window for each task
- Focused, brief execution
- Return summaries to orchestrator
- Session memory is discarded after completion

This architecture keeps the orchestrator's context lean while enabling focused, specialized work.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking the orchestrator while waiting for subagent completion, a **SubAgentPool** enables:

- Multiple parallel subagents running simultaneously
- Non-blocking orchestrator operations
- Improved throughput and efficiency

#### Key Components

**Hooks**: Track current active tools for each subagent, providing visibility into parallel work

**Status Updates**: Subagents can call `set_status` to update progress without exiting back to the orchestrator

**List Subagents Tool**: Allows orchestrator to monitor all active parallel work

**Example Use Case**: Training MNIST across three different ML frameworks (PyTorch, TensorFlow, JAX) in parallel with separate subagents.

### Stage 6: Resource Quotas

With async capabilities enabling unbounded subagent spawning, quotas prevent excessive resource consumption:

- Fixed limits on expensive resources (e.g., 8× [[H100]] GPUs)
- Cost control for autonomous systems
- Prevents runaway spending

### Stage 7: Filesystem Snapshots

As tasks grow longer, subagents waste GPU time on repetitive setup work. [[Filesystem Snapshots]] address this by:

- Freezing active sandbox state into an ID
- Allowing new subagents to branch from known checkpoints
- Reducing redundant work across parallel tasks

#### Dual Benefits

1. **Time savings**: Skip setup work when resuming from checkpoints
2. **Context management**: Use filesystem as implicit memory, offloading from session context

Artifacts from prior agent work remain available to future agents through the shared filesystem, even without explicit context passing.

### Stage 8: Skills Subsystem

For general-purpose harnesses, a **skills plugin system** allows:

- Selective opt-in to specialized context
- Domain-specific prompting without hardcoding
- Reusable knowledge components
- Flexibility across different task types

---

## Real-World Application: Parameter Golf

The article demonstrates these concepts using OpenAI's [[Parameter Golf]] challenge—optimizing model intelligence while minimizing parameter count. The complete harness:

1. Spawns parallel subagents for different approaches
2. Manages GPU resources via quotas
3. Maintains orchestrator memory efficiently
4. Uses filesystem snapshots to branch work from checkpoints
5. Applies specialized skills for the specific challenge

---

## Key Advantages of This Architecture

| Feature | Benefit |
|---------|---------|
| [[Sandboxes]] | Security isolation and environment control |
| [[GPU]] attachment | Enables compute-intensive agent tasks |
| [[Sessions]] | Multi-turn memory and conversation history |
| Orchestrator/Subagent split | Scalable, token-efficient long-horizon work |
| Async parallelization | Improved throughput and resource utilization |
| Resource quotas | Cost control for autonomous systems |
| Filesystem snapshots | Reduced redundant work, implicit memory |
| Skills system | General-purpose, composable harnesses |

---

## Implementation Takeaways

The key insight is that agent systems are **composable**. You can:

- Start with basic local execution
- Add sandboxes for security
- Introduce memory with sessions
- Scale with orchestrator/subagent patterns
- Parallelize with async workers
- Optimize with snapshots and quotas
- Extend with pluggable skills

Each layer builds on previous capabilities, creating increasingly sophisticated systems without requiring complete rewrites.

---

## Related Technologies

- [[Modal]] - Serverless compute platform providing sandboxes and GPU resources
- [[OpenAI Agents SDK]] - Framework for building agent systems
- [[Sandboxes]] - Isolated execution environments
- [[GPU|GPUs]] - Accelerated computing for agent tasks
- [[Large Language Models]] - Core decision-making component
- [[Filesystem Snapshots]] - State preservation and branching

---

## Metadata

**Source**: Modal Engineering Blog (April 15, 2026)  
**Author**: Erik Dunteman, Modal Labs  
**Article Type**: Technical Tutorial  
**Read Time**: 8 minutes

**Tags**: 
- [[AI Agents]]
- [[OpenAI]]
- [[Modal]]
- [[Agent Architecture]]
- [[Parallel Computing]]
- [[GPU Computing]]
- [[Machine Learning]]
- [[API Development]]

**Related Articles**:
- [[Ramp's Background Coding Agents on Modal]]
- [[OpenAI Agents SDK Overview]]
- [[Modal Sandboxes Guide]]
- [[Serverless GPU Computing]]

**Example Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

**External Links**:
- [Modal Platform](https://modal