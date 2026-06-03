---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-03T06:59:11.617143
raw_file_updated: 2026-06-03T06:59:11.617143
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-03T06:59:11.617143
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using [[OpenAI]]'s Agents SDK integrated with [[Modal]]'s cloud computing platform. It demonstrates progressive techniques for creating increasingly sophisticated agent harnesses, from basic coding agents to parallel, GPU-accelerated multi-agent systems capable of autonomous research and experimentation.

## Overview

[[OpenAI]] recently launched the Agents SDK, a framework for building agent systems designed for coding, research, and complex task automation. This guide demonstrates how to leverage [[Modal]]'s [[Sandboxes]] infrastructure to create production-ready agent harnesses that can scale across multiple [[GPU]] instances while maintaining clean context management and efficient resource allocation.

The example application uses OpenAI's [[Parameter Golf]] challenge—a competition to achieve baseline intelligence thresholds with minimal model parameters—as a practical use case for parallel agent-driven experimentation.

## Foundational Concepts

### What is an Agent?

An [[Agent]] is fundamentally a control loop that combines:
- A [[Large Language Model]] (LLM) for decision-making
- A set of [[Tool|tools]] (executable functions) for task completion
- State management for multi-step problem solving

The collection of tools, state management, and orchestration logic surrounding the core agent loop is called a **Harness**.

### The Basic Coding Agent

The simplest agent implementation includes an `exec(command)` tool that allows the LLM to execute arbitrary shell commands. While functional, this approach presents significant [[Security|security]] risks with malicious prompts or unreliable models.

## Core Architecture Progression

### Stage 1: Local Execution (Unsafe)

The initial approach runs agents directly on the host system with full shell access. This serves as a proof-of-concept but is unsuitable for production use.

### Stage 2: Sandboxed Execution

[[Modal]] provides [[Sandboxes]]—isolated Linux environments running on [[Virtual Machine|VMs]] or security-hardened containers. The OpenAI Agents SDK includes:

- **SandboxAgent**: A specialized agent class with built-in sandbox integration
- **ShellTool**: A command execution tool with additional guardrails
- **ModalSandboxSession**: The client interface to remote sandbox instances

Sandboxes enable the LLM to operate within a confined environment, eliminating host system exposure. [[Capability|Capabilities]] bind sets of tools to specific sandbox instances, allowing stateful operations.

#### GPU Integration

[[Modal]] allows attaching [[GPU]] resources to sandboxes through `ModalSandboxClientOptions`, enabling computationally intensive tasks like model training directly within agent environments.

**Example: MNIST Training**

Agents can autonomously train [[MNIST]] models with single-prompt instructions, handling the complete workflow from environment setup to model evaluation.

### Stage 3: Memory and State Management

#### Sessions

By default, agents are stateless. [[Session|Sessions]] objects accumulate conversation context across multiple agent runs, enabling multi-turn interactions and persistent memory.

**Challenge: Context Rot**

As sessions accumulate indefinitely, [[Context Rot|context rot]] becomes problematic. The harness must implement intelligent context management to prevent token bloat and maintain relevance.

### Stage 4: Orchestration with Subagents

To manage long-horizon tasks and control token consumption, agents are split into:

- **Orchestrator Agent**: Maintains high-level task memory and coordination
- **Subagents**: Spawn for focused, short-duration tasks with fresh context windows

The orchestrator delegates work through an `invoke_subagent` tool, receiving summaries rather than detailed execution logs. This pattern dramatically reduces context overhead while enabling complex, multi-step workflows.

### Stage 5: Parallel Execution

#### SubAgent Pool

Rather than blocking orchestrator execution during subagent work, a **SubAgentPool** manages multiple concurrent agents using:

- [[Asyncio]] for non-blocking execution
- Worker pool patterns for resource management
- `asyncio.Future` objects for tracking completion

#### Visibility and Status Tracking

Parallel execution requires mechanisms for the orchestrator to monitor subagent progress:

- **Hooks**: Track currently active tools in each subagent
- **set_status Tool**: Allows subagents to update progress without returning to orchestrator
- **list_subagents Tool**: Provides orchestrator visibility into all active workers

#### Quota Systems

[[GPU]] resource costs necessitate quota management. The harness implements limits on concurrent expensive resources (e.g., H100 GPUs) to prevent unbounded spending while maintaining parallelism.

### Stage 6: Filesystem Snapshots

#### Problem: Redundant Setup Work

With multiple subagents starting from base sandboxes, each wastes [[GPU]] time on identical setup tasks (repository cloning, dependency installation).

#### Solution: Snapshots

**Filesystem Snapshots** freeze sandbox state into reusable images. Subagents can branch from known checkpoints rather than starting from scratch.

**Benefits:**
- Eliminates redundant setup operations
- Reduces [[GPU]] utilization and costs
- Enables implicit memory through filesystem state
- Allows future agents to resume from working states without explicit context inclusion

### Stage 7: Skills Subsystem

The final sophistication layer adds **Skills**—pluggable context modules that agents can selectively adopt. Rather than hardcoding domain knowledge into the harness, skills provide:

- Specialized prompting for specific challenges
- Domain-specific tool sets
- Modular capability expansion
- Reusability across different agent instances

## Implementation Patterns

### Context Management Strategy

The complete harness maintains lean context through:

1. **Session-based memory** for orchestrator persistence
2. **Subagent isolation** to prevent context bloat
3. **Filesystem snapshots** for implicit memory
4. **Skills plugins** for selective knowledge injection

### Scaling Considerations

The architecture enables:

- **Parallel experimentation** across multiple subagents
- **GPU efficiency** through snapshot-based branching
- **Cost control** via quota systems
- **Long-horizon autonomy** through orchestration patterns

## Practical Example: Parameter Golf Research

The complete harness can autonomously run [[Parameter Golf]] experiments by:

1. Accepting high-level research objectives
2. Spawning parallel subagents to explore different approaches
3. Creating filesystem snapshots at progress checkpoints
4. Branching new subagents from snapshots for follow-up work
5. Coordinating results through the orchestrator

This enables autonomous research at scale, with minimal human intervention beyond initial prompting.

## Key Takeaways

- Agent harnesses are composable systems built around core LLM loops
- [[Modal]] [[Sandboxes]] provide secure, scalable execution environments
- Progressive architectural patterns enable increasingly sophisticated agent behaviors
- Context management is critical for maintaining efficiency in long-running systems
- Parallelization and resource quotas are essential for production deployment

## Related Topics

- [[OpenAI]] - AI model provider
- [[Modal]] - Cloud computing platform for AI workloads
- [[Sandboxes]] - Isolated execution environments
- [[Large Language Models]] - Foundation models powering agents
- [[Agents]] - Autonomous systems using LLMs and tools
- [[Parameter Golf]] - Efficiency optimization challenge
- [[Context Rot]] - Degradation of context quality over time
- [[GPU]] - Hardware acceleration for training and inference

## Metadata

**Source:** Modal Blog - Engineering  
**Author:** Erik Dunteman, Member of Technical Staff  
**Published:** April 15, 2026  
**Read Time:** 8 minutes  
**Original URL:** https://share.google/S4lTnOo7l96jQZFyP  
**Repository:** [openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

**Tags:** `#agents` `#openai` `#modal` `#sandboxes` `#gpu` `#python` `#orchestration` `#parallel-computing` `#ai-engineering`

**Related Articles:**
- How Ramp Built a Full-Context Background Coding Agent on Modal
- OpenAI Agents SDK Launch
- Parameter Golf Challenge