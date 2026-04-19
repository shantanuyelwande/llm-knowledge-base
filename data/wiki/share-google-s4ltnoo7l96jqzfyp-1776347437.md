---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-19T04:55:23.114217
raw_file_updated: 2026-04-19T04:55:23.114217
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-19T04:55:23.114217
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom agent harnesses using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates progressive development from a basic coding agent to a sophisticated parallel system capable of managing multiple subagents with GPU resources, context management, and asynchronous task execution.

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in agent-based system development, providing fundamental building blocks for teams to construct customized agentic systems. When combined with [[Modal]]'s serverless compute platform, particularly its [[Sandboxes]] and GPU capabilities, developers can create powerful autonomous research and coding systems that operate at scale.

This guide demonstrates how to progressively build a production-ready agent harness, starting from basic implementation principles and advancing to sophisticated features like parallel execution, memory management, and filesystem snapshots.

## Core Concepts

### What is an Agent Harness?

An agent harness is the complete system architecture surrounding a core agent loop. It comprises:

- **Agent**: A for-loop executing an [[LLM]] running callable tools (functions) to task completion
- **Tools**: Functions that the agent can invoke to perform actions
- **State**: Memory and context management systems
- **Infrastructure**: The underlying compute environment

The harness represents everything beyond the basic agent loop that enables specialized functionality for specific tasks.

## Building Progression

### Stage 1: Basic Coding Agent

The simplest agent implementation includes an `exec(command)` function allowing arbitrary shell command execution. While functional, this approach presents significant security risks and is unsuitable for production use.

**Key limitation**: Direct execution on the host system creates vulnerability to malicious prompts or model failures.

### Stage 2: Sandbox-Based Agent

[[Sandboxes]] provide isolated Linux environments running on VMs or security-hardened containers. The [[OpenAI Agents SDK]] provides:

- **SandboxAgent**: A specialized agent class with preloaded sandbox tools
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client interface to remote sandboxes
- **Capability**: Binds tool sets to specific sandbox instances

**GPU Integration**: [[Modal]] allows GPU attachment to sandboxes via `ModalSandboxClientOptions`, enabling computationally intensive tasks like model training.

### Stage 3: Memory and Sessions

**Problem**: By default, agents are stateless and don't accumulate conversation context across multiple runs.

**Solution**: [[Sessions]] are context-accumulating objects passed across agent runs, enabling:
- Multi-turn conversation memory
- Persistent context across agent instances
- Conversation history maintenance

**Challenge introduced**: [[Context rot]] emerges as memory accumulates indefinitely, requiring intelligent context management strategies.

### Stage 4: Orchestrator and Subagent Architecture

To manage long-horizon tasks and control context bloat:

- **Orchestrator Agent**: Main chat agent maintaining high-level task memory
- **Subagents**: Short-lived agents with fresh context windows spawned for specific tasks
- **invoke_subagent Tool**: Allows orchestrator to delegate work to subagents
- **Benefit**: Subagent context is discarded after task completion, keeping orchestrator memory lean

This architecture separates concerns between high-level planning and implementation details.

### Stage 5: Asynchronous Parallel Execution

**SubAgentPool Implementation**:
- Key-value store of active subagents
- Attached to orchestrator instance
- `invoke_subagent` returns `asyncio.Future` instead of blocking
- Non-blocking orchestrator operation

**Visibility Tools**:
- **Hooks**: Track current active tool for each subagent
- **set_status Tool**: Allows subagents to update status without exiting
- **list_subagents Tool**: Makes subagent status visible to orchestrator

This enables the orchestrator to manage multiple parallel research threads while maintaining awareness of ongoing work.

### Stage 6: Resource Quotas

With asynchronous capabilities, agents can spawn unbounded GPU subagents. A quota system prevents excessive resource consumption by enforcing fixed limits on expensive GPU allocations (e.g., 8x H100s).

### Stage 7: Filesystem Snapshots

**Problem**: Multiple subagents starting from base sandboxes waste GPU time repeating setup work (repository cloning, dependency installation).

**Solution**: Filesystem snapshots freeze sandbox state into an ID that new subagents can use as a starting image, enabling:
- Work branching from known checkpoints
- Significant time savings on repeated setup
- Implicit context management through on-disk memory
- Artifact persistence across subagent generations

**Dual benefit**: Filesystems serve as implicit memory when accessed via shell tools, allowing future agents to access prior work without explicit context inclusion.

### Stage 8: Skills Subsystem

A pluggable skills system allows the orchestrator to selectively opt-in to specialized knowledge domains without bloating the core harness. This maintains generality while enabling task-specific expertise through:
- Optional skill plugins
- Selective context injection
- Modular prompt augmentation

## Practical Example: Parameter Golf

The article demonstrates these concepts through OpenAI's [[Parameter Golf]] challenge—optimizing model intelligence within strict parameter constraints. The complete harness enables:

- Parallel training across multiple ML frameworks
- Autonomous research and experimentation
- GPU-accelerated model training
- Intelligent work distribution and checkpointing

## Architecture Diagram

```
Orchestrator Agent (Persistent Memory)
    ↓
    ├─→ SubAgent Pool (Async Workers)
    │       ├─→ SubAgent 1 (Framework A) [GPU]
    │       ├─→ SubAgent 2 (Framework B) [GPU]
    │       └─→ SubAgent 3 (Framework C) [GPU]
    │
    ├─→ Filesystem Snapshots (Checkpoint Management)
    ├─→ Skills System (Domain Knowledge)
    └─→ Quota Manager (Resource Limits)
```

## Key Technologies

### [[Modal]]
Serverless compute platform providing:
- [[Sandboxes]]: Isolated execution environments
- GPU access and allocation
- Scalable parallel execution
- Filesystem persistence

### [[OpenAI Agents SDK]]
Framework components:
- Base `Agent` class
- `SandboxAgent` for remote execution
- `ShellTool` for safe command execution
- Session management
- Hook system for monitoring

### [[LLM|Large Language Models]]
- OpenAI model integration
- Tool invocation and planning
- Autonomous reasoning

## Best Practices

1. **Security**: Always use sandboxes rather than host execution
2. **Context Management**: Implement aggressive context pruning and filesystem-based memory
3. **Resource Control**: Add quotas for expensive operations
4. **Visibility**: Provide monitoring and status tools for long-running tasks
5. **Modularity**: Use skills and capabilities to keep harnesses composable
6. **Checkpointing**: Leverage filesystem snapshots for work resumption

## Performance Considerations

- **Token Efficiency**: Coding agents are token-heavy; subagent delegation mitigates this
- **GPU Utilization**: Filesystem snapshots reduce redundant setup work
- **Parallel Throughput**: Async subagent pools enable massive parallelization
- **Context Window Management**: Orchestrator separation prevents context explosion

## Related Concepts

- [[Agent Architecture]]
- [[Autonomous Systems]]
- [[Distributed Computing]]
- [[GPU Computing]]
- [[Memory Management in AI]]
- [[Context Window Optimization]]
- [[Model Training]]
- [[Serverless Computing]]

## Resources

- **GitHub Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example) - Complete working implementation
- **Modal Platform**: https://modal.com - Infrastructure provider
- **OpenAI Agents SDK**: Official documentation and API reference
- **Parameter Golf Challenge**: OpenAI optimization challenge

## Metadata

**Source**: Modal Blog  
**Author**: Erik Dunteman  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  

**Tags**: `#agents` `#llm` `#modal` `#openai` `#gpu-computing` `#distributed-systems` `#agent-architecture` `#autonomous-systems` `#infrastructure`

**Related Topics**:
- [[OpenAI Agents SDK]]
- [[Modal Sandboxes]]
- [[Orchestration Patterns]]
- [[Asynchronous Programming]]
- [[GPU Resource Management]]
- [[Context Management in LLMs]]
- [[Autonomous Coding Agents]]