---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:15:53.092773
raw_file_updated: 2026-04-17T20:15:53.092773
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:15:53.092773
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[agent harnesses]] using the [[OpenAI Agents SDK]] integrated with [[Modal]] for serverless computation. It demonstrates a progression from basic coding agents to sophisticated multi-agent systems with parallel execution, GPU support, and memory management capabilities. The example uses OpenAI's Parameter Golf challenge to illustrate building production-grade agentic systems.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable agent systems for coding, research, and automation tasks. Combined with [[Modal]]'s infrastructure, it enables teams to construct powerful internal tools similar to those used by companies like Ramp, which uses background coding agents to generate over half of their pull requests.

This guide walks through building a general-purpose coding harness that can massively parallelize tasks across multiple agents running on [[GPU]] infrastructure, progressing from basic implementations to enterprise-grade systems.

## Core Concepts

### What is an Agent Harness?

An **agent harness** is the complete system surrounding an agent's core loop, including:
- The [[Large Language Model]] (LLM) making decisions
- Available [[tools]] (functions) the agent can invoke
- State management and memory systems
- Context and resource management

The harness is where most product engineering occurs, as it determines how effectively agents can accomplish complex tasks.

### Basic Coding Agent

The simplest implementation is an agent with an `exec(command)` function that can run arbitrary shell commands. While functional, this approach presents significant security risks and is unsuitable for production environments.

## Building Progressively Secure Systems

### Moving to Sandboxes

[[Sandbox|Sandboxes]] are isolated Linux environments built on VMs or security-hardened containers that make agent execution safer. The OpenAI Agents SDK provides:

- **SandboxAgent**: A specialized agent class with preloaded tools for remote sandbox interaction
- **ShellTool**: Adds guardrails to command execution
- **ModalSandboxSession**: Client for managing remote sandbox connections

By running agent commands in sandboxes, the LLM effectively operates within an isolated environment rather than on the host system.

#### GPU Integration

[[Modal]] enables attaching [[GPU]] resources to sandboxes through `ModalSandboxClientOptions`, allowing agents to train models and perform computationally intensive tasks.

## Advanced Harness Architecture

### Memory Management with Sessions

By default, agents are stateless. **Sessions** solve this problem by:
- Accumulating context across multiple agent runs
- Persisting conversation history
- Maintaining state across agent instances

However, sessions introduce new challenges:
- **[[Context Rot]]**: Accumulated context degrades model performance over time
- Context bloat from token-heavy operations
- Need for intelligent context management and resetting

### Orchestrator-Subagent Pattern

To handle long-horizon work while managing context efficiently, harnesses employ a hierarchical structure:

**Orchestrator Agent**
- Maintains high-level task context and memory
- Manages overall strategy and planning
- Delegates focused tasks to subagents
- Remains unconcerned with implementation details

**Subagents**
- Receive specific tasks with fresh context windows
- Have isolated [[Session]] state
- Return summaries rather than detailed logs
- Keep orchestrator context lean and focused

This separation allows agents to work on complex problems without accumulating irrelevant implementation details in the main context window.

### Asynchronous Parallel Execution

Rather than blocking the orchestrator while subagents work, the system can be made asynchronous:

- **SubAgentPool**: Manages multiple active subagents as a key-value set
- **Asyncio Futures**: Store references to parallel work
- **Hooks**: Track active tools and operations in each subagent
- **Status Tools**: Allow subagents to update progress without exiting

This architecture enables the orchestrator to spawn multiple parallel research threads while maintaining control and visibility.

### Resource Management with Quotas

To prevent unbounded resource consumption, quota systems limit:
- Number of concurrent GPU subagents
- Total compute resources in use
- Cost of parallel experimentation

This ensures expensive resources like [[GPU|GPUs]] remain within operational budgets.

### Filesystem Snapshots

**Filesystem Snapshots** freeze a sandbox's state into a reusable image, enabling:

- **Deduplication**: Fresh subagents can branch from known checkpoints rather than repeating setup work
- **Context Offloading**: Filesystems act as implicit memory, reducing context window pressure
- **Artifact Persistence**: Code, models, and data from prior work remain available to future agents
- **Checkpoint-based Branching**: Different research paths can diverge from stable states

This approach combines explicit memory (via Sessions) with implicit memory (via filesystem state).

### Skills and Plugin System

To keep harnesses general-purpose while supporting domain-specific tasks, **Skills** are pluggable components that:
- Provide specialized prompts and instructions
- Enable agents to opt-in to specific capabilities
- Reduce core harness complexity
- Support task-specific optimization

## Practical Example: Parameter Golf

The article demonstrates these concepts using OpenAI's [[Parameter Golf]] challenge, which asks participants to achieve baseline intelligence thresholds with minimal model parameters.

The resulting system:
1. Accepts high-level research goals
2. Spawns parallel subagents on GPUs
3. Each agent explores different approaches (frameworks, architectures, training methods)
4. Uses filesystem snapshots to checkpoint progress
5. Coordinates results through the orchestrator
6. Automatically manages resource quotas and context

## Key Takeaways

1. **Composition is Powerful**: Agent capabilities emerge from composing simple building blocks (sessions, sandboxes, async pools, snapshots)

2. **Context Management is Critical**: As agents accumulate work, managing context becomes essential through memory limits, hierarchical delegation, and filesystem offloading

3. **Infrastructure Enables Scale**: [[Modal]]'s serverless [[GPU]] infrastructure allows agents to parallelize work without manual resource management

4. **Generality vs. Specialization**: Harnesses can remain general-purpose while supporting domain-specific tasks through pluggable skills

## Related Technologies

- [[OpenAI Agents SDK]]
- [[Modal]] (serverless computing platform)
- [[Large Language Models]] (LLMs)
- [[GPU Computing]]
- [[Sandbox Environments]]
- [[Asynchronous Programming]]
- [[Orchestration Patterns]]

## Resources

- **Full Example Repository**: [modal-labs/openai-agents-python-example](https://github.com/modal-labs/openai-agents-python-example)
- **Modal Documentation**: [modal.com/docs](https://modal.com/docs)
- **OpenAI Agents SDK**: [openai.com agents documentation](https://developers.openai.com/api/docs/guides/agents/)
- **Parameter Golf Challenge**: [openai.com/parameter-golf](https://openai.com/index/parameter-golf/)

---

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman (Member of Technical Staff, Modal)  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  

**Tags**: `agents`, `llm`, `openai-sdk`, `modal`, `gpu-computing`, `orchestration`, `parallel-processing`, `agent-harnesses`, `sandboxes`, `infrastructure`

**Related Topics**: [[AI Agents]], [[Large Language Model Applications]], [[Cloud Computing]], [[Distributed Systems]], [[GPU Infrastructure]], [[Serverless Computing]]

**See Also**: [[How Ramp Built a Full-Context Background Coding Agent on Modal]], [[OpenAI Agents SDK]], [[Parameter Golf Challenge]]