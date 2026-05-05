---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-05T05:20:33.035208
raw_file_updated: 2026-05-05T05:20:33.035208
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-05T05:20:33.035208
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates progressive development of an agent harness, starting from a basic coding agent and evolving into a sophisticated parallel system capable of managing multiple subagents with [[GPU]] resources, memory management, and context optimization for complex tasks like OpenAI's Parameter Golf challenge.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems. Unlike off-the-shelf solutions such as [[GitHub Copilot|Codex]] or Claude Code, the SDK provides developers with building blocks to create powerful internal agentic tools tailored to specific organizational needs. This guide demonstrates how to integrate the SDK with [[Modal]]'s computing platform to build scalable, parallel agent systems.

The example used throughout this article is OpenAI's [[Parameter Golf]] challenge—a competition focused on achieving baseline intelligence thresholds with minimal model parameters—which showcases how agents can be parallelized across [[GPU]]-equipped environments to discover efficient ML approaches.

---

## Core Concepts

### Agents and Harnesses

An **Agent** is fundamentally a loop that runs an [[Large Language Model|LLM]] to invoke [[function calling|tools]] (functions) until task completion. The collection of tools and state built around this core agent loop is called a **Harness**—the infrastructure that provides context, manages memory, and enables coordination between multiple agents.

### Basic Coding Agent

The simplest implementation uses an `exec(command)` function that allows the agent to execute arbitrary shell commands. While straightforward, this approach poses significant security risks with malicious prompts or unreliable models and is not recommended for production use.

---

## Progressive Development Approach

### Phase 1: Moving to Sandboxes

**[[Sandboxes]]** are isolated Linux environments built on VMs or security-hardened containers. By executing agent commands within sandboxes rather than on the host system, the agent effectively interacts with an isolated environment, significantly improving security.

The OpenAI Agents SDK provides:
- **`SandboxAgent`**: A superset of the basic `Agent` class with preloaded tools for remote sandbox interaction
- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: The client managing the remote sandbox connection

**Capabilities** bind sets of tools to specific sandbox instances. [[Modal]] uniquely allows requesting [[GPU]] resources for sandboxes through `ModalSandboxClientOptions`.

#### Example: Training MNIST

With sandbox capabilities and shell tools configured, agents can execute complete coding tasks end-to-end, such as training image models on the [[MNIST]] dataset with minimal setup.

### Phase 2: Memory and Context Management

#### Sessions

By default, agents are stateless. **Sessions** solve this by accumulating context across multiple agent runs, enabling multi-turn conversations and maintaining state across agent instances.

However, introducing persistent memory creates new challenges:
- **[[Context Rot]]**: The degradation of response quality as context windows grow
- **Context Bloat**: Excessive accumulated information reducing agent efficiency

Solutions focus on protecting primary work threads from unnecessary context accumulation through intelligent context management and strategic resets.

### Phase 3: Orchestration with Subagents

To manage long-horizon tasks and control token usage, agents are split into two specialized roles:

**Orchestrator Agent**
- Maintains high-level memory for entire tasks
- Manages workflow and planning
- Delegates specific work via an `invoke_subagent` tool

**Subagents**
- Receive fresh context windows and clean [[Session|Sessions]]
- Execute focused, short-duration tasks
- Return summarized results to the orchestrator
- Have session memory discarded after completion

This architecture keeps orchestrator context lean while enabling specialized task execution.

### Phase 4: Asynchronous Parallel Execution

Rather than blocking the orchestrator during subagent execution, a **SubAgentPool** enables parallel task management:

- Maintains a key-value set of active subagents
- Stores `asyncio.Future` objects for non-blocking execution
- Provides tools for selective waiting on specific work threads

**Visibility mechanisms** include:
- **[[Hooks]]**: Track current active tools for each subagent
- **`set_status` tool**: Allows subagents to update progress without exiting
- **`list_subagents` tool**: Exposes subagent status to the orchestrator

### Phase 5: Resource Management with Quotas

As asynchronous execution enables unbounded task spawning, **quota systems** limit expensive [[GPU]] resource consumption. This ensures a fixed maximum of high-cost resources (such as 8x [[H100]] GPUs) remain in use simultaneously.

### Phase 6: Filesystem Snapshots

**Filesystem Snapshots** freeze active sandbox states into reusable starting points. This addresses two critical problems:

1. **Deduplication**: Eliminates redundant setup work (repository cloning, dependency installation) across parallel subagents
2. **Context Management**: Offloads memory to persistent filesystems, allowing implicit state preservation

Subagents can branch from known checkpoints, resuming work without context bloat from prior execution steps. The sandbox filesystem acts as implicit memory—artifacts from previous agents remain available even without explicit context window inclusion.

### Phase 7: Skills Subsystem

A **Skills** plugin system allows agents to selectively opt into specialized context and prompting:

- Keeps the core harness general-purpose
- Enables task-specific knowledge injection
- Reduces required prompting for complex challenges like Parameter Golf

---

## Architecture Pattern

The final architecture demonstrates a powerful composition pattern:

```
Orchestrator Agent
├── Maintains task-level memory via Sessions
├── Manages SubAgentPool
├── Monitors parallel work via Hooks and status updates
└── Invokes subagents with branching from Filesystem Snapshots

SubAgentPool
├── Enforces GPU quotas
├── Manages async execution via asyncio.Future
├── Snapshots working states for branching
└── Executes focused tasks in isolated contexts

Sandbox Environment
├── Provides isolated Linux execution
├── Offers GPU resource attachment
└── Enables filesystem persistence
```

---

## Key Advantages

1. **Scalability**: Parallel execution across multiple subagents leverages [[Modal]]'s distributed infrastructure
2. **Context Efficiency**: Orchestrator-subagent separation prevents context bloat in long-horizon tasks
3. **Resource Control**: Quotas prevent runaway [[GPU]] spending from autonomous agent behavior
4. **Composability**: Modular design allows progressive feature addition without core redesign
5. **State Management**: Filesystem snapshots provide checkpointing for resumable work

---

## Implementation Resources

The complete example project is available at: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

Key implementation files demonstrate:
- Basic agent setup and sandbox integration
- Session management and context handling
- Orchestrator-subagent coordination
- Async pool implementation
- Snapshot-based branching
- Skills plugin system

---

## Related Topics

- [[OpenAI Agents SDK]] - The foundational framework
- [[Modal]] - Compute infrastructure platform
- [[AI Agents]] - Autonomous system fundamentals
- [[Large Language Models]] - Core technology
- [[GPU Computing]] - Hardware acceleration
- [[Sandboxes]] - Isolated execution environments
- [[Prompt Engineering]] - Effective agent instruction
- [[Parallel Processing]] - Distributed execution patterns
- [[Memory Management]] - Context and state handling

---

## Metadata

**Source**: Modal Engineering Blog  
**Date**: April 15, 2026  
**Author**: Erik Dunteman (Member of Technical Staff, Modal)  
**Read Time**: 8 minutes  
**Original URL**: https://modal.com/blog/building-with-modal-and-the-openai-agents-sdk

**Tags**: `#agents` `#openai` `#modal` `#llm` `#gpu` `#distributed-systems` `#orchestration` `#sandboxing` `#python`

**Related Articles**:
- How Ramp Built a Full-Context Background Coding Agent on Modal
- OpenAI Agents SDK Launch
- Parameter Golf Challenge