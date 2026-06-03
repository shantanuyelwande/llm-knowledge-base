---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-03T06:59:39.588049
raw_file_updated: 2026-06-03T06:59:39.588049
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-03T06:59:39.588049
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how AgentField's team orchestrated 200+ autonomous Claude Code instances to ship production code through a unified system, moving human responsibility from iteration loops to review loops. The key innovations include two distinct [[LLM]] integration primitives, three nested failure recovery loops, and checkpoint-based execution for durable long-running builds.

## Overview

Multi-agent code generation at scale requires fundamentally different architectural patterns than single-agent systems. Rather than having one engineer iterate with one [[AI coding assistant]], the AgentField team abstracted the human role upward by coordinating dozens of autonomous "harnesses"—full coding environments with filesystem access, test execution, and git capabilities—working in parallel on a shared codebase.

The shift moved human responsibility from line-by-line iteration to architectural sign-off, with draft [[pull requests]] already verified through multiple rounds of automated writing, testing, review, and verification before human review.

## Core Concepts

### The Convergence Problem

The first major challenge emerged when running 30+ harnesses in parallel: one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. The code compiled and the PR looked clean, but the system did not work.

This **convergence problem** required new primitives for:
- [[Isolation]] of parallel processes
- [[Failure recovery]] and retry strategies
- [[State reconciliation]] across agents

## The Two-Primitive Architecture

### 1. Constrained Single-Shot Calls (`.ai()`)

The first primitive handles **routing and classification** with predictable characteristics:

- **Single-shot execution**: No iteration or tool use
- **Structured input and output**: Deterministic format
- **Predictable latency and cost**: Milliseconds and fractions of a cent
- **Use cases**: Issue triage, risk assessment, routing decisions

Each issue receives an `IssueGuidance` block:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive downstream routing, while the guidance string carries context for autonomous agents.

### 2. Autonomous Harnesses (`.harness()`)

The second primitive handles **goal-driven autonomous work** with full iteration:

- **Multi-turn execution**: Iterate until reaching verifiable outcome
- **Tool access**: Read files, write code, run tests, discover failures
- **Goal-oriented**: Receive objectives and toolset, then self-iterate
- **Variable cost and latency**: Depends on problem complexity

A single coder invocation on a complex issue can run up to 150 tool-use turns and cost over $4.

### Design Philosophy

The two primitives coexist in the same system. A boolean from a cheap `.ai()` call determines whether an issue runs through a lean two-call path (coder, then reviewer) or a thorough four-call path (coder, then QA and reviewer in parallel, then synthesizer). This separation enables both flexibility and cost efficiency.

Unlike abstractions designed theoretically, these primitives emerged from watching builds fail repeatedly. The constrained call was obvious from day one; the harness took months of failed builds to recognize as a distinct abstraction.

## Failure Recovery: Three Nested Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three escalation levels to handle different failure types.

### Inner Loop: Per-Issue Retry (Up to 5 iterations)

The agent retries itself with feedback from [[QA]] and [[code review]]. Handles problems the same agent can solve given better information.

**Example**: The app-module issue had all 119 tests passing and met all acceptance criteria, but the code reviewer caught that the module was not exported in `lib.rs`. Iteration 2 fixed the export with 354 tests passing.

### Middle Loop: Issue Advisor

Activates when the inner loop exhausts retries. Provides five typed recovery actions:

| Action | Response |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria; record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps with severity rating |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

**Example**: The integration-tests issue timed out after 2700 seconds due to an infinite loop in the CLI binary. Retrying would never help because the same agent would produce the same deadlock. The system blocked the issue and recorded typed debt, allowing the rest of the build to continue.

### Outer Loop: Replanner

Fires when issues in a dependency level produce unrecoverable failures. Can skip downstream dependents, restructure the issue graph, reduce scope, or abort. Previous replan decisions feed back on subsequent invocations to prevent repeating failed strategies.

**Default behavior**: If the replanner crashes, the system defaults to continue rather than abort. For expensive workflows, graceful degradation is better than fail-fast.

### Debt Tracking

Failed acceptance criteria become typed, severity-rated data structures that downstream agents consume:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, enabling them to work around known gaps instead of building on assumptions that no longer hold.

## Durable Execution: Checkpointing and Isolation

### Checkpoint Everything

At $116 per diagrams build, restarting from scratch is not viable. The system checkpoints at every level boundary:

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": ["project-scaffold", "types-module", ...],
  "original_plan_summary": "15 issues organized in 6 levels...",
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0.

The checkpoint also captures [[git]] state (integration branch, original branch, initial commit SHA, worktree directory mapping) for full workspace reconstruction without re-cloning.

### Git Worktree Isolation

Each issue gets its own working directory and branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.), preventing lock contention and conflicts during parallel coding.

Between levels, a **merger agent** integrates completed branches into the integration branch. The merger is not mechanical; it reads the architecture spec and file conflict annotations to make intent-aware resolution decisions.

### Gate Sequence Between Levels

Every level enforces a clean handoff:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code works together
3. **Debt gate**: Process completed-with-debt results; propagate debt notes downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

### Unified API

The control plane provides a single endpoint to trigger multi-agent builds:

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

Response: 202 Accepted with execution_id. Thirty minutes later: draft PR with full codebase, test results, and debt section.

## Architecture Over Model Selection

Contrary to expectations, smarter models did not produce better results. On a Node.js benchmark, the same architecture scored 95/100 with both Claude Haiku (~$20 total) and MiniMax M2.5 (~$6 total), while single