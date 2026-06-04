---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-04T06:48:48.759029
raw_file_updated: 2026-06-04T06:48:48.759029
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-04T06:48:48.759029
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[agent harness|agent harnesses]] using the [[OpenAI Agents SDK]] in combination with [[Modal]], a cloud computing platform. It demonstrates a progressive approach to creating sophisticated AI agents, starting with basic coding agents and evolving into a parallel, GPU-accelerated system capable of handling complex research tasks. The guide uses OpenAI's [[Parameter Golf]] challenge as a practical example of implementing autonomous agent systems at scale.

## Introduction

The [[OpenAI Agents SDK]], launched in April 2026, provides developers with powerful tools for building agent harnesses designed for coding, research, and autonomous task completion. This article details how to integrate the SDK with [[Modal]]'s sandbox infrastructure to create scalable, secure, and efficient agent systems. The approach is illustrated through a real-world example inspired by how companies like [[Ramp]] have built internal coding agents responsible for significant portions of their development workflow.

## Core Concepts

### What is an Agent Harness?

An [[agent harness]] is the complete system built around a core agent loop. It encompasses:

- The [[Large Language Model]] (LLM) performing the reasoning
- Available [[tools]] (functions) the agent can invoke
- State management and context
- Security boundaries and resource constraints
- Monitoring and control mechanisms

The harness is distinct from the agent itself—it's the "everything around the agent loops that gives them the context and tools needed."

### Basic Agent Architecture

At its simplest, an [[Agent]] is a for-loop with an LLM executing [[tools]] to reach task completion. The foundational pattern involves:

1. The LLM receives a prompt and context
2. The LLM decides which tool to invoke
3. The tool executes and returns results
4. The loop continues until task completion

## Building Blocks: From Simple to Complex

### Stage 1: Basic Coding Agent

The simplest implementation provides an `exec()` function that allows the agent to run arbitrary shell commands:

```python
# Minimal agent with shell execution
agent = Agent(tools=[exec_tool])
agent.run("Train a model on MNIST")
```

**Security Note:** This approach is unsafe and not recommended for production use, as it gives the LLM unrestricted access to the host system.

### Stage 2: Sandboxed Execution

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. By moving agent execution into sandboxes, you:

- Isolate the LLM from the host system
- Prevent malicious or erroneous commands from affecting production
- Enable resource control (CPU, memory, GPU allocation)
- Create reproducible execution environments

The [[OpenAI Agents SDK]] provides:

- **`SandboxAgent`**: A specialized agent class with pre-built sandbox integration
- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: Client for remote sandbox management
- **`Capability`**: Binds tools to specific sandbox instances

**GPU Integration:** [[Modal]] allows attaching GPUs to sandboxes via `ModalSandboxClientOptions`, enabling computationally intensive tasks like model training.

### Stage 3: Memory and Sessions

By default, [[Agents]] are stateless—each run is independent. To enable multi-turn conversations and long-horizon tasks, use [[Sessions]]:

- Accumulate conversation history across multiple runs
- Maintain context across different agent instances
- Preserve intermediate results and decisions

**Challenge:** Sessions introduce [[context rot]]—as memory accumulates indefinitely, the context window becomes bloated, reducing efficiency and increasing costs.

### Stage 4: Orchestration with Subagents

For long-horizon work, split functionality into two agent types:

**Orchestrator Agent:**
- Maintains high-level task memory
- Makes strategic decisions
- Manages overall workflow
- Delegates specific tasks to subagents

**Subagents:**
- Receive focused, short-term tasks
- Have fresh context windows
- Complete work and return summaries
- Context is discarded after completion

This architecture keeps the orchestrator's context lean while allowing deep focus on specific problems.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking orchestrator execution on subagent completion:

- Maintain a **`SubAgentPool`** of active workers
- Store results as `asyncio.Future` objects
- Allow orchestrator to spawn multiple parallel tasks
- Implement monitoring tools for status visibility

**New Tools:**
- **`invoke_subagent(task)`**: Spawn a new subagent asynchronously
- **`list_subagents()`**: View status of all active workers
- **`set_status(message)`**: Subagents report progress without exiting

**Monitoring:** Use [[Hooks]] to track active tools and provide real-time visibility into subagent work.

### Stage 6: Resource Management with Quotas

With unbounded async spawning, GPU costs can spiral. Implement quota systems to:

- Limit concurrent expensive operations (e.g., "max 3 concurrent H100 GPUs")
- Prevent resource exhaustion
- Balance parallelism with cost control

### Stage 7: Filesystem Snapshots for Deduplication

Subagents starting from base sandboxes waste time on setup (dependency installation, repository cloning). [[Filesystem Snapshots]] solve this by:

- Freezing a sandbox state at a checkpoint
- Creating a reusable image for future subagents
- Allowing branching from known-good states
- Reducing redundant setup work

**Secondary Benefit - Implicit Memory:** The filesystem acts as distributed memory:
- Artifacts from prior agent work remain available
- Future agents inherit previous progress without explicit context
- On-disk files reduce reliance on token-limited context windows

### Stage 8: Skills Subsystem

To keep the core harness general-purpose while supporting specific tasks, implement a **Skills** plugin system:

- Define task-specific prompts as optional modules
- Allow orchestrator to selectively enable relevant skills
- Avoid hardcoding domain knowledge into the core harness
- Enable reusability across different problem domains

## Practical Example: Parameter Golf

[[Parameter Golf]] is an OpenAI challenge to achieve baseline intelligence thresholds with minimal model parameters. Using the complete harness architecture:

1. **Orchestrator** receives the Parameter Golf challenge
2. **Orchestrator** spawns three parallel subagents (one per ML framework)
3. Each **subagent** develops and trains models independently
4. **Filesystem snapshots** preserve working states for continuation
5. **Quota system** prevents excessive GPU spending
6. **Skills** provide Parameter Golf-specific guidance
7. Results accumulate across parallel experiments

## Key Design Patterns

### Context Management

- Keep orchestrator context lean through delegation
- Use sessions for multi-turn memory
- Offload long-term memory to filesystem
- Reset subagent context after task completion

### Parallelism

- Spawn subagents asynchronously
- Use worker pools for resource coordination
- Implement quota systems for cost control
- Monitor parallel work through status tools

### State Preservation

- Use filesystem snapshots as checkpoints
- Allow branching from known-good states
- Leverage implicit memory through file artifacts
- Reduce redundant setup through snapshot reuse

### Composability

Build harnesses by composing features:
- Start with basic agent
- Add sandboxing for safety
- Add sessions for memory
- Add orchestration for complexity
- Add parallelism for scale
- Add snapshots for efficiency
- Add skills for domain specificity

## Related Technologies

- [[Modal]]: Cloud computing platform providing sandboxes and GPU access
- [[OpenAI Agents SDK]]: Framework for building agent systems
- [[Large Language Models]]: The reasoning engine (e.g., GPT-4)
- [[Sandboxes]]: Isolated execution environments
- [[Async Programming]]: Enabling parallel task execution
- [[Context Windows]]: LLM memory constraints requiring management

## Getting Started

1. Sign up for [[Modal]] ($30 free monthly credits)
2. Install the [[OpenAI Agents SDK]]
3. Reference the [complete example repository](https://github.com/modal-labs/openai-agents-python-example)
4. Start with a basic agent and progressively add features
5. Deploy to Modal for production use

---

## Metadata

**Source:** Modal Blog - Building with Modal and the OpenAI Agents SDK  
**Author:** Erik Dunteman, Modal Labs  
**Published:** April 15, 2026  
**Read Time:** 8 minutes  

**Tags:** #agents #llm #modal #openai #sandboxes #gpu #parallelism #orchestration

**Related Topics:**
- [[Ramp]] - Case study of internal coding agents on Modal
- [[OpenAI]] - Agents