---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-07-01T06:38:25.244335
raw_file_updated: 2026-07-01T06:38:25.244335
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-07-01T06:38:25.244335
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores the integration of [[Modal]] cloud infrastructure with [[OpenAI Agents SDK]] to build scalable, autonomous agent systems. It demonstrates how to construct a sophisticated agent harness that progresses from a basic coding agent to a parallel, GPU-accelerated research system capable of managing multiple subagents, memory management, and context optimization.

## Overview

[[OpenAI]] recently launched their [[Agents SDK]], a framework for building agent harnesses designed for coding tasks, research, and autonomous problem-solving. [[Modal]] provides the underlying infrastructure—specifically [[Sandboxes]] and [[GPU]] access—that enables these agents to execute safely and at scale.

This guide shows how to build a complete agent system from first principles, demonstrating architectural patterns that scale from simple single-agent loops to complex orchestration systems managing dozens of parallel workers.

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop that combines:
- A large language model (LLM)
- A set of callable tools (functions)
- State management
- Task completion logic

The tools and organizational structure surrounding the core agent loop is called a **harness**—the operational framework that gives agents context and capabilities.

### Agents in Practice

Companies like [[Ramp]] have successfully deployed background coding agents on Modal that now generate over half of their pull requests, demonstrating the practical value of well-designed agent systems.

## Building a Basic Coding Agent

### Starting Point: Unsafe but Simple

The simplest coding agent provides an `exec(command)` function that allows the [[LLM]] to execute arbitrary shell commands. While functional, this approach poses significant security risks with malicious prompts or unreliable models.

```python
# Minimal example structure
agent = Agent()
agent.add_tool(exec_command)
agent.run(user_prompt)
```

## Moving to Secure Sandboxes

### Isolation Through Sandboxes

[[Modal Sandboxes]] are isolated Linux environments running on virtual machines or security-hardened containers. By moving agent execution into sandboxes, the LLM operates within a contained environment rather than on the host system, dramatically improving security.

### SandboxAgent and Capabilities

The OpenAI Agents SDK provides:
- **SandboxAgent**: An Agent subclass with built-in sandbox integration
- **ShellTool**: A guarded execution tool with safety constraints
- **ModalSandboxSession**: The client managing remote sandbox connections
- **Capability**: A pattern for binding tool sets to specific sandbox instances

### GPU Integration

[[Modal]] allows attaching [[GPU]] resources to sandboxes via `ModalSandboxClientOptions`, enabling compute-intensive tasks like model training directly within agent environments.

## Advanced Harness Architecture

### Memory and Sessions

By default, agents are stateless—each run receives input and produces output without context of previous interactions. [[Session]] objects solve this problem by accumulating context across multiple agent runs and even across different agent instances.

#### Context Management Challenge

As memory accumulates indefinitely, **[[context rot]]**—the degradation of context quality as irrelevant information builds up—becomes a critical problem requiring intelligent context pruning and reset strategies.

### Orchestrator-Subagent Pattern

To handle long-horizon tasks while managing token consumption, the harness splits into two agent types:

**Orchestrator Agent**
- Maintains high-level memory of the entire task
- Makes strategic decisions
- Spawns and monitors subagents
- Remains context-aware of overall progress

**Subagent**
- Receives focused task descriptions from orchestrator
- Operates with a fresh, clean context window
- Performs specific work (e.g., implementing a feature, running an experiment)
- Returns a summary of completed work
- Session memory is discarded after task completion

This separation keeps the orchestrator's context lean while allowing detailed work to proceed without token bloat.

### Asynchronous Parallel Execution

Rather than blocking the orchestrator while waiting for subagent completion, a **SubAgentPool** enables:
- Multiple concurrent subagents managed as key-value pairs
- Non-blocking tool invocation returning `asyncio.Future` objects
- Selective waiting for specific work threads
- Tools for monitoring active subagent status

#### Visibility Mechanisms

Two approaches provide the orchestrator visibility into parallel work:
1. **Hooks**: Track the currently active tool for each subagent in real-time
2. **set_status Tool**: Allows subagents to provide status updates without exiting to the orchestrator

### GPU Quota Management

With asynchronous task spawning, unconstrained subagent creation could lead to unbounded GPU costs. A quota system limits the number of expensive resources (e.g., 8x [[H100]] GPUs) in simultaneous use, preventing runaway costs.

### Filesystem Snapshots for Work Deduplication

#### The Problem

When subagents start from base sandbox images, they redundantly perform setup work:
- Cloning repositories
- Installing dependencies
- Configuring environments

Over long-horizon tasks, this represents significant wasted GPU time.

#### The Solution

[[Filesystem Snapshots]] freeze an active sandbox's state into a reusable image ID. The orchestrator can:
- Create snapshots at checkpoint moments
- Spawn new subagents from these snapshots
- Branch work from known good states
- Dramatically reduce setup overhead

#### Filesystem as Implicit Memory

Beyond performance, snapshots enable **filesystem-based context management**:
- Artifacts from previous agent work remain available on disk
- Future agents can access this implicit memory without explicit context
- Codebase state provides continuity across agent generations
- Reduces reliance on token-consuming explicit context

### Skills Subsystem

For domain-specific tasks, a **Skills** plugin system allows the orchestrator to selectively opt into specialized context:
- Skills are loaded as tools that provide task-specific knowledge
- Keep the core harness general-purpose
- Enable reuse across different problem domains
- For example: [[Parameter Golf]] challenge-specific optimization strategies

## Practical Example: Parameter Golf

### The Challenge

OpenAI's [[Parameter Golf]] challenge asks participants to achieve a baseline intelligence threshold with the minimum number of model parameters—testing efficiency optimization.

### The Harness in Action

The complete system:
1. Accepts Parameter Golf challenge context and constraints
2. Orchestrator strategically plans optimization approaches
3. Spawns parallel subagents to explore different methods (different ML frameworks, architectures, training strategies)
4. Each subagent:
   - Starts from a snapshot with baseline setup complete
   - Implements and trains approaches
   - Reports results back to orchestrator
5. Orchestrator synthesizes results and directs further exploration
6. System scales to run dozens of parallel GPU-backed experiments

## Key Architectural Patterns

| Pattern | Purpose | Benefit |
|---------|---------|---------|
| [[Sandbox]] Isolation | Security & containment | Safe LLM code execution |
| [[Session]] Memory | Multi-turn context | Coherent long-horizon reasoning |
| Orchestrator-Subagent | Work decomposition | Token efficiency + parallelism |
| [[Async]] Pools | Concurrent execution | Maximize throughput |
| [[Filesystem Snapshots]] | State preservation | Reduce redundant setup |
| Quota Systems | Cost control | Prevent runaway expenses |
| Skills Plugins | Domain knowledge | Reusable, modular harnesses |

## Implementation Resources

- **Complete Example Code**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Modal Documentation**: [modal.com/docs](https://modal.com/docs)
- **OpenAI Agents SDK**: [OpenAI Developer Documentation](https://developers.openai.com/api/docs/guides/agents)

## Key Takeaways

1. **Composition Over Monoliths**: Build sophisticated systems by composing layers atop a simple core agent loop
2. **Context is Precious**: Manage context aggressively through memory systems, snapshots, and work decomposition
3. **Parallelism Requires Orchestration**: Effective multi-agent systems need strategic coordination, not just task parallelism
4. **Infrastructure Matters**: [[Modal]]'s sandbox and GPU capabilities unlock agent capabilities not possible on commodity hardware
5. **Iterative Refinement**: Start simple (unsafe local execution), then progressively add security, scale, and sophistication

## Getting Started

- Sign up for [[Modal]] to access sandboxes and GPUs
- Receive $30/month in free compute credits
- Reference the complete example repository while building
- Start with basic agents and progressively add harness features as needed

---

## Metadata

**Source**: Modal Blog - Engineering  
**Author**: Erik Dunteman (Member of Technical Staff, Modal)  
**Published**: April 15, 2026  