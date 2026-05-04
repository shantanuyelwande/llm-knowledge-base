---
title: share-google-S4lTnOo7l96jQZFyP-1776347437
source_file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
source_url: https://share.google/S4lTnOo7l96jQZFyP
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-04T05:41:13.349466
raw_file_updated: 2026-05-04T05:41:13.349466
version: 1
sources:
  - file: share-google-S4lTnOo7l96jQZFyP-1776347437.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-04T05:41:13.349466
tags: []
related_topics: []
backlinked_by: []
---
# Building with Modal and the OpenAI Agents SDK

## Summary

This article explores how to build custom [[AI agents]] using the [[OpenAI Agents SDK]] integrated with [[Modal]], a cloud platform for running code at scale. It demonstrates a progression from basic coding agents to sophisticated multi-agent systems with parallel execution, GPU acceleration, and context management capabilities.

## Overview

The [[OpenAI Agents SDK]] provides powerful building blocks for creating agent harnesses—systems that enable [[large language models]] (LLMs) to autonomously execute tasks through tool use. When combined with [[Modal]]'s [[sandboxes]] and GPU infrastructure, teams can build production-grade internal agent systems similar to those deployed by companies like [[Ramp]].

This guide walks through constructing a complete agent harness from scratch, using OpenAI's [[Parameter Golf]] challenge as a practical example. The system demonstrates how to parallelize tasks across multiple GPU-accelerated agents while maintaining context efficiency and cost control.

## Core Concepts

### What is an Agent?

An [[agent]] is fundamentally a loop that:
1. Accepts input context
2. Runs an [[LLM]] to decide which tools to invoke
3. Executes those tools (functions)
4. Repeats until task completion

The collection of tools and supporting infrastructure around this core loop is called a **harness**.

### The Agent Harness

A harness provides agents with:
- **Tools**: Functions the agent can invoke
- **State**: Memory and context across runs
- **Capabilities**: Sets of related tools bound to specific resources
- **Constraints**: Limits on resource usage and behavior

## Building Progression

### Stage 1: Basic Coding Agent

The simplest agent implementation provides an `exec()` function allowing arbitrary shell command execution:

```python
agent = Agent(
    tools=[
        {
            "name": "exec",
            "description": "Execute a shell command",
            "function": lambda cmd: subprocess.run(cmd, shell=True)
        }
    ]
)
```

**Warning**: This approach is unsafe and vulnerable to malicious prompts or model errors.

### Stage 2: Sandboxed Execution

[[Modal Sandboxes]] are isolated Linux environments running on VMs or security-hardened containers. Moving agent execution into sandboxes provides:

- **Security isolation**: The LLM interacts with a sandbox, not the host system
- **Resource control**: GPU attachment and memory limits
- **Reproducibility**: Consistent environments across runs

The [[OpenAI Agents SDK]] provides `SandboxAgent` class and `ShellTool` with built-in guardrails:

```python
from modal import Sandbox
from openai.agents.sandbox import SandboxAgent, ShellTool

agent = SandboxAgent(
    tools=[ShellTool()],
    sandbox=ModalSandboxSession()
)
```

**GPU Integration**: [[Modal]] enables GPU attachment to sandboxes via `ModalSandboxClientOptions`, allowing agents to run compute-intensive tasks like model training.

### Stage 3: Multi-Turn Memory with Sessions

By default, agents are stateless. [[Sessions]] accumulate conversation context across multiple runs:

```python
session = Session()
response = agent.run(
    "Train a model on MNIST",
    session=session
)
```

**Challenge**: [[Context rot]] emerges as memory accumulates indefinitely, requiring active context management and strategic resets.

### Stage 4: Orchestrator and Subagent Architecture

For long-horizon tasks, a two-tier architecture prevents context bloat:

- **Orchestrator**: Main agent maintaining high-level task memory
- **Subagents**: Fresh agents spawned for focused subtasks with isolated [[sessions]]

The orchestrator invokes subagents through an `invoke_subagent` tool, receiving only summaries of completed work rather than implementation details. This keeps the orchestrator's context window lean while enabling complex multi-step reasoning.

### Stage 5: Asynchronous Parallel Execution

A `SubAgentPool` manages multiple concurrent subagents, allowing the orchestrator to:
- Spawn parallel work without blocking
- Monitor progress via `list_subagents` tool
- Coordinate results asynchronously

```python
class SubAgentPool:
    active_agents: dict[str, asyncio.Future]
    
    async def invoke_parallel(self, tasks: list[str]):
        futures = {}
        for task in tasks:
            futures[task_id] = asyncio.create_task(
                self.spawn_subagent(task)
            )
        return futures
```

**Benefits**: 
- Higher throughput for parallel experiments
- Efficient GPU utilization
- Flexible work distribution

### Stage 6: GPU Cost Management

[[Quotas]] prevent unbounded resource consumption:

```python
pool = SubAgentPool(
    max_concurrent_gpus=8,  # Limit expensive H100 instances
    gpu_type="h100"
)
```

This ensures predictable infrastructure costs while maintaining parallelism.

### Stage 7: Filesystem Snapshots for Work Deduplication

[[Filesystem Snapshots]] freeze a sandbox's state into a reusable image, enabling:

- **Work branching**: Spawn new agents from known checkpoints
- **Time savings**: Skip redundant setup (dependency installation, repo cloning)
- **Implicit memory**: Filesystem artifacts available to future agents without explicit context

```python
# Snapshot after successful setup
snapshot_id = sandbox.create_snapshot()

# Later: spawn new agent from snapshot
new_agent = SubAgent(
    sandbox=Sandbox.from_snapshot(snapshot_id)
)
```

This approach separates **explicit memory** (context windows) from **implicit memory** (filesystem state), enabling efficient context management.

### Stage 8: Skills Subsystem

[[Skills]] are pluggable modules that extend agent capabilities without modifying core harness code:

```python
agent.load_skills([
    ParameterGolfSkill(),
    ResearchSkill(),
    CodeOptimizationSkill()
])
```

Benefits:
- Keep harness general-purpose
- Customize behavior per task
- Reduce core prompt complexity

## Advanced Patterns

### Context Management Strategies

1. **Session rotation**: Clear context periodically to prevent rot
2. **Filesystem offloading**: Store working state on disk
3. **Hierarchical context**: Orchestrators maintain summaries; subagents handle details
4. **Snapshot branching**: Use filesystem state as implicit memory

### Monitoring and Observability

- **Hooks**: Track current tool execution for each subagent
- **Status updates**: Subagents report progress without exiting
- **List operations**: Orchestrator queries active subagent state

### Orchestration Patterns

- **Sequential**: Wait for task completion before proceeding
- **Parallel**: Spawn multiple independent tasks
- **Conditional**: Branch based on intermediate results
- **Hierarchical**: Multi-level orchestrator-subagent relationships

## Practical Example: Parameter Golf

The guide demonstrates these concepts through [[Parameter Golf]], a challenge to achieve baseline model intelligence with minimal parameters.

The complete system:
1. **Orchestrator** plans experimental approaches
2. **Subagents** implement and train models in parallel
3. **Snapshots** preserve working codebases between experiments
4. **Skills** provide domain-specific guidance
5. **Quotas** constrain GPU spending

Result: Autonomous, parallelized research on GPUs with efficient context management.

## Key Takeaways

1. **Composition**: Build sophisticated systems by layering features on core agent loops
2. **Isolation**: Use sandboxes for security and resource control
3. **Scalability**: Async patterns and work pools enable massive parallelism
4. **Efficiency**: Combine explicit memory (sessions) with implicit memory (filesystems)
5. **Flexibility**: Skills and plugins keep harnesses general-purpose

## Getting Started

- Review the [complete project code on GitHub](https://github.com/modal-labs/openai-agents-python-example)
- Sign up for [[Modal]] to access sandboxes and GPU infrastructure
- Receive $30 in free monthly compute credits

## Related Topics

- [[OpenAI Agents SDK]]
- [[Modal]] (cloud platform)
- [[AI Agents]]
- [[Sandboxes]]
- [[Large Language Models]]
- [[Context Management]]
- [[Asynchronous Programming]]
- [[GPU Computing]]
- [[Orchestration Patterns]]
- [[Multi-Agent Systems]]

## Metadata

**Source**: Modal Engineering Blog  
**Author**: Erik Dunteman (Member of Technical Staff)  
**Published**: April 15, 2026  
**Reading Time**: 8 minutes  
**Original URL**: https://share.google/S4lTnOo