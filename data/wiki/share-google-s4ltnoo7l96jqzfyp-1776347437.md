---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-28T05:36:39.101031
raw_file_updated: 2026-04-28T05:36:39.101031
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-28T05:36:39.101031
tags: []
related_topics: []
backlinked_by: []
---
# Building Agents with Modal and OpenAI Agents SDK

## Summary

This article explores how to build custom AI agent systems using [[OpenAI]]'s Agents SDK integrated with [[Modal]]'s computing infrastructure. It demonstrates a progressive approach to agent development, starting with basic coding agents and evolving into a sophisticated parallel agent system capable of managing multiple subagents with [[GPU]] acceleration, memory management, and filesystem snapshots.

---

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building autonomous agent systems. Unlike off-the-shelf solutions such as Codex or Claude Code, the SDK provides developers with the building blocks to create customized agent harnesses tailored to specific organizational needs. This article documents the integration of the Agents SDK with [[Modal Sandboxes]], enabling teams to build scalable, efficient agent systems similar to those deployed by companies like [[Ramp]].

The example implementation tackles [[OpenAI]]'s [[Parameter Golf]] challenge—an optimization competition focused on achieving high model performance with minimal parameters—using a parallel agent architecture running on GPUs.

---

## Core Concepts

### What is an Agent?

An [[Agent]] is fundamentally a loop that runs an [[Large Language Model]] (LLM) with access to tools (functions) until task completion. The collection of tools and state management surrounding the core agent loop is called a **Harness**. The harness is where developers implement the product engineering that makes agents practical and powerful.

### Basic Coding Agent Architecture

The simplest implementation provides an agent with an `exec()` function to run shell commands:

```python
# Minimal unsafe example
agent = Agent()
agent.add_tool(exec_command)
agent.run("write and execute a Python script")
```

**Warning:** This approach is unsafe and not recommended for production use, as it grants unrestricted command execution access to an LLM.

---

## Progressive Development Stages

### Stage 1: Securing with Sandboxes

[[Sandboxes]] are isolated Linux environments built on virtual machines or security-hardened containers. Moving agent execution into a sandbox significantly improves security by preventing direct access to the host system.

The OpenAI Agents SDK provides:
- **`SandboxAgent`**: An extended Agent class with sandbox-specific tools
- **`ShellTool`**: A tool that adds guardrails to command execution
- **`ModalSandboxSession`**: The client managing communication with remote sandboxes

#### GPU Integration

[[Modal]] supports attaching [[GPU]] resources to sandboxes via `ModalSandboxClientOptions`, enabling computationally intensive tasks like model training directly within agent environments.

#### Capabilities

[[Capability|Capabilities]] are mechanisms for binding sets of tools to specific sandbox instances. This pattern enables stateful tool management across agent operations.

### Stage 2: Adding Memory with Sessions

By default, agents are stateless. Each run accepts string input and returns string output, preventing accumulation of conversation history.

[[Session|Sessions]] solve this problem by maintaining context across multiple agent runs:

```python
session = Session()
agent.run(prompt, session=session)
# Context persists across subsequent runs
agent.run(follow_up_prompt, session=session)
```

#### Context Management

As memory accumulates indefinitely, developers must address [[context rot]]—the degradation of conversation quality as context windows grow. This requires strategic context pruning and management.

### Stage 3: Subagent Architecture for Scalability

Coding agents consume significant tokens as they explore codebases and process output. To enable long-horizon work, the system splits into two components:

- **[[Orchestrator]]**: Main agent maintaining high-level task memory and coordination
- **[[Subagent|Subagents]]**: Specialized agents with fresh context windows for focused tasks

The orchestrator has an `invoke_subagent` tool that spawns subagents with independent sessions. Upon completion, subagents return summaries rather than verbose logs, keeping orchestrator context lean.

### Stage 4: Asynchronous Parallel Execution

Rather than blocking orchestrator execution, the system implements a **SubAgentPool**—a key-value store of active subagents enabling parallel work:

```python
# Orchestrator spawns multiple parallel subagents
orchestrator.invoke_subagent("task_1")  # Returns Future
orchestrator.invoke_subagent("task_2")  # Returns Future
orchestrator.invoke_subagent("task_3")  # Returns Future
```

#### Monitoring Parallel Work

Two mechanisms provide visibility into subagent progress:
- **[[Hook|Hooks]]**: Track active tools for each subagent
- **`set_status` tool**: Allows subagents to report progress without exiting

A `list_subagents` tool exposes subagent status to the orchestrator, enabling informed coordination decisions.

#### GPU Quota Management

To prevent unbounded spending on expensive GPU resources, the system implements quota limits:

```python
# Restrict to fixed number of H100 GPUs
subagent_pool.set_quota(max_h100_instances=8)
```

### Stage 5: Filesystem Snapshots for Work Deduplication

As multiple subagents start from base sandbox images, they waste GPU time on redundant setup (repository cloning, dependency installation). **Filesystem Snapshots** freeze a sandbox state into a reusable ID:

```python
# Snapshot working environment
snapshot_id = sandbox.create_snapshot()

# Future subagents start from this checkpoint
new_agent = SandboxAgent(snapshot_id=snapshot_id)
```

#### Implicit Memory Through Filesystems

Filesystems serve as implicit memory layers. Artifacts produced by prior agents remain available to future agents without explicit context inclusion, reducing session bloat while maintaining continuity.

### Stage 6: Skills Subsystem

To maintain harness generality while supporting task-specific knowledge, the system implements a **Skills** plugin architecture:

```python
# Orchestrator selectively enables skills
orchestrator.enable_skill("parameter_golf_optimization")
orchestrator.enable_skill("ml_framework_comparison")
```

Skills provide context and guidance without hardcoding task-specific logic into the core harness.

---

## Complete Architecture: Parallel Auto-Research

The fully developed system combines all components:

1. **Orchestrator** manages high-level task strategy
2. **SubAgentPool** coordinates parallel execution with quota limits
3. **Sandboxes** provide isolated, GPU-accelerated compute environments
4. **Sessions** maintain conversation history while preventing context rot
5. **Filesystem Snapshots** enable efficient work branching from known states
6. **Skills** provide domain-specific guidance

This architecture enables autonomous parallel research on expensive GPU resources while maintaining cost control and context efficiency.

---

## Practical Example: Parameter Golf Research

The [[Parameter Golf]] challenge prompts the system to optimize model performance within strict parameter constraints. The orchestrator might issue:

```
"Compare three approaches to Parameter Golf using PyTorch, TensorFlow, and JAX. 
Run each in parallel, snapshot successful approaches, and iterate on the best one."
```

The orchestrator automatically:
- Spawns three parallel subagents (one per framework)
- Monitors progress via hooks and status updates
- Snapshots working implementations
- Branches future work from successful snapshots
- Aggregates results while keeping its own context manageable

---

## Key Takeaways

1. **Composition over Monoliths**: Build harnesses by composing features around core agent loops
2. **Security First**: Use sandboxes to isolate agent execution
3. **Scalability Through Parallelism**: Subagent pools enable massive throughput
4. **Memory Management**: Balance context retention with context rot prevention
5. **Cost Control**: Implement quotas for expensive resources
6. **Implicit Memory**: Use filesystems as memory layers to reduce token usage

---

## Related Technologies

- [[OpenAI]] - Provider of the Agents SDK and LLM models
- [[Modal]] - Infrastructure platform for sandboxes and GPU compute
- [[Large Language Model]] - Foundation technology for agent reasoning
- [[GPU]] - Accelerated compute resource for training and inference
- [[Parameter Golf]] - Benchmark challenge for model efficiency

---

## Metadata

**Source:** Modal Blog - Engineering  
**Author:** Erik Dunteman, Member of Technical Staff  
**Published:** April 15, 2026  
**Read Time:** 8 minutes  
**Repository:** [github.com/modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

**Tags:** `#agents` `#llm` `#modal` `#openai` `#gpu` `#distributed-systems` `#ai-engineering` `#sandbox` `#orchestration`

**Related Articles:**
- [[How Ramp Built a Full-Context Background Coding Agent on Modal]]
-