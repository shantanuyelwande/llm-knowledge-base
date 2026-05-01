---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:46:55.528028
raw_file_updated: 2026-05-01T05:46:55.528028
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:46:55.528028
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[Claude Code]] instances to collaboratively generate, test, and review production code. The system addresses the convergence problem—ensuring N independent agents produce one coherent result—through two core LLM primitives, three nested failure recovery loops, and checkpoint-based execution. Key findings include the necessity of separating constrained classification calls from autonomous coding loops, implementing escalation hierarchies for failure recovery, and designing systems where architecture compensates for model capability through iteration rather than relying on model intelligence alone.

---

## Overview

[[AgentField]] has developed a production-grade system for orchestrating multiple autonomous code generation agents on shared codebases. Rather than having one engineer iterate with a single [[Claude Code]] session, the system coordinates dozens of parallel agent instances—called "harnesses"—each with full filesystem access, test execution capabilities, and git integration. This approach moves human responsibility from line-by-line iteration to final architectural review of completed, verified draft pull requests.

The system has been tested on real projects:
- **Diagrams-as-code CLI** (Rust): 15 issues, 200+ agent invocations, $116 total cost
- **Go SDK feature**: 10 issues, 80+ invocations, $19 total cost
- **Node.js benchmark**: 95/100 score on both cheapest and mid-tier models

---

## The Convergence Problem

The initial challenge emerged when running 30+ agents in parallel on a shared codebase. While individual pull requests appeared correct—tests passed, code compiled—the system did not actually function. One agent had built an entire API layer on a module that another agent never exported. Tests passed because the downstream agent had mocked the dependency.

This revealed the **convergence problem**: getting N autonomous processes to produce one coherent result requires explicit primitives for:
- **Isolation** between parallel agents
- **Failure recovery** when agents cannot proceed
- **State reconciliation** across the distributed system

---

## Two Modes of LLM Integration

The most critical architectural decision is separating [[LLM]] integration into two distinct primitives, each with different operational characteristics.

### Constrained Call (`.ai()`)

The **constrained call** is a single-shot, structured interaction with:
- **Fixed input/output format**: structured data, no arbitrary tool use
- **No iteration**: one call, one response
- **Predictable characteristics**: milliseconds latency, fractions of a cent cost
- **Deterministic routing**: downstream code switches on structured outputs

**Use cases**: routing decisions, classification, planning guidance

**Example output**:
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

### Autonomous Harness (`.harness()`)

The **autonomous harness** is a multi-turn, tool-using agent with:
- **Full coding environment**: filesystem, test runner, git integration
- **Iterative goal-seeking**: reads files, writes code, runs tests, discovers failures, retries
- **Unpredictable characteristics**: variable latency (minutes to hours), variable cost ($0.50–$4.26 per invocation)
- **Outcome-focused**: system checks what was delivered, not how it was obtained

**Use cases**: code generation, implementation, complex problem-solving

Both primitives coexist in the same system. A cheap `.ai()` classification call determines routing: does an issue need deeper QA? This boolean gates whether the issue takes a lean two-call path (coder → reviewer) or a thorough four-call path (coder → QA + reviewer in parallel → synthesizer).

---

## Three Nested Failure Recovery Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three nested control loops, each handling different failure modes.

### Inner Loop: Per-Issue Iteration (Up to 5 Attempts)

The inner loop runs a single agent with feedback from [[QA]] and code review. The agent retries with better information.

**Handled failure type**: Problems the same agent can solve given feedback

**Example**: The app-module issue had 119 passing tests and met all acceptance criteria, but the module was not exported in `lib.rs`. The code reviewer blocked the PR. Iteration 2 fixed the export with 354 passing tests.

### Middle Loop: Issue Advisor

When the inner loop exhausts its attempts (typically 5 iterations), an issue advisor activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., use different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Handled failure type**: Deadlocks where retrying the same approach produces the same failure

**Example**: The integration-tests issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The tests themselves were correct (passed code review), but the underlying code had a deadlock. Retrying would produce the same timeout. The advisor blocked the issue and recorded typed debt:

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

When issues in a dependency level produce unrecoverable failures, a replanner fires with visibility into the full execution state. It can:
- Skip downstream dependents of failed issues
- Restructure the remaining issue graph
- Reduce scope
- Abort the build

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes (LLM timeout, malformed output), the system defaults to **continue** rather than abort—for expensive workflows, graceful degradation is better than fail-fast.

---

## Debt Tracking

Instead of silently dropping failures or retrying endlessly, the system records typed, severity-rated debt items that downstream agents consume. When a dependent issue starts, it receives `debt_notes` explaining what upstream failed to deliver, allowing it to work around known gaps.

Example debt item structure:
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "description",
  "issue_name": "upstream issue",
  "severity": "high|medium|low",
  "justification": "why this gap exists"
}
```

This transforms failures from silent bugs into explicit, documented constraints that the rest of the system adapts to.

---

## Checkpoint-Based Execution

At $116 per build (diagrams project), restarting from scratch after a crash at invocation 140 is not viable. The system checkpoints at every level boundary, capturing:

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

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. The checkpoint also captures git state (integration branch, original branch, initial commit SHA, worktree directory mapping) for full workspace reconstruction.

### Git Worktree Isolation

Each issue gets its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This enables:
- **Parallel execution**: multiple issues modify different files simultaneously without lock contention
- **Isolation**: changes stay isolated until integration
- **Clean rollback**: failed issues do not corrupt the shared codebase

Between levels, a merger agent integrates completed branches into the integration branch. The merger is not mechanical `git merge`; it reads the architecture spec and file conflict annotations to make intent-aware resolution decisions.

### Level Gates

Between every level, a sequence of gates enforces clean handoffs:

1. **Merge gate**: integrate completed branches
2. **Integration test gate**: validate merged code still works together
3. **Debt gate**: process completed-with-debt results, propag