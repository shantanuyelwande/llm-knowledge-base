---
title: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents
source_file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:49:17.255485
raw_file_updated: 2026-04-24T18:49:17.255485
version: 1
sources:
  - file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:49:17.255485
tags: []
related_topics: []
backlinked_by: []
---
# Open SWE: An Open-Source Framework for Internal Coding Agents

## Summary

**Open SWE** is an open-source framework for building internal [[coding agents]] that operate within engineering organizations. Built on [[Deep Agents]] and [[LangGraph]], it provides customizable architectural components based on patterns observed in production deployments at companies like [[Stripe]], [[Ramp]], and [[Coinbase]]. The framework emphasizes isolated execution environments, curated toolsets, workflow integration, and deterministic orchestration to enable AI-assisted coding tasks in production settings.

## Overview

Over the past year, several major engineering organizations have independently developed internal coding agents that integrate with existing developer workflows rather than requiring adoption of new interfaces. These systems—including Stripe's Minions, Ramp's Inspect, and Coinbase's Cloudbot—converged on similar architectural patterns despite being developed independently. Open SWE captures these patterns in a reusable, customizable framework designed to serve as a starting point for organizations exploring internal coding agents.

## Key Architectural Patterns

Open SWE implements six core architectural patterns observed across production deployments:

### 1. Isolated Execution Environments

Tasks execute in dedicated cloud sandboxes with full permissions inside strict boundaries. This approach:
- Isolates the blast radius of agent mistakes from production systems
- Allows agents to execute commands without approval prompts for each action
- Supports multiple sandbox providers including [[Modal]], [[Daytona]], [[Runloop]], and [[LangSmith]]
- Enables custom sandbox backend implementations for internal infrastructure

### 2. Curated Toolsets

Rather than accumulating tools over time, Open SWE ships with a focused, carefully maintained set of tools:

| Tool | Purpose |
|------|---------|
| `execute` | Shell commands in the sandbox |
| `fetch_url` | Fetch web pages as markdown |
| `http_request` | API calls (GET, POST, etc.) |
| `commit_and_open_pr` | Git commit and open GitHub draft PR |
| `linear_comment` | Post updates to Linear tickets |
| `slack_thread_reply` | Reply in Slack threads |

Additional tools from [[Deep Agents]] include: `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `write_todos`, and `task` (for [[subagent]] spawning).

A smaller, curated toolset is easier to test, maintain, and reason about. Organizations can explicitly add tools for internal APIs, custom deployment systems, and specialized frameworks.

### 3. Slack-First Invocation

Open SWE integrates with developer workflows through multiple channels:

- **Slack**: Mention the bot in any thread; supports `repo:owner/name` syntax for repository specification
- **Linear**: Comment `@openswe` on any issue; agent reads full context and posts results as comments
- **GitHub**: Tag `@openswe` in PR comments to address review feedback

Each invocation creates a deterministic thread ID, routing follow-up messages to the same running agent.

### 4. Rich Context at Startup

Agents receive full context before beginning work through a two-layer approach:

- **AGENTS.md file**: Repository-wide knowledge including conventions, testing requirements, architectural decisions, and team-specific patterns
- **Source context**: Full Linear issue details or Slack thread history assembled and passed to the agent before execution

This reduces the overhead of discovering requirements through tool calls.

### 5. Subagent Orchestration

Complex tasks are decomposed and delegated to specialized child agents via the `task` tool. Each subagent receives:
- Isolated context
- Focused responsibilities
- Its own middleware stack and file operations
- Separate conversation history to prevent pollution across subtasks

### 6. Validation: Prompt-Driven with Safety Nets

Agents are instructed to run linters, formatters, and tests before committing. The `open_pr_if_needed` middleware acts as a backstop, automatically committing and opening a PR if the agent doesn't complete this step, ensuring critical steps happen reliably.

## Architecture Components

### Agent Harness: Composition on Deep Agents

Open SWE composes on the [[Deep Agents]] framework rather than forking or building from scratch. This approach provides:

**Upgrade Path**: When Deep Agents improves context management, planning efficiency, or token usage, these improvements can be incorporated without rebuilding customizations.

**Customization Without Forking**: Organization-specific tools, prompts, and workflows remain as configuration rather than core agent logic modifications.

#### Example Configuration

```python
create_deep_agent(
    model="anthropic:claude-opus-4-6",
    system_prompt=construct_system_prompt(repo_dir, ...),
    tools=[
        http_request,
        fetch_url,
        commit_and_open_pr,
        linear_comment,
        slack_thread_reply
    ],
    backend=sandbox_backend,
    middleware=[
        ToolErrorMiddleware(),
        check_message_queue_before_model,
        ...
    ],
)
```

### Sandbox Behavior

Each conversation thread receives a persistent sandbox that is reused across follow-up messages. Key behaviors include:

- Sandboxes automatically recreate if they become unreachable
- Multiple tasks run in parallel, each in its own sandbox
- Full repository cloning with complete permissions inside the boundary

### Orchestration: Subagents and Middleware

Open SWE combines two orchestration mechanisms:

**Subagents**: Child agents spawned via the `task` tool operate with isolated context and focused responsibilities.

**Middleware**: Deterministic middleware hooks run around the agent loop at specific points:
- `check_message_queue_before_model`: Injects follow-up messages (Linear comments or Slack messages arriving mid-run) before the next model call
- `open_pr_if_needed`: Acts as a safety net, committing and opening a PR if the agent didn't complete this step
- `ToolErrorMiddleware`: Catches and handles tool errors gracefully

This separation between agentic (model-driven) and deterministic (middleware-driven) orchestration balances reliability with flexibility.

## Why Deep Agents

[[Deep Agents]] provides the foundation making this architecture composable and maintainable:

### Context Management

Long-running coding tasks produce large amounts of intermediate data (file contents, command outputs, search results). Deep Agents handles this through file-based memory, offloading large results instead of keeping everything in conversation history. This prevents context overflow when working on larger codebases.

### Planning Primitives

The built-in `write_todos` tool provides structured task breakdown, progress tracking, and plan adaptation. This is particularly helpful for multi-step tasks spanning extended periods.

### Subagent Isolation

Child agents spawned via the `task` tool receive isolated context, preventing different subtasks from polluting each other's conversation history and enabling clearer reasoning on complex work.

### Middleware Hooks

The middleware system allows injection of deterministic logic at specific agent loop points. This enables message injection and automatic PR creation—behaviors requiring reliable execution.

### Upgrade Path

As Deep Agents is actively developed as a standalone library, improvements to context compression, prompt caching, planning efficiency, and subagent orchestration flow to Open SWE without requiring customization rebuilds.

## Customization for Your Organization

Open SWE is designed as a customizable foundation rather than a finished product. Every major component is pluggable:

- **Sandbox provider**: Swap between Modal, Daytona, Runloop, or LangSmith; implement custom backends
- **Model**: Use any [[LLM]] provider; default is Claude Opus 4
- **Tools**: Add tools for internal APIs, deployment systems, testing frameworks, or monitoring platforms
- **Triggers**: Modify Slack, Linear, and GitHub integration logic; add new surfaces like email or webhooks
- **System prompt**: Customize base prompt and AGENTS.md incorporation logic
- **Middleware**: Add hooks for validation, approval gates, logging, or safety checks

## Comparison to Internal Implementations

| Decision | Open SWE | Stripe (Minions) | Ramp (Inspect) | Coinbase (Cloudbot) |
|----------|----------|------------------|----------------|-------------------|
| Harness | Composed (Deep Agents/LangGraph) | Forked (Goose) | Composed (OpenCode) | Built from scratch |
| Sandbox | Pluggable (Modal, Daytona, Runloop, etc.) | AWS EC2 devboxes (pre-warmed) | Modal containers (pre-warmed) | In-house |
| Tools | ~15, curated | ~500, curated per-agent | OpenCode SDK + extensions | MCPs + custom Skills |
| Context | AGENTS.md + issue/thread | Rule files + pre-hydration | OpenCode built-in | Linear-first + MC