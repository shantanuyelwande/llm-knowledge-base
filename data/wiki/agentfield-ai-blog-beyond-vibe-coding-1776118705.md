---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-23T04:56:10.280014
raw_file_updated: 2026-04-23T04:56:10.280014
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-23T04:56:10.280014
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation: Orchestrating Autonomous Agents for Production Software

## Summary

This article explores how to coordinate multiple autonomous [[Large Language Models|LLM]] instances to collaboratively produce production-ready code. Rather than relying on a single "smart" model, the approach uses architectural patterns—two distinct LLM integration modes, nested failure recovery loops, and checkpoint-based execution—to enable 200+ agents to work in parallel on a shared codebase while maintaining coherence and cost efficiency.

## Overview

The traditional approach to [[AI-assisted software development]] pairs a single engineer with a single [[Claude Code]] session, where the human guides each iteration. [[AgentField]] inverts this relationship: dozens of autonomous agents coordinate in parallel, with humans reviewing finished, verified drafts rather than guiding line-by-line changes. This shift moves human responsibility from the iteration loop to the architectural review loop.

The core challenge is the **convergence problem**: getting N autonomous processes to produce one coherent result requires explicit primitives for isolation, failure recovery, and state reconciliation. The team's solution emerged from production experience rather than theoretical design, particularly through building [[SWE-AF]] (Software Engineering Agent Framework), which was tested on real projects including a 15-issue Rust CLI tool, a Go SDK feature, and a Node.js benchmark.

## Key Concepts

### Two Modes of LLM Integration

Rather than giving every agent identical access to tools and iteration time, the system separates LLM calls into two distinct primitives:

#### Constrained Calls (`.ai()`)

Single-shot calls with structured input and output, no tools, and no iteration. These handle:
- Routing and classification decisions
- Risk assessment ("Is this change high-risk?")
- Scope estimation
- Guidance generation for downstream agents

**Characteristics:**
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Outputs that downstream code can reliably switch on
- Deterministic behavior

**Example output:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Loops (`.harness()`)

Multi-turn, tool-using, goal-driven agents that receive a goal and toolset, then iterate until producing a verifiable outcome. These handle:
- [[Code generation]]
- Test writing and execution
- Failure discovery and recovery
- Implementation iteration

**Characteristics:**
- Full coding environment access (filesystem, test runner, [[Git]])
- Variable latency and cost based on task complexity
- Up to 150 tool-use turns on complex issues
- Verification-driven iteration

**Distinction:** While constrained calls are common in agentic frameworks, the harness abstraction emerged from production failure patterns rather than theoretical design. It represents the abstraction the team wished existed from the start.

### Failure Recovery Architecture

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three nested control loops, each with different escalation strategies:

#### Inner Loop (Per-Issue Iteration)

- **Scope:** Single issue, up to 5 iterations maximum
- **Participants:** Coder agent, QA verification, code review
- **Success criteria:** Acceptance criteria met, tests passing, code review approved
- **Failure handling:** Agent retries with feedback from QA and review

**Example:** The `app-module` issue passed 119 tests and met all criteria in iteration 1, but code review caught a missing `pub mod app;` export in `lib.rs`. Iteration 2 fixed the export with 354 tests passing.

#### Middle Loop (Issue Advisory)

Activates when the inner loop exhausts retries. The issue advisor has five typed recovery actions:

| Action | Response |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

**Example:** The `integration-tests` issue timed out after 2700 seconds with an infinite loop in the CLI binary. Rather than retry (which would produce the same deadlock), the system blocked the issue and recorded:
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging"
}
```

#### Outer Loop (Replanning)

Fires when issues in a dependency level produce unrecoverable failures. The replanner:
- Views full execution state
- Can skip downstream dependents
- Restructures remaining issue graph
- Reduces scope or aborts if necessary
- Receives feedback on previous replan decisions to prevent repeating failed strategies

**Default behavior:** If the replanner itself crashes due to timeout or malformed output, the system defaults to continue rather than abort—graceful degradation is preferable to fail-fast for expensive workflows.

### Failure Pattern Examples

**Deadlocks that retrying cannot fix:** The integration-tests issue had an infinite loop in the CLI binary. Retrying the same agent produced the same timeout. Solution: block and record typed debt.

**Review catches that tests miss:** The app-module issue had all 119 tests passing and met acceptance criteria, but the module wasn't exported in `lib.rs`, making it inaccessible to consumers. Solution: inner retry loop caught it; iteration 2 fixed the export.

**Regressions on trivial tasks:** The project-scaffold issue (create Cargo.toml and src/main.rs) passed iteration 1 with all 13 tests passing but regressed in iteration 2 when the coder added module declarations for non-existent code. Solution: inner loop detected and fixed.

**Cascading verification failures:** The final-acceptance-verification issue required three iterations: iteration 1 found four blocking issues, iteration 2 introduced a new bug with `|| true` masking unformatted code, iteration 3 finally passed.

## Durable Execution: Making Expensive Builds Survivable

At $116 per 200+ invocation build, a crash at invocation 140 cannot mean restarting from invocation 1. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint-based recovery.

### Checkpointing Strategy

Every level boundary captures full execution state:

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

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 resumes from minute 25, not minute 0.

The checkpoint also captures:
- [[Git]] state (integration branch, original branch, initial commit SHA, worktree directory mapping)
- Workspace configuration for reconstruction without re-cloning
- All accumulated debt items and typed failure records

**Principle:** Longer workflows accumulate more recovery points, not more fragility.

### Git Worktree Isolation

Each issue gets its own [[Git]] worktree on a dedicated branch:
- `issue/01-project-scaffold`
- `issue/02-types-module`
- `issue/03-error-module`
- etc.

**Benefits:**
- No lock contention between parallel agents
- No conflicts during coding (each agent modifies different files)
- Clean isolation until merge time
- Enables fine-grained parallelization

**Surprising finding:** Agents consistently produce finer-grained, more parallelizable issue graphs than humans would. The diagrams build was decomposed into 15 issues across 6 dependency levels, with level 2 running three issues in parallel (lexer, parser, validator) each in its own wor