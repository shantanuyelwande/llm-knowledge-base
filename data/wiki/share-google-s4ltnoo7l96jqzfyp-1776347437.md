---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-27T05:32:34.011098
raw_file_updated: 2026-04-27T05:32:34.011098
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-27T05:32:34.011098
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progressive approach to creating sophisticated agent harnesses, starting from basic coding agents and evolving into a parallel, GPU-enabled system capable of autonomous research tasks. The guide uses OpenAI's Parameter Golf challenge as a practical example.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems. Unlike off-the-shelf solutions such as Codex or Claude Code, the SDK provides developers with the fundamental building blocks to create specialized agent harnesses tailored to specific organizational needs. [[Modal]] complements this capability by providing secure, scalable execution environments through its [[Sandbox]] technology.

This article demonstrates how companies like [[Ramp]] have successfully built internal agent systems that now generate the majority of their pull requests, establishing a template for enterprise-scale agentic systems.

## Core Concepts

### Agents and Harnesses

An **Agent** is fundamentally a loop that combines an [[Large Language Model|LLM]] with executable [[Tool|tools]] (functions) to accomplish tasks. A **Harness** is the broader system architecture built around the core agent loop, including state management, context handling, and tool orchestration.

The distinction between a basic agent and a production harness is crucial: while an agent provides the core reasoning loop, a harness provides the scaffolding that makes agents reliable, efficient, and safe for real-world applications.

### Sandboxes for Security

[[Sandbox|Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. By running agent tools within sandboxes rather than on the host system, developers can safely grant agents the ability to execute arbitrary code without risking the integrity of the production environment.

Modal's [[ModalSandboxSession]] provides a client interface to remotely running sandboxes, enabling agents to execute commands in isolated environments. The [[SandboxAgent]] class extends the base Agent with preloaded tools for sandbox interaction, including the [[ShellTool]] which adds guardrails to command execution.

### Capabilities

[[Capability|Capabilities]] are mechanisms for binding sets of tools to specific instances of [[ModalSandboxSession]]. They enable stateful tool interactions where each tool maintains awareness of its execution environment and can maintain state across multiple invocations.

## Progressive Architecture

### Stage 1: Basic Local Agent

The simplest approach creates an agent with an `exec()` function that can run arbitrary shell commands. While functional, this approach is inherently unsafe and unsuitable for production use, particularly with untrusted prompts or lower-quality models.

### Stage 2: Sandboxed Execution

Moving agent execution into Modal Sandboxes provides critical security isolation. Agents effectively operate within a restricted environment, unable to access the host system. The [[ShellTool]] adds additional guardrails to command execution.

**Key advancement:** GPU support can be attached to sandboxes using `ModalSandboxClientOptions`, enabling resource-intensive machine learning tasks.

### Stage 3: Memory and Sessions

By default, agents are stateless—each run receives input and produces output without retaining context from previous interactions. [[Session|Sessions]] objects solve this problem by accumulating conversation history across multiple agent runs.

**Challenge introduced:** As memory accumulates indefinitely, [[Context Rot|context rot]] becomes a concern. Context management strategies become necessary to prevent token bloat and degraded performance.

### Stage 4: Orchestration with Subagents

To manage long-horizon tasks while controlling context growth, the architecture introduces an [[Orchestrator]] agent and [[Subagent|subagents]]:

- The **Orchestrator** maintains high-level task memory and strategy
- **Subagents** handle focused, short-duration tasks with fresh context windows
- Subagent sessions are discarded after completion, preventing context accumulation

This separation allows the orchestrator to delegate implementation details while maintaining awareness of overall progress.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking orchestrator execution on subagent completion, a [[SubAgentPool]] manages multiple parallel subagents using `asyncio.Future` objects. This enables:

- **Higher throughput:** Multiple experiments run simultaneously
- **Non-blocking orchestration:** The orchestrator can spawn work and continue planning
- **Visibility tools:** `list_subagents` and `set_status` tools keep the orchestrator informed without blocking

**Implementation note:** The orchestrator requires careful prompting to prevent premature exit before async tasks complete.

### Stage 6: Resource Management with Quotas

To prevent unbounded GPU consumption, quota systems limit the number of expensive resources (such as 8x H100 GPUs) that can be provisioned simultaneously.

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshot|Filesystem snapshots]] freeze the state of an active sandbox into a reusable image. This enables:

- **Work deduplication:** Subagents can branch from known checkpoints rather than repeating setup
- **Implicit memory:** The sandbox filesystem acts as persistent storage for artifacts and state
- **Context offloading:** Implementation details stored on disk reduce pressure on token-based context windows

Snapshots enable the orchestrator to progress work through stages, snapshot successful states, and spawn fresh subagents from those checkpoints with minimal context.

### Stage 8: Pluggable Skills System

A [[Skill|skills]] subsystem allows the orchestrator to selectively opt into domain-specific context and capabilities through plugins. This maintains harness generality while enabling task-specific optimization.

## Practical Example: Parameter Golf

OpenAI's [[Parameter Golf]] challenge prompted the development of this architecture. The challenge requires fitting baseline intelligence into minimal model parameters—a task requiring:

- Parallel experimentation across different approaches
- GPU-intensive training and evaluation
- Code generation and modification
- Long-horizon autonomous research

The complete harness architecture enables the orchestrator to:

1. Spawn multiple parallel subagents, each exploring different frameworks or approaches
2. Provide each subagent with GPU resources
3. Snapshot filesystem state at successful checkpoints
4. Branch new subagents from snapshots for follow-up work
5. Manage overall resource consumption through quotas
6. Maintain high-level strategy without token bloat

## Key Takeaways

1. **Composition over monoliths:** Complex agent systems are built by composing capabilities around a core agent loop rather than creating monolithic solutions.

2. **Context as a resource:** Token-based context windows are finite resources requiring active management through sessions, snapshots, and strategic information offloading.

3. **Isolation enables capability:** Sandbox execution allows safe delegation of powerful capabilities (code execution, package installation, GPU access) to agents.

4. **Parallelism requires orchestration:** Async execution dramatically improves throughput but requires careful orchestration to maintain coherent overall progress.

5. **Generality through plugins:** Skills systems allow harnesses to remain general-purpose while supporting domain-specific optimization.

## Related Technologies

- [[Modal]] - Cloud platform providing sandboxes and GPU infrastructure
- [[OpenAI Agents SDK]] - Framework for building agent systems
- [[Large Language Model|LLMs]] - The reasoning component of agents
- [[Asynchronous Programming]] - Enabling parallel agent execution
- [[Container Orchestration]] - Infrastructure for sandbox management

## Implementation Resources

- **Complete project code:** [GitHub - modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Modal documentation:** [https://modal.com/docs](/docs)
- **OpenAI Agents SDK:** [https://openai.com/index/the-next-evolution-of-the-agents-sdk/](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)

---

## Metadata

**Source:** Modal Engineering Blog  
**Author:** Erik Dunteman  
**Date Published:** April 15, 2026  
**Read Time:** 8 minutes  
**Original URL:** https://share.google/S4lTnOo7l96jQZFyP

**Tags:** #agents #llm #modal #openai #infrastructure #parallelization #gpu #coding-agents #autonomous-systems

**Related Articles:**
- [[How Ramp Built a Full-Context Background Coding Agent on Modal]]
- [[Introduction to AI Agents]]
- [[GPU Computing for Machine Learning]]
- [[Containerization and Sandbox Technology]]
- [[Asynchronous Programming Patterns]]

**Categories:** Engineering | AI/ML | Infrastructure | Tutorial