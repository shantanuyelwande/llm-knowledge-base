---
title: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents
source_file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:17:25.527424
raw_file_updated: 2026-04-05T20:17:25.527424
version: 1
sources:
  - file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:17:25.527424
tags: []
related_topics: []
backlinked_by: []
---
# Open SWE Framework

## Summary

**Open SWE** is an open-source framework for building internal [[coding agents]] that operate within engineering organizations. Built on [[Deep Agents]] and [[LangGraph]], it provides architectural components for deploying AI-powered development assistants integrated into existing workflows like [[Slack]], [[Linear]], and [[GitHub]]. The framework is based on patterns observed in production deployments at companies including Stripe, Ramp, and Coinbase.

---

## Overview

Open SWE provides a customizable, production-ready implementation for internal coding agents—AI systems that work alongside development teams to automate code-related tasks. Rather than requiring engineers to adopt new interfaces, these agents integrate into existing communication and project management platforms.

The framework emerged from observing independent implementations at major technology companies that converged on similar architectural patterns, suggesting common requirements for deploying AI agents in production engineering environments.

## Key Architectural Patterns

Open SWE implements several core patterns observed across production deployments:

### Isolated Execution Environments

Tasks execute in dedicated cloud sandboxes with full permissions inside strict boundaries. This design:
- Isolates the blast radius of agent errors from production systems
- Allows agents to execute commands without requiring approval for each action
- Provides a secure, contained environment for code execution

Supported sandbox providers include [[Modal]], Daytona, Runloop, and LangSmith, with support for custom implementations.

### Curated Toolsets

Rather than accumulating tools over time, Open SWE emphasizes careful curation. The framework ships with approximately 15 core tools:

| Tool | Purpose |
|------|---------|
| `execute` | Shell commands in the sandbox |
| `fetch_url` | Fetch web pages as markdown |
| `http_request` | API calls (GET, POST, etc.) |
| `commit_and_open_pr` | Git commit and open GitHub draft PR |
| `linear_comment` | Post updates to Linear tickets |
| `slack_thread_reply` | Reply in Slack threads |
| `read_file`, `write_file`, `edit_file` | File operations |
| `ls`, `glob`, `grep` | File system navigation |
| `write_todos`, `task` | Planning and subagent spawning |

Organizations can extend this toolset with custom tools for internal APIs, deployment systems, and specialized frameworks.

### Slack-First Invocation

Open SWE follows the pattern of all three major production implementations by prioritizing [[Slack]] as the primary interface:
- Mention the bot in any thread
- Use `repo:owner/name` syntax to specify repositories
- Agent replies in-thread with status updates and PR links
- Follow-up messages route to the same running agent via deterministic thread IDs

Additional invocation surfaces include [[Linear]] (via comments) and [[GitHub]] (via PR comments).

### Rich Context at Startup

Agents receive full context before beginning work:
- **AGENTS.md files**: Repository-specific conventions, testing requirements, and architectural decisions
- **Issue/thread history**: Complete Linear issue descriptions or Slack thread history
- This approach reduces overhead of discovering requirements through tool calls

### Subagent Orchestration

Complex tasks are decomposed and delegated to specialized child [[agents]], each with:
- Isolated context
- Focused responsibilities
- Own middleware stack and file operations

This enables parallel execution and clearer reasoning on multi-faceted work.

## Architecture Components

### 1. Agent Harness

Open SWE composes on the [[Deep Agents]] framework rather than forking or building from scratch. This approach provides:

**Upgrade Path**: Improvements to Deep Agents (context management, planning efficiency, token optimization) can be incorporated without rebuilding customizations.

**Customization Without Forking**: Organization-specific tools, prompts, and workflows exist as configuration rather than core modifications.

Example configuration:
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

### 2. Sandbox Infrastructure

Each task runs in its own isolated cloud sandbox—a remote Linux environment with:
- Full shell access
- Repository cloned in
- Complete permissions within boundaries
- Automatic error containment

Key behaviors:
- Persistent sandboxes per conversation thread, reused across follow-up messages
- Automatic sandbox recreation if unreachable
- Multiple tasks running in parallel, each in separate sandbox

### 3. Context Engineering

A two-layer approach balances repository-wide and task-specific knowledge:

**AGENTS.md**: If present at repository root, this file is injected into the system prompt and encodes:
- Team conventions
- Testing requirements
- Architectural decisions
- Team-specific patterns

**Source Context**: Full Linear issue or Slack thread history is assembled and passed before agent startup.

### 4. Orchestration Mechanisms

Two complementary systems manage agent coordination:

**Subagents**: Child agents spawned via the `task` tool operate with isolated context, preventing subtasks from polluting conversation history.

**Middleware**: Deterministic hooks run around the agent loop:
- `check_message_queue_before_model`: Injects follow-up messages before model calls
- `open_pr_if_needed`: Safety net ensuring critical steps complete
- `ToolErrorMiddleware`: Graceful tool error handling

This separation balances reliability (deterministic middleware) with flexibility (model-driven agentic behavior).

### 5. Validation Layer

Validation combines multiple approaches:

**Prompt-Driven**: Agents are instructed to run linters, formatters, and tests before committing.

**Safety Nets**: The `open_pr_if_needed` middleware acts as a backstop, automatically handling PR creation if the agent doesn't complete this step.

**Extensible**: Organizations can add deterministic CI checks, visual verification, or review gates as additional middleware.

## Why Deep Agents

Open SWE builds on [[Deep Agents]] for several advantages:

### Context Management
Long-running coding tasks produce large intermediate data (file contents, command outputs, search results). Deep Agents handles this through file-based memory, offloading large results instead of keeping everything in conversation history. This prevents context overflow on larger codebases.

### Planning Primitives
The built-in `write_todos` tool provides structured task breakdown, progress tracking, and plan adaptation as new information emerges. Particularly helpful for multi-step tasks spanning extended periods.

### Subagent Isolation
Child agents spawned via the `task` tool receive isolated context. Different subtasks don't pollute each other's conversation history, enabling clearer reasoning on complex work.

### Middleware Hooks
The middleware system allows injection of deterministic logic at specific agent loop points. This enables message injection and automatic PR creation—behaviors requiring reliability.

### Upgrade Path
As a standalone, actively-developed library, improvements to context compression, prompt caching, planning efficiency, and orchestration can flow to Open SWE without requiring customization rebuilds.

## Customization

Every major component is pluggable:

- **Sandbox provider**: Swap between Modal, Daytona, Runloop, LangSmith, or implement custom backends
- **Model**: Use any LLM provider; default is Claude Opus 4
- **Tools**: Add tools for internal APIs, deployment systems, testing frameworks, monitoring
- **Triggers**: Modify Slack/Linear/GitHub integration; add email, webhooks, custom UIs
- **System prompt**: Customize base prompt and AGENTS.md incorporation logic
- **Middleware**: Add validation, approval gates, logging, or safety checks

## Comparison to Production Implementations

| Aspect | Open SWE | Stripe (Minions) | Ramp (Inspect) | Coinbase (Cloudbot) |
|--------|----------|------------------|----------------|-------------------|
| Harness | Composed (Deep Agents/LangGraph) | Forked (Goose) | Composed (OpenCode) | Built from scratch |
| Sandbox | Pluggable (Modal, Daytona, Runloop) | AWS EC2 devboxes (pre-warmed) | Modal containers (pre-warmed) | In-house |
| Tools | ~15, curated | ~500, curated | OpenCode SDK + extensions | MCPs + custom Skills |
| Context | AGENTS.md + issue/thread | Rule files + pre-hydration | OpenCode built-in | Linear-first + MCPs |
| Orchestration | Subagents + middleware | Blueprints (deterministic +