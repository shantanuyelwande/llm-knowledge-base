---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-03T05:36:55.311109
raw_file_updated: 2026-05-03T05:36:55.311109
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-03T05:36:55.311109
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] for secure, scalable execution. It demonstrates a progression from basic coding agents to sophisticated multi-agent systems with parallel processing, memory management, and GPU resource optimization, using OpenAI's Parameter Golf challenge as a practical example.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agentic systems. Rather than relying solely on off-the-shelf solutions like Codex or Claude Code, organizations can now construct their own internal agent harnesses tailored to specific needs. This article demonstrates how to leverage [[Modal]] infrastructure to create powerful, parallelized agent systems suitable for complex tasks like machine learning research and optimization.

The example uses OpenAI's [[Parameter Golf]] challenge—a task requiring efficient model development within strict parameter constraints—to illustrate how agents can be scaled across multiple GPUs with sophisticated orchestration.

---

## Core Concepts

### What is an Agent?

An [[Agent (AI)|agent]] is fundamentally a loop that combines:
- A [[Large Language Model]] (LLM) for decision-making
- A set of callable [[Tool (AI)|tools]] (functions) for task execution
- State management for tracking progress

The collection of tools, state management, and control logic around this core loop is called a **harness**.

### Agent Harness

An **agent harness** encompasses everything surrounding the basic agent loop that enables it to function effectively:
- Tool definitions and capabilities
- Memory and session management
- Resource allocation
- Orchestration logic
- Context management strategies

---

## Building Agent Systems: A Progressive Approach

### Stage 1: Basic Coding Agent

The simplest agent implementation uses an `exec(command)` tool that allows the LLM to execute arbitrary shell commands:

```python
# Minimal agent with shell execution capability
agent = Agent(tools=[exec_tool])
```

**Security Consideration**: This approach is unsafe for production use, as malicious prompts or unreliable models could cause damage to the host system.

### Stage 2: Sandboxed Execution with Modal

The [[OpenAI Agents SDK]] provides `SandboxAgent`, which isolates agent execution within remote [[Sandbox (computing)|sandboxes]]. This approach:

- Isolates the LLM from the host system
- Provides the [[ShellTool]] class with built-in guardrails
- Manages a `ModalSandboxSession` for remote communication
- Enables [[GPU]] attachment via `ModalSandboxClientOptions`

**Capabilities** are defined as groups of tools bound to specific sandbox instances, allowing stateful operations across multiple agent runs.

#### Example: Training MNIST

A sandboxed agent can execute end-to-end machine learning tasks:

```python
# Agent with sandbox and GPU capability
agent = SandboxAgent(
    sandbox_session=modal_sandbox,
    capabilities=[shell_capability, gpu_capability]
)
agent.run("Train an MNIST model and report accuracy")
```

### Stage 3: Memory and Sessions

By default, agents are stateless. The [[Session (software)|session]] mechanism enables:

- **Multi-turn conversations**: Accumulating context across multiple agent runs
- **Persistent memory**: Maintaining conversation history across user prompts
- **Shared state**: Transferring sessions between different agent instances

**Challenge**: [[Context Rot|Context rot]] emerges as memory accumulates indefinitely, requiring intelligent context management and pruning strategies.

### Stage 4: Multi-Agent Orchestration

For long-horizon tasks, a single agent becomes inefficient due to token overhead from exploring codebases and processing output. The solution uses an **orchestrator-subagent** pattern:

#### Orchestrator Agent
- Maintains high-level task memory
- Makes strategic decisions
- Delegates work via `invoke_subagent` tool
- Remains isolated from implementation details

#### Subagents
- Receive fresh [[Context Window|context windows]]
- Execute focused, short-duration tasks
- Report summaries back to orchestrator
- Have session memory discarded after completion

This architecture keeps the orchestrator's context lean while allowing detailed work to proceed in parallel.

### Stage 5: Asynchronous Parallel Processing

Rather than blocking the orchestrator while subagents work, a **SubAgentPool** enables:

- **Concurrent execution**: Multiple subagents running simultaneously
- **Non-blocking orchestration**: Orchestrator continues planning while subagents work
- **Work visibility**: Tools like `list_subagents` and `set_status` provide real-time status updates

The orchestrator manages an `asyncio.Future` for each subagent, allowing selective waiting on specific tasks.

#### Status Tracking Mechanisms
- **Hooks**: Track current active tools for each subagent
- **Status updates**: Subagents can report progress without returning to orchestrator
- **Visibility tools**: Orchestrator can query subagent status and results

### Stage 6: Resource Management with Quotas

With unbounded async task spawning, GPU costs can escalate rapidly. A **quota system** limits:
- Maximum number of concurrent expensive operations (e.g., 8x [[H100]] GPUs)
- Total resource consumption across the subagent pool
- Prevents runaway spending while maintaining parallelism

### Stage 7: Filesystem Snapshots for Efficiency

Subagents performing identical setup work (repository cloning, dependency installation) waste GPU time. **Filesystem Snapshots** address this by:

- **Freezing sandbox state**: Creating immutable snapshots of configured sandboxes
- **Branching work**: Spawning new subagents from checkpoint states
- **Context offloading**: Using filesystem state as implicit memory

This approach provides dual benefits:
1. **Performance**: Subagents skip redundant setup
2. **Memory efficiency**: Filesystem acts as external memory store, reducing session bloat

#### Implicit vs. Explicit Memory
- **Explicit**: Skills/memory files written to filesystem
- **Implicit**: Codebase already in working state from prior agent work

### Stage 8: Skills Subsystem

For domain-specific tasks, a **skills** plugin system allows:

- **Optional context loading**: Agents selectively opt into specialized knowledge
- **Modular prompting**: Task-specific guidance without cluttering core harness
- **Reusability**: Skills can be shared across different agent instances

Example: Parameter Golf-specific skills teach agents about the challenge's constraints and objectives.

---

## Complete System Architecture

The final system combines all components:

```
Orchestrator Agent
├── Memory (Session)
├── SubAgent Pool
│   ├── Subagent 1 (Sandbox + GPU)
│   ├── Subagent 2 (Sandbox + GPU)
│   └── Subagent N (Sandbox + GPU)
├── Quota Manager (GPU limits)
├── Filesystem Snapshots (checkpoints)
└── Skills System (domain knowledge)
```

### Key Characteristics

- **Parallel execution**: Multiple subagents work simultaneously on different tasks
- **Context efficiency**: Lean orchestrator memory, detailed work isolated in subagents
- **Resource-aware**: GPU quotas prevent runaway costs
- **Checkpoint-based**: Filesystem snapshots enable efficient work branching
- **Extensible**: Skills system allows domain customization

---

## Practical Example: Parameter Golf Research

The complete system enables autonomous, parallel research on the [[Parameter Golf]] challenge:

- **Orchestrator** understands the task and coordinates research
- **Subagents** implement different approaches (different ML frameworks, architectures)
- **Parallel training**: Multiple experiments run simultaneously on separate GPUs
- **Checkpointing**: Successful configurations are saved for branching
- **Skills**: Domain-specific knowledge guides the research process

### Execution

```bash
python orchestrator.py --task "parameter-golf" --parallel-workers 3
```

---

## Key Takeaways

1. **Composition over monoliths**: Build complex systems by composing simple components
2. **Isolation improves safety**: Sandboxes protect infrastructure from agent actions
3. **Memory management is critical**: Context rot requires active mitigation strategies
4. **Parallelism requires orchestration**: Async work needs visibility and coordination
5. **Resource awareness matters**: Quotas and snapshots prevent cost overruns
6. **Modularity enables reuse**: Skills and capabilities make systems extensible

---

## Related Technologies

- [[Modal]] - Serverless cloud platform for compute-intensive workloads
- [[OpenAI Agents SDK]] - Framework for building agent systems
- [[Sandbox (computing)]] - Isolated execution environments
- [[GPU Computing]] - Hardware acceleration for ML workloads
- [[Large Language Models]] - Foundation for agent decision-making
- [[Async/await]] -