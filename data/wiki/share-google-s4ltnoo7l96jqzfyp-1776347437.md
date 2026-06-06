---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-06T06:00:18.419370
raw_file_updated: 2026-06-06T06:00:18.419370
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-06T06:00:18.419370
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article describes how to build custom AI agent systems using [[OpenAI]]'s Agents SDK integrated with [[Modal]] infrastructure. It demonstrates a progression from basic coding agents to sophisticated parallel agent architectures with GPU support, using the [[Parameter Golf]] challenge as a practical example.

---

## Introduction

The [[OpenAI]] Agents SDK represents a significant advancement in building customizable agentic systems. Unlike off-the-shelf solutions such as Codex and Claude Code, teams can now construct their own specialized agent harnesses for internal use. This guide demonstrates how to combine the OpenAI Agents SDK with [[Modal Sandboxes]] to create scalable, parallelized agent systems capable of running on GPU infrastructure.

The example project showcases building a general-purpose coding harness that can tackle complex tasks like parameter optimization while managing multiple parallel subagents efficiently.

---

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop containing a large language model ([[LLM]]) that executes tools (functions) to accomplish tasks. The collection of tools and supporting state architecture surrounding this core loop is called a "[[Harness]]."

### Agent Harness Architecture

A harness comprises everything surrounding the base agent loop, providing context and tools needed for specialized tasks. Building a harness is analogous to product engineering—it remains entirely under programmer control and can be customized extensively using the OpenAI Agents SDK's composable building blocks.

---

## Building Progression

### Stage 1: Basic Coding Agent

The simplest coding agent includes an `exec(command)` function allowing arbitrary shell command execution. While functional, this approach presents severe security risks with malicious prompts or unreliable models.

### Stage 2: Sandboxed Execution

[[Modal Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. Moving agent execution into sandboxes provides critical security isolation.

**Key Features:**
- The `SandboxAgent` class extends base `Agent` with sandbox-specific tools
- `ShellTool` class adds safety guardrails to command execution
- `ModalSandboxSession` manages remote sandbox connections
- `Capability` objects bind tool sets to specific sandbox instances
- [[GPU]] attachment is possible via `ModalSandboxClientOptions`

### Stage 3: Memory and Sessions

By default, agents are stateless. The [[Session]] object solves this limitation by accumulating context across multiple agent runs and user prompts.

**Challenge:** Context management and [[context rot]] become critical concerns as memory accumulates indefinitely. Protecting the primary thread of work from context bloat requires strategic context management.

### Stage 4: Hierarchical Agent Organization

Long-horizon tasks require splitting agents into two roles:

**Orchestrator Agent**
- Maintains memory for the entire task
- Manages high-level planning and coordination
- Has limited concern for implementation details

**Subagent**
- Executes focused, short-duration tasks
- Operates with fresh context window and session
- Returns summarized results to orchestrator
- Session memory is discarded after task completion

This architecture keeps orchestrator context lean while enabling specialized work delegation.

### Stage 5: Asynchronous Parallel Execution

Rather than blocking the orchestrator during subagent execution, a [[SubAgentPool]] enables parallel task management:

**Implementation Details:**
- Key-value storage of active subagents
- Non-blocking `invoke_subagent` tool using `asyncio.Future`
- Tools for selective waiting on specific work threads
- [[Hooks]] for tracking active tools in each subagent
- `set_status` tool for subagent progress updates
- `list_subagents` tool for orchestrator visibility

### Stage 6: GPU Resource Management

With asynchronous capabilities, GPU spending requires explicit quotas to prevent unbounded resource consumption. A quota system ensures fixed limits on expensive hardware (e.g., 8x H100s) in simultaneous use.

### Stage 7: Filesystem Snapshots for Deduplication

[[Filesystem Snapshots]] freeze active sandbox sessions into reusable starting images, eliminating redundant setup work across subagents.

**Benefits:**
- Eliminates duplicate dependency installation and repository setup
- Enables work branching from known checkpoints
- Provides implicit memory via on-disk state
- Reduces context bloat while preserving artifact availability

Sandboxes can be snapshotted after reaching a stable state, allowing future subagents to resume work from that point with minimal instructions.

### Stage 8: Skills Subsystem

A pluggable skills system allows the orchestrator to selectively opt-into domain-specific context through a list of `Skills` plugins. This maintains general-purpose harness design while enabling task-specific optimization through prompting.

---

## Practical Example: Parameter Golf

The [[Parameter Golf]] challenge—fitting baseline intelligence into minimal parameters—serves as the article's worked example. The resulting system:

- Parallelizes experiments across different ML frameworks
- Maintains GPU efficiency through resource quotas
- Leverages filesystem snapshots to avoid redundant setup
- Uses skills plugins for domain-specific optimization
- Orchestrates multiple coding and training tasks autonomously

---

## Key Technical Components

### ModalSandboxSession
Client interface for remote sandbox management, enabling stateful tool execution bound to specific sandbox instances.

### Capability
Binding mechanism for associating tool sets with sandbox instances, enabling organized tool management.

### ShellTool
Safety-enhanced shell command execution with guardrails, replacing unsafe arbitrary `exec()` calls.

### SubAgentPool
Collection management system for parallel subagent execution, supporting async futures and selective waiting.

### Hooks
Monitoring mechanism for tracking active tools across subagent instances, enabling orchestrator visibility.

---

## Design Principles

1. **Composition Over Monolith**: Build systems by composing features on top of base agent loops
2. **Context Efficiency**: Keep primary agent context lean through delegation and summarization
3. **Implicit Memory**: Leverage filesystem state as memory to reduce explicit context requirements
4. **Parallelization**: Take advantage of infrastructure capabilities for throughput maximization
5. **Modularity**: Use skills and capabilities for task-specific customization without modifying core harness

---

## Getting Started

The complete project code is available in the [official Modal Labs repository](https://github.com/modal-labs/openai-agents-python-example).

**Prerequisites:**
- [[OpenAI]] Agents SDK
- [[Modal]] account with GPU access
- Python environment with required dependencies

**Initial Steps:**
1. Start with basic agent implementation
2. Migrate to sandboxed execution
3. Add session-based memory
4. Implement orchestrator/subagent hierarchy
5. Enable async parallel execution
6. Add resource quotas and snapshots
7. Integrate skills system

---

## Related Concepts

- [[OpenAI]] - AI research company providing the Agents SDK
- [[Modal]] - Cloud platform for serverless GPU computing
- [[Large Language Models]] - Foundation for agent decision-making
- [[LLM Tools and Function Calling]] - Mechanism for agent action execution
- [[Agentic Systems]] - Broader category of autonomous AI systems
- [[Prompt Engineering]] - Technique for directing agent behavior
- [[Distributed Computing]] - Architecture pattern for parallel execution
- [[Resource Management]] - GPU quota and allocation systems

---

## Metadata

**Source:** Modal Engineering Blog  
**Published:** April 15, 2026  
**Author:** Erik Dunteman (Member of Technical Staff, Modal)  
**Read Time:** 8 minutes  
**Category:** Engineering, AI/ML Infrastructure

**Tags:** `#agents` `#openai` `#modal` `#gpu` `#sandboxes` `#parallel-computing` `#llm` `#infrastructure`

**Related Articles:**
- How Ramp Built a Full-Context Background Coding Agent on Modal
- OpenAI Agents SDK Launch
- Parameter Golf Challenge

**External Resources:**
- [Modal Documentation](/docs)
- [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [Modal Pricing](/pricing)
- [GitHub Repository](https://github.com/modal-labs/openai-agents-python-example)