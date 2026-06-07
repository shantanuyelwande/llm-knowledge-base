---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:30:59.337654
raw_file_updated: 2026-06-07T06:30:59.337654
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:30:59.337654
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build sophisticated AI agent systems using [[Modal]] infrastructure combined with [[OpenAI Agents SDK]]. It demonstrates a progression from a basic coding agent to a fully-featured parallel research system capable of running complex tasks like OpenAI's Parameter Golf challenge across multiple GPUs. The guide emphasizes composable architecture patterns for agent harnesses, including memory management, subagent orchestration, asynchronous execution, and resource quotas.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and autonomous task execution. Rather than relying solely on off-the-shelf solutions like [[Codex]] or Claude Code, organizations can now build specialized internal agent harnesses tailored to their specific needs.

[[Modal]] provides the ideal infrastructure for these systems, offering isolated computing environments ([[Sandboxes]]), GPU access, and the ability to parallelize agent work at scale. This guide demonstrates how to integrate these technologies to create a production-capable agent orchestration system.

## Core Concepts

### What is an Agent?

An agent is fundamentally a loop that combines:
- An [[Large Language Model|LLM]] decision maker
- A set of callable functions ([[tools]])
- State management for task tracking

The infrastructure and logic surrounding this core loop is called an "[[Agent Harness]]" - it provides context, capabilities, and constraints that shape agent behavior.

### Agent Harness Architecture

A well-designed harness includes:
- **Tools**: Functions the agent can invoke ([[ShellTool]], [[ExecutionTool]])
- **State**: Persistent context across multiple agent runs ([[Sessions]])
- **Capabilities**: Grouped tool sets bound to specific environments ([[Capability|Capabilities]])
- **Safeguards**: Quotas, timeouts, and execution constraints

---

## Building Blocks: From Basic to Advanced

### Stage 1: Basic Local Agent

The simplest agent configuration allows direct execution of shell commands:

```python
agent = Agent()
agent.run("Train an ML model on MNIST")
```

**Limitations**: This approach is unsafe and not recommended for production use, as the agent can execute arbitrary commands on the host system.

### Stage 2: Sandboxed Execution

[[Sandboxes]] provide isolated Linux environments that improve security:

- Agents execute commands in remote, containerized environments
- The agent perceives the sandbox filesystem, not the host
- [[Modal]] provides `ModalSandboxSession` for client management
- [[SandboxAgent]] class simplifies sandbox integration

**Key Advantage**: Complete isolation between agent execution and host systems.

#### GPU-Enabled Sandboxes

[[Modal]] uniquely supports attaching GPUs to sandboxes via `ModalSandboxClientOptions`, enabling:
- GPU-accelerated training and inference
- Parallel experiments on expensive hardware
- Cost-effective resource allocation

### Stage 3: Memory and Sessions

By default, agents are stateless. [[Sessions]] enable:

- **Multi-turn conversations**: Agents remember previous interactions
- **Accumulated context**: Conversation history persists across runs
- **Context management**: Strategic memory handling to prevent [[context rot]]

**Trade-off**: As memory accumulates, token usage increases and context becomes diluted.

### Stage 4: Orchestration with Subagents

Complex tasks benefit from hierarchical agent structures:

#### Orchestrator Agent
- Maintains high-level task context
- Makes strategic decisions
- Spawns and monitors subagents
- Accumulates long-term memory

#### Subagents
- Execute focused, time-limited tasks
- Operate with fresh context windows
- Report summaries back to orchestrator
- Discard detailed execution context after completion

**Benefit**: Keeps orchestrator context lean while enabling complex work delegation.

### Stage 5: Asynchronous Parallel Execution

The [[SubAgentPool]] pattern enables:

- **Non-blocking execution**: Orchestrator spawns multiple subagents without waiting
- **Parallel research**: Multiple experiment threads run simultaneously
- **Throughput scaling**: Increased task completion rate

Key components:
- `asyncio.Future` for tracking pending work
- [[Hooks]] for monitoring active tools in each subagent
- `set_status` tool for subagent progress updates
- `list_subagents` tool for orchestrator visibility

### Stage 6: Resource Management with Quotas

GPU resources are expensive. Quota systems prevent unbounded resource consumption:

```python
# Limit concurrent GPU usage
subagent_pool.set_gpu_quota(max_concurrent_h100s=8)
```

This ensures the system respects budgetary and infrastructure constraints.

### Stage 7: Filesystem Snapshots

[[Filesystem Snapshots]] enable:

- **Work deduplication**: Avoid repeated setup across subagents
- **Checkpoint branching**: Create fresh agents from known-good states
- **Implicit memory**: On-disk artifacts available to future agents
- **Context offloading**: Reduce session memory requirements

**Workflow**:
1. Subagent performs setup and makes progress
2. Filesystem snapshot captures current state
3. New subagents spawn from snapshot with minimal instructions
4. Agents quickly resume work without context bloat

### Stage 8: Skills Subsystem

A modular approach to specialized knowledge:

- Agents selectively opt-in to [[Skills]] plugins
- Keeps core harness general-purpose
- Enables domain-specific prompting without hardcoding
- Supports composable task-specific guidance

---

## Practical Example: Parameter Golf Research

[[Parameter Golf]] challenges participants to achieve baseline intelligence with minimal model parameters. The complete system orchestrates:

1. **Parallel exploration**: Multiple subagents test different approaches simultaneously
2. **Framework diversity**: Different ML frameworks (PyTorch, TensorFlow, JAX) explored in parallel
3. **Intelligent checkpointing**: Filesystem snapshots prevent redundant work
4. **GPU coordination**: Quota system ensures resource availability
5. **Autonomous research**: Orchestrator guides exploration without manual intervention

---

## Key Design Patterns

### Composition Over Monoliths

Rather than building a single complex agent, compose:
- Multiple specialized agents
- Layered capabilities
- Modular tools and skills
- Configurable quotas and constraints

### Context Management

Strategies to prevent [[context rot]]:
- Delegate work to subagents with fresh context
- Use filesystem snapshots for implicit memory
- Implement explicit memory files for important state
- Reset sessions strategically

### Asynchronous Orchestration

Enable parallelism through:
- Non-blocking subagent spawning
- Future-based result tracking
- Periodic status updates
- Selective waiting on critical paths

### Resource-Aware Design

Respect infrastructure constraints:
- GPU quotas prevent overspending
- Filesystem snapshots reduce redundant computation
- Sandbox isolation prevents resource leaks
- Async execution maximizes throughput

---

## Implementation Considerations

### Security

[[Sandboxes]] provide:
- Process isolation
- Filesystem boundaries
- Network segmentation
- Resource limits

Agents cannot escape to the host system or access unintended resources.

### Cost Optimization

- Filesystem snapshots eliminate duplicate setup work
- Async execution maximizes GPU utilization
- Quotas prevent runaway resource consumption
- Subagent context pruning reduces token usage

### Scalability

[[Modal]] infrastructure enables:
- Horizontal scaling of subagent pools
- GPU distribution across availability zones
- Automatic resource provisioning
- Containerized execution for consistency

---

## Getting Started

### Prerequisites
- [[Modal]] account (with $30 free credits available)
- OpenAI API access
- Python environment with OpenAI Agents SDK

### Resources
- **Complete example code**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **OpenAI Agents SDK documentation**: OpenAI official docs
- **Modal documentation**: [modal.com/docs](/docs)

### Deployment
```bash
# Run the complete parallel research system
python orchestrator.py
```

---

## Related Approaches

### Industry Examples

[[Ramp]] built production coding agents on [[Modal]] that now generate over 50% of their pull requests, demonstrating the viability of sophisticated agent systems for real-world software development.

### Comparable Frameworks

- [[Codex]]: Off-the-shelf code generation
- [[Claude Code]]: Anthropic's code execution system
- [[OpenCode]]: Alternative code agent framework

---

## Metadata

**Source**: Modal Engineering Blog (April 15, 2026)  
**Author**: Erik Dunteman, Modal Technical Staff  
**Article URL**: https://share.google/S4lTnOo7l96jQZFyP