---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-10T05:43:28.740615
raw_file_updated: 2026-05-10T05:43:28.740615
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-10T05:43:28.740615
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent]] harnesses using the [[OpenAI Agents SDK]] integrated with [[Modal]] infrastructure. It demonstrates progressive development from a basic coding agent to a sophisticated parallel system capable of running complex tasks like parameter optimization across multiple GPU-enabled sandboxes. The guide emphasizes composable architecture patterns including memory management, subagent orchestration, async parallelization, and filesystem snapshots.

---

## Introduction

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems. Rather than relying solely on off-the-shelf solutions like Codex or Claude Code, teams can now construct their own agentic systems tailored to specific needs. This article demonstrates how to leverage [[Modal]] infrastructure alongside the OpenAI Agents SDK to create scalable, parallel agent harnesses capable of handling complex research and coding tasks.

The example uses OpenAI's [[Parameter Golf]] challenge—a task requiring agents to discover efficient machine learning approaches within strict parameter constraints—as a practical demonstration of the framework's capabilities.

---

## Foundational Concepts

### What is an Agent Harness?

An agent harness is the complete system surrounding a core [[agent loop]]. It includes:

- **Tools**: Functions the agent can invoke to accomplish tasks
- **State management**: Context and memory systems
- **Execution environment**: Where the agent operates
- **Orchestration logic**: Coordination mechanisms for complex workflows

The harness is where most customization occurs, allowing teams to build purpose-specific agent systems.

### The Basic Coding Agent

The simplest implementation uses an `Agent` class with an `exec(command)` function, allowing the agent to run arbitrary shell commands. While straightforward, this approach is inherently unsafe without proper isolation and security measures.

---

## Security and Isolation

### Moving to Sandboxes

[[Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers. By executing agent commands within sandboxes rather than on the host system, you achieve:

- **Security isolation**: Malicious or erroneous commands cannot affect the host
- **Resource limitation**: CPU, memory, and GPU resources can be bounded
- **Clean environments**: Each sandbox can start fresh or from known checkpoints

### SandboxAgent and ShellTool

The OpenAI Agents SDK provides specialized classes for sandbox integration:

- **SandboxAgent**: Extends the base `Agent` class with remote sandbox capabilities
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client for managing remote sandbox connections

### GPU Integration

[[Modal]] uniquely supports GPU attachment to sandboxes via `ModalSandboxClientOptions`, enabling resource-intensive tasks like model training directly within agent execution environments.

---

## Building the Complete Harness

### Memory and Sessions

By default, agents are stateless—each run begins without context from previous interactions. [[Sessions]] solve this by accumulating conversation history and context across multiple agent runs.

**Key Challenge**: Context management and [[context rot]]. As memory accumulates indefinitely, systems must implement strategies to:

- Summarize old context
- Archive completed work
- Reset irrelevant information
- Maintain focus on active tasks

### Orchestration with Subagents

Complex tasks benefit from hierarchical agent structures:

- **Orchestrator Agent**: Maintains high-level task context and strategic decisions
- **Subagents**: Handle focused, short-duration tasks with fresh context windows
- **Delegation**: Orchestrator invokes subagents via `invoke_subagent` tool

This pattern prevents context bloat by:
- Keeping implementation details out of orchestrator memory
- Scrapping subagent sessions after task completion
- Returning only task summaries to the orchestrator

### Asynchronous Parallel Execution

The harness can be enhanced to run multiple subagents in parallel using:

- **SubAgentPool**: Manages multiple concurrent subagent instances
- **asyncio.Future**: Non-blocking subagent invocation
- **Status tracking**: Hooks and `set_status` tools for monitoring progress

This architecture allows the orchestrator to spawn multiple parallel research threads while maintaining responsiveness.

### Resource Management with Quotas

When subagents can spawn GPU resources, cost control becomes critical. Quota systems limit the number of expensive resources (e.g., 8x H100 GPUs) in simultaneous use, preventing unbounded resource consumption.

### Filesystem Snapshots

Filesystem snapshots freeze the state of an active sandbox, creating reusable starting points for new subagents. Benefits include:

- **Deduplication**: Avoid redundant setup work across parallel tasks
- **Checkpointing**: Branch work from known-good states
- **Implicit memory**: On-disk artifacts serve as context for future agents
- **Context management**: Offload memory to filesystem rather than token budgets

### Skills Subsystem

Rather than embedding task-specific prompts into the core harness, a [[skills]] plugin system allows orchestrators to selectively opt into specialized context. This maintains generality while enabling specialization.

---

## Complete Example: Parameter Golf

The article demonstrates a fully functional system that:

1. **Initializes** an orchestrator agent with sandbox capabilities
2. **Spawns** multiple parallel subagents for different approaches (e.g., different ML frameworks)
3. **Monitors** subagent progress via hooks and status tools
4. **Checkpoints** successful work using filesystem snapshots
5. **Branches** new subagents from checkpoints with focused follow-up tasks
6. **Applies** specialized skills for Parameter Golf optimization
7. **Manages** GPU quotas to control costs
8. **Accumulates** results across parallel experiments

This system runs entirely on [[Modal]] infrastructure, leveraging its sandbox platform for isolation and GPU support.

---

## Key Architectural Patterns

| Pattern | Purpose | Implementation |
|---------|---------|-----------------|
| **Orchestrator/Subagent** | Hierarchical task decomposition | Separate agent instances with delegation |
| **Session Management** | Multi-turn memory | Context accumulation with rotation |
| **Async Pools** | Parallel execution | asyncio with Future-based subagent spawning |
| **Filesystem Snapshots** | State persistence | Checkpoint and restore sandbox state |
| **Quota Systems** | Resource control | Limit concurrent expensive resources |
| **Skills Plugins** | Specialization | Selective context injection |
| **Hook-based Monitoring** | Observability | Track active tools and status updates |

---

## Implementation Considerations

### Context Management
- Implement aggressive summarization strategies
- Use filesystem storage for large artifacts
- Rotate old context out of active sessions
- Consider specialized "thinking" tools for planning

### Subagent Lifecycle
- Keep individual subagent contexts lean
- Return only relevant summaries to orchestrator
- Clean up resources after task completion
- Use snapshots to preserve intermediate progress

### Scaling Considerations
- Monitor token consumption across parallel agents
- Implement early stopping for unproductive threads
- Balance parallelism against context coherence
- Use quotas to prevent resource exhaustion

---

## Related Technologies

- [[OpenAI Agents SDK]]: Core agent framework
- [[Modal]]: Infrastructure for sandboxes and GPU computing
- [[Sandboxes]]: Isolated execution environments
- [[LLM]] (Large Language Models): Agent decision-making engine
- [[Parameter Golf]]: Example optimization challenge
- [[Ramp]]: Real-world implementation reference (background coding agents)

---

## Practical Applications

This architecture is particularly suited for:

- **Autonomous research**: Running parallel experiments with different hypotheses
- **Code generation**: Multi-approach coding with checkpoint-based branching
- **Model optimization**: Distributed hyperparameter search
- **Background task automation**: Long-running work without blocking main threads
- **Custom agent systems**: Any domain requiring specialized agent behavior

---

## Getting Started

The complete implementation is available in the [Modal Labs GitHub repository](https://github.com/modal-labs/openai-agents-python-example).

To begin:

1. Set up a [[Modal]] account (includes $30 free monthly credits)
2. Review the example repository structure
3. Start with a basic sandbox agent
4. Progressively add features (memory, subagents, parallelization)
5. Integrate domain-specific skills as needed

---

## Metadata

**Author**: Erik Dunteman (Member of Technical Staff, Modal)

**Published**: April 15, 2026

**Read Time**: 8 minutes

**Source**: Modal Engineering Blog

**Tags**: `#agents` `#openai` `#modal` `#sandboxes` `#gpu-computing` `#llm` `#orchestration` `#parallel-computing` `#agentic-systems`

**Related Articles**:
- [[How Ramp Built a Full-Context Background Coding Agent on Modal]]
- [[