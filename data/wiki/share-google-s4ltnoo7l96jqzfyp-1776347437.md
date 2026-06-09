---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-09T06:16:15.693685
raw_file_updated: 2026-06-09T06:16:15.693685
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-09T06:16:15.693685
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|agent harnesses]] using the [[OpenAI Agents SDK]] integrated with [[Modal]], a cloud computing platform. It demonstrates a progression from basic local agents to sophisticated parallel systems capable of managing multiple subagents with [[GPU]] access, using techniques like [[filesystem snapshots]] for context management and work deduplication.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in agent development, providing building blocks for teams to construct custom agentic systems. When integrated with [[Modal's sandbox environment|Modal Sandboxes]], it enables developers to create scalable, isolated agent systems that can leverage distributed computing resources.

This guide demonstrates how [[Modal]] and the OpenAI Agents SDK work together to enable organizations to build internal [[AI agent|agent systems]] similar to those deployed by companies like [[Ramp]], which uses background coding agents to automate more than half of their pull requests.

## Core Concepts

### What is an Agent?

An [[AI agent|agent]] is fundamentally a loop containing an [[large language model|LLM]] that invokes [[function calling|tools (functions)]] to accomplish tasks. The supporting infrastructure around this core loop—including tools, state management, and execution context—is called a **harness**.

### The Agent Harness Architecture

A well-designed harness provides:
- **Tools**: Functions the agent can invoke to interact with its environment
- **State Management**: Memory and context persistence across multiple runs
- **Execution Environment**: Isolated, secure spaces where agents can operate
- **Capabilities**: Bundled sets of tools bound to specific instances

## Building Progression

### Stage 1: Basic Local Agent

The simplest coding agent includes an `exec()` function allowing arbitrary shell command execution. While straightforward, this approach poses significant [[security]] risks when dealing with untrusted prompts or lower-quality models.

```python
# Pseudocode structure
Agent(tools=[exec_command])
```

### Stage 2: Sandboxed Execution

[[Modal Sandboxes]] provide isolated [[Linux]] environments running on VMs or security-hardened containers. The OpenAI Agents SDK offers:

- **SandboxAgent**: A specialized agent class with preloaded sandbox tools
- **ShellTool**: Enhanced command execution with built-in guardrails
- **ModalSandboxSession**: Client interface to remote sandboxes

Agents can be configured with [[GPU]] access through `ModalSandboxClientOptions`, enabling compute-intensive tasks like model training.

### Stage 3: Memory and Sessions

By default, agents are stateless. **Sessions** enable:
- Accumulation of conversation context across multiple runs
- Multi-turn interactions with persistent memory
- Context window management across agent instances

**Challenge**: [[Context rot]] occurs as memory accumulates indefinitely, requiring intelligent context management strategies.

### Stage 4: Orchestration with Subagents

To manage long-horizon tasks and control [[token]] usage, the architecture splits into:

- **Orchestrator Agent**: Main agent maintaining high-level task memory
- **Subagents**: Spawned for focused, short-duration tasks with fresh context windows
- **invoke_subagent Tool**: Allows orchestrator to delegate work while maintaining clean context

This separation enables:
- Implementation details to remain isolated from orchestrator context
- Subagent sessions to be discarded after task completion
- Significant reduction in context bloat

### Stage 5: Asynchronous Parallel Processing

The **SubAgentPool** enables multiple concurrent subagents:

- **Async Execution**: Subagent invocations return `asyncio.Future` objects rather than blocking
- **Worker Pool Pattern**: Key-value store of active subagents
- **Status Tracking**: 
  - **Hooks** monitor active tools in each subagent
  - **set_status Tool** allows subagents to report progress without exiting
  - **list_subagents Tool** gives orchestrator visibility into parallel work

This architecture allows the orchestrator to manage multiple independent research threads simultaneously.

### Stage 6: Resource Management with Quotas

[[GPU]] quota systems prevent unbounded resource consumption by:
- Setting maximum limits on concurrent expensive operations (e.g., 8x [[H100]] instances)
- Allowing the orchestrator to manage resource allocation across subagent spawning
- Preventing runaway costs from parallel agent execution

### Stage 7: Filesystem Snapshots for Work Deduplication

**Filesystem Snapshots** freeze a sandbox session's state into a reusable image, enabling:

- **Checkpoint-based Work**: Subagents can branch from known good states rather than starting from scratch
- **Setup Time Reduction**: Eliminates redundant dependency installation and repository cloning
- **Implicit Memory**: The sandbox filesystem acts as an additional memory layer beyond session context
- **Context Offloading**: Artifacts and code state persist in the filesystem, reducing context window requirements

Fresh subagents can resume work from snapshots with minimal context, understanding their position through the filesystem state.

### Stage 8: Skills Subsystem

A pluggable **skills** architecture allows:
- Selective opt-in to specialized context and prompting
- Harness to remain general-purpose while supporting domain-specific tasks
- Clean separation between core harness and task-specific knowledge

## Practical Example: Parameter Golf

The [[Parameter Golf]] challenge tasks agents with achieving baseline intelligence thresholds using minimal model parameters. The complete harness enables:

1. **Parallel Research**: Multiple subagents explore different ML frameworks and approaches simultaneously
2. **GPU Acceleration**: Each subagent has access to GPU resources for training and optimization
3. **Persistent Progress**: Filesystem snapshots preserve intermediate discoveries
4. **Autonomous Optimization**: The orchestrator manages multiple research threads without manual intervention

## Key Architectural Patterns

### Context Management Strategy

- **Hot Context**: Session memory for active, high-priority information
- **Warm Context**: Filesystem state for recent work and artifacts
- **Cold Context**: Snapshots and checkpoints for historical knowledge

### Orchestrator Responsibilities

- High-level task planning and decomposition
- Subagent lifecycle management
- Resource allocation and quota enforcement
- Progress tracking and status monitoring

### Subagent Responsibilities

- Focused, time-bounded task execution
- Detailed implementation work
- Status reporting and progress updates
- Artifact generation and filesystem updates

## Technical Implementation Details

### Tool Binding with Capabilities

Tools in the sandbox environment are stateful and bound to specific `ModalSandboxSession` instances. The **Capability** pattern groups related tools:

```python
# Conceptual structure
Capability = {
    tools: [ShellTool, FilesystemTool, ...],
    session: ModalSandboxSession
}
```

### Async Orchestration Challenges

Keeping the orchestrator from prematurely exiting while managing async subagents requires deliberate design:
- Explicit synchronization points
- Future management and tracking
- Productive waiting mechanisms (potential "self thought" tools for future development)

## Integration with Modal

[[Modal]] provides:
- **Isolated Execution**: Secure sandboxes preventing agent escape or host compromise
- **GPU Access**: Direct allocation of specialized hardware (H100, A100, etc.)
- **Scalability**: Infrastructure for spawning and managing numerous parallel agents
- **Cost Efficiency**: Pay-per-use model with quota management

## Related Work and References

- **Ramp's Implementation**: Production use of background coding agents handling >50% of PRs
- **OpenAI's Parameter Golf Challenge**: Benchmark task for the example implementation
- **Complete Example Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)

## Conclusion

Building sophisticated agent harnesses involves composing multiple architectural patterns:
1. Start with secure, sandboxed execution
2. Add stateful memory management
3. Implement hierarchical orchestration
4. Enable parallel execution and resource management
5. Optimize through filesystem snapshots
6. Extend with pluggable skills

This composable approach allows teams to build production-grade [[AI agent|agent systems]] tailored to their specific needs, leveraging both the OpenAI Agents SDK and Modal's infrastructure.

---

## Metadata

**Source**: Modal Blog  
**Author**: Erik Dunteman (Member of Technical Staff, Modal)  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  
**Original URL**: https://share.google/S4lTnOo7l96jQZFyP

### Tags

- [[AI Agents]]
- [[OpenAI]]
- [[Modal]]
- [[Large Language Models]]
- [[Agent Architecture]]
- [[GPU Computing]]
- [[Distributed Systems]]
- [[Software Engineering]]
- [[Cloud Computing]]

### Related Topics

- [[Large Language Model