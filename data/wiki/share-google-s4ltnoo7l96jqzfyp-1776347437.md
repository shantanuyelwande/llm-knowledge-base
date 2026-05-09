---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-09T05:27:43.056855
raw_file_updated: 2026-05-09T05:27:43.056855
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-09T05:27:43.056855
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] for serverless computing. It demonstrates progressive enhancement of an agent system, starting from a basic coding agent and evolving into a sophisticated parallel research platform capable of managing multiple subagents with GPU acceleration, context management, and task delegation.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and autonomous task execution. Unlike off-the-shelf solutions such as Codex or Claude Code, the SDK provides building blocks for teams to construct their own agentic systems tailored to specific organizational needs.

[[Modal]], a serverless computing platform, integrates seamlessly with the OpenAI Agents SDK through sandbox extensions, providing agents with isolated computing environments and GPU resources. This combination enables organizations to build sophisticated agent harnesses that can parallelize work across multiple instances while maintaining security and cost efficiency.

---

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop that repeatedly executes:
1. Accepts input from a [[Large Language Model]] (LLM)
2. Invokes available [[Tools]] (functions) based on LLM decisions
3. Processes tool outputs and feeds them back to the LLM
4. Continues until task completion

The set of tools and state management surrounding this core loop is called a "[[Harness]]"—the infrastructure that enables the agent to function effectively.

### The Agent Harness

A harness encompasses:
- **Tools**: Functions the agent can invoke
- **State management**: Memory and context preservation
- **Capabilities**: Bound sets of tools for specific functionality
- **Safety guardrails**: Security constraints and execution limits

---

## Building a Basic Coding Agent

### Minimal Implementation

The simplest coding agent provides an `exec(command)` tool that allows the LLM to execute arbitrary shell commands. While functional, this approach presents significant security risks and is unsuitable for production use.

```python
# Pseudocode example
agent = Agent(
    tools=[ShellTool(exec)]
)
agent.run("Train an MNIST model")
```

### Security Concerns

Direct shell execution on the host machine creates attack surface vulnerabilities:
- Malicious prompts could compromise the system
- Low-quality model outputs may produce destructive commands
- No isolation between agent actions and host resources

---

## Securing Agents with Sandboxes

### Introduction to Sandboxes

[[Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. By executing agent tools within sandboxes, the LLM effectively operates within a confined environment rather than directly on the host system.

### SandboxAgent and Modal Integration

The OpenAI Agents SDK provides:

- **`SandboxAgent`**: An agent class with preloaded sandbox tools
- **`ShellTool`**: Command execution with additional guardrails
- **`ModalSandboxSession`**: Client interface to remote sandboxes
- **`Capability`**: Mechanism for binding tool sets to specific sandbox instances

### Adding GPU Resources

[[Modal]] enables GPU attachment to sandboxes through `ModalSandboxClientOptions`, allowing computationally intensive tasks to leverage specialized hardware:

```python
sandbox_options = ModalSandboxClientOptions(
    gpu="H100",  # Specify GPU type
    memory=40000  # MB
)
```

### Example: MNIST Training

A properly configured sandbox agent can train image models end-to-end with a single prompt, executing all necessary steps within the isolated environment.

---

## Building the Ultimate Harness

Progressive enhancement transforms a basic agent into a sophisticated system capable of complex, long-horizon tasks. The following sections detail key architectural improvements.

### Memory Management with Sessions

#### Problem: Statelessness

By default, agents are stateless. Each run accepts string input and produces string output without retaining conversation history. This prevents multi-turn interactions and long-term task continuity.

#### Solution: Sessions

[[Sessions]] are objects passed across multiple agent runs that accumulate context and conversation history. They enable:
- Multi-turn conversations
- Persistent memory across agent instances
- Shared context in orchestrator-subagent architectures

#### Context Rot Challenge

Indefinite memory accumulation creates new problems:
- **[[Context Rot]]**: Degradation of model performance as context window fills with irrelevant information
- **Token consumption**: Unnecessary API costs from redundant context
- **Attention dilution**: LLM focus scattered across accumulated history

Effective harnesses implement context management strategies to maintain lean, focused memory.

### Orchestrator-Subagent Architecture

#### Motivation

Coding agents consume tokens rapidly while exploring codebases and processing output streams. Single-agent systems have limited effective lifespans for complex, long-horizon tasks.

#### Solution: Hierarchical Delegation

The system splits into two agent types:

**[[Orchestrator]]**
- Main chat agent maintaining overall task memory
- High-level planning and decision-making
- Minimal implementation details in context
- Long operational lifetime

**[[Subagent]]**
- Spawned for focused, short-duration tasks
- Fresh context window and dedicated session
- Executes specific instructions
- Returns work summary to orchestrator
- Session memory discarded after completion

This architecture provides [[Orchestration]] benefits:
- Orchestrator focuses on strategy, not implementation
- Subagents handle tactical execution
- Context remains lean and focused
- Task parallelization becomes possible

### Asynchronous Parallel Execution

#### Blocking vs. Non-Blocking

Sequential subagent invocation blocks the orchestrator, reducing throughput. Asynchronous execution allows the orchestrator to manage multiple parallel subagents simultaneously.

#### SubAgentPool Implementation

A `SubAgentPool` manages multiple concurrent subagents:

**Key features:**
- Key-value store of active subagents
- `asyncio.Future` objects track completion
- Non-blocking orchestrator operation
- Selective waiting for specific work threads

#### Visibility and Status Tracking

With async execution, the orchestrator requires visibility into subagent progress:

- **[[Hooks]]**: Track current active tool for each subagent
- **`set_status` tool**: Allows subagents to report progress without exiting
- **`list_subagents` tool**: Provides orchestrator with real-time status of all workers

### Resource Management with Quotas

#### Problem: Unbounded Costs

Async execution grants LLMs the ability to spawn unlimited GPU subagents, creating uncontrolled infrastructure costs.

#### Solution: Quota System

A quota mechanism enforces fixed limits on expensive resources:
- Maximum concurrent GPU instances (e.g., 8x H100s)
- Prevents runaway resource consumption
- Ensures predictable cost profiles
- Allows orchestrator autonomy within constraints

### Filesystem Snapshots for Work Deduplication

#### Problem: Redundant Setup

Each subagent starting from a base sandbox must repeat setup work:
- Repository cloning
- Dependency installation
- Environment configuration

Over long-horizon tasks, this redundancy consumes substantial GPU time and compute resources.

#### Solution: Filesystem Snapshots

[[Filesystem Snapshots]] freeze sandbox state at specific points:

**Benefits:**
- **Work deduplication**: Fresh subagents start from known checkpoints
- **Branching**: Multiple subagents diverge from common baseline
- **Context offloading**: Implicit memory via filesystem state
- **Recovery**: Return to previous states for alternative approaches

#### Implicit Memory via Filesystem

Sandboxes provide two forms of memory:

1. **Explicit**: Context stored in [[Session]] objects
2. **Implicit**: Artifacts and state in the sandbox filesystem

Subagents accessing a filesystem with prior work already in place can quickly resume, even without explicit context about how that state was created.

### Skills Subsystem for Extensibility

#### Problem: Hardcoded Prompting

Effective agent performance requires task-specific prompting. Embedding this directly in the harness reduces generality.

#### Solution: Skills Plugins

A skills subsystem allows agents to selectively opt into task-specific context:

**Architecture:**
- `Skills` objects encapsulate domain knowledge
- Agents query available skills via `list_skills` tool
- Selective activation based on task requirements
- Keeps core harness general-purpose

**Example**: Parameter Golf challenge context becomes a skill plugin rather than core harness logic.

---

## Practical Example: Parameter Golf Research

### Challenge Overview

OpenAI's [[Parameter Golf]] challenge prompts researchers to achieve baseline intelligence thresholds using minimal model parameters. This requires:
- Architectural innovation
- Hyperparameter optimization
- Training methodology exploration
- Parallel experimentation

### Parallel Multi-Framework Training

The orchestrator can spawn parallel subagents to explore different ML frameworks:

```