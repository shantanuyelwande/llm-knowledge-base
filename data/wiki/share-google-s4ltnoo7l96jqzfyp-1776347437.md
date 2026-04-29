---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-29T05:32:30.825261
raw_file_updated: 2026-04-29T05:32:30.825261
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-29T05:32:30.825261
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article describes how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]], a cloud computing platform. The guide progresses from basic agent implementation to a sophisticated parallel research system capable of running GPU-accelerated experiments. Key architectural patterns include [[sandbox]] isolation, [[async programming|asynchronous execution]], memory management, and subagent orchestration.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable [[autonomous agent|autonomous agents]] for coding, research, and task automation. While off-the-shelf solutions like [[Codex]], [[Claude]], and OpenCode provide baseline capabilities, many organizations need to build specialized agent systems tailored to their specific needs.

[[Modal]] provides an ideal platform for hosting these agents through its [[sandbox]] infrastructure and GPU availability. This article demonstrates how to progressively build a sophisticated agent harness capable of parallel task execution, starting from basic implementations and advancing to production-ready patterns.

---

## Core Concepts

### What is an Agent?

An [[AI agent|agent]] is fundamentally a loop that runs an [[Large Language Model|LLM]] with access to tools (functions) until task completion. The collection of tools and state management surrounding this core loop is called a "harness."

### What is a Harness?

A harness encompasses all the infrastructure surrounding the agent loop, providing:
- Tool definitions and execution environments
- State management and memory
- Context management
- Error handling and recovery
- Monitoring and observability

---

## Building Blocks

## Level 1: Basic Local Coding Agent

The simplest implementation provides an agent with an `exec(command)` function to run arbitrary shell commands:

**Key characteristics:**
- Single-threaded execution
- Direct host access (security risk)
- Minimal setup required
- Not suitable for production use

**Security concerns:** Malicious prompts or poor model behavior could compromise the host system.

---

## Level 2: Sandboxed Execution

[[Sandbox|Sandboxes]] are isolated [[Linux]] environments running on [[Virtual Machine|VMs]] or security-hardened containers. Moving agent execution into sandboxes provides crucial isolation.

### Implementation Details

The OpenAI Agents SDK provides:
- **`SandboxAgent`**: Extends the base `Agent` class with sandbox-specific capabilities
- **`ShellTool`**: Adds guardrails to command execution
- **`ModalSandboxSession`**: Client interface to remote sandboxes

### Capabilities Pattern

The SDK uses a "Capability" pattern to bind sets of tools to specific sandbox instances. This allows:
- Stateful tool management
- GPU attachment via `ModalSandboxClientOptions`
- Isolated execution contexts

### Example: Training MNIST

A sandbox-based agent can autonomously:
1. Install dependencies
2. Download datasets
3. Write and execute training code
4. Report results

This works end-to-end with minimal additional configuration.

---

## Level 3: Advanced Harness Features

### Memory Management with Sessions

By default, agents are stateless. The [[OpenAI Agents SDK#Sessions|Session]] pattern accumulates context across multiple agent runs:

**Benefits:**
- Multi-turn conversations
- Persistent memory across agent instances
- Cross-agent state sharing

**Challenges:**
- [[Context rot]]: Memory accumulation causes context bloat
- Token efficiency degradation
- Increased latency

### Subagent Architecture for Orchestration

To handle long-horizon tasks, the harness implements a two-level architecture:

**Orchestrator Agent:**
- Maintains high-level task memory
- Delegates work to subagents
- Manages overall progress
- Keeps context lean

**Subagent:**
- Receives focused task instructions
- Operates with fresh context window
- Completes specific work items
- Returns summary to orchestrator
- Session memory is discarded after completion

**Benefits:**
- Prevents context bloat in long-running tasks
- Enables work parallelization
- Improves token efficiency
- Allows specialized task handling

---

## Level 4: Asynchronous Parallel Execution

### Subagent Pool

Rather than blocking on individual subagent completion, the orchestrator manages multiple parallel subagents using a worker pool pattern:

**Implementation:**
- `SubAgentPool`: Key-value store of active subagents
- `asyncio.Future`: Non-blocking task tracking
- Status monitoring via hooks and status tools

**Tools for orchestration:**
- `invoke_subagent`: Spawn new parallel work
- `list_subagents`: View active subagent status
- `set_status`: Subagent progress updates
- `wait_for_subagent`: Selective completion waiting

**Advantages:**
- Massively increased throughput
- Orchestrator remains responsive
- Natural parallelization of independent tasks

### GPU Cost Management

With unbounded async capability, GPU spending becomes a concern. The harness implements:
- **Quota systems**: Fixed limits on concurrent expensive resources
- **Resource tracking**: Monitor active GPU subagents
- **Graceful degradation**: Queue tasks when quota exceeded

---

## Level 5: Filesystem Snapshots for Deduplication

### The Problem

Multiple subagents starting from base sandboxes waste GPU time repeating:
- Repository cloning
- Dependency installation
- Environment setup

### The Solution: Filesystem Snapshots

[[Filesystem Snapshots|Snapshots]] freeze a sandbox's state into a reusable image:

**Workflow:**
1. Subagent completes setup work
2. Orchestrator creates filesystem snapshot (returns unique ID)
3. Future subagents spawn from snapshot
4. Subagents resume work from known checkpoint

**Benefits:**
- Eliminates duplicate setup work
- Reduces GPU utilization
- Enables work branching from checkpoints
- Provides implicit memory via filesystem state

### Filesystem as Memory

The sandbox filesystem serves as distributed memory:
- **Explicit memory**: Skills and memory files written to disk
- **Implicit memory**: Codebase state reflects prior work
- **Context offloading**: Reduces Session memory pressure
- **Availability**: Accessible to all future subagents

---

## Level 6: Skills Subsystem

The final architectural layer adds pluggable domain knowledge:

**Purpose:**
- Encapsulate task-specific prompting
- Keep core harness general-purpose
- Enable selective context opt-in
- Reduce token usage

**Implementation:**
- Skills plugins provide specialized instructions
- Orchestrator selectively activates relevant skills
- Reduces need for extensive prompting
- Improves task success rates

---

## Real-World Example: Parameter Golf

[[Parameter Golf]] is OpenAI's challenge to achieve baseline intelligence with minimal model parameters.

### Orchestrator Task

The orchestrator receives:
- Challenge description
- Baseline requirements
- Available skills (ML frameworks, optimization techniques)

### Execution Flow

1. **Planning**: Orchestrator decides on parallel approaches
2. **Spawning**: Creates multiple subagents for different strategies
3. **Monitoring**: Tracks progress via `list_subagents`
4. **Checkpointing**: Creates snapshots at key milestones
5. **Branching**: Spawns new subagents from successful snapshots
6. **Iteration**: Continues until baseline achieved

### Results

The system autonomously:
- Trains models on GPUs in parallel
- Explores multiple architectural approaches
- Maintains checkpoints for future work
- Discovers novel efficiency techniques

---

## Key Architectural Patterns

### Pattern 1: Composition Over Monolith

The harness demonstrates that complex systems emerge from composing simple, orthogonal patterns:
- Agents + Sandboxes = Secure execution
- Sandboxes + Sessions = Stateful agents
- Sessions + Subagents = Hierarchical planning
- Subagents + Pools = Parallelization
- Pools + Snapshots = Efficient resource use
- Snapshots + Skills = Domain specialization

### Pattern 2: Context Management

Three complementary mechanisms manage context:

| Mechanism | Purpose | Scope |
|-----------|---------|-------|
| [[Session]] memory | Conversation history | Agent instance |
| Filesystem state | Artifact storage | Sandbox lifetime |
| Snapshots | Checkpoint recovery | Across sandbox instances |

### Pattern 3: Async-First Design

The orchestrator never blocks waiting for subagent completion, enabling:
- Responsive management
- Opportunistic task scheduling
- Better resource utilization

---

## Implementation Considerations

### Security

- Sandboxes provide isolation from host systems
- `ShellTool` adds command guardrails
- GPU quotas prevent resource exhaustion
- Filesystem snapshots preserve known-good states

### Scalability

- Async architecture enables