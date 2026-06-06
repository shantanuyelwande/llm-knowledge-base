---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-06T06:00:45.026976
raw_file_updated: 2026-06-06T06:00:45.026976
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-06T06:00:45.026976
tags: []
related_topics: []
backlinked_by: []
---
# Autonomous Multi-Agent Code Generation

## Summary

**Beyond Vibe Coding** describes a production system for orchestrating 200+ autonomous [[Large Language Model|LLM]] agents to collaboratively write, test, and review code. The approach separates [[LLM Integration]] into two distinct modes: constrained single-shot calls for routing and classification, and autonomous harnesses for iterative code generation. The system manages failures through three nested control loops, uses [[Git Worktrees|git worktrees]] for agent isolation, and implements checkpoint-based execution for cost efficiency. This architecture enables draft pull requests that require minimal human review, moving [[Software Engineering]] from line-by-line iteration to architectural sign-off.

---

## Overview

Autonomous code generation at scale presents a fundamentally different set of challenges than single-agent [[AI-Assisted Development]]. When multiple agents work on the same codebase simultaneously, they must coordinate around shared dependencies, handle cascading failures, and produce coherent results despite working in isolation. The AgentField team solved these problems through architectural patterns rather than relying on model capability alone.

## Core Concepts

### Two Modes of LLM Integration

The system distinguishes between two fundamentally different types of [[LLM Integration]]:

#### Constrained Single-Shot Calls (`.ai()`)

**Purpose**: Routing, classification, and structured decision-making

- Single turn, no iteration
- Structured input and output
- No tool use
- Predictable latency (milliseconds) and cost (fractions of a cent)
- Outputs that downstream code can switch on

**Example use case**: Analyzing an issue to determine if it needs deeper [[Quality Assurance|QA]], estimating scope, identifying risk level, and providing guidance for downstream agents.

Each issue receives an `IssueGuidance` block:

```
needs_new_tests: true
estimated_scope: "medium"
touches_interfaces: true
needs_deeper_qa: true
agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

**Purpose**: Multi-turn, goal-driven code generation with full development environment

- Multi-turn iteration with tool use
- Full filesystem access, test execution, and [[Git]] integration
- Goal-driven execution until verifiable outcome
- Unpredictable latency and cost (depends on task complexity)
- Focus on output verification, not execution path

In the diagrams-as-code build, a single coder harness ran up to 150 tool-use turns and cost over $4 on complex issues.

### The Convergence Problem

When 30+ agents work in parallel on a shared codebase, coherence breaks down. The classic failure: one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. Code compiled. The PR looked clean. The system did not work.

This illustrates the need for:
- **Isolation**: Agents must work independently without interfering with each other
- **Failure recovery**: Failures must be recoverable, not fatal
- **State reconciliation**: The system must reconcile independent work into one coherent result

## Failure Management

In a build with 200+ agent invocations, failures are the normal path, not edge cases. The system manages failures through three nested control loops.

### Inner Loop: Per-Issue Retry (Up to 5 iterations)

The agent retries itself with feedback from [[Quality Assurance|QA]] and [[Code Review]]. This loop handles problems the same agent can solve given better information.

**Example**: The app-module issue had all 119 tests passing and met all acceptance criteria, but the module was not exported in `lib.rs`. The code reviewer blocked the PR. On iteration 2, the agent added `pub mod app;` and passed with 354 tests.

### Middle Loop: Issue Advisor

When the inner loop exhausts its retries, an issue advisor activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gaps as typed debt |
| `RETRY_APPROACH` | Keep criteria, try different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as structured debt items |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

**Example of debt recording**: The integration-tests issue timed out with an infinite loop in the CLI binary. After two failed iterations, the advisor blocked it with:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

### Outer Loop: Replanner

Fires when issues in a dependency level produce unrecoverable failures. The replanner sees the full execution state and can:
- Skip downstream dependents
- Restructure the remaining issue graph
- Reduce scope
- Abort the build

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies.

## Execution Architecture

### Planning and Parallelization

Agents plan differently than humans. Given a large epic, the planner consistently produces finer-grained, more parallelizable issue graphs. Decomposition into 50-100 issues with dependency structures humans would not attempt is common, because the orchestrator absorbs the coordination cost.

### Isolation with Git Worktrees

Each issue gets a [[Git Worktrees|git worktree]] on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This provides:
- No lock contention between parallel agents
- No conflicts during coding
- Clean isolation of changes

Between levels, a merger agent integrates completed branches into the integration branch. The merger is not mechanical `git merge`; it reads the architecture spec and file conflict annotations to make intent-aware resolution decisions.

### Gate Sequence Between Levels

Every level enforces a clean handoff:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code still works
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

## Durability and Cost Management

### Checkpoint-Based Execution

LLM timeouts, rate limits, network errors, and malformed output can each crash a build. At $116 per build, restarting from scratch is not viable.

The system checkpoints at every level boundary, capturing:
- Current execution level
- Completed levels
- All issues and their state
- Original plan summary
- Replan count
- Accumulated debt

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build that fails at minute 25 does not restart from minute 0.

### One-Call Interface

The control plane provides a unified API regardless of runtime or model:

```bash
curl -X POST http://localhost:8080/api/v1/execute/async/swe-planner.build \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "goal": "Build a diagrams-as-code CLI tool with DSL parser and SVG output",
      "repo_url": "https://github.com/user/my-project",
      "config": {
        "runtime": "claude_code",
        "models": { "default": "sonnet", "coder": "haiku" }
      }
    }
  }'
```

Response is a 202 Accepted with an `execution_id`. Thirty minutes later, there is a draft PR with full codebase, test results, and debt documentation.

## Model Selection vs. Architecture

Counterintuitively, architecture beats model selection. On a Node.js CLI benchmark, the same architecture scored 95/100 with both Claude Haiku ($20 total) and MiniMax M2.5 via OpenRouter ($6 total). Single-agent approaches on the same task scored between 59 and 73.

The model configuration is a flat map:

```json
{
  "runtime": "claude_code",
  "models": {
    "default": "sonnet",
    "coder": "haiku",
    "qa": "haiku",
    "architect": "sonnet"
  }
}
```

Each role can be assigned independently. The cheaper model