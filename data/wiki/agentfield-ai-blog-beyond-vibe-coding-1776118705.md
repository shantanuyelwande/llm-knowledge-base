---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-26T05:17:16.242340
raw_file_updated: 2026-04-26T05:17:16.242340
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-26T05:17:16.242340
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] instances to generate production code through a system called [[SWE-AF]]. The key innovation separates [[LLM integration]] into two primitives: constrained single-shot calls (`.ai()`) for routing and classification, and autonomous harnesses (`.harness()`) for iterative code generation. The system manages failures through three nested control loops and uses [[checkpoint-based execution]] to make expensive builds recoverable.

---

## Overview

Building software with multiple autonomous agents working in parallel on a shared codebase presents fundamental coordination challenges. AgentField's team discovered that naive approaches—where all agents have identical access to tools and iteration budgets—fail because they lack operational visibility, cost predictability, and failure recovery mechanisms.

By running 200+ agent invocations on real projects (a Rust CLI tool, Go SDK, and Node.js benchmark), the team identified three core principles that apply to any multi-agent system:

1. Separate [[LLM]] access into two distinct modes
2. Implement nested failure recovery loops
3. Use [[checkpoint-based execution]] for durability

## Core Architecture

### Two Primitives: Constrained Calls and Autonomous Harnesses

The most critical architectural decision is separating [[LLM integration]] into two complementary primitives rather than giving all agents identical capabilities.

#### The Constrained Call (`.ai()`)

A **constrained call** is a single-shot [[LLM]] invocation with:
- Structured input and output
- No tool use
- No iteration
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)

These calls handle routing and classification tasks like:
- "Does this issue need deeper QA?"
- "Is this change high-risk?"
- "What is the estimated scope?"

Each constrained call produces structured guidance that downstream agents consume:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive routing decisions. The `agent_guidance` string carries context for downstream agents. This approach enables cost-efficient filtering without sacrificing information quality.

#### The Autonomous Harness (`.harness()`)

An **autonomous harness** is a multi-turn, tool-using, goal-driven agent that:
- Receives a goal and a toolset
- Iterates until it produces a verifiable outcome
- Has access to filesystem, test execution, and git
- Manages its own retry logic
- Produces outcomes that are checked, not guided

In the diagrams-as-code build, a single harness invocation ran up to 150 tool-use turns and cost over $4 on complex issues. The harness is responsible for writing code, running tests, discovering failures, and attempting fixes.

The harness abstraction emerged from observing actual build failures rather than from theoretical design. It became the abstraction the team wished it had from the start.

### Convergence Problem

When multiple agents work on a shared codebase, the **convergence problem** arises: getting N autonomous processes to produce one coherent result requires primitives for:
- **Isolation**: preventing agents from interfering with each other
- **Failure recovery**: handling the inevitable failures at scale
- **State reconciliation**: merging parallel work into a unified result

The initial failure that revealed this problem occurred when one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. The code compiled and the PR looked clean, but the system did not work.

## Failure Recovery: Three Nested Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three nested control loops to handle failures at different scales.

### Inner Loop: Per-Issue Iteration

The **inner loop** runs per issue, up to 5 iterations maximum. The agent retries itself with feedback from [[QA]] and [[code review]].

**Example**: The `app-module` issue produced 119 passing tests and met all acceptance criteria, but the code reviewer discovered that the module was not exported in `lib.rs`, making it inaccessible to library consumers. Iteration 2 fixed the export with 354 tests passing.

This loop handles problems that the same agent can solve given better information.

### Middle Loop: Issue Advisor

The **middle loop** activates when the inner loop exhausts its iterations. An issue advisor evaluates the situation and selects from five typed recovery actions:

| Action | Purpose |
|--------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record the gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., use a different library) |
| `SPLIT` | Break the issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

On its final invocation, the prompt explicitly warns this is the last chance, biasing the advisor toward acceptance or escalation rather than futile retries.

**Example**: The `integration-tests` issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The tests themselves were correct and passed code review, but the underlying code had a deadlock. The advisor blocked the issue and recorded typed debt:

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

The **outer loop** fires when issues in a dependency level produce unrecoverable failures. The replanner:
- Sees the full execution state
- Can skip downstream dependents
- Restructures the remaining issue graph
- Reduces scope or aborts entirely
- Receives previous replan decisions to prevent repeating failed strategies

If the replanner itself crashes, the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation is superior to fail-fast behavior.

## Checkpoint-Based Execution

Multi-agent builds are long-running, expensive processes. At $116 per build, restarting from scratch after a failure at invocation 140 is not viable. The system treats checkpointing as a survival requirement, not an optimization.

### Checkpoint Capture

The system checkpoints at every [[dependency level]] boundary. A checkpoint captures:

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": [
    "project-scaffold", "types-module", "error-module",
    "lexer", "parser", "validator",
    "layout-engine", "svg-renderer", "ascii-renderer",
    "smoke-test", "app-module", "cli-module",
    "integration-tests", "documentation", "final-acceptance-verification"
  ],
  "original_plan_summary": "15 issues organized in 6 levels...",
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

The `resume_build()` function loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build that fails at minute 25 does not restart from minute 0.

The checkpoint also captures [[git]] state (integration branch, original branch, initial commit SHA, worktree directory mapping) so resumed builds can reconstruct the full workspace without re-cloning.

### Git Worktrees for Agent Isolation

Each issue gets its own [[git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This pattern:
- Prevents lock contention between parallel agents
- Eliminates conflicts during coding
- Allows independent iteration
- Enables clean integration between levels

In the diagrams build, level 2 ran three issues in parallel (lexer, parser, validator), each in its own worktree, each modifying different files with no conflicts.

### Integration Gates Between Levels

Between every [[dependency level]], a sequence of gates enforces clean handoffs:

1. **Merge gate**: integrate completed branches using intent-aware conflict resolution
2. **Integration test gate**: validate merged code still works together
3. **Debt gate**: process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: inject sub-issues if any issue was split