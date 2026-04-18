---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-18T13:51:29.377956
raw_file_updated: 2026-04-18T13:51:29.377956
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-18T13:51:29.377956
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article describes how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates progressive complexity, starting from a basic coding agent and advancing to a sophisticated parallel research system with memory management, sandbox isolation, and GPU resource optimization.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems. Unlike off-the-shelf solutions such as Codex and Claude Code, the SDK provides building blocks for teams to construct their own agentic systems tailored to specific organizational needs. This article explores how to leverage [[Modal Sandboxes]] to create a scalable, production-ready agent harness capable of parallel task execution across [[GPU]] resources.

The practical example uses OpenAI's [[Parameter Golf]] challenge—a task requiring optimization of model parameters for efficiency—to demonstrate how agents can tackle complex problems and parallelize work across multiple subagents.

## Core Concepts

### What is an Agent?

An agent is fundamentally a loop containing an [[Large Language Model|LLM]] that executes [[tool use|tools]] (functions) to complete tasks. The set of tools and state management surrounding this core loop is called a "harness."

### What is a Harness?

A harness is the complete system built around the agent loop that provides:
- Context and memory management
- Tool definitions and capabilities
- Resource constraints and quotas
- Task orchestration logic

## Building Blocks: From Simple to Complex

### Stage 1: Basic Coding Agent

The simplest agent implementation includes an `exec(command)` function allowing arbitrary shell command execution. While functional, this approach poses significant security risks with malicious prompts or unreliable models.

**Key limitation:** Operates directly on the host system with full access.

### Stage 2: Sandboxed Agent

Security improves dramatically by executing the agent within [[Modal Sandboxes]]—isolated Linux environments running on [[virtual machines]] or hardened containers.

**Key improvements:**
- The LLM operates within an isolated sandbox rather than on the host
- [[ShellTool]] class provides additional guardrails
- [[ModalSandboxSession]] manages the remote sandbox client
- [[Capability|Capabilities]] bind sets of tools to specific sandbox instances
- [[GPU]] resources can be attached via `ModalSandboxClientOptions`

### Stage 3: Memory and Sessions

Default agents are stateless, losing context across multiple interactions. [[Session|Sessions]] solve this by accumulating context across multiple agent runs.

**Challenge introduced:** [[Context rot]]—the degradation of response quality as context windows grow indefinitely.

**Solution:** Implement context management strategies to protect the primary thread of work from context bloat.

### Stage 4: Orchestrator with Subagents

To enable long-horizon work, the system splits into two agent types:

- **Orchestrator Agent:** Maintains high-level memory and task context
- **Subagents:** Operate with fresh context windows for focused, brief tasks

The orchestrator has an `invoke_subagent` tool that spawns subagents with their own [[Session|Sessions]]. Upon completion, subagents return summaries while their detailed context is discarded, keeping the orchestrator's context window lean.

### Stage 5: Asynchronous Subagent Pool

Rather than blocking on subagent completion, a [[SubAgentPool]] enables the orchestrator to manage multiple parallel subagents using [[asyncio]].

**Implementation details:**
- Subagent runs store `asyncio.Future` objects
- New tools allow selective waiting for specific work threads
- [[Hook|Hooks]] track active tools for each subagent
- `set_status` tool enables subagents to update status without exiting

### Stage 6: Resource Management with Quotas

Async capabilities create potential for unbounded GPU resource consumption. A quota system limits expensive resources (e.g., 8x [[H100]] GPUs) to a fixed maximum.

### Stage 7: Filesystem Snapshots

All subagents starting from base sandboxes waste GPU time on redundant setup (repository cloning, dependency installation).

**Solution:** [[Filesystem Snapshot|Filesystem Snapshots]] freeze sandbox state into reusable images, allowing:
- Fresh subagents to branch from known checkpoints
- Reduction in setup overhead
- Implicit memory offloading to disk
- Context management through on-disk artifacts

A subagent can resume work from a snapshot with minimal context, as the filesystem implicitly contains the prior state.

### Stage 8: Skills Subsystem

The final enhancement adds pluggable [[Skill|Skills]]—optional context modules that agents can selectively enable. This keeps the core harness general-purpose while allowing task-specific knowledge to be added as needed.

## Architecture Summary

The complete system architecture flows as follows:

```
User Input
    ↓
Orchestrator Agent (with Session memory)
    ├→ invoke_subagent (async) → Subagent Pool
    ├→ list_subagents (monitoring)
    ├→ set_quota (resource control)
    └→ use_snapshot (checkpoint management)
    
Subagent (with fresh Session)
    ├→ Shell commands (in sandbox)
    ├→ File operations
    ├→ set_status (status updates)
    └→ Access to GPU resources
    
Filesystem Snapshots (persistent state)
    └→ Available to future subagents
```

## Key Advantages of This Approach

| Feature | Benefit |
|---------|---------|
| **Sandbox isolation** | Security and resource containment |
| **Async subagents** | Parallel task execution and higher throughput |
| **Session memory** | Context accumulation across multiple runs |
| **Filesystem snapshots** | Reduced setup overhead and context offloading |
| **Quota system** | Controlled resource consumption |
| **Skills subsystem** | Extensibility without core harness modification |

## Practical Example: Parameter Golf Research

The article demonstrates these concepts through automating OpenAI's [[Parameter Golf]] challenge. The orchestrator can:

1. Spawn parallel subagents for different ML frameworks (TensorFlow, PyTorch, JAX)
2. Each subagent trains models with different parameter optimization strategies
3. Orchestrator monitors progress via `list_subagents`
4. Successful approaches trigger filesystem snapshots
5. Fresh subagents branch from snapshots to explore variations
6. Results accumulate in the orchestrator's session memory

## Implementation Resources

- **Complete example code:** [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Platform:** [[Modal]] (with $30 free compute credits)
- **SDK:** OpenAI Agents SDK (Python)

## Key Takeaways

1. **Composability:** Complex agent systems emerge from composing simple building blocks
2. **Context management:** Long-horizon tasks require careful memory and context handling
3. **Parallelism:** Async subagent pools dramatically increase throughput
4. **Resource efficiency:** Snapshots and quotas prevent runaway costs
5. **Extensibility:** Skills subsystems enable task-specific customization without core modifications

## Related Topics

- [[OpenAI Agents SDK]]
- [[Modal]] (serverless computing platform)
- [[AI Agent Architecture]]
- [[Large Language Models]]
- [[Tool Use in AI]]
- [[Sandbox Security]]
- [[GPU Computing]]
- [[Async Programming]]
- [[Context Window Management]]
- [[Prompt Engineering]]

---

## Metadata

**Source:** Modal Engineering Blog  
**Author:** Erik Dunteman (Member of Technical Staff, Modal)  
**Publication Date:** April 15, 2026  
**Read Time:** 8 minutes  
**Category:** Engineering, AI Systems  

**Tags:** #agents #openai #modal #sandboxes #gpu #python #agentic-systems #orchestration #parallel-computing #llm

**Related Articles:**
- [How Ramp Built a Full Context Background Coding Agent on Modal](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal)
- [OpenAI Agents SDK Launch](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)
- [OpenAI Parameter Golf Challenge](https://openai.com/index/parameter-golf/)