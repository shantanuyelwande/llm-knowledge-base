---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-02T06:48:45.751810
raw_file_updated: 2026-06-02T06:48:45.751810
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-02T06:48:45.751810
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation Architecture

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[AI agents]] to collaboratively generate production code. The system uses two distinct LLM integration modes, nested failure recovery loops, and checkpoint-based execution to manage complexity in multi-agent software development workflows. Key innovations include the constrained call (`.ai()`) primitive for routing and the autonomous harness (`.harness()`) for goal-driven iteration.

---

## Overview

Building software with multiple autonomous agents introduces coordination challenges that single-agent systems do not face. The [[AgentField]] team developed [[SWE-AF]], a system for orchestrating 200+ [[Claude Code]] instances on shared codebases, discovering three core principles applicable to any multi-agent architecture:

1. **Two distinct modes of [[LLM]] integration** rather than a single unified approach
2. **Nested failure recovery loops** that escalate gracefully rather than retry blindly
3. **Checkpoint-based execution** for cost-effective recovery in expensive, long-running workflows

The system moves human responsibility from line-by-line code iteration to architectural review, where engineers approve finished, verified draft [[pull requests]] instead of guiding each change.

---

## Core Architecture

### The Convergence Problem

When multiple autonomous agents work on a shared codebase in parallel, they must produce one coherent result. Early attempts failed spectacularly: one agent built an API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency, but the system did not work. This is the **convergence problem**—requiring primitives for isolation, failure recovery, and state reconciliation.

### Two LLM Integration Primitives

Rather than giving every agent identical [[LLM]] access, the system separates integration into two modes:

#### 1. Constrained Call (`.ai()`)

A **single-shot, structured** interaction with:
- Fixed input/output schemas
- No tool use or iteration
- Predictable latency and cost (milliseconds, fractions of a cent)
- Deterministic outputs for routing and classification

Used for decisions like:
- "Does this issue need deeper QA?"
- "Is this change high-risk?"
- Generating structured guidance blocks with fields like `needs_new_tests`, `estimated_scope`, `touches_interfaces`, and `agent_guidance`

This primitive enables cheap routing; downstream expensive work is allocated based on these decisions.

#### 2. Autonomous Harness (`.harness()`)

A **multi-turn, goal-driven** agent with:
- Full coding environment (filesystem, test runner, [[git]])
- Tool use and iteration until verifiable outcome
- Variable latency and cost depending on issue complexity
- Failure recovery built into the harness itself

The harness reads files, writes code, runs tests, discovers failures, and retries. A single coder invocation on complex issues can run 150+ tool-use turns and cost over $4.

**Design Philosophy**: Rather than inventing abstractions theoretically, the `.harness()` primitive emerged from watching builds fail repeatedly. It captures the pattern that kept appearing: agents need a full coding environment with iteration loops and retry capability. This abstraction was not obvious at the start; it took months of failed builds to recognize.

---

## Failure Recovery: Three Nested Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system uses three nested control loops with different responsibilities:

### Inner Loop: Per-Issue Iteration

- **Scope**: Single issue, up to 5 iterations
- **Mechanism**: Agent retries with feedback from [[QA]] and code review
- **Success Condition**: Issue passes acceptance criteria
- **Example**: The `app-module` issue failed iteration 1 because it was not exported in `lib.rs`, despite 119 passing tests. The reviewer caught it; iteration 2 fixed the export.

### Middle Loop: Issue Advisor

Activates when the inner loop exhausts retries. Provides five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria; record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., use different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

The prompt explicitly warns that this is the last chance, biasing toward acceptance or escalation rather than futile retry.

### Outer Loop: Replanner

Fires when issues in a dependency level produce unrecoverable failures. The replanner:
- Sees full execution state across all issues
- Can skip downstream dependents
- Restructures remaining issue graph
- Reduces scope or aborts if necessary
- Receives previous replan decisions to prevent repeating failed strategies

**Graceful Degradation**: If the replanner crashes (LLM timeout, malformed output), the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation is better than fail-fast.

### Real-World Failure Examples

#### Deadlocks Beyond Retry
The `integration-tests` issue timed out after 2700 seconds. Tests were correct, but the CLI binary had an infinite loop. Retrying the same agent produced the same timeout. Solution: **block** the issue, record typed debt, let rest of build work around the gap.

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks; test suite correct but binary needs runtime debugging"
}
```

#### Review Catches Tests Miss
The `app-module` issue passed 119 tests and all acceptance criteria, but the code reviewer blocked it: the module was not exported in `lib.rs`. One missing `pub mod app;` line. Inner loop fixed it in iteration 2.

#### Regressions on Trivial Tasks
The `project-scaffold` issue (create `Cargo.toml` and `src/main.rs`) passed iteration 1 with 13 tests passing. Iteration 2 regressed: `main.rs` referenced 10 non-existent modules. Autonomous code generation fails unpredictably, even on simple tasks.

#### Cascading Verification Failures
The `final-acceptance-verification` issue required three iterations:
1. Found four blocking issues: `set -e` crashes, macOS-specific `stat` flags, infinite recursion, missing dependency checks
2. Fixed those but introduced new bug: `cargo fmt` check used `|| true`, always passing
3. Finally correct

---

## Cost-Effective Execution at Scale

### Checkpoint Everything

A 200+ invocation build costing $116 cannot restart from invocation 1 on failure. The system checkpoints at every level boundary, capturing:

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

### Isolation with Git Worktrees

Each issue gets its own [[git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`). In parallel execution:
- No lock contention
- No merge conflicts during coding
- Full isolation until integration

**Surprising Discovery**: Agents consistently produce finer-grained, more parallelizable issue graphs than humans would. The planner decomposed epics into 50-100 issues with dependency structures too complex for human coordination, but exactly the scheduling problem the orchestrator absorbs.

Between levels, a **merger agent** integrates completed branches. It is not mechanical `git merge`; it reads the architecture spec and file conflict annotations to make intent-aware resolution decisions. When two issues modify the same file, the merger understands each change's purpose and produces a result preserving both intents.

### Level Gating Sequence

Every level enforces a clean handoff:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code works together
3. **Debt gate**: