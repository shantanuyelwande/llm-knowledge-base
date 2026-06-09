---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-09T06:16:44.059954
raw_file_updated: 2026-06-09T06:16:44.059954
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-09T06:16:44.059954
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively ship production code through a structured system of verification loops, failure recovery mechanisms, and checkpoint-based execution. The work demonstrates that proper architecture can compensate for model capability, with cheaper models achieving equivalent results to expensive ones when paired with robust orchestration patterns.

## Overview

[[Multi-agent systems]] that coordinate autonomous processes on shared codebases face a critical challenge known as the **convergence problem**: getting N independent agents to produce one coherent result requires explicit primitives for isolation, failure recovery, and state reconciliation. The AgentField team discovered this through painful experience when their first 30+ parallel agent run produced code where agents built dependencies on modules never exported by other agents—tests passed due to mocking, but the system did not work.

The solution involved moving human responsibility from the iteration loop to the review loop, where engineers review finished, verified draft pull requests rather than guiding each individual change. This represents a fundamental shift in how [[AI-native engineering teams]] approach software development.

## Key Architectural Principles

### 1. Two Modes of LLM Integration

The most critical architectural insight is that multi-agent systems require two distinct LLM interaction patterns, not one:

#### Constrained Single-Shot Calls (`.ai()`)

- **Characteristics**: Single-turn, structured input/output, no tools, no iteration
- **Purpose**: Routing and classification decisions ("Does this issue need deeper QA?", "Is this change high-risk?")
- **Properties**: Predictable latency, predictable cost, verifiable outputs
- **Example Output**: Structured guidance blocks with fields like `needs_new_tests`, `estimated_scope`, `touches_interfaces`
- **Cost**: Fractions of a cent per call, milliseconds latency

#### Autonomous Harnesses (`.harness()`)

- **Characteristics**: Multi-turn, tool-using, goal-driven iteration
- **Capabilities**: Filesystem access, test execution, git operations, code writing
- **Behavior**: Receives a goal and toolset, iterates until producing verifiable outcome
- **Scope**: Reads files, writes code, runs tests, discovers failures, retries
- **Cost**: Can range from $0.50 to $4+ per invocation depending on issue complexity

The constrained call provides routing efficiency while the harness provides the actual work capability. Cheap routing decisions determine whether an issue takes a lean two-call path or a thorough four-call path, keeping the system both flexible and cost-efficient.

### 2. Nested Failure Recovery Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three nested control loops to handle different failure modes:

#### Inner Loop (Per-Issue Retry)

- **Scope**: Up to 5 iterations per issue
- **Mechanism**: Agent retries with feedback from [[Quality Assurance|QA]] and code review
- **Success Case**: Catches problems that the same agent can solve with better information
- **Example**: Missing module export in Rust codebase caught and fixed on iteration 2

#### Middle Loop (Issue Advisory)

Activates when the inner loop exhausts all retries. Provides five typed recovery actions:

| Action | Mechanism |
|--------|-----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

#### Outer Loop (Replanner)

Activates when issues produce unrecoverable failures. Capabilities include:

- Full execution state visibility
- Skip downstream dependents
- Restructure remaining issue graph
- Reduce scope or abort
- Learn from previous replan decisions to prevent repeating failed strategies
- Default to **continue** rather than abort on LLM failures (graceful degradation for expensive workflows)

#### Real-World Failure Examples

**Deadlock Scenario**: Integration tests timed out after 2700 seconds. Tests were correct but the CLI binary had an infinite loop. Retrying would never help because the same agent would produce the same binary with the same deadlock. Solution: Block the issue, record typed debt item, let rest of build work around the gap.

**Review Catch**: App module had 119 passing tests and met all acceptance criteria, but was not exported in `lib.rs`, making it inaccessible to library consumers. Caught by code reviewer, fixed in iteration 2 with 354 tests passing.

**Regression on Trivial Tasks**: Project scaffold issue passed iteration 1 but regressed in iteration 2 when the agent added module declarations for code that did not exist yet.

**Cascading Failures**: Final acceptance verification required three iterations—first fixing `set -e` crashes and infinite recursion, then fixing `|| true` making cargo fmt always pass, finally getting it right.

### 3. Durable Execution Through Checkpointing

At $116 per build, restarting from scratch is not viable. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint-based recovery.

#### Checkpoint Scope

Captures at every level boundary:

- Current execution level
- Completed levels
- Full issue list
- Original plan summary
- Replan count
- Accumulated debt items
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)

#### Resume Mechanism

`resume_build()` loads checkpoint, skips completed levels, and continues from exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0.

#### Git Worktree Isolation

Each issue gets its own git worktree on a dedicated branch (e.g., `issue/01-project-scaffold`, `issue/02-types-module`). In the diagrams build, level 2 ran three issues in parallel, each in its own worktree, modifying different files with no lock contention.

#### Merge Gate Sequence

Between levels, a merger agent integrates completed branches into the integration branch. The merger is not mechanical—it reads architecture specs and file conflict annotations to make intent-aware resolution decisions.

#### Gate Sequence Between Levels

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

### 4. Typed Debt Tracking

Rather than silently dropping failures or aborting builds, the system records structured debt items:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, allowing them to work around known gaps instead of building on false assumptions.

## Architectural Performance

### Model Selection vs. Architecture

Contrary to initial assumptions, model capability is less important than orchestration architecture. On a benchmark (Node.js CLI todo app), the same architecture scored **95/100** with both:

- Claude Haiku (cheapest model, ~$20 total)
- MiniMax M2.5 via OpenRouter (~$6 total)

Single-agent approaches on the same task scored 59-73. The architecture compensates for model capability through iteration: more inner loop cycles, cheaper per cycle, same outcome.

Model configuration is a flat map allowing independent assignment:

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

### Real Build Metrics

**Diagrams-as-Code CLI (Rust)**:
- 15 issues across 6 dependency levels
- 200+ agent invocations
- 157 log files
- Total cost: $116
- Architect: $0.83 for 9 turns
- Coding agents: $0.50-$4.26 per invocation
- QA (integration tests): $4.26

**Go SDK Feature**:
- 10 issues