---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:54:10.302434
raw_file_updated: 2026-04-24T18:54:10.302434
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:54:10.302434
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progressive approach to creating increasingly sophisticated agent harnesses, from basic coding agents to parallel, GPU-accelerated research systems. The example uses OpenAI's Parameter Golf challenge to showcase practical implementation of advanced features like sandboxing, memory management, async parallelization, and filesystem snapshots.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and automation tasks. While off-the-shelf solutions like Codex and Claude Code are widely available, many organizations require specialized agent harnesses tailored to their specific needs. This guide demonstrates how to build such systems by combining the OpenAI Agents SDK with [[Modal]]'s computing infrastructure.

The approach outlined here progresses from simple implementations to a sophisticated parallel research system capable of managing multiple autonomous agents with GPU acceleration, context management, and efficient resource utilization.

---

## Fundamentals of Agent Systems

### What is an Agent?

An [[Agent]] is fundamentally a loop that combines:
- An [[Large Language Model|LLM]] for decision-making
- A set of callable [[Tool|tools]] (functions)
- State management for task completion

The collection of tools and surrounding infrastructure built around this core loop is called a **Harness**.

### Basic Coding Agent

The simplest implementation provides an `exec(command)` tool that allows the agent to execute shell commands:

```python
# Minimal example - unsafe and not recommended
agent = Agent(tools=[exec_tool])
agent.run("Write and execute a Python script")
```

**Security Consideration:** Allowing arbitrary command execution on a host system creates significant security risks with malicious prompts or low-quality models.

---

## Securing Agents with Sandboxes

### Sandbox Architecture

[[Sandbox|Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. They provide:
- Process isolation from the host system
- Controlled resource allocation
- Safe execution environment for untrusted code

### SandboxAgent Implementation

The OpenAI Agents SDK provides a `SandboxAgent` class that:
- Extends the base `Agent` functionality
- Manages remote sandbox sessions via `ModalSandboxSession`
- Includes a `ShellTool` with built-in guardrails
- Supports GPU attachment through `ModalSandboxClientOptions`

### Capabilities System

[[Capability|Capabilities]] are stateful tool bindings attached to specific sandbox instances. This architecture enables:
- Persistent state across multiple agent invocations
- Clean separation of concerns
- GPU resource allocation specific to sandbox requirements

### Example: Training MNIST

A one-shot prompt can direct the agent to complete end-to-end machine learning tasks within a sandboxed environment:

```python
sandbox_agent = SandboxAgent(
    sandbox_session=modal_sandbox_session,
    capabilities=[shell_capability, gpu_capability]
)
sandbox_agent.run("Train an MNIST model and report accuracy")
```

---

## Building Sophisticated Harnesses

### Memory Management with Sessions

#### The Problem

By default, agents are stateless—they cannot maintain conversation history across multiple invocations or user interactions.

#### The Solution: Sessions

[[Session|Sessions]] are persistent context objects that:
- Accumulate conversation history across agent runs
- Maintain state across multiple user prompts
- Enable long-horizon task execution
- Can be shared between agent instances

```python
session = Session()
result = agent.run(prompt, session=session)
# Session retains context for subsequent runs
```

#### Context Rot Management

As memory accumulates, **[[context rot]]** becomes a concern—the quality of decision-making degrades as the context window becomes cluttered. Effective harnesses must implement strategies for:
- Context prioritization
- Selective memory retention
- Context window optimization

### Orchestration with Subagents

#### Hierarchical Agent Architecture

For long-horizon work, a single agent quickly becomes token-heavy as it:
- Explores and modifies codebases
- Processes extensive stdout/stderr output
- Maintains accumulated conversation history

**Solution:** Split agents into two roles:

1. **Orchestrator Agent**
   - Maintains high-level memory of the entire task
   - Makes strategic decisions
   - Delegates focused work to subagents
   - Receives summaries rather than implementation details

2. **Subagent**
   - Receives fresh context window
   - Completes focused, bounded tasks
   - Returns summary of work performed
   - Session memory is discarded after completion

#### Benefits

- Keeps orchestrator context lean and focused
- Enables [[task delegation]]
- Allows subagents to specialize in specific domains
- Reduces overall token consumption

### Parallel Execution with SubAgent Pools

#### Async Architecture

Rather than blocking orchestrator execution while waiting for subagent results, implement asynchronous execution:

```python
subagent_pool = SubAgentPool()
future = subagent_pool.spawn_subagent(task)
# Orchestrator continues without blocking
```

#### SubAgentPool Implementation

A `SubAgentPool` maintains:
- Key-value store of active subagents
- [[asyncio.Future|Futures]] for tracking work completion
- Status monitoring capabilities

#### Visibility Tools

Maintain orchestrator awareness of parallel work through:

1. **Hooks System**
   - Track current active tool for each subagent
   - Monitor execution progress in real-time

2. **Status Updates**
   - `set_status` tool allows subagents to report progress
   - Enables orchestrator to understand ongoing work without blocking

3. **List Subagents Tool**
   - Provides orchestrator visibility into all active parallel tasks
   - Shows current status and progress of each worker

### Resource Management with Quotas

#### GPU Cost Control

Parallel execution creates risk of unbounded resource consumption. Implement quota systems to:
- Limit concurrent GPU allocations
- Prevent runaway cost escalation
- Ensure fair resource distribution

```python
subagent_pool = SubAgentPool(gpu_quota=8)  # Max 8x H100 GPUs
```

#### Example: Parallel MNIST Training

An orchestrator can spawn multiple subagents to train models across different frameworks simultaneously:

```
"Train MNIST models using PyTorch, TensorFlow, and JAX in parallel,
each on a separate GPU, and report comparative results"
```

The orchestrator naturally spawns three parallel subagents, each with dedicated GPU resources.

---

## Advanced Harness Features

### Filesystem Snapshots

#### The Problem

When multiple subagents start from base sandbox images, they redundantly perform identical setup work:
- Cloning repositories
- Installing dependencies
- Building environments

Over long-horizon tasks, this represents significant wasted GPU time and cost.

#### The Solution: Snapshots

[[Filesystem Snapshot|Filesystem snapshots]] freeze an active sandbox state into an identifier that can serve as a starting point for new subagents:

```python
snapshot_id = active_sandbox.create_snapshot()
new_subagent = SubAgent(initial_snapshot=snapshot_id)
# New subagent starts from checkpoint, not base image
```

#### Benefits

1. **Performance**
   - Eliminate redundant setup across parallel workers
   - Reduce time to productive work

2. **Context Management**
   - Offload memory from [[Session|sessions]] to filesystem
   - Implicit memory via codebase state
   - Artifacts from prior work available to future agents

3. **Branching Workflows**
   - Orchestrator progresses work to known checkpoints
   - Spawn fresh subagents from checkpoints with follow-up instructions
   - Subagents quickly orient themselves without context bloat

#### On-Disk Memory

The filesystem serves as implicit memory:
- Explicit: Skills and memory files written to disk
- Implicit: Codebase already in working state from prior agent work

---

### Skills Subsystem

#### Pluggable Knowledge

Rather than hardcoding domain-specific prompts into the core harness, implement a skills system:

```python
skills = [
    ParameterGolfSkill(),
    ResearchMethodologySkill(),
    OptimizationTechniquesSkill()
]
orchestrator.attach_skills(skills)
```

#### Advantages

- **Generalizability**: Core harness remains domain-agnostic
- **Composability**: Mix and match skills for different tasks
- **Maintainability**: Domain knowledge isolated and versioned
- **Reusability**: Skills shared across multiple agents and projects

---

## Complete Harness Architecture

### System Overview

A production agent harness integrates:

1. **Core