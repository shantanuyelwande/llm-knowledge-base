---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-30T05:35:49.676922
raw_file_updated: 2026-04-30T05:35:49.676922
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-30T05:35:49.676922
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents the architectural patterns and lessons learned from orchestrating 200+ autonomous [[AI agents]] to collaboratively write and test production code. It presents three core design principles: separating [[LLM]] integration into constrained single-shot calls and autonomous loops, implementing nested failure recovery mechanisms, and using checkpoint-based execution for cost-effective long-running workflows. The work is embodied in the open-source [[SWE-AF]] system and informed the design of [[AgentField]], an infrastructure platform for multi-agent systems.

---

## Overview

[[AgentField]] is an AI-native engineering infrastructure that abstracts the human role from the iteration loop to the review loop. Rather than one engineer iterating with one [[Claude Code]] session, the system coordinates dozens of autonomous agent instances (called "harnesses") in parallel on a shared codebase. The goal is to produce draft pull requests that have already passed multiple rounds of automated writing, testing, review, and verification before human review.

### The Convergence Problem

When multiple autonomous processes operate on a shared codebase, coordination failures emerge that no amount of retrying can fix. In early trials, the system produced a pull request where one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. This revealed the core challenge: **getting N autonomous processes to produce one coherent result requires primitives for isolation, failure recovery, and state reconciliation**.

---

## Core Principles

### 1. Two Modes of LLM Integration

The most common architectural mistake in multi-agent systems is giving every agent identical [[LLM]] access. This prevents operational reasoning about SLAs, costs, and retry semantics.

#### Constrained Calls (`.ai()`)

The first primitive is a **constrained single-shot call**:
- Structured input and output
- No tools or iteration
- No external function calls
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)

Used for routing and classification decisions. For example, an issue receives an `IssueGuidance` block:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive downstream routing decisions. The `agent_guidance` string carries context for downstream agents.

#### Autonomous Loops (`.harness()`)

The second primitive is an **autonomous loop with full environment access**:
- Multi-turn, tool-using, goal-driven iteration
- Full filesystem access
- Test execution capability
- [[Git]] integration
- Verifiable outcomes

The harness receives a goal and toolset, then iterates until producing a result. It reads files, writes code, runs tests, discovers failures, and retries. The caller evaluates the delivered outcome, not the iteration path. A single harness invocation may run up to 150 tool-use turns and cost several dollars on complex issues.

#### Integration Pattern

The two primitives coexist in the same system. A boolean from a cheap `.ai()` classification call (e.g., `needs_deeper_qa`) determines whether an issue runs through a lean two-call path (coder, then reviewer) or a thorough four-call path (coder, then QA and reviewer in parallel, then synthesizer).

---

### 2. Nested Failure Recovery Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three nested control loops to handle different failure modes.

#### Failure Categories

**Deadlocks that retrying cannot fix**: When an agent produces code with an infinite loop or deadlock, the inner retry loop cannot help because the same agent produces the same broken output. These require escalation and blocking.

**Review catches that tests miss**: Missing module exports, violated conventions, and architectural violations that tests do not catch. These are fixed by the inner loop when the coder receives review feedback.

**Regressions on trivial tasks**: Even simple scaffolding tasks regress on subsequent iterations. Autonomous code generation fails unpredictably.

**Cascading verification failures**: Issues compound across iterations (e.g., `set -e` crashes, then `|| true` masking failures, then finally correct).

#### The Three Control Loops

```
┌─────────────────────────────────────────────┐
│         OUTER LOOP: Replanner               │
│  (Full execution state, dependency graph)   │
└─────────────────────────────────────────────┘
         ↓ (Escalation)
┌─────────────────────────────────────────────┐
│      MIDDLE LOOP: Issue Advisor             │
│  (5 typed recovery actions per issue)       │
└─────────────────────────────────────────────┘
         ↓ (Exhausted retries)
┌─────────────────────────────────────────────┐
│      INNER LOOP: Per-Issue Iteration        │
│  (Up to 5 iterations with QA/review)        │
└─────────────────────────────────────────────┘
```

##### Inner Loop (Per-Issue)

Runs up to 5 iterations with feedback from [[Quality Assurance|QA]] and code review. Handles problems that the same agent can solve with better information. The missing export in the app-module issue was caught and fixed here.

##### Middle Loop (Issue Advisor)

Activates when the inner loop exhausts retries. Provides five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The final invocation explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retry.

##### Outer Loop (Replanner)

Fires when issues in a dependency level produce unrecoverable failures. Views the full execution state and can:
- Skip downstream dependents
- Restructure the remaining issue graph
- Reduce scope
- Abort entirely

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes, the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation is better than fail-fast.

#### Typed Debt Items

When an issue cannot be fixed, it produces a typed debt record:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, so they can work around known gaps instead of building on false assumptions.

---

### 3. Checkpoint-Based Execution for Cost Efficiency

A 200+ invocation build running at $116 cannot restart from failure point 1. The system must treat multi-agent builds as long-running, expensive processes requiring durability from the start.

#### Checkpoint Contents

Checkpoints capture:
- Current execution level
- Completed levels
- Full issue list and original plan
- Replan count
- Accumulated debt items
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)

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

#### Resume Capability

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0. Git state reconstruction allows resumed builds to skip re-cloning.