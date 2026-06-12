---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-12T06:47:16.903927
raw_file_updated: 2026-06-12T06:47:16.903927
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-12T06:47:16.903927
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom AI agents using the [[OpenAI Agents SDK]] integrated with [[Modal]] sandboxes. It demonstrates a progressive approach to creating sophisticated agent systems, starting from basic coding agents and evolving into a parallel, GPU-accelerated research harness capable of handling complex tasks like OpenAI's Parameter Golf challenge.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and autonomous task execution. Unlike off-the-shelf solutions such as Codex, Claude Code, and OpenCode, the SDK provides building blocks for organizations to create tailored agentic systems. This guide demonstrates how to integrate the SDK with [[Modal]] to create scalable, secure, and efficient agent harnesses.

## Core Concepts

### What is an Agent?

An [[AI Agent]] is fundamentally a for-loop with a [[Large Language Model]] (LLM) executing [[Tools]] (functions) to accomplish tasks. The set of tools and state surrounding the core agent loop is called a "Harness," which functions as the framework enabling the agent to operate effectively.

### The Agent Harness

A harness encompasses everything surrounding the base agent loop—context, tools, capabilities, and state management. Building a harness is similar to product engineering, as it provides complete programmer control over how agents operate and what capabilities they possess.

## Building Blocks: From Basic to Advanced

### Stage 1: The Basic Coding Agent

The simplest coding agent includes an `exec(command)` function allowing arbitrary shell command execution. While straightforward to implement, this approach presents significant security risks:

- **Security vulnerability**: Malicious prompts or low-quality model outputs could damage the host system
- **Lack of isolation**: Direct access to the host environment
- **Unsafe for production**: Not recommended for any real-world application

### Stage 2: Sandboxed Execution with Modal

[[Modal Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. Integrating sandboxes improves security significantly:

**Key improvements:**
- The LLM operates within an isolated environment rather than accessing the host
- The `SandboxAgent` class provides pre-built tools for remote sandbox interaction
- `ShellTool` adds guardrails to command execution
- `ModalSandboxSession` manages the client connection to remote sandboxes

**Capabilities and GPU Attachment:**
- Tools become stateful, bound to specific sandbox instances
- [[Capability]] objects bind sets of tools to sandbox instances
- GPU resources can be attached via `ModalSandboxClientOptions`, a unique advantage of [[Modal]]

### Stage 3: Memory and Session Management

**The Problem:** By default, agents are stateless. Each run accepts string context and returns output without accumulating conversation history.

**The Solution:** [[Sessions]] are objects passed across agent runs to accumulate context windows across multiple prompts and agent instances.

**Challenges introduced:**
- **Context management**: Unlimited memory accumulation leads to bloat
- **Context rot**: As context grows, earlier information becomes less relevant and effective
- **Token efficiency**: Larger contexts consume more tokens and slow execution

### Stage 4: Orchestration with Subagents

For long-horizon tasks, a single agent becomes inefficient due to token limitations. The solution is an [[Agent Orchestration]] pattern:

**Architecture:**
- **Orchestrator**: Main chat agent maintaining high-level task memory
- **Subagents**: Fresh agents spawned for focused, brief tasks with clean context windows
- **Tool**: `invoke_subagent` allows the orchestrator to delegate work

**Benefits:**
- Orchestrator remains focused on high-level planning
- Subagents handle implementation details without context bloat
- Subagent sessions are discarded after task completion
- Implementation details stay isolated from main task memory

### Stage 5: Asynchronous Parallel Execution

**The Enhancement:** Rather than blocking orchestrator execution, subagent runs can occur in parallel using a worker pool pattern.

**Implementation:**
- `SubAgentPool` class manages active subagents as key-value pairs
- `invoke_subagent` stores `asyncio.Future` objects instead of blocking
- New tools allow orchestrators to selectively await specific work threads

**Visibility and Coordination:**
- **Hooks**: Track the current active tool for each subagent
- **Status updates**: `set_status` tool allows subagents to report progress without exiting
- **Monitoring**: `list_subagents` tool provides orchestrator visibility into parallel work

### Stage 6: Cost Control with GPU Quotas

With unbounded parallel execution, GPU costs can spiral. A quota system prevents excessive resource consumption:

- **Fixed limits**: Cap the number of expensive GPU instances (e.g., 8x H100s)
- **Resource awareness**: Prevent LLMs from spawning unlimited expensive subagents
- **Budget protection**: Maintain cost predictability in production systems

### Stage 7: Filesystem Snapshots for Deduplication

**The Challenge:** Multiple subagents starting from base sandboxes waste GPU time on redundant setup—pulling repositories, installing dependencies, and configuring environments.

**The Solution:** [[Filesystem Snapshots]] freeze sandbox state into reusable images:

**Benefits:**
- **Time savings**: Subagents branch from known checkpoints rather than starting from scratch
- **Context offloading**: Filesystems serve as implicit memory, separate from session context
- **Artifact persistence**: Code, models, and outputs from prior agents remain available
- **Implicit memory**: Future agents access prior work through the filesystem without explicit context inclusion

**Practical application:** Orchestrator progresses work, snapshots the filesystem, then spawns fresh subagents into that snapshot with minimal instructions.

### Stage 8: Skills Subsystem

A pluggable skills architecture allows orchestrators to selectively opt into specialized context:

- **Modular prompting**: Keep the core harness general-purpose
- **Task-specific context**: Skills plugins provide domain knowledge when needed
- **Composability**: Mix and match skills for different use cases
- **Example**: Parameter Golf-specific prompting without hardcoding into the harness

## Practical Example: Parameter Golf Research

The [[Parameter Golf]] challenge from OpenAI prompts participants to achieve baseline intelligence with minimal model parameters. Using the complete harness architecture:

**Orchestrator capabilities:**
- Spawns three parallel subagents for different ML frameworks
- Manages async task execution without blocking
- Monitors subagent progress via status updates
- Snapshots filesystem checkpoints for branching work
- Applies Parameter Golf-specific skills for domain knowledge

**Result:** Autonomous, parallel GPU-accelerated research running on Modal infrastructure.

## Key Design Principles

### Composability
Systems are built by composing features atop base agent loops. Each addition—memory, orchestration, parallelism, snapshots, skills—layers onto the foundation without replacing it.

### Context Lean, Execution Rich
- **Thin orchestrator context**: High-level planning only
- **Rich execution environment**: Subagents have full access to tools and sandboxes
- **Filesystem as memory**: Off-load context to persistent storage

### Progressive Enhancement
Start simple (basic agent), then incrementally add:
1. Security (sandboxes)
2. Memory (sessions)
3. Scale (orchestration)
4. Parallelism (async workers)
5. Efficiency (snapshots)
6. Specialization (skills)

## Security and Safety Considerations

- **Isolation**: Always run agents in sandboxes, never on the host
- **Guardrails**: Use `ShellTool` and similar safety-focused tools
- **Resource limits**: Implement quotas to prevent runaway execution
- **Monitoring**: Track active agents and resource consumption
- **Gradual trust**: Start with restricted capabilities and expand carefully

## Getting Started

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

**Quick start:**
1. Sign up for [[Modal]] ($30 free monthly compute credits)
2. Clone the example repository
3. Configure OpenAI API credentials
4. Run the orchestrator with Parameter Golf context
5. Monitor parallel subagent execution on GPUs

## Related Technologies

- [[OpenAI API]] - LLM backbone for agents
- [[Modal]] - Compute platform for sandboxes and GPUs
- [[GPU Computing]] - Hardware acceleration for training tasks
- [[Asynchronous Programming]] - Parallel agent execution
- [[Containerization]] - Sandbox isolation mechanism

---

## Metadata

**Source:** Modal Engineering Blog  
**Author:** Erik Dunteman  
**Date:** April 15, 2026  
**Read Time:** 8 minutes  

**Tags:** #agents #openai #modal #sandboxes #gpu #orchestration #parallelism #python #agentic-systems #ll