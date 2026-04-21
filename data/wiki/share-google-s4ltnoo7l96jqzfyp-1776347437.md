---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-21T04:53:35.150388
raw_file_updated: 2026-04-21T04:53:35.150388
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-21T04:53:35.150388
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI Agent|agent harnesses]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progressive approach to creating sophisticated agentic systems, starting from basic coding agents and advancing to parallel, GPU-accelerated multi-agent architectures capable of handling complex research tasks.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable AI agent systems. Unlike off-the-shelf solutions such as Codex and Claude Code, the SDK provides developers with the building blocks needed to construct powerful internal agentic tools tailored to specific organizational needs. This guide demonstrates integration with [[Modal]], a cloud platform specializing in serverless computing and GPU resources, to create scalable agent systems.

## Core Concepts

### What is an Agent Harness?

An **agent harness** is the complete system built around a core [[AI Agent]] loop. It encompasses:
- The fundamental agent loop (an LLM running tools iteratively to task completion)
- Supporting tools and functions available to the agent
- State management and memory systems
- Context management strategies
- Integration layers with external systems

The harness represents the product engineering layer where developers customize agents for specific use cases.

### The Basic Coding Agent

The simplest agent implementation is a loop containing:
1. An [[LLM|Large Language Model]] that reasons about tasks
2. A set of available tools the agent can invoke
3. An `exec()` function allowing shell command execution

**Security Consideration:** Basic implementations executing arbitrary commands on the host system pose significant security risks and are not recommended for production use.

## Progressive Architecture Development

### Stage 1: Securing with Sandboxes

[[Sandbox|Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. Integrating sandboxes provides:

- **Isolation**: The LLM operates within a contained environment rather than the host system
- **Safety**: Arbitrary code execution cannot compromise the host
- **Resource Control**: GPU allocation and computational resources are managed independently

The OpenAI Agents SDK provides a `SandboxAgent` class that:
- Pre-loads tools for remote sandbox interaction
- Includes a `ShellTool` class with built-in guardrails
- Manages `ModalSandboxSession` for client-sandbox communication
- Supports [[GPU]] attachment via `ModalSandboxClientOptions`

### Stage 2: Adding Memory with Sessions

By default, agents are stateless—each invocation has no knowledge of previous interactions. **Sessions** solve this by:

- Accumulating conversation context across multiple agent runs
- Maintaining state across different agent instances
- Enabling multi-turn interactions with persistent memory

**Challenge Introduced:** [[Context Rot|Context rot]] emerges when memory accumulates indefinitely, requiring intelligent context management strategies.

### Stage 3: Orchestration with Subagents

To manage long-horizon tasks while controlling context bloat, agents are split into two types:

**Orchestrator Agent:**
- Maintains high-level task memory
- Makes strategic decisions
- Delegates implementation work

**Subagent:**
- Receives focused task descriptions
- Operates with fresh context window
- Returns work summaries rather than detailed logs
- Session memory is discarded after task completion

This separation keeps orchestrator context lean while enabling specialized task execution.

### Stage 4: Asynchronous Parallel Processing

A **SubAgentPool** manages multiple concurrent subagents:

- Orchestrator spawns parallel subagents without blocking
- `asyncio.Future` objects track work in progress
- Tools enable selective waiting for specific tasks to complete
- Orchestrator visibility maintained through:
  - **Hooks**: Track active tools for each subagent
  - **Status Updates**: Subagents report progress without exiting
  - **List Subagents Tool**: Provides orchestrator with real-time worker status

### Stage 5: Resource Management with Quotas

GPU resource costs are controlled through quota systems:

- Fixed limits on expensive GPU resources (e.g., 8x H100s)
- Prevents unbounded spawning of parallel subagents
- Balances computational capability with cost constraints

### Stage 6: Filesystem Snapshots for Deduplication

**Filesystem Snapshots** freeze sandbox state into reusable images, enabling:

- **Efficiency**: New subagents branch from established checkpoints rather than starting from scratch
- **Context Management**: Filesystems serve as implicit memory, offloading information from token-limited [[Context Window|context windows]]
- **Artifact Persistence**: Code repositories and trained models remain available to future agents
- **Branching**: Multiple work threads can diverge from known-good states

### Stage 7: Skills Subsystem

A pluggable **skills system** allows agents to selectively opt into specialized knowledge:

- Generic harness remains general-purpose
- Domain-specific skills (e.g., Parameter Golf challenge expertise) are modular
- Reduces prompt engineering overhead
- Enables harness reuse across different problem domains

## Practical Implementation: Parameter Golf

[[Parameter Golf]] is an OpenAI challenge to achieve baseline intelligence thresholds with minimal model parameters. The complete harness enables:

1. **Parallel Research**: Multiple subagents simultaneously explore different approaches
2. **GPU Acceleration**: Each subagent has access to GPU resources for model training
3. **Checkpoint Management**: Successful approaches are snapshotted for branching
4. **Autonomous Operation**: Orchestrator manages experiment workflow without human intervention
5. **Context Efficiency**: Long-horizon research without token explosion

## Key Technical Components

### ModalSandboxSession
Client interface for remote sandbox communication, managing state and tool invocation.

### Capabilities
Binding mechanisms for attaching tools to specific sandbox instances, enabling stateful tool interactions.

### Hooks System
Monitoring mechanism tracking agent tool usage and execution state across the subagent pool.

### Async Task Management
Non-blocking orchestrator operations enabling true parallelism while maintaining coordination.

## Design Principles

1. **Composability**: Systems are built by composing simple, focused components
2. **Context Efficiency**: Memory and context are carefully managed to prevent bloat
3. **Isolation**: Work is compartmentalized to prevent cascading failures
4. **Scalability**: Architecture naturally parallelizes across available resources
5. **Generalizability**: Core harness remains reusable across different domains

## Practical Considerations

### Context Management
- Keep orchestrator context focused on high-level decisions
- Delegate implementation details to subagents
- Use filesystem snapshots to externalize state
- Implement selective context reset for long-running tasks

### GPU Resource Optimization
- Snapshot sandboxes after expensive setup work
- Branch subagents from established checkpoints
- Implement quota systems for cost control
- Parallelize independent work streams

### Debugging and Observability
- Hook systems provide visibility into subagent activities
- Status tools enable progress tracking without full context transmission
- Filesystem artifacts persist for inspection
- Logs accumulate in isolated environments

## Related Concepts

- [[AI Agent|AI Agents]]
- [[OpenAI Agents SDK]]
- [[Modal]] (cloud platform)
- [[Sandbox|Sandboxes]] (isolated environments)
- [[LLM|Large Language Models]]
- [[GPU]] (graphics processing units)
- [[Context Window]]
- [[Context Rot]]
- [[Orchestration]] (multi-agent coordination)
- [[Async Programming]]

## Example Use Cases

- **Research Automation**: Parallel exploration of ML approaches
- **Code Generation**: Multi-agent coding tasks with GPU acceleration
- **Model Training**: Distributed training experiments with checkpoint management
- **Parameter Optimization**: Concurrent optimization across different configurations
- **Internal Tools**: Custom agent systems replacing off-the-shelf solutions

## Getting Started

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

Key resources:
- [[OpenAI Agents SDK]] documentation
- [[Modal]] platform and sandbox documentation
- Example: Training MNIST with one-shot prompts
- GPU allocation and configuration guides

---

## Metadata

**Source:** Modal Engineering Blog  
**Author:** Erik Dunteman (Member of Technical Staff, Modal)  
**Published:** April 15, 2026  
**Read Time:** 8 minutes  
**Original URL:** https://share.google/S4lTnOo7l96jQZFyP

**Tags:** #AI-Agents #OpenAI #Modal #Sandboxes #GPU #Distributed-Computing #Agent-Orchestration #Python #LLM

**Related Topics:**
- [[Ramp]] - Case study: background coding agents
- [[Parameter Golf]] - OpenAI efficiency challenge
- [[Agentic Systems]] - Multi-agent architecture patterns
- [[Cloud Computing]] - Serverless and containerized