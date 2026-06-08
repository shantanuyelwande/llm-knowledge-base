---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-08T06:50:35.636646
raw_file_updated: 2026-06-08T06:50:35.636646
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-08T06:50:35.636646
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent]] systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates progressive development of an agent harness, from basic implementation to a sophisticated parallel research system capable of running GPU-accelerated tasks. The example uses OpenAI's Parameter Golf challenge to showcase how to build scalable, autonomous coding agents with memory management, task delegation, and resource optimization.

---

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building custom agentic systems. Unlike off-the-shelf solutions such as [[Codex]], [[Claude Code]], and OpenCode, the SDK provides foundational building blocks that allow teams to construct specialized agent harnesses tailored to their specific needs. [[Modal]] serves as the execution platform, providing [[sandboxes]], [[GPU]] resources, and infrastructure for scaling these agents.

This guide walks through building a production-ready agent harness from first principles, demonstrating how companies like [[Ramp]] have successfully deployed coding agents responsible for significant portions of their pull request generation.

---

## Core Concepts

### What is an Agent Harness?

An **Agent Harness** is the complete system surrounding a core [[agent loop]]. It consists of:

- The base [[Agent]] (a loop running an [[LLM]] with callable tools)
- Tools and functions the agent can invoke
- State management and context handling
- Security boundaries and resource limits
- Orchestration logic for complex workflows

The harness is where product engineering happens—it's entirely within the programmer's control and determines how effectively an agent can accomplish its goals.

### The Agent Loop

At its core, an [[Agent]] is a for-loop executing the following pattern:

1. LLM receives current context and available [[tools]]
2. LLM decides which tool to invoke (or complete the task)
3. Tool executes and returns results
4. Results feed back into context for next iteration
5. Loop continues until task completion

---

## Building Progressive Complexity

### Stage 1: Basic Coding Agent

The simplest implementation provides an `exec(command)` function allowing the agent to run arbitrary shell commands. While functional, this approach is **unsafe** and not recommended for production use:

- No isolation between agent and host system
- Malicious prompts could compromise the system
- Quality of model affects security posture

This serves as a proof-of-concept only.

### Stage 2: Sandboxed Execution

[[Modal Sandboxes]] provide isolated [[Linux]] environments running on [[VMs]] or security-hardened containers. Moving agent execution into sandboxes provides:

- **Isolation**: The [[LLM]] operates within a contained environment
- **Safety**: Host system remains protected from agent actions
- **Flexibility**: Multiple independent agent instances can run simultaneously

The OpenAI Agents SDK provides the `SandboxAgent` class, a superset of `Agent` with preloaded tools for remote sandbox interaction. Key components include:

- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: Client managing the remote sandbox connection
- **`Capability`**: Binds a set of tools to a specific sandbox instance

#### GPU Integration

[[Modal]] uniquely allows attaching [[GPUs]] to sandboxes via `ModalSandboxClientOptions`. This enables agents to:

- Train [[machine learning]] models
- Run computationally intensive tasks
- Execute parallel workloads across GPU clusters

**Example Use Case**: Training [[MNIST]] models with a one-shot prompt—the agent receives a task description and autonomously writes code, executes training, and reports results.

### Stage 3: Memory and Session Management

By default, agents are stateless. Each invocation starts fresh with no memory of previous interactions. [[Sessions]] solve this problem:

- **Accumulate context** across multiple agent runs
- **Preserve conversation history** for multi-turn interactions
- **Enable long-horizon tasks** spanning many steps

#### Context Management Challenges

With indefinite memory accumulation comes new problems:

- **[[Context Rot]]**: Older information becomes less relevant as context grows
- **Token limits**: [[LLM]] context windows are finite
- **Degraded performance**: Excessive context can confuse the model

Solutions include:

- Intelligent context pruning
- Summarization of completed work
- Strategic context resets

### Stage 4: Orchestrator and Subagent Architecture

Coding agents are inherently token-heavy as they explore codebases and process logs. Long-horizon tasks require a different approach: **agent delegation**.

#### Orchestrator Pattern

The system splits into two agent types:

1. **Orchestrator**: Main agent maintaining task-level memory and high-level planning
2. **Subagents**: Specialized agents spawned for specific tasks with fresh contexts

The orchestrator has an `invoke_subagent` tool that:

- Creates a new agent with clean context
- Assigns a focused subtask
- Receives a summary of completed work
- Maintains only high-level details in its own context

**Benefits**:
- Prevents context bloat in primary thread
- Enables focused, efficient subtask execution
- Allows work decomposition and parallelization

### Stage 5: Asynchronous Parallel Execution

Rather than blocking on subagent completion, the orchestrator can manage multiple parallel subagents using a **worker pool** pattern:

#### SubAgentPool Implementation

A `SubAgentPool` maintains:

- Key-value store of active subagents
- Asynchronous task management
- Status tracking and monitoring

The orchestrator gains new tools:

- **`invoke_subagent`**: Spawns non-blocking subagent tasks, returning futures
- **`list_subagents`**: Views active subagents and their status
- **`set_status`**: Allows subagents to report progress without exiting

#### Monitoring Subagent Activity

Two mechanisms provide visibility:

1. **[[Hooks]]**: Track current active tools for each subagent
2. **`set_status` tool**: Subagents periodically update status without returning to orchestrator

**Challenge**: Preventing the orchestrator from exiting before async tasks complete. This requires careful prompt engineering to keep the orchestrator engaged in productive thinking.

### Stage 6: Resource Management with Quotas

Async parallelization creates risk: unbounded spawning of expensive [[GPU]] subagents could rapidly consume budget.

**Quota System Solution**:

- Define maximum concurrent expensive resources (e.g., 8x [[H100]] GPUs)
- Pool enforces limits before spawning new subagents
- Orchestrator must wait for capacity before delegating new work

This enables safe parallelization while maintaining cost control.

### Stage 7: Filesystem Snapshots and Checkpointing

As tasks grow longer, subagents waste time repeating setup work:

- Cloning repositories
- Installing dependencies
- Building environments

**Filesystem Snapshots** freeze sandbox state into reusable checkpoints:

- Snapshot an active sandbox after setup completion
- Capture filesystem state as an image ID
- Spawn future subagents from this checkpoint
- New agents resume from known state without setup overhead

#### Filesystem as Implicit Memory

The filesystem serves dual purposes:

1. **Performance**: Avoid redundant setup work
2. **Memory**: Store artifacts and context on disk rather than in [[LLM]] context

This enables:

- Implicit memory sharing across agents
- Offloading context from [[token]] limits
- Stateful codebase evolution across agent generations

#### Context Management Benefits

Subagents can:

- Examine prior work through filesystem inspection
- Resume interrupted tasks from checkpoints
- Access shared artifacts without explicit context inclusion
- Maintain working state across generations

### Stage 8: Skills and Plugin System

The final optimization layer uses a **skills subsystem** for domain-specific knowledge:

- **Skills**: Pluggable context modules the orchestrator can selectively enable
- **Selective Activation**: Agents opt into relevant skills based on task requirements
- **Generality**: Core harness remains task-agnostic while supporting specialized domains

For the [[Parameter Golf]] challenge, skills provide:

- Specific challenge rules and constraints
- Optimization strategies
- Framework-specific guidance
- Efficiency techniques

This approach keeps the harness general-purpose while enabling specialized expertise.

---

## Complete Architecture

The final system combines all components:

```
Orchestrator Agent (with Session memory)
├── invoke_subagent (async, non-blocking)
├── list_subagents (status monitoring)
├── set_status (progress updates)
└── SubAgentPool (quota management)
    ├── Subagent 1 (ModalSandboxSession + GPU)
    │   ├── ShellTool
    │   ├── Filesystem Snapshot
    │   └── Skills
    ├──