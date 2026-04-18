---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-18T13:51:01.116713
raw_file_updated: 2026-04-18T13:51:01.116713
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-18T13:51:01.116713
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively write and review production code. The key innovation is separating LLM integration into two modes: constrained single-shot calls (`.ai()`) for routing and classification, and autonomous harnesses (`.harness()`) for iterative development work. The system manages agent failures through three nested control loops and uses checkpoint-based execution to survive expensive, long-running builds. Architecture and failure recovery prove more impactful than model selection.

---

## Overview

[[Vibe coding]] refers to writing code without systematic verification or structured processes—relying on intuition rather than rigorous testing and review. Beyond vibe coding requires moving the human role from line-by-line iteration to architectural review of finished, verified [[pull requests]].

[[AgentField]] and its reference implementation, [[SWE-AF]] (Software Engineering Agent Framework), enable teams to run dozens of [[Claude Code]] instances in parallel on a shared codebase. Instead of one engineer iterating with one [[LLM]] session, multiple autonomous agents coordinate across dependency-ordered issues while maintaining code coherence.

### The Convergence Problem

The first challenge in multi-agent systems is the **convergence problem**: getting N autonomous processes to produce one coherent result. Early attempts revealed critical gaps:

- One agent built an entire [[API]] layer on a module another agent never exported
- Tests passed because the downstream agent mocked the missing dependency
- Code compiled and pull requests looked clean, but the system did not function

This failure revealed the need for explicit primitives for [[isolation]], [[failure recovery]], and [[state reconciliation]].

---

## Architecture: Two Modes of LLM Integration

### The Core Innovation

The most common architectural mistake in multi-agent systems is giving every agent identical [[LLM]] access. When every call can use any tool, take unlimited time, and produce any output shape, operational reasoning becomes impossible: you cannot set [[SLA|SLAs]], predict costs, or design meaningful retry logic.

The solution is separating [[LLM]] integration into two distinct primitives.

### Constrained Call: `.ai()`

The **constrained call** is a single-shot operation with:
- **Structured input and output** - defined schema
- **No tool use** - classification only
- **Predictable latency** - milliseconds
- **Predictable cost** - fractions of a cent

Constrained calls handle routing and classification decisions. During [[planning]], each issue receives a guidance block:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive downstream routing. The `agent_guidance` string carries context for subsequent agents. This pattern maps directly to [[AgentField]]'s `.ai()` primitive.

### Autonomous Harness: `.harness()`

The **autonomous harness** is a multi-turn, tool-using, goal-driven loop that:
- Receives a goal and toolset
- Iterates until producing verifiable outcomes
- Reads and writes files
- Runs tests and discovers failures
- Retries with learned context

A harness operates in a full coding environment (filesystem, test runner, [[git]]) and may execute 50-150 tool-use turns on complex issues, costing $4+ per invocation. The harness abstraction emerged from watching builds fail repeatedly, not from theoretical design.

### Integration Pattern

The two primitives coexist. A boolean from a cheap `.ai()` call (e.g., `needs_deeper_qa`) determines whether an issue follows a lean two-call path (coder → reviewer) or a thorough four-call path (coder → QA and reviewer in parallel → synthesizer).

This design philosophy—extracting abstractions from recurring failure patterns rather than inventing them theoretically—informed [[AgentField]]'s broader architecture.

---

## Failure Recovery: Three Nested Control Loops

In a 200+ invocation build, failures are normal, not edge cases. The system requires three nested control loops to handle different failure modes.

### The Inner Loop: Per-Issue Iteration

**Scope:** Single issue, up to 5 iterations  
**Agents:** Coder, QA, Reviewer  
**Recovery:** Retry with feedback

The inner loop handles problems that the same agent can solve with better information. Example: the `app-module` issue passed 119 tests but failed code review because it was not exported in `lib.rs`. Iteration 2 fixed the export with 354 tests passing.

### The Middle Loop: Issue Advisor

**Scope:** When inner loop exhaustion occurs  
**Agents:** Advisor with five typed recovery actions  
**Recovery:** Escalate or accept with debt

When an issue exhausts its inner loop retries, an advisor activates with five possible actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria; record gaps as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; document each gap with type and severity |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

Example: The `integration-tests` issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The test suite itself was correct and passed review, but retrying would reproduce the same timeout. The advisor blocked the issue and recorded it as typed debt:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining upstream failures, allowing them to work around known gaps instead of building on false assumptions.

### The Outer Loop: Replanner

**Scope:** When issues in a dependency level produce unrecoverable failures  
**Agents:** Replanner with full execution state visibility  
**Recovery:** Skip dependents, restructure graph, reduce scope, or abort

The replanner sees the complete execution state and can:
- Skip downstream dependents of failed issues
- Restructure the remaining [[dependency graph]]
- Reduce overall scope
- Abort the build

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes, the system defaults to **continue** rather than abort—graceful degradation is better than fail-fast for expensive workflows.

### Failure Mode Examples

**Deadlocks that retrying cannot fix:** The `integration-tests` issue deadlocked; retrying would produce identical failure.

**Review catches that tests miss:** The `app-module` issue had 119 passing tests but was not exported. Code review caught the architectural issue; iteration 2 fixed it.

**Regressions on trivial tasks:** The `project-scaffold` issue regressed on iteration 2, adding module declarations for nonexistent code despite passing iteration 1.

**Cascading verification failures:** The `final-acceptance-verification` issue required 3 iterations, discovering `set -e` crashes, macOS-specific flags, infinite recursion, missing dependency checks, and incorrect `cargo fmt` logic.

---

## Durability: Checkpoint-Based Execution

At $116 per build, restarting from failure point 1 is economically unviable. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint recovery from the start.

### Checkpoint Strategy

The system checkpoints at every dependency level boundary. A typical checkpoint captures:

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

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0.

The checkpoint also