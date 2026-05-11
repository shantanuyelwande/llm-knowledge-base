---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-11T06:04:53.825597
raw_file_updated: 2026-05-11T06:04:53.825597
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-11T06:04:53.825597
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agent|AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]], a cloud computing platform. It demonstrates a progressive approach to creating sophisticated agent systems, starting from basic implementations and evolving into a parallel, GPU-accelerated research framework capable of autonomous experimentation.

## Overview

The [[OpenAI Agents SDK]] represents a significant advancement in building customizable [[agent harness|agent harnesses]] for specialized tasks including [[code generation|coding]], research, and experimentation. Unlike off-the-shelf solutions such as Codex and Claude Code, the SDK provides developers with building blocks to construct domain-specific agentic systems tailored to their specific needs.

[[Modal]] provides the infrastructure layer, offering [[sandbox|sandboxes]] and GPU resources that enable agents to safely execute code and perform computationally intensive tasks. This integration creates a powerful platform for scaling agent-based workflows.

## Core Concepts

### What is an Agent?

An [[agent (AI)|agent]] is fundamentally a for-loop with a [[large language model|large language model (LLM)]] that iteratively invokes [[tool use|tools]] (functions) to accomplish tasks. The collection of tools, state management, and supporting infrastructure around this core loop is called a "[[harness]]" or "[[agent harness]]."

### Agent Harnesses

An [[agent harness]] is the complete system surrounding the core agent loop that provides:
- Context and memory management
- Tool definitions and capabilities
- State persistence
- Execution environment configuration

Building an effective harness is often compared to product engineering, as it requires careful design of how the agent will interact with its environment and tools.

## Building a Basic Coding Agent

### The Minimal Implementation

The simplest coding agent includes an `exec(command)` function that allows the [[LLM]] to execute arbitrary shell commands. While straightforward, this approach presents significant security risks and is unsuitable for production use.

### Security and Isolation with Sandboxes

[[Sandbox|Sandboxes]] are isolated Linux environments built on [[virtual machine|virtual machines]] or security-hardened containers. By executing agent commands within sandboxes rather than on the host system, the agent effectively operates within a confined environment.

The OpenAI Agents SDK provides:
- **SandboxAgent**: A specialized agent class with built-in sandbox integration
- **ShellTool**: Enhanced command execution with additional guardrails
- **ModalSandboxSession**: Client for managing remote sandbox connections

#### Attaching GPU Resources

[[Modal]] enables agents to request [[GPU|GPUs]] for their sandboxes through `ModalSandboxClientOptions`, allowing agents to perform compute-intensive tasks such as [[machine learning|machine learning]] model training.

## Advanced Harness Architecture

### Memory and State Management

By default, agents are stateless—each execution receives input and produces output without retaining previous context. This limitation is overcome through **Sessions**.

[[Session|Sessions]] are objects passed across multiple agent runs that accumulate context across:
- Multiple user prompts
- Different agent instances
- Long-horizon task sequences

#### Context Management Challenges

Accumulating memory indefinitely creates **[[context rot]]**—degradation in model performance as the context window becomes cluttered with irrelevant information. Effective harnesses must implement strategies to:
- Prioritize relevant context
- Archive or summarize historical information
- Reset context when appropriate

### Orchestration and Subagents

For complex, long-horizon tasks, a single agent becomes token-heavy as it explores codebases and processes output. The solution is to split work into:

- **Orchestrator Agent**: Maintains high-level memory and planning
- **Subagents**: Spawn fresh agents with clean context windows for focused subtasks

The orchestrator invokes subagents through an `invoke_subagent` tool, receiving only a summary of completed work. This architecture:
- Keeps orchestrator context lean
- Allows focused problem-solving at the subagent level
- Prevents context bloat from implementation details

### Asynchronous Execution and Worker Pools

Rather than blocking orchestrator execution while subagents work, a **SubAgentPool** manages multiple parallel subagents using asynchronous patterns. This enables:
- Non-blocking subagent invocation
- Orchestrator visibility into ongoing work through status updates
- Massive parallelization of independent tasks

#### Monitoring Parallel Work

Two mechanisms provide orchestrator visibility:
1. **Hooks**: Track the current active tool for each subagent
2. **Status Tools**: Allow subagents to provide progress updates without returning to the orchestrator

### Resource Management with Quotas

Since asynchronous patterns allow unbounded subagent spawning, quota systems prevent uncontrolled resource consumption. [[GPU|GPU]] quotas ensure that expensive resources (e.g., 8x [[H100|H100]] accelerators) remain within defined limits.

### Filesystem Snapshots

**Filesystem Snapshots** freeze sandbox state into persistent identifiers, allowing new subagents to branch from known checkpoints. This approach:
- Eliminates redundant setup work (dependency installation, repository cloning)
- Reduces GPU time waste on repeated initialization
- Provides implicit memory through persistent filesystem state

The filesystem acts as an additional memory layer alongside [[session]] state, allowing artifacts from prior agent work to be available to future agents without explicit context inclusion.

### Skills Subsystem

A **skills** plugin system allows agents to selectively opt into specialized context and prompting strategies without embedding task-specific logic into the core harness. This maintains harness generality while enabling domain expertise for specific challenges.

## Practical Example: Parameter Golf

The article demonstrates these concepts through [[OpenAI]]'s [[Parameter Golf]] challenge—an optimization task requiring agents to achieve baseline intelligence thresholds with minimal model parameters.

### Parallel Research Framework

The complete harness enables:
1. Orchestrator agent manages overall research strategy
2. Multiple subagents explore different [[machine learning|ML]] approaches in parallel
3. Filesystem snapshots preserve successful configurations
4. GPU quotas prevent runaway resource consumption
5. Skills plugins provide domain-specific guidance

This architecture allows autonomous, parallel experimentation across multiple approaches simultaneously.

## Key Advantages of the Modal and OpenAI Integration

- **Security**: Sandboxed execution prevents agent access to host systems
- **Scalability**: GPU resources enable computationally intensive agent tasks
- **Parallelism**: Async subagent pools maximize throughput
- **Composability**: Modular harness components can be mixed and matched
- **Flexibility**: General-purpose architecture supports diverse applications

## Related Technologies

- [[OpenAI Agents SDK]]: Core framework for agent development
- [[Modal]]: Cloud computing platform providing sandboxes and GPUs
- [[Large Language Model|Large Language Models]]: The reasoning engine for agents
- [[Tool Use]]: Mechanism for agents to interact with external systems
- [[Agentic Systems]]: Broader field of autonomous agent architectures

## Implementation Resources

- **Complete Example Code**: [GitHub Repository](https://github.com/modal-labs/openai-agents-python-example)
- **OpenAI Agents SDK Documentation**: [Official Docs](https://developers.openai.com/api/docs/guides/agents)
- **Modal Documentation**: [Modal Docs](/docs)

## Getting Started

New users can begin building on Modal with $30 in free monthly compute credits. The platform provides integrated support for the OpenAI Agents SDK with minimal configuration required.

---

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman, Member of Technical Staff  
**Published**: April 15, 2026  
**Read Time**: 8 minutes  

**Tags**: [[AI agents]], [[LLM]], [[cloud computing]], [[GPU computing]], [[agent architecture]], [[OpenAI]], [[Modal]], [[parallel processing]], [[sandboxing]]

**Related Topics**: 
- [[Agentic Systems]]
- [[Large Language Models]]
- [[Cloud Infrastructure]]
- [[Code Generation]]
- [[Machine Learning Operations]]
- [[Distributed Computing]]

**Example Use Cases**:
- Autonomous coding agents
- Parallel research and experimentation
- Model optimization and training
- Background task automation
- Multi-agent coordination systems