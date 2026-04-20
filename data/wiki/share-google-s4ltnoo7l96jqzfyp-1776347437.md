---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-20T05:18:47.333319
raw_file_updated: 2026-04-20T05:18:47.333319
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-20T05:18:47.333319
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] for scalable, parallel execution. It demonstrates a progression from a basic coding agent to a sophisticated multi-agent system capable of running complex tasks like [[Parameter Golf]] optimization challenges on [[GPU]] infrastructure. The guide emphasizes composable architecture patterns including [[agent orchestration]], [[sandbox|sandboxes]], memory management, and async parallel processing.

---

## Overview

The [[OpenAI Agents SDK]] provides a foundational framework for building agent harnesses—the tools and context that enable [[Large Language Models]] (LLMs) to autonomously complete coding, research, and other complex tasks. When combined with [[Modal]]'s compute infrastructure, particularly its [[Sandbox|Sandboxes]] and [[GPU]] resources, developers can create powerful, scalable systems for autonomous work.

This approach represents a significant shift from using off-the-shelf agent solutions like Codex or Claude Code toward building customized internal agent systems, as demonstrated by companies like [[Ramp]] with their background coding agents.

---

## Core Concepts

### What is an Agent?

An [[AI agent|Agent]] is fundamentally a loop that runs an [[Large Language Model|LLM]] with access to callable tools (functions) until a task reaches completion. The broader ecosystem around this core loop—including tools, state management, memory, and execution environment—is called a "harness."

### The Agent Harness

An agent harness encompasses:
- **Tools**: Functions the agent can invoke
- **State**: Context and memory available to the agent
- **Environment**: The execution context (local, sandboxed, etc.)
- **Capabilities**: Bound sets of tools and resources

---

## Building Progression

### Stage 1: Basic Local Coding Agent

The simplest agent implementation provides an `exec(command)` tool that allows the LLM to run arbitrary shell commands. While functional, this approach poses significant security risks with malicious prompts or unreliable models.

**Key limitation**: Operates on the host system with full access.

### Stage 2: Sandboxed Execution

[[Modal]] provides [[Sandbox|Sandboxes]]—isolated Linux environments running on VMs or security-hardened containers. The [[OpenAI Agents SDK]] includes a `SandboxAgent` class that:

- Manages remote sandbox execution
- Includes a `ShellTool` with built-in guardrails
- Maintains a `ModalSandboxSession` client connection
- Supports [[GPU]] attachment via `ModalSandboxClientOptions`

This approach isolates the agent's execution environment from the host system while maintaining full capability.

### Stage 3: Memory and Sessions

By default, agents are stateless. The [[OpenAI Agents SDK]] provides `Sessions` objects that:

- Accumulate context across multiple agent runs
- Maintain conversation history and state
- Persist across different agent instances
- Enable multi-turn interactions

**Challenge introduced**: [[Context rot]]—the degradation of context quality as memory accumulates indefinitely.

**Solution**: Explicit context management and selective memory reset strategies.

### Stage 4: Orchestration with Subagents

To manage long-horizon tasks while controlling [[context window|context]] bloat, the architecture splits into:

- **Orchestrator Agent**: Main agent maintaining high-level task context and memory
- **Subagents**: Short-lived agents spawned for focused, specific tasks with fresh context windows

The orchestrator has an `invoke_subagent` tool that:
- Creates a new agent with isolated [[Session|Sessions]]
- Returns a summary of work completed
- Keeps orchestrator context lean and focused

This pattern follows [[agent orchestration]] principles.

### Stage 5: Parallel Async Execution

Rather than blocking on subagent completion, a `SubAgentPool` enables:

- Multiple parallel subagents managed by the orchestrator
- Async task execution using `asyncio.Future`
- Non-blocking orchestrator behavior
- Tools for selective waiting on specific work threads

**Visibility mechanisms**:
- **Hooks**: Track active tools in each subagent
- **Status tool**: Allows subagents to report progress without exiting
- **List subagents tool**: Shows orchestrator the state of all active subagents

### Stage 6: Resource Management with Quotas

With unbounded async spawning capability, quota systems become essential to:
- Limit concurrent [[GPU]] usage
- Control expensive resource allocation
- Prevent runaway compute costs
- Maintain predictable resource consumption

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshot|Filesystem Snapshots]] freeze sandbox state into reusable images, enabling:

- **Work deduplication**: Subagents start from pre-configured checkpoints rather than from scratch
- **Reduced setup overhead**: Eliminates redundant dependency installation and repository cloning
- **Implicit memory**: The filesystem acts as persistent memory across agent generations
- **Context offloading**: Complex state can be stored on disk rather than in token-limited context windows

This creates a branching architecture where new subagents can resume work from known good states.

### Stage 8: Skills System

A pluggable skills subsystem allows the orchestrator to selectively opt into specialized knowledge domains via:

- Skill plugins with domain-specific prompts
- Optional context loading
- Generalized harness with specialized capabilities
- Task-specific optimization without core harness modification

---

## Practical Example: Parameter Golf

[[Parameter Golf]] is an [[OpenAI]] challenge to achieve baseline intelligence thresholds with minimal model parameters. The complete harness enables:

1. **Parallel exploration**: Multiple subagents simultaneously explore different ML frameworks
2. **Stateful progression**: Filesystem snapshots preserve working states
3. **Autonomous research**: Orchestrator directs research strategy while subagents implement
4. **GPU optimization**: Efficient resource utilization across multiple parallel experiments
5. **Context management**: Lean orchestrator context despite complex ongoing work

---

## Key Architectural Patterns

### Composition Over Monoliths

The guide emphasizes that agent harnesses are built by composing features around a core agent loop. Each addition (memory, orchestration, async, quotas, snapshots, skills) is independently valuable and can be selectively applied.

### Stateful vs. Stateless Design

- **Stateless components**: Reduce coupling and enable parallelism
- **Stateful components**: Maintain context and enable long-horizon tasks
- **Strategic state placement**: Sessions for conversation, filesystem for artifacts

### Context Economy

Managing token usage through:
- Delegating detailed work to subagents
- Storing artifacts on filesystem rather than context
- Resetting subagent contexts after task completion
- Explicit memory management in orchestrator

### Isolation and Safety

- Sandboxed execution prevents host compromise
- Quota systems prevent resource exhaustion
- Guardrailed tools prevent dangerous operations
- Stateless subagents limit blast radius of failures

---

## Related Technologies

- [[Modal]]: Serverless compute platform providing [[Sandbox|Sandboxes]] and [[GPU]] infrastructure
- [[OpenAI Agents SDK]]: Framework for building agent harnesses
- [[OpenAI API]]: LLM backbone for agent reasoning
- [[Parameter Golf]]: Benchmark task demonstrating parallel agent capabilities
- [[Ramp]]: Real-world implementation of background coding agents

---

## Implementation Considerations

### Getting Started

The complete example implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

### Development Workflow

1. Start with local agents for rapid iteration
2. Move to sandboxes for isolation
3. Add memory via sessions for multi-turn capability
4. Implement orchestration for long-horizon tasks
5. Parallelize with subagent pools
6. Optimize resources with quotas
7. Reduce setup overhead with snapshots
8. Specialize with skills

### Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Security risks | Sandboxed execution |
| Stateless behavior | Session objects |
| Context bloat | Subagent delegation |
| Blocking execution | Async pools |
| Resource exhaustion | Quota systems |
| Redundant setup | Filesystem snapshots |
| Generic capability | Skills plugins |

---

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman, Modal Labs  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  

**Tags**: [[AI agents]], [[LLM]], [[OpenAI]], [[Modal]], [[Sandboxes]], [[GPU computing]], [[Agent orchestration]], [[Async programming]], [[Distributed systems]], [[Machine learning operations]]

**Related Topics**: 
- [[Large Language Models]]
- [[Agentic systems]]
-