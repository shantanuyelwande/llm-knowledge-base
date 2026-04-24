---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T04:59:43.032180
raw_file_updated: 2026-04-24T04:59:43.032180
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T04:59:43.032180
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article explores the architectural patterns and lessons learned from orchestrating 200+ autonomous [[LLM]] agents to collaboratively generate, test, and review production code. Rather than relying on increasingly sophisticated models, the approach demonstrates that **architecture beats model selection** through systematic failure recovery, checkpoint-based execution, and two distinct modes of [[LLM integration]].

---

## Overview

[[AgentField]] developed a system called **SWE-AF** that enables dozens of [[autonomous agent]] instances to coordinate in parallel on a shared codebase, moving human engineers from iterative line-by-line guidance to architectural review of completed, verified draft [[pull requests]]. The system successfully generated production code across multiple languages (Rust, Go, Node.js) while managing the complexity of coordinating independent agents on shared resources.

The core insight: effective multi-agent orchestration requires explicit primitives for isolation, failure recovery, and state reconciliation rather than hoping that more capable models will naturally coordinate.

---

## Key Concepts

### Two Modes of LLM Integration

Rather than giving all agents identical access to [[LLM]] capabilities, the architecture separates integration into two complementary primitives:

#### Constrained Single-Shot Calls (`.ai()`)

- **Characteristics**: Single-turn, structured input/output, no tool use, no iteration
- **Purpose**: Routing, classification, and decision-making with predictable latency and cost
- **Example use cases**: 
  - Determining if an issue needs deeper QA
  - Assessing whether a change is high-risk
  - Generating guidance blocks for downstream agents
- **Cost profile**: Fractions of a cent, milliseconds latency
- **Output structure**: Typed, machine-readable guidance that downstream processes can switch on

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

- **Characteristics**: Multi-turn, tool-using, goal-driven iteration loops
- **Environment**: Full coding environment with filesystem access, test execution, and [[git]] integration
- **Purpose**: Complex problem-solving requiring experimentation, failure recovery, and adaptive strategies
- **Behavior**: Reads files, writes code, runs tests, discovers failures, and iterates
- **Cost profile**: Variable, ranging from $0.50 to $4+ per invocation depending on issue complexity
- **Success metric**: Verifiable outcome, not the path taken to reach it

The harness abstraction emerged from observing repeated patterns in production failures rather than from theoretical design. It represents the abstraction that teams wish they had from the start when building multi-agent systems.

---

## Failure Management Architecture

In a 200+ invocation build, failures are the normal path, not edge cases. The system manages failures through a **three-nested control loop** hierarchy:

### Inner Loop: Per-Issue Iteration (up to 5 attempts)

- **Scope**: Single issue retry with feedback from [[QA]] and code review
- **Mechanism**: Agent receives structured feedback and attempts to fix identified problems
- **Success example**: The app-module issue, where a missing `pub mod app;` export in `lib.rs` was caught by review and fixed on iteration 2
- **Handles**: Problems that the same agent can solve with better information

### Middle Loop: Issue Advisor with Recovery Actions

Activates when the inner loop exhausts its retries. Provides five typed recovery strategies:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., use different library) |
| `SPLIT` | Break issue into smaller sub-issues for parallel execution |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Typed Debt Structure**: Rather than silent failures or log messages, the system records debt as structured data:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, enabling them to work around known gaps instead of building on false assumptions.

### Outer Loop: Replanner for Structural Failures

- **Scope**: Full execution state, dependency graph restructuring
- **Triggers**: When issues produce unrecoverable failures at a dependency level
- **Capabilities**: Skip downstream dependents, restructure issue graph, reduce scope, or abort
- **Memory**: Previous replan decisions fed back to prevent repeating failed strategies
- **Graceful degradation**: Defaults to `continue` rather than `abort` on LLM timeouts or malformed output

### Failure Case Studies

**Deadlock Recovery**: Integration-tests issue timed out after 2700 seconds. The tests were correct, but the CLI binary had an infinite loop. Retrying would never help because the same agent would produce the same broken binary. The system **blocked** the issue, recorded typed debt, and let dependent work continue around the gap.

**Review Catches What Tests Miss**: The app-module issue passed 119 tests and met all acceptance criteria, but was not exported in `lib.rs`, making it inaccessible to library consumers. The code review caught what automated testing missed, and iteration 2 fixed the export.

**Regressions on Trivial Tasks**: The project-scaffold issue (create Cargo.toml and src/main.rs) passed iteration 1 but regressed in iteration 2 when the coder added non-existent module declarations. Autonomous code generation fails in unpredictable ways even on simple tasks.

**Cascading Verification Failures**: The final-acceptance-verification issue required three iterations to pass: iteration 1 found four blocking issues, iteration 2 introduced a new bug with `cargo fmt` checking, iteration 3 finally succeeded.

---

## Durable Execution and State Management

Building at scale ($116 for the diagrams-as-code project, 200+ invocations) requires treating multi-agent builds as long-running, expensive processes that can fail at any point. The system applies [[checkpoint]]-based recovery patterns from high-performance computing.

### Checkpoint Strategy

Checkpoints capture full execution state at every level boundary, enabling resumption without restarting from the beginning:

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

**Recovery mechanism**: `resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0.

**Git state preservation**: Checkpoint captures git state (integration branch, original branch, initial commit SHA, worktree directory mapping) so resumed builds can reconstruct the full workspace without re-cloning.

### Isolation with Git Worktrees

Each issue receives a dedicated [[git worktree]] on its own branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.), enabling true parallel execution without lock contention or merge conflicts during coding.

**Planning advantage**: The system generates finer-grained, more parallelizable issue graphs than humans typically would, decomposing epics into 50-100 issues with dependency structures that would be impractical for humans to coordinate but are natural for orchestrators.

### Level Gates

Between every dependency level, a sequence of gates enforces clean handoffs:

1. **Merge gate**: Integrate completed branches using intent-aware conflict resolution
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any issue