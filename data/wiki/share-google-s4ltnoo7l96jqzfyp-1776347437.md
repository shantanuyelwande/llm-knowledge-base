---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-07T05:38:18.886001
raw_file_updated: 2026-05-07T05:38:18.886001
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-07T05:38:18.886001
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] in conjunction with [[Modal]], a cloud computing platform. It demonstrates a progressive approach to building agent harnesses, starting from basic implementations and advancing to sophisticated parallel systems capable of managing multiple concurrent tasks with GPU acceleration. The guide uses OpenAI's Parameter Golf challenge as a practical example.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and autonomous task completion. Unlike off-the-shelf solutions such as Codex and Claude Code, the SDK provides building blocks for teams to develop their own internal agentic systems. When integrated with [[Modal's]] [[Sandbox|Sandboxes]], agents gain access to isolated computing environments with GPU capabilities, enabling scalable parallel processing.

This article documents the journey from a simple local agent to a sophisticated orchestration system capable of managing multiple parallel subagents while maintaining context efficiency and controlling computational costs.

## Core Concepts

### Agents and Harnesses

An **[[Agent]]** is fundamentally a loop that runs an [[Large Language Model|LLM]] to invoke tools (functions) until task completion. The set of tools and state built around this core loop is called a **Harness** — essentially the product engineering layer that makes agents practical and powerful.

The simplest agent implementation includes an `exec()` function allowing arbitrary shell command execution, though this approach poses significant security risks without proper isolation.

### Sandboxes and Security

[[Modal Sandbox|Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. By moving agent execution into sandboxes, the LLM operates within a confined environment rather than on the host system, dramatically improving security.

The [[OpenAI Agents SDK]] provides:
- **SandboxAgent**: A specialized agent class with preloaded sandbox tools
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client interface to remote sandboxes

### Capabilities

**Capabilities** are bindings of tool sets to specific sandbox instances. Since sandbox tools are stateful and bound to particular sessions, capabilities provide a clean abstraction for managing these relationships.

## Building Progressive Complexity

### Stage 1: Basic Local Agent

The minimal viable agent executes shell commands directly on the host. While simple to implement, this approach is unsafe without strict input validation and model quality assurance.

### Stage 2: Sandboxed Execution

Moving execution to remote sandboxes provides isolation. Agents can now be attached to [[GPU]] resources via `ModalSandboxClientOptions`, enabling computationally intensive tasks like MNIST model training.

### Stage 3: Memory and Sessions

By default, agents are stateless. **Sessions** solve this by accumulating context across multiple runs, enabling multi-turn conversations and persistent memory.

**Challenge**: As memory accumulates indefinitely, **[[context rot]]** becomes problematic. Managing context bloat requires strategic memory pruning and reset mechanisms.

### Stage 4: Orchestration with Subagents

To enable long-horizon work while managing token consumption, agents split into two tiers:

- **Orchestrator Agent**: Maintains high-level memory and task coordination
- **Subagents**: Fresh context windows for focused, short-burst tasks

Subagents complete work and return summaries, keeping orchestrator context lean and implementation details isolated.

### Stage 5: Async Parallel Execution

Rather than blocking orchestrator execution, a **SubAgentPool** manages multiple parallel subagents using `asyncio.Future` objects. The orchestrator can:
- Spawn multiple subagents asynchronously
- Monitor progress via hooks and status updates
- Selectively wait for specific work threads to complete

**Tools added**:
- `invoke_subagent`: Spawns parallel work
- `list_subagents`: Monitors active agents
- `set_status`: Allows subagents to report progress

### Stage 6: Resource Management with Quotas

Since async execution grants LLMs the ability to spawn potentially expensive GPU subagents unbounded, quota systems enforce fixed limits on concurrent expensive resources (e.g., 8x H100 GPUs).

### Stage 7: Filesystem Snapshots

With multiple subagents starting from base sandboxes, they redundantly perform setup work (repository cloning, dependency installation). **Filesystem Snapshots** freeze sandbox state into reusable images, allowing fresh subagents to branch from known checkpoints.

**Dual benefits**:
- **Performance**: Eliminates redundant setup work
- **Context Management**: Filesystems serve as implicit memory, offloading context from LLM sessions

### Stage 8: Skills Subsystem

**Skills** are pluggable context modules that orchestrators can selectively opt into, keeping the core harness general-purpose while enabling task-specific expertise. For Parameter Golf, skills provide domain-specific prompting and guidance without hardcoding task logic.

## Advanced Patterns

### Context Management Strategies

Effective agent harnesses employ multiple context layers:

1. **Session Memory**: Explicit conversation history
2. **Filesystem State**: Implicit memory through codebase state
3. **Checkpoint Snapshots**: Frozen system states for branching work

### Parallel Research Architecture

The final harness architecture enables autonomous parallel research:

```
Orchestrator (Main Chat Agent)
├── Subagent Pool (Async Workers)
│   ├── Subagent 1 (Fresh Context)
│   ├── Subagent 2 (Fresh Context)
│   └── Subagent N (Fresh Context)
├── Filesystem Snapshots (Checkpoints)
└── Skills System (Domain Knowledge)
```

### Parameter Golf Implementation

The [[OpenAI]] Parameter Golf challenge serves as the practical example — cramming intelligence into minimal parameters. The parallel harness tackles this by:

1. Spawning multiple subagents with different ML frameworks
2. Running training in parallel on GPUs
3. Sharing checkpoints across experiment branches
4. Accumulating results in orchestrator memory

## Key Takeaways

1. **Composability**: Complex agent systems are built by composing simple building blocks around core agent loops
2. **Context is Expensive**: Parallel subagents with fresh contexts prevent token bloat in long-horizon tasks
3. **Isolation Enables Scale**: [[Modal Sandbox|Sandboxes]] provide the isolation necessary for safe, parallel agent execution
4. **Hybrid Memory**: Combining session memory, filesystem state, and snapshots creates efficient context management
5. **Resource Awareness**: Quota systems prevent runaway costs when agents spawn GPU workloads

## Implementation Resources

- **Complete Example Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Platform**: [Modal](https://modal.com) (includes $30 free monthly compute credits)
- **SDK Documentation**: [OpenAI Agents SDK](https://openai.com/index/the-agents-sdk/)

## Related Examples

- [[Ramp]]: Built background coding agents on Modal responsible for >50% of PRs
- [[Parameter Golf]]: OpenAI efficiency challenge for model compression
- [[MNIST]]: Standard dataset for demonstrating agent training capabilities

---

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman (Member of Technical Staff)  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  
**Original URL**: https://share.google/S4lTnOo7l96jQZFyP

**Tags**: #agents #llm #modal #openai #gpu #parallel-computing #python #orchestration #sandboxes #ai-infrastructure

**Related Topics**:
- [[Large Language Models]]
- [[AI Agent Architecture]]
- [[Cloud Computing Platforms]]
- [[GPU Computing]]
- [[Asynchronous Programming]]
- [[Context Management in LLMs]]
- [[Model Training and Optimization]]