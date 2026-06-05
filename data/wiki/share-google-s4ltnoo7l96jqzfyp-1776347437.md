---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-05T06:30:15.054494
raw_file_updated: 2026-06-05T06:30:15.054494
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-05T06:30:15.054494
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]]'s computing platform. It demonstrates a progressive approach to creating a sophisticated agent harness that leverages [[sandboxes]], [[GPU computing]], and asynchronous task management to enable parallel autonomous research and experimentation.

## Overview

The [[OpenAI Agents SDK]] provides foundational building blocks for constructing agent systems. When combined with [[Modal]]'s infrastructure, it enables teams to build powerful internal tools capable of handling complex, long-horizon tasks with parallel execution across multiple computational resources.

This guide demonstrates building a general-purpose coding agent harness using [[Parameter Golf]] as a practical example, showcasing how to progressively enhance a basic agent loop with advanced features including memory management, parallel task execution, and resource optimization.

## Key Concepts

### Basic Agent Architecture

An **Agent** is fundamentally a loop that executes an [[Large Language Model]] (LLM) with access to tools—functions that the model can invoke to accomplish tasks. The broader system of tools, state management, and context surrounding this core loop is called a **Harness**.

#### Minimal Coding Agent

The simplest implementation provides an `exec(command)` function that allows the agent to run arbitrary shell commands. While functional, this approach presents significant security risks and is not recommended for production use.

### Sandboxes and Security

[[Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. By running agent commands within a sandbox rather than on the host system, the LLM effectively operates within a confined environment, improving security.

#### SandboxAgent

The OpenAI Agents SDK provides a `SandboxAgent` class that extends the base `Agent` with preloaded tools for managing remote sandbox execution. Key features include:

- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client for communicating with remote sandboxes
- **GPU Support**: Capability to request GPU resources via `ModalSandboxClientOptions`

### Harness Development Patterns

Building an effective harness requires careful attention to several architectural concerns:

#### Memory Management with Sessions

By default, agents are stateless. [[Sessions]] solve this by accumulating context across multiple agent runs and user interactions. However, persistent memory introduces new challenges:

- **Context Bloat**: Accumulated memory can grow indefinitely
- **Context Rot**: Long context windows may degrade model performance
- **Context Management**: Strategic pruning and reset mechanisms become necessary

#### Orchestrator and Subagent Pattern

For long-horizon tasks, a two-tier architecture improves efficiency:

- **Orchestrator Agent**: Maintains high-level memory and coordination
- **Subagents**: Execute focused, short-duration tasks with fresh context windows

The orchestrator delegates work via an `invoke_subagent` tool, receiving summaries rather than implementation details. This keeps the orchestrator's context lean while enabling task decomposition.

#### Asynchronous Parallel Execution

Rather than blocking on subagent completion, a **SubAgentPool** enables the orchestrator to manage multiple parallel workers:

- Subagents execute concurrently without blocking the orchestrator
- [[Hooks]] track active tools in each subagent
- A `set_status` tool allows subagents to report progress
- A `list_subagents` tool provides visibility to the orchestrator

#### Resource Management with Quotas

GPU resources can be expensive. A quota system limits the maximum number of concurrent GPU-accelerated subagents, preventing unbounded resource consumption while maintaining parallelism.

#### Filesystem Snapshots

**Filesystem Snapshots** freeze a sandbox's state into a reusable checkpoint, enabling:

- **Deduplication**: Future subagents start from known good states rather than repeating setup work
- **Context Offloading**: Filesystem state serves as implicit memory, reducing session bloat
- **Branching**: Multiple subagents can diverge from the same checkpoint

This is particularly valuable for long-horizon tasks where intermediate progress should be preserved.

#### Skills Subsystem

A pluggable **Skills** system allows the orchestrator to selectively adopt task-specific knowledge without embedding it in the core harness. This maintains generality while enabling specialization for specific challenges like [[Parameter Golf]].

## Practical Example: Parameter Golf Research

The article demonstrates these concepts through building an autonomous research harness for [[Parameter Golf]]—a challenge to achieve baseline intelligence with minimal model parameters.

The complete harness:

1. Starts with a basic agent executing in a sandbox
2. Adds memory via sessions for multi-turn interaction
3. Introduces an orchestrator-subagent pattern for task decomposition
4. Enables parallel subagent execution via a worker pool
5. Implements quotas to control GPU spending
6. Uses filesystem snapshots to avoid redundant setup
7. Adds a skills system for task-specific guidance

This architecture enables the orchestrator to spawn multiple parallel research threads, each exploring different approaches (e.g., different ML frameworks) while maintaining efficient resource utilization and context management.

## Implementation Patterns

### Capability Binding

Stateful tools are bound to specific sandbox instances through **Capabilities**, which group related tools and state together.

### Hook System

[[Hooks]] provide observability into subagent execution, allowing the orchestrator to track which tools are currently active in each worker.

### Context Preservation

Multiple mechanisms work together to manage context:

- **Sessions**: Explicit conversation memory
- **Filesystem State**: Implicit memory via working directory state
- **Snapshots**: Checkpoints for branching and resumption

## Related Concepts

- [[OpenAI Agents SDK]]: Foundation framework for agent development
- [[Modal]]: Infrastructure platform providing sandboxes and GPU resources
- [[Large Language Models]]: Core reasoning engine for agents
- [[AI Agents]]: Broader category of autonomous systems
- [[Parameter Golf]]: Specific challenge for model efficiency optimization
- [[Orchestration]]: Patterns for coordinating multiple agents
- [[Prompt Engineering]]: Technique for guiding agent behavior through skills

## Advantages of This Architecture

- **Scalability**: Parallel subagent execution enables massive throughput
- **Efficiency**: Filesystem snapshots and quotas prevent wasted computation
- **Maintainability**: Modular harness design keeps concerns separated
- **Flexibility**: Pluggable skills system allows task customization
- **Safety**: Sandboxed execution isolates agent operations
- **Generality**: Core architecture applies beyond Parameter Golf

## Getting Started

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

To begin building:

1. Sign up for [[Modal]] ($30 free monthly compute credits)
2. Review the example repository
3. Start with a basic agent and sandbox
4. Progressively add harness features as needed for your use case

## Key Takeaway

Agent systems can be composed from modular building blocks. Rather than adopting monolithic off-the-shelf solutions, teams can construct custom harnesses tailored to their specific requirements by layering capabilities like memory management, parallel execution, resource quotas, and checkpoint systems.

---

## Metadata

**Source**: Modal Blog  
**Author**: Erik Dunteman (Member of Technical Staff, Modal)  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  
**Original URL**: https://share.google/S4lTnOo7l96jQZFyP

**Tags**: `#agents` `#openai` `#modal` `#llm` `#infrastructure` `#parallel-computing` `#gpu` `#system-design`

**Related Topics**: 
- [[OpenAI API]]
- [[Cloud Computing]]
- [[Machine Learning Operations]]
- [[Distributed Systems]]
- [[Agent Orchestration]]
- [[GPU Computing]]

**Example Projects**:
- Parameter Golf Research Harness
- MNIST Training Agent
- Multi-Framework Parallel Experimentation