---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-25T04:41:45.014445
raw_file_updated: 2026-04-25T04:41:45.014445
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-25T04:41:45.014445
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to construct sophisticated AI agent systems using [[Modal]] and the [[OpenAI Agents SDK]]. It demonstrates a progression from basic coding agents to a production-grade parallel agent architecture capable of running complex research tasks like [[Parameter Golf]] across multiple GPUs. The guide emphasizes composable harness architecture, context management, and scalable agent orchestration.

## Introduction

[[OpenAI]] recently launched their Agents SDK, providing foundational tools for building [[AI agents|agent]] systems designed for coding, research, and autonomous task completion. This article documents a practical approach to integrating the OpenAI Agents SDK with [[Modal]]'s sandboxing and compute infrastructure to create a general-purpose agent harness capable of parallel execution and long-horizon task planning.

The example implementation uses OpenAI's Parameter Golf challenge—a task requiring optimization of machine learning models under parameter constraints—to demonstrate how agent systems can be scaled across multiple subagents running on [[GPU]] infrastructure.

## Core Concepts

### Agents and Harnesses

An **agent** is fundamentally a loop structure that combines an [[large language model|LLM]] with tool-calling capabilities. The agent iteratively:
1. Receives context and instructions
2. Invokes available tools (functions)
3. Processes results
4. Continues until task completion

A **harness** refers to the broader system architecture surrounding the core agent loop—the set of tools, state management, memory systems, and orchestration logic that enables agents to function effectively for specific domains.

### Sandboxes and Isolation

[[Sandbox|Sandboxes]] are isolated Linux environments built on [[virtual machines]] or security-hardened containers. Using sandboxes provides:
- **Security isolation**: Agents cannot access the host system
- **Environment control**: Reproducible execution contexts
- **Resource management**: GPU allocation and quota enforcement
- **Filesystem persistence**: State preservation across agent runs

Modal's `SandboxAgent` class extends the base `Agent` with:
- `ShellTool`: Command execution with guardrails
- `ModalSandboxSession`: Client management for remote sandboxes
- `ModalSandboxClientOptions`: Configuration for [[GPU]] attachment

### Capabilities and Sessions

**Capabilities** are bindings of tool sets to specific sandbox instances, enabling stateful tool execution. Tools bound to a capability maintain state with their associated sandbox.

**Sessions** provide [[memory management|memory]] across multiple agent runs by accumulating context windows. Without sessions, agents are stateless and cannot maintain multi-turn conversations or task context.

## Building Progressive Complexity

### Stage 1: Basic Local Agent

The simplest agent implementation includes an `exec()` tool allowing arbitrary shell command execution. This approach is unsafe for production use but demonstrates core agent mechanics.

### Stage 2: Sandboxed Execution

Moving agent execution into remote sandboxes provides security isolation. The agent now operates within a contained environment rather than on the host system, mitigating security risks from malicious prompts or model failures.

### Stage 3: Memory and Sessions

Adding session management enables:
- Multi-turn conversations
- Context accumulation across runs
- Task state persistence

However, this introduces **[[context rot]]**—the degradation of agent performance as accumulated context grows stale or irrelevant. Managing context becomes a critical engineering concern.

### Stage 4: Orchestration with Subagents

A two-tier architecture separates concerns:
- **Orchestrator agent**: Maintains high-level task memory and planning
- **Subagents**: Execute focused, short-duration tasks with fresh context windows

The orchestrator spawns subagents via an `invoke_subagent` tool, receiving summaries rather than implementation details. This pattern:
- Keeps orchestrator context lean
- Enables task parallelization
- Allows work delegation with context isolation

### Stage 5: Asynchronous Parallelization

A `SubAgentPool` manages multiple concurrent subagents using [[asyncio]] and [[Future|futures]]. Rather than blocking on subagent completion, the orchestrator can:
- Spawn multiple parallel workers
- Monitor progress via `list_subagents` tool
- Receive status updates without blocking

This requires mechanisms for:
- **Hooks**: Tracking active tools in each subagent
- **Status updates**: Allowing subagents to report progress without exiting
- **Blocking prevention**: Ensuring the orchestrator completes its work

### Stage 6: Resource Quotas

Quota systems limit concurrent resource consumption, preventing unbounded [[GPU]] allocation. This is essential when orchestrators can autonomously spawn workers, as it caps operational costs and prevents resource exhaustion.

### Stage 7: Filesystem Snapshots

**Filesystem snapshots** freeze sandbox state into reusable images, allowing:
- **Deduplication**: New subagents start from checkpoint states rather than base images
- **Context offloading**: Filesystem state serves as implicit memory
- **Work branching**: Multiple subagents can diverge from known-good checkpoints

This pattern treats the filesystem as a [[persistent memory]] layer, complementing session-based context management.

### Stage 8: Skills Subsystem

A pluggable skills system allows agents to selectively opt into domain-specific context and tools. Rather than embedding task-specific prompts in the core harness, skills are:
- Modular and composable
- Selectively enabled by agents
- Kept separate from general-purpose infrastructure

## Key Architectural Patterns

### Context Management Strategy

The architecture manages context across multiple layers:
- **Session memory**: LLM context window for active agent
- **Filesystem memory**: Artifacts and state on disk
- **Snapshot memory**: Checkpoint states for branching work

This multi-layered approach prevents context bloat while maintaining task continuity.

### Parallel Research Pattern

The orchestrator-subagent-pool pattern enables:
1. Orchestrator plans high-level research direction
2. Spawns multiple parallel subagents for independent experiments
3. Receives summaries and status updates
4. Coordinates results and next steps

This mirrors human research team dynamics where a lead researcher directs work across multiple junior researchers.

### Work Checkpointing

Filesystem snapshots enable:
- Saving progress at meaningful points
- Branching experiments from known states
- Reducing redundant setup work
- Implicit memory through filesystem state

## Integration with Modal

[[Modal]] provides several key capabilities for agent harnesses:

- **Sandboxes**: Isolated execution environments with configurable resources
- **GPU attachment**: Direct allocation of [[GPU]] resources to sandbox instances
- **Scalability**: Infrastructure for managing many concurrent sandboxes
- **Cost efficiency**: Pay-per-use pricing for compute resources

The integration allows agents to access powerful computing resources without managing underlying infrastructure.

## Implementation Example: Parameter Golf

The Parameter Golf challenge uses this architecture to:
1. Accept baseline model parameters and efficiency targets
2. Spawn parallel subagents exploring different optimization approaches
3. Train models on [[GPU]]s within subagent sandboxes
4. Compare results and iterate on promising directions
5. Snapshot successful states for branching further experiments

The orchestrator coordinates this research without directly executing code, delegating all implementation details to subagents.

## Related Concepts

- [[OpenAI API|OpenAI]] - Provider of language models and agents framework
- [[Modal]] - Serverless cloud platform for code execution
- [[GPU computing]] - Hardware acceleration for model training and inference
- [[Sandboxing]] - Security isolation technique for untrusted code
- [[Asynchronous programming]] - Concurrent execution patterns
- [[Large language models]] - Foundation for agent intelligence
- [[Tool use|Tool calling]] - Mechanism for agents to invoke functions
- [[Agentic systems]] - Broader category of autonomous agent architectures
- [[Context window]] - LLM input size limitations
- [[Distributed systems]] - Architecture for parallel work coordination

## See Also

- [[Ramp]] - Case study of production agent implementation
- [[Codex]], [[Claude Code]], [[OpenCode]] - Alternative agent frameworks
- [[MNIST]] - Common machine learning benchmark used in examples

## Metadata

**Source:** Modal Engineering Blog  
**Date:** April 15, 2026  
**Author:** Erik Dunteman  
**Read Time:** 8 minutes  

**Tags:** #agents #openai #modal #ai-engineering #gpu #sandboxing #orchestration #parallel-computing #python #llm

**Related Topics:** [[AI agents]], [[Cloud computing]], [[Machine learning operations]], [[Distributed systems]], [[API integration]]

**Repository:** [openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)