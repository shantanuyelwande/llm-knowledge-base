---
title: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents
source_file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:50:22.337800
raw_file_updated: 2026-04-17T20:50:22.337800
version: 1
sources:
  - file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:50:22.337800
tags: []
related_topics: []
backlinked_by: []
---
# Open SWE: An Open-Source Framework for Internal Coding Agents

## Summary

**Open SWE** is an open-source framework built on [[Deep Agents]] and [[LangGraph]] that provides core architectural components for deploying [[AI coding agents]] in production engineering environments. The framework captures patterns observed in production implementations at companies like [[Stripe]], [[Ramp]], and [[Coinbase]], offering a customizable foundation for organizations building internal coding agents that integrate with existing developer workflows.

## Overview

Open SWE emerged from observing several engineering organizations independently developing internal coding agents that operate alongside their development teams. These systems—including Stripe's Minions, Ramp's Inspect, and Coinbase's Cloudbot—converged on similar architectural patterns despite being developed independently. This convergence suggested common requirements for deploying [[AI agents]] in production engineering contexts.

The framework provides a reusable, customizable implementation of these patterns while remaining flexible enough for organizations to adapt components to their specific needs and infrastructure.

## Architecture

Open SWE's architecture consists of six core components:

### 1. Agent Harness: Deep Agents Composition

Rather than forking existing agents or building from scratch, Open SWE composes on the [[Deep Agents]] framework. This approach mirrors how Ramp built Inspect on top of OpenCode.

**Advantages of composition:**
- **Upgrade path**: Improvements in Deep Agents (better context management, efficient planning, optimized token usage) can be incorporated without rebuilding customizations
- **Customization without forking**: Organization-specific tools, prompts, and workflows remain as configuration rather than modifications to core agent logic

Deep Agents provides essential infrastructure:
- Built-in planning via `write_todos`
- File-based context management
- Native [[subagent]] spawning via the `task` tool
- Middleware hooks for deterministic orchestration

### 2. Sandbox: Isolated Cloud Environments

Each task runs in its own isolated cloud sandbox—a remote [[Linux]] environment with full shell access. The repository is cloned in, and the agent receives complete permissions while errors remain contained within that environment.

**Supported sandbox providers:**
- [[Modal]]
- [[Daytona]]
- [[Runloop]]
- [[LangSmith]]
- Custom implementations

**Key behaviors:**
- Each conversation thread gets a persistent sandbox, reused across follow-up messages
- Sandboxes automatically recreate if they become unreachable
- Multiple tasks run in parallel, each in its own sandbox

This follows the pattern: isolate first, then grant full permissions inside the boundary.

### 3. Tools: Curated, Not Accumulated

Open SWE ships with a focused, carefully selected toolset rather than accumulating tools over time:

| Tool | Purpose |
|------|---------|
| `execute` | Shell commands in the sandbox |
| `fetch_url` | Fetch web pages as markdown |
| `http_request` | API calls (GET, POST, etc.) |
| `commit_and_open_pr` | Git commit and open GitHub draft PR |
| `linear_comment` | Post updates to Linear tickets |
| `slack_thread_reply` | Reply in Slack threads |

**Built-in Deep Agents tools:** `read_file`, `write_file`, `edit_file`, `ls`, `glob`, `grep`, `write_todos`, and `task` (subagent spawning)

A smaller, curated toolset is easier to test, maintain, and reason about. Organizations can add additional tools for internal APIs, custom deployment systems, or specialized testing frameworks.

### 4. Context Engineering: AGENTS.md + Source Context

Open SWE gathers context from two sources:

**AGENTS.md file**: If a repository contains an `AGENTS.md` file at the root, it's read from the sandbox and injected into the system prompt. This file encodes:
- Conventions
- Testing requirements
- Architectural decisions
- Team-specific patterns

**Source context**: The full [[Linear]] issue (title, description, comments) or [[Slack]] thread history is assembled and passed to the agent before it starts, providing task-specific context without additional tool calls.

This two-layer approach balances repository-wide knowledge with task-specific information.

### 5. Orchestration: Subagents + Middleware

Open SWE's orchestration combines two complementary mechanisms:

**Subagents**: The Deep Agents framework supports spawning child agents via the `task` tool. The main agent can delegate independent subtasks to isolated subagents, each with:
- Its own middleware stack
- Separate todo list
- Independent file operations

**Middleware**: Deterministic middleware hooks run around the agent loop:
- **`check_message_queue_before_model`**: Injects follow-up messages (Linear comments or Slack messages arriving mid-run) before the next model call, allowing users to provide additional input while the agent is working
- **`open_pr_if_needed`**: Acts as a safety net that commits and opens a PR if the agent didn't complete this step, ensuring critical steps happen reliably
- **`ToolErrorMiddleware`**: Catches and handles tool errors gracefully

This separation between agentic (model-driven) and deterministic (middleware-driven) orchestration balances reliability with flexibility.

### 6. Invocation: Slack, Linear, and GitHub

Open SWE follows the observed pattern of Slack as a primary invocation surface:

**Slack**: Mention the bot in any thread
- Supports `repo:owner/name` syntax to specify which repository to work on
- Agent replies in-thread with status updates and PR links

**Linear**: Comment `@openswe` on any issue
- Agent reads the full issue context
- Reacts with 👀 to acknowledge
- Posts results back as comments

**GitHub**: Tag `@openswe` in PR comments on agent-created PRs
- Addresses review feedback
- Pushes fixes to the same branch

Each invocation creates a deterministic thread ID, so follow-up messages on the same issue or thread route to the same running agent.

## Validation and Safety

The agent is instructed to run linters, formatters, and tests before committing. The `open_pr_if_needed` middleware acts as a backstop—if the agent finishes without opening a PR, the middleware handles it automatically.

Validation can be extended by adding:
- Deterministic [[CI]] checks
- Visual verification
- Review gates as additional middleware

## Why Deep Agents

[[Deep Agents]] provides the foundation that makes Open SWE's architecture composable and maintainable:

### Context Management
Long-running coding tasks produce large amounts of intermediate data (file contents, command outputs, search results). Deep Agents handles this through file-based memory, offloading large results instead of keeping everything in conversation history. This prevents context overflow when working on larger codebases.

### Planning Primitives
The built-in `write_todos` tool provides a structured way to:
- Break down complex work
- Track progress
- Adapt plans as new information emerges

This proves particularly helpful for multi-step tasks spanning extended periods.

### Subagent Isolation
When the main agent spawns a child agent via the `task` tool, that subagent gets its own isolated context. Different subtasks don't pollute each other's conversation history, leading to clearer reasoning on complex, multi-faceted work.

### Middleware Hooks
Deep Agents' middleware system allows injection of deterministic logic at specific points in the agent loop. This is how Open SWE implements message injection and automatic PR creation—behaviors that need to happen reliably.

### Upgrade Path
Because Deep Agents is actively developed as a standalone library, improvements to context compression, prompt caching, planning efficiency, and [[subagent]] orchestration can flow to Open SWE without requiring users to rebuild customizations.

## Patterns from Production Deployments

Analysis of Stripe's Minions, Ramp's Inspect, and Coinbase's Cloudbot revealed several convergent patterns:

### Isolated Execution Environments
Tasks run in dedicated cloud sandboxes with full permissions inside strict boundaries. This isolates the blast radius of mistakes from production systems while allowing agents to execute commands without approval prompts for each action.

### Curated Toolsets
Rather than accumulating tools over time, production systems maintain carefully selected toolsets. Stripe's agents have access to approximately 500 tools, but these are curated and maintained. Tool curation appears to matter more than tool quantity.

### Slack-First Invocation
All three systems integrate with [[Slack]] as a primary interface, meeting developers in their existing communication workflows rather than requiring context switches to new applications.

### Rich Context at Startup
Agents pull full context from [[Linear]] issues, Slack threads, or [[GitHub]] PRs before beginning work, reducing the overhead of discovering requirements through tool calls.

### Subagent Orchestration
Complex tasks get decomposed and delegated to specialized child agents, each with isolated context