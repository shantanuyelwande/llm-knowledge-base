---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:17:06.480701
raw_file_updated: 2026-05-02T05:17:06.480701
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:17:06.480701
tags: []
related_topics: []
backlinked_by: []
---
# Building Agents with Modal and OpenAI Agents SDK

## Summary

This article explores how to build custom AI agents using the [[OpenAI Agents SDK]] integrated with [[Modal]] serverless computing platform. It demonstrates a progression from basic coding agents to sophisticated multi-agent systems with parallel execution, memory management, and resource optimization. The guide uses OpenAI's [[Parameter Golf]] challenge as a practical example for building autonomous research agents running on GPUs.

---

## Introduction

The [[OpenAI Agents SDK]], launched in April 2026, provides foundational tools for building agent systems capable of coding, deep research, and complex task automation. Companies like [[Ramp]] have pioneered the use of [[background coding agents]] on Modal, with agents now responsible for over half of their pull requests.

This article demonstrates how to construct a production-ready agent harness from scratch, combining the OpenAI Agents SDK with [[Modal Sandboxes]] to create scalable, parallelizable agent systems. The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

---

## Building the Foundation

### Basic Coding Agent

The simplest agent implementation consists of an [[Agent]] class—essentially a loop running an [[Large Language Model|LLM]] that invokes [[tools]] (functions) to achieve task completion. A "harness" refers to the complete set of tools and state management surrounding this core loop.

A minimal coding agent includes an `exec(command)` function allowing arbitrary shell command execution:

```python
agent = Agent()
agent.add_tool(exec_command)
agent.run("Train a model on MNIST")
```

**Warning:** This approach creates significant security risks with malicious prompts or unreliable models.

### Moving to Sandboxed Environments

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. By executing agent commands within sandboxes, the LLM operates within a confined environment rather than the host system, dramatically improving security.

The OpenAI Agents SDK provides:
- **[[SandboxAgent]]**: An Agent subclass with built-in sandbox integration
- **[[ShellTool]]**: Command execution with additional guardrails
- **[[ModalSandboxSession]]**: Client for managing remote sandbox connections

[[Capabilities]] bind sets of tools to specific sandbox instances. [[GPU]] support can be requested through `ModalSandboxClientOptions`, enabling compute-intensive tasks.

#### Example: Training MNIST

With sandbox integration and GPU support, agents can train models end-to-end:

```python
sandbox_agent = SandboxAgent(
    sandbox_session=ModalSandboxSession(),
    capabilities=[ShellTool()]
)
sandbox_agent.run("Train an image model on MNIST dataset")
```

---

## Advanced Harness Architecture

### Memory and Session Management

By default, [[Agent|Agents]] are stateless—each execution receives only the current input without conversation history. [[Sessions]] solve this problem by accumulating context across multiple agent runs and user interactions.

```python
session = Session()
agent.run("First task", session=session)
agent.run("Follow-up task", session=session)  # Sees previous context
```

**Challenge:** As memory accumulates indefinitely, [[context rot]] becomes problematic. Effective harnesses require intelligent context management and periodic resets.

### Orchestrator and Subagent Pattern

Long-horizon tasks require splitting work between:

- **[[Orchestrator]]**: Main agent maintaining high-level memory and task coordination
- **[[Subagent|Subagents]]**: Specialized agents with fresh context windows for focused tasks

The orchestrator has an `invoke_subagent` tool that spawns subagents with independent [[Session|Sessions]]. Subagents complete focused work and return summaries, keeping orchestrator context lean.

**Benefits:**
- Reduces token overhead from code exploration and debugging output
- Enables context compartmentalization
- Allows work parallelization

### Asynchronous Parallel Execution

Rather than blocking the orchestrator during subagent execution, a [[SubAgentPool]] manages multiple concurrent subagents:

```python
subagent_pool = SubAgentPool()
orchestrator.tools.add(
    invoke_subagent_async,  # Returns asyncio.Future
    list_subagents,
    wait_for_subagent
)
```

**Monitoring mechanisms:**
- **[[Hooks]]**: Track active tools for each subagent
- **`set_status` tool**: Allows subagents to report progress without exiting
- **`list_subagents` tool**: Provides orchestrator visibility into parallel work

### Resource Management with Quotas

Asynchronous execution creates risk of unbounded resource consumption. [[Quota systems]] limit concurrent expensive resources (e.g., GPU instances):

```python
subagent_pool = SubAgentPool(max_gpu_agents=4)
```

This ensures a fixed number of expensive 8x H100 GPUs remain in use.

### Filesystem Snapshots for Checkpoint Management

[[Filesystem Snapshots]] freeze sandbox state into reusable images, eliminating redundant setup work across subagent spawns:

```python
snapshot_id = sandbox_session.create_snapshot()
new_subagent = SubAgent(
    sandbox_image=snapshot_id,
    initial_prompt="Resume from checkpoint: continue optimization"
)
```

**Advantages:**
- Reduces GPU time spent on duplicate setup (dependency installation, repository cloning)
- Provides implicit memory through filesystem state
- Enables work branching from known checkpoints
- Offloads context from [[Session|Sessions]] to disk

### Skills System

A [[Skills]] subsystem allows agents to opt into specialized prompts and context without hardcoding task-specific logic into the harness:

```python
orchestrator.load_skills([
    ParameterGolfSkill(),
    ResearchSkill(),
    OptimizationSkill()
])
```

This maintains harness generality while enabling task-specific capabilities.

---

## Complete System Architecture

The final harness combines all components:

1. **Orchestrator Agent**: Manages high-level strategy and memory
2. **Async Subagent Pool**: Executes parallel focused tasks
3. **Modal Sandboxes**: Provides isolated, GPU-enabled execution environments
4. **Session Management**: Maintains conversation history with context rot mitigation
5. **Filesystem Snapshots**: Enables efficient work resumption
6. **Quota System**: Controls resource consumption
7. **Skills Framework**: Pluggable task-specific capabilities

This architecture enables autonomous research at scale, as demonstrated by the [[Parameter Golf]] challenge implementation.

---

## Key Concepts

### Core Components

- **[[Agent]]**: Loop executing LLM-driven tool invocation
- **[[Harness]]**: Complete tool set and state management around agent loops
- **[[Tool|Tools]]**: Functions agents can invoke to accomplish tasks
- **[[Large Language Model|LLM]]**: Neural network model powering agent decision-making

### Infrastructure

- **[[Modal]]**: Serverless computing platform providing sandboxes and GPU resources
- **[[Sandbox|Sandboxes]]**: Isolated Linux environments for secure agent execution
- **[[GPU]]**: Graphics processing units for compute-intensive tasks
- **[[Filesystem Snapshot|Filesystem Snapshots]]**: Checkpoint mechanism for sandbox state

### Architecture Patterns

- **[[Orchestrator]]**: High-level coordination agent
- **[[Subagent]]**: Specialized focused agent spawned by orchestrator
- **[[Session]]**: Context accumulation across multiple agent runs
- **[[Capability|Capabilities]]**: Bound tool sets for specific sandbox instances
- **[[Skills]]**: Pluggable specialized prompt and capability modules

### Challenges and Solutions

- **[[Context Rot]]**: Degradation of context quality as history accumulates
- **[[Quota]]**: Resource limits preventing unbounded consumption
- **[[Hook|Hooks]]**: Mechanisms for monitoring and observability

---

## Related Topics

- [[OpenAI API]]
- [[Large Language Models]]
- [[AI Agents]]
- [[Autonomous Systems]]
- [[Distributed Computing]]
- [[Machine Learning Operations]]
- [[Parameter Golf]] (optimization challenge)
- [[Code Generation]]
- [[Background Jobs]]

---

## Metadata

**Source:** Modal Engineering Blog  
**Date:** April 15, 2026  
**Author:** Erik Dunteman (Member of Technical Staff, Modal)  
**Read Time:** 8 minutes  
**Repository:** [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

**Tags:** `agents` `openai` `modal` `sandboxes` `gpu` `distributed-systems` `llm`