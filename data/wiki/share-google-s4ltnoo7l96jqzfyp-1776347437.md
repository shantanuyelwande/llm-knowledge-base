---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-30T05:36:17.293164
raw_file_updated: 2026-04-30T05:36:17.293164
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-30T05:36:17.293164
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom agent systems using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates a progression from basic coding agents to sophisticated parallel multi-agent systems capable of handling complex tasks like machine learning optimization. The guide covers key architectural patterns including [[agent sandboxing]], [[context management]], [[asynchronous task execution]], and [[filesystem snapshots]] for efficient resource utilization.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and automation tasks. Rather than relying solely on off-the-shelf solutions like Codex or Claude Code, organizations can now construct tailored agent harnesses suited to their specific needs. This article demonstrates how to integrate the OpenAI Agents SDK with [[Modal]]'s compute infrastructure to create scalable, parallel agent systems.

The example presented uses OpenAI's [[Parameter Golf]] challenge—a competition to achieve intelligence thresholds with minimal model parameters—as a practical use case for demonstrating a fully functional agent harness.

## Core Concepts

### Understanding Agent Architecture

An [[Agent]] at its core is a loop containing a large language model (LLM) that invokes tools (functions) to complete tasks. The broader system of tools, state management, and supporting infrastructure surrounding the agent loop is called a "Harness."

**Basic Agent Structure:**
- An LLM decision-making loop
- A set of callable tools/functions
- State management for context
- Execution environment (local or remote)

### Initial Approach: Local Execution

The simplest coding agent implementation provides an `exec(command)` function that allows the LLM to execute arbitrary shell commands. While straightforward, this approach presents significant security risks with malicious prompts or unreliable models.

## Building a Secure Agent Harness

### Moving to Sandboxed Environments

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. By running agent commands within sandboxes rather than on the host system, the LLM operates within a confined environment, preventing damage to production systems.

**Key Components:**
- **SandboxAgent**: An extension of the base Agent class with built-in sandbox integration
- **ShellTool**: Provides guardrails and safety mechanisms for command execution
- **ModalSandboxSession**: Client interface to remotely running sandbox environments

### Adding GPU Capabilities

[[Modal]] enables attaching GPU resources to sandboxes through `ModalSandboxClientOptions`. This allows agents to perform computationally intensive tasks like model training directly within their execution environment.

**Example Use Case:** Training MNIST models with a single prompt, with the agent autonomously managing the complete training pipeline.

## Advanced Harness Features

### Memory and Session Management

By default, agents are stateless—each run operates independently without access to previous interactions. [[Sessions]] solve this limitation by accumulating context across multiple agent runs and user interactions.

**Challenges Introduced:**
- [[Context Rot]]: Accumulated context becomes stale or irrelevant over time
- Context bloat: Memory grows unbounded, consuming tokens and reducing efficiency
- Token limitations: Longer contexts consume more API tokens

### Orchestrator and Subagent Pattern

Complex tasks benefit from a hierarchical agent structure:

**Orchestrator Agent:**
- Maintains high-level task memory
- Makes strategic decisions
- Delegates focused work to subagents
- Remains unencumbered by implementation details

**Subagents:**
- Receive specific, bounded tasks
- Operate with fresh context windows
- Execute work in parallel
- Return summaries rather than full logs

This separation prevents context bloat in the main orchestrator while enabling efficient parallel task execution.

### Asynchronous Task Execution

Rather than blocking the orchestrator while subagents work, [[asynchronous execution]] allows multiple subagents to run in parallel using a worker pool pattern.

**SubAgentPool Implementation:**
- Maintains a key-value store of active subagents
- Uses `asyncio.Future` for non-blocking task invocation
- Provides tools for selective waiting on specific work threads
- Tracks active operations via hooks and status updates

**Visibility Mechanisms:**
- `list_subagents` tool: Shows orchestrator the current state of all subagents
- `set_status` tool: Allows subagents to update progress without exiting
- Hook tracking: Monitors which tool each subagent is currently executing

### Resource Management with Quotas

When agents can spawn unbounded parallel tasks with GPU access, costs can escalate rapidly. A [[quota system]] on the subagent pool enforces hard limits on expensive resources (e.g., maximum concurrent H100 GPUs in use).

### Filesystem Snapshots for Checkpoint-Based Work

[[Filesystem Snapshots]] freeze the state of a sandbox at specific points, creating reusable starting images for new subagents. This approach provides multiple benefits:

**Efficiency Gains:**
- Eliminates redundant setup work (dependency installation, repository cloning)
- Allows subagents to branch from known checkpoints
- Reduces GPU time spent on initialization

**Context Management:**
- Offloads memory from session state to persistent storage
- Implicit memory through filesystem state
- Future agents inherit the working state without explicit context

**Workflow:**
1. Orchestrator progresses work to a checkpoint
2. Filesystem state is captured as a snapshot
3. New subagents spawn from that snapshot with minimal instructions
4. Subagents quickly resume work without context bloat

### Skills and Plugin System

To maintain a general-purpose harness while supporting task-specific optimizations, a [[skills subsystem]] allows the orchestrator to selectively enable specialized prompts and instructions.

**Benefits:**
- Keeps core harness generic and reusable
- Enables task-specific optimizations without hardcoding
- Allows dynamic capability composition
- Simplifies prompt engineering and maintenance

## Practical Example: Parameter Golf Research

The complete example demonstrates these patterns in action:

1. **Single-agent baseline**: Basic MNIST training with one prompt
2. **Sandbox integration**: Secure execution with GPU support
3. **Parallel framework exploration**: Three subagents simultaneously exploring different ML frameworks
4. **Checkpoint-based iteration**: Building on previous work through filesystem snapshots
5. **Autonomous research**: Orchestrator managing parallel optimization experiments

## Key Takeaways

- **Composability**: Agent systems are built by layering capabilities atop core agent loops
- **Context management**: Long-horizon tasks require explicit strategies for memory and token efficiency
- **Parallelization**: Subagent pools enable massive task throughput through asynchronous execution
- **Resource optimization**: Snapshots and quotas prevent cost overruns while improving efficiency
- **Flexibility**: Modular harnesses remain general-purpose while supporting specialized tasks

## Implementation Resources

- **Complete Example Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Modal Platform**: Provides sandboxes, GPU access, and distributed execution infrastructure
- **OpenAI Agents SDK**: Official SDK for building custom agent systems

## Related Topics

- [[OpenAI Agents SDK]]
- [[Modal]] (cloud compute platform)
- [[Large Language Models]]
- [[Agent Orchestration]]
- [[Distributed Computing]]
- [[GPU Computing]]
- [[Context Management in AI]]
- [[Asynchronous Programming]]
- [[Machine Learning Operations]]

---

## Metadata

**Source:** Modal Engineering Blog  
**Date:** April 15, 2026  
**Author:** Erik Dunteman (Technical Staff Member, Modal)  
**Reading Time:** 8 minutes  
**Original URL:** https://share.google/S4lTnOo7l96jQZFyP

**Tags:** `#agents` `#openai` `#modal` `#llm` `#distributed-systems` `#gpu-computing` `#python` `#engineering`

**Related Articles:**
- How Ramp Built a Full-Context Background Coding Agent on Modal
- OpenAI Agents SDK Launch Announcement
- Parameter Golf Challenge