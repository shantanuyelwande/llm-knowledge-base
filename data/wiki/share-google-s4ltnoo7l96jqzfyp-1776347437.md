---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-23T04:56:39.840559
raw_file_updated: 2026-04-23T04:56:39.840559
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-23T04:56:39.840559
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article describes how to construct sophisticated [[AI Agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It provides a comprehensive guide to building agent "harnesses"—the systems and tools surrounding core agent loops—progressing from basic implementations to production-ready parallel systems capable of handling complex tasks like machine learning research and experimentation.

## Introduction

The [[OpenAI Agents SDK]] represents a significant evolution in building customizable agent systems for [[autonomous agents|autonomous coding]], deep research, and task automation. Unlike off-the-shelf solutions such as Codex or Claude Code, the SDK enables teams to build tailored agentic systems in-house. This article demonstrates how to integrate the OpenAI Agents SDK with [[Modal]]'s [[sandbox|sandboxes]] and [[GPU computing]] capabilities to create scalable, parallel agent systems.

## Core Concepts

### What is an Agent Harness?

An agent harness encompasses everything surrounding the core [[agent loop]]—the set of tools, state management, and capabilities that enable an [[AI Agent]] to function effectively. The harness is where product engineering meets AI, as it's entirely customizable to suit specific task requirements.

### Basic Agent Architecture

At its foundation, an [[Agent]] is a loop that runs an [[large language model|LLM]] to invoke [[function calling|tools]] (functions) until task completion. The simplest implementation might include:

- A set of available tools the agent can invoke
- State management for tracking progress
- A loop that continues until the agent signals completion

## Building Blocks

### 1. Starting with Local Execution

The most basic approach creates a coding agent with access to an `exec(command)` function, allowing it to run arbitrary shell commands. While simple for demonstration, this approach presents significant security risks and is not recommended for production use.

### 2. Sandboxed Execution

[[Sandbox|Sandboxes]] are isolated [[Linux]] environments built on [[virtual machine|VMs]] or security-hardened containers. Moving agent execution into sandboxes provides crucial security isolation, allowing the LLM to interact with a remote environment rather than the host system.

The OpenAI Agents SDK provides:

- **SandboxAgent**: A specialized agent class with preloaded sandbox tools
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client for managing remote sandbox communication

**Capabilities** are mechanisms for binding sets of tools to specific sandbox instances, enabling [[stateful computing|stateful]] interactions with remote environments.

#### GPU Integration

[[Modal]] allows attaching [[GPU]] resources to sandboxes via `ModalSandboxClientOptions`, enabling resource-intensive [[machine learning]] tasks to run directly within agent environments.

### 3. Memory and Session Management

By default, agents are stateless, processing input and returning output without retaining context. **Sessions** solve this problem by accumulating conversation history and context across multiple agent runs.

However, sessions introduce new challenges:

- **[[Context Management]]**: Preventing unbounded growth of context windows
- **[[Context Rot]]**: Degradation of information quality as context accumulates

### 4. Orchestration with Subagents

For long-horizon tasks, a two-tier architecture prevents context bloat:

- **Orchestrator Agent**: The main agent that maintains high-level task memory and planning
- **Subagents**: Fresh agent instances with clean context windows, spawned for focused subtasks

The orchestrator maintains only task-level summaries while subagents handle implementation details. Each subagent receives a fresh [[session]] that is discarded after task completion.

### 5. Asynchronous Parallel Execution

Rather than blocking on individual subagent completion, a **SubAgentPool** enables the orchestrator to manage multiple parallel subagents simultaneously:

- Subagent invocations return `asyncio.Future` objects
- The orchestrator can spawn multiple parallel research threads
- [[Hook|Hooks]] track active tools and progress in each subagent
- A `set_status` tool allows subagents to report progress without exiting

### 6. Resource Quotas

With parallel execution, agents can spawn unbounded numbers of expensive GPU subagents. **Quota systems** enforce limits on concurrent resource usage (e.g., maximum number of active H100 GPUs), controlling costs while maintaining parallelism.

### 7. Filesystem Snapshots

[[Filesystem snapshot|Filesystem snapshots]] freeze sandbox state into persistent images, enabling:

- **Work Deduplication**: Fresh subagents can start from checkpoints rather than repeating setup work
- **Implicit Memory**: Filesystem state serves as distributed memory accessible to future agents
- **Context Offloading**: Artifacts and intermediate results persist on disk, reducing [[context window]] pressure

### 8. Skills Subsystem

A **skills** plugin system allows agents to selectively opt into specialized knowledge and prompting without coupling task-specific logic to the core harness. Skills provide:

- Domain-specific prompting and context
- Task-specific tool definitions
- Modular knowledge that can be composed with different agents

## Practical Example: Parameter Golf Research

The article demonstrates these concepts through OpenAI's [[Parameter Golf]] challenge—optimizing model performance within strict parameter budgets. The complete system:

1. Accepts high-level research objectives
2. Spawns parallel subagents on GPUs
3. Each subagent explores different approaches (frameworks, architectures, training methods)
4. Snapshots successful configurations for future exploration
5. Maintains orchestrator-level memory of overall progress
6. Reports discoveries back to the user

## Implementation Patterns

### Session Management

```
Session → accumulates context across agent runs
        → enables multi-turn conversations
        → requires context management strategies
```

### Async Subagent Pattern

```
Orchestrator → spawns multiple SubAgents asynchronously
            → maintains SubAgentPool
            → monitors progress via hooks and status updates
            → waits selectively for specific results
```

### Filesystem Persistence

```
Active Sandbox → performs work
              → filesystem snapshot created
              → fresh subagent spawned from snapshot
              → continues work from known state
```

## Key Advantages of This Architecture

- **Security**: Isolated sandboxes prevent agent access to host systems
- **Scalability**: Parallel subagents and async execution maximize throughput
- **Cost Control**: Quotas prevent runaway resource consumption
- **Context Efficiency**: Orchestrator/subagent separation and filesystem caching minimize [[token]] usage
- **Composability**: Modular skills and capabilities enable reuse across different tasks
- **Transparency**: Hooks and status tools provide visibility into parallel work

## Related Concepts

- [[OpenAI Agents SDK]]: The foundational framework
- [[Modal]]: Cloud infrastructure for execution and resource management
- [[AI Agent]]: The autonomous decision-making entity
- [[Large Language Model]]: The cognitive engine powering decisions
- [[Sandbox]]: Isolated execution environment
- [[GPU Computing]]: Hardware acceleration for training and inference
- [[Autonomous Agents]]: Broader category of self-directed AI systems
- [[Function Calling]]: Mechanism for agents to invoke tools
- [[Context Window]]: Limitation on information agents can process simultaneously

## See Also

- [[Ramp]] - Real-world example of background coding agents
- [[OpenAI Parameter Golf]] - Challenge used in the demonstration
- [[Asynchronous Programming]] - Technical foundation for parallel execution

---

## Metadata

**Source**: Modal Engineering Blog  
**Date**: April 15, 2026  
**Author**: Erik Dunteman, Modal Labs  
**Read Time**: 8 minutes  

**Tags**: #AI-Agents #OpenAI #Modal #Sandboxes #GPU #LLM #Agent-Architecture #Parallel-Computing #Python

**Related Topics**: [[Agent Design Patterns]], [[Distributed Computing]], [[LLM Orchestration]], [[Cloud Infrastructure]], [[Autonomous Systems]]

**Repository**: [openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)