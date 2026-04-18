---
title: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents
source_file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:11:38.227067
raw_file_updated: 2026-04-17T20:11:38.227067
version: 1
sources:
  - file: Harness - Open SWE_ An Open-Source Framework for Internal Coding Agents.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:11:38.227067
tags: []
related_topics: []
backlinked_by: []
---
# Open SWE: An Open-Source Framework for Internal Coding Agents

## Summary

**Open SWE** is an open-source framework for building internal [[coding agents]] that integrate with existing developer workflows. Built on [[Deep Agents]] and [[LangGraph]], it provides customizable architectural components based on patterns observed in production deployments at companies like Stripe, Ramp, and Coinbase. The framework emphasizes isolated execution environments, curated toolsets, and workflow integration through [[Slack]], [[Linear]], and [[GitHub]].

---

## Overview

Open SWE captures architectural patterns observed across multiple production [[AI agent]] implementations. Rather than requiring engineers to adopt new interfaces, these systems integrate directly into existing workflows through familiar communication and task management platforms.

### Key Insight

Several major engineering organizations have independently developed internal coding agents that converge on similar architectural patterns:
- Stripe's **Minions**
- Ramp's **Inspect**
- Coinbase's **Cloudbot**

Open SWE abstracts these common patterns into a reusable, customizable framework.

---

## Architectural Patterns

### Isolated Execution Environments

Tasks run in dedicated cloud sandboxes with full permissions inside strict boundaries. This architecture:
- Isolates the blast radius of agent mistakes from production systems
- Allows agents to execute commands without approval prompts for each action
- Provides a contained environment for testing and development work

### Curated Toolsets

Rather than accumulating tools over time, Open SWE maintains a focused, carefully selected set of tools. Research from Stripe indicates that tool curation matters more than tool quantity—their agents have access to approximately 500 tools, all carefully maintained.

### Slack-First Invocation

All three reference implementations prioritize [[Slack]] as the primary interface. This design choice:
- Meets developers in existing communication workflows
- Eliminates context switches to new applications
- Reduces friction in agent adoption

### Rich Context at Startup

Agents pull full context from [[Linear]] issues, [[Slack]] threads, or [[GitHub]] PRs before beginning work. This approach:
- Reduces overhead of discovering requirements through tool calls
- Provides task-specific information upfront
- Minimizes back-and-forth communication

### Subagent Orchestration

Complex tasks are decomposed and delegated to specialized child agents, each with:
- Isolated context
- Focused responsibilities
- Independent execution paths

---

## Open SWE Architecture

### 1. Agent Harness: Composition on Deep Agents

Open SWE composes on the [[Deep Agents]] framework rather than forking or building from scratch. This approach provides:

**Advantages:**
- **Upgrade path**: Improvements in context management, planning efficiency, and token usage flow automatically to customizations
- **Customization without forking**: Org-specific tools, prompts, and workflows remain as configuration rather than core modifications

**Supported Infrastructure:**
- Built-in planning via `write_todos`
- File-based context management
- Native [[subagent]] spawning via the `task` tool
- Middleware hooks for deterministic orchestration

### 2. Sandbox: Isolated Cloud Environments

Each task runs in its own isolated cloud sandbox—a remote Linux environment with full shell access.

**Supported Providers:**
- [[Modal]]
- [[Daytona]]
- [[Runloop]]
- [[LangSmith]]
- Custom implementations

**Key Behaviors:**
- Repository is cloned into the sandbox
- Agent receives complete permissions within the boundary
- Errors are contained within the environment
- Each conversation thread gets a persistent sandbox, reused across follow-up messages
- Sandboxes automatically recreate if unreachable
- Multiple tasks run in parallel, each in its own sandbox

### 3. Tools: Curated, Not Accumulated

Open SWE ships with a focused toolset designed for common coding tasks:

| Tool | Purpose |
|------|---------|
| `execute` | Shell commands in the sandbox |
| `fetch_url` | Fetch web pages as markdown |
| `http_request` | API calls (GET, POST, etc.) |
| `commit_and_open_pr` | Git commit and open GitHub draft PR |
| `linear_comment` | Post updates to Linear tickets |
| `slack_thread_reply` | Reply in Slack threads |

**Built-in Deep Agents tools:**
- `read_file`, `write_file`, `edit_file`
- `ls`, `glob`, `grep`
- `write_todos`
- `task` (subagent spawning)

**Design Philosophy:**
A smaller, curated toolset is easier to test, maintain, and reason about. Organizations can add explicit tools for internal APIs, custom deployment systems, or specialized testing frameworks as needed.

### 4. Context Engineering: AGENTS.md + Source Context

Open SWE gathers context from two sources:

**AGENTS.md File:**
- Read from the repository root during sandbox execution
- Injected into the system prompt
- Encodes conventions, testing requirements, architectural decisions, and team-specific patterns

**Source Context:**
- Full [[Linear]] issue (title, description, comments) or [[Slack]] thread history
- Assembled and passed to the agent before execution
- Provides task-specific information without additional tool calls

This two-layer approach balances repository-wide knowledge with task-specific information.

### 5. Orchestration: Subagents + Middleware

Open SWE's orchestration combines two complementary mechanisms:

**Subagents:**
- Deep Agents framework supports spawning child agents via the `task` tool
- Main agent delegates independent subtasks to isolated subagents
- Each subagent has its own middleware stack, todo list, and file operations

**Middleware:**
Deterministic middleware hooks run around the agent loop:

- **`check_message_queue_before_model`**: Injects follow-up messages ([[Linear]] comments or [[Slack]] messages that arrive mid-run) before the next model call, allowing users to provide additional input while the agent is working
- **`open_pr_if_needed`**: Acts as a safety net that commits and opens a PR if the agent didn't complete this step, ensuring critical steps happen reliably
- **`ToolErrorMiddleware`**: Catches and handles tool errors gracefully

This separation between agentic (model-driven) and deterministic (middleware-driven) orchestration balances reliability with flexibility.

### 6. Invocation: Slack, Linear, and GitHub

Open SWE follows the observed pattern of multi-platform invocation:

**Slack:**
- Mention the bot in any thread
- Supports `repo:owner/name` syntax to specify repository
- Agent replies in-thread with status updates and PR links

**Linear:**
- Comment `@openswe` on any issue
- Agent reads full issue context
- Reacts with 👀 to acknowledge
- Posts results back as comments

**GitHub:**
- Tag `@openswe` in PR comments on agent-created PRs
- Agent addresses review feedback and pushes fixes to the same branch

**Thread Management:**
Each invocation creates a deterministic thread ID, so follow-up messages on the same issue or thread route to the same running agent.

### 7. Validation: Prompt-Driven + Safety Nets

The agent is instructed to:
- Run linters and formatters
- Execute tests before committing
- Use the `open_pr_if_needed` middleware as a backstop

Organizations can extend this validation layer by adding:
- Deterministic CI checks
- Visual verification
- Review gates as additional middleware

---

## Why Deep Agents

Open SWE is built on [[Deep Agents]] for several architectural advantages:

### Context Management

Long-running coding tasks produce large amounts of intermediate data (file contents, command outputs, search results). [[Deep Agents]] handles this through:
- File-based memory
- Offloading large results instead of keeping everything in conversation history
- Prevention of context overflow when working on larger codebases

### Planning Primitives

The built-in `write_todos` tool provides:
- Structured way to break down complex work
- Progress tracking
- Plan adaptation as new information emerges
- Particular utility for multi-step tasks spanning extended periods

### Subagent Isolation

When the main agent spawns a child agent via the `task` tool:
- Subagent gets its own isolated context
- Different subtasks don't pollute each other's conversation history
- Leads to clearer reasoning on complex, multi-faceted work

### Middleware Hooks

[[Deep Agents]]' middleware system allows:
- Injection of deterministic logic at specific points in the agent loop
- Implementation of message injection and automatic PR creation
- Behaviors that need to happen reliably

### Upgrade Path

Because [[Deep Agents]] is actively developed as a standalone library:
- Improvements to context compression, prompt caching, planning efficiency,