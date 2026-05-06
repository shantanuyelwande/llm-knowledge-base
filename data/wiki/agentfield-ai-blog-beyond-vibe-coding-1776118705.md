---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-06T05:34:37.097487
raw_file_updated: 2026-05-06T05:34:37.097487
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-06T05:34:37.097487
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article describes how [[AgentField]] orchestrates 200+ autonomous [[Large Language Model|LLM]] agents to collaboratively generate production code. The key innovation involves separating LLM integration into two distinct primitives: constrained single-shot calls (`.ai()`) for routing and classification, and autonomous harnesses (`.harness()`) for iterative coding tasks. The system manages agent failures through three nested control loops, uses [[Git]] worktrees for isolation, and implements checkpoint-based execution to survive expensive multi-hour builds. Real-world results show that architecture design and failure recovery matter more than model capability—the same system achieved 95/100 performance on both the cheapest and mid-tier models.

---

## Core Concepts

### Two LLM Integration Primitives

The fundamental architectural insight is that multi-agent systems require two distinct modes of [[Large Language Model|LLM]] access, not one:

#### Constrained Single-Shot Calls (`.ai()`)

- **Purpose**: Routing, classification, and structured decision-making
- **Characteristics**:
  - Single turn, no iteration
  - Structured input and output
  - No tool use
  - Predictable latency (milliseconds)
  - Predictable cost (fractions of a cent)
- **Example Use Cases**:
  - Determining if an issue needs deeper QA
  - Assessing if a change is high-risk
  - Generating guidance blocks for downstream agents

The constrained call produces typed outputs that downstream code can reliably switch on, enabling cost-efficient routing without sacrificing determinism.

#### Autonomous Harnesses (`.harness()`)

- **Purpose**: Complex, iterative coding tasks requiring full development environments
- **Characteristics**:
  - Multi-turn, goal-driven iteration
  - Full tool access (filesystem, test runners, version control)
  - Verifiable outcomes (tests pass, code compiles)
  - Variable latency and cost depending on complexity
  - Up to 150+ tool-use turns on complex issues
- **Example Use Cases**:
  - Writing and debugging code implementations
  - Running test suites and iterating on failures
  - Refactoring and optimization tasks

The harness abstraction emerged from observing real build failures rather than from theoretical design. It represents the abstraction the [[AgentField]] team wished they had from the start.

### The Convergence Problem

When multiple autonomous agents operate on a shared codebase, they face the **convergence problem**: getting N independent processes to produce one coherent result. The canonical failure case occurred when one agent built an entire API layer on a module that another agent never exported. Tests passed because the downstream agent mocked the dependency, but the system did not actually work.

This problem requires explicit primitives for:
- **Isolation**: Preventing agents from interfering with each other's work
- **Failure recovery**: Distinguishing between retryable and unrecoverable failures
- **State reconciliation**: Merging parallel work back into a coherent codebase

---

## Failure Management and Control Loops

### Three Nested Control Loops

The system manages agent failures through a hierarchy of escalating intervention levels:

#### Inner Loop: Per-Issue Iteration

- **Scope**: Single issue, up to 5 iterations
- **Mechanism**: Agent retries with feedback from [[Quality Assurance|QA]] and code review
- **Success Criteria**: Issue passes automated testing and review approval
- **Example**: The app-module issue where a missing `pub mod app;` export was caught by review and fixed on iteration 2

This loop handles problems that the same agent can solve given better information or feedback.

#### Middle Loop: Issue Advisor

When the inner loop exhausts retries, an issue advisor activates with five typed recovery actions:

| Action | Mechanism |
|--------|-----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gaps as typed debt |
| `RETRY_APPROACH` | Keep criteria, use different strategy (e.g., different library) |
| `SPLIT` | Decompose issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The advisor's final invocation includes an explicit warning that this is the last chance, biasing decisions toward acceptance or escalation rather than futile retries.

#### Outer Loop: Replanner

- **Trigger**: Unrecoverable failures in a dependency level
- **Scope**: Full execution state, remaining issue graph
- **Actions**: Skip downstream dependents, restructure issues, reduce scope, abort
- **Memory**: Feeds previous replan decisions back to prevent repeating failed strategies

If the replanner itself crashes, the system defaults to **continue** rather than abort, favoring graceful degradation over fail-fast semantics for expensive workflows.

### Failure Patterns in Practice

The diagrams-as-code build (15 issues, 200+ invocations, $116 total cost) illustrated several failure categories:

**Deadlocks That Retrying Cannot Fix**
- Integration tests timed out after 2700 seconds due to an infinite loop in the CLI binary
- Retrying the same agent produced the same failure
- Solution: Block the issue, record typed debt, let dependent issues work around the gap

**Review Catches That Tests Miss**
- Code passed 119 tests and met all acceptance criteria
- But the module was not exported in `lib.rs`, violating Rust conventions
- Tests could not catch this because they were all internal
- Solution: Inner loop fixed the export on iteration 2 (354 tests passing)

**Regressions on Trivial Tasks**
- Project scaffold passed iteration 1 (13 tests, successful build, review approval)
- Iteration 2 regressed: main.rs referenced non-existent modules
- Solution: The system caught the regression and required another fix cycle

**Cascading Verification Failures**
- Final acceptance verification required 3 iterations
- Iteration 1: Found 4 blocking issues (set -e crashes, platform-specific stat flags, infinite recursion, missing dependency checks)
- Iteration 2: Fixed those but introduced new bug (|| true making cargo fmt always pass)
- Iteration 3: Finally correct

### Typed Debt Tracking

When issues cannot be resolved, the system records **typed debt items** rather than silently dropping failures:

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

---

## Execution Durability and Checkpointing

### Checkpoint-Based Execution

At $116 per build with 200+ invocations, a crash at invocation 140 cannot mean restarting from invocation 1. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint recovery.

**Checkpoint Scope**:
- Current execution level and completed levels
- Full issue graph and original plan summary
- Replan count and accumulated debt items
- [[Git]] state (integration branch, original branch, initial commit SHA, worktree mappings)

**Resume Mechanism**:
- `resume_build()` loads the checkpoint
- Skips all completed levels
- Continues from exact failure point
- Reconstructs full workspace without re-cloning

A 30-minute build failing at minute 25 resumes from minute 25, not minute 0. Durable execution inverts the fragility relationship: longer workflows accumulate more recovery points rather than more vulnerability to interruption.

### Git Worktree Isolation

Each issue gets a dedicated [[Git]] worktree on its own branch (e.g., `issue/01-project-scaffold`, `issue/02-types-module`). This pattern:

- Prevents lock contention and conflicts during parallel coding
- Allows multiple agents to modify different files simultaneously
- Enables fine-grained issue decomposition (50-100 issues per epic)

The diagrams build's level 2 ran three issues in parallel (lexer, parser, validator), each in its own worktree, each modifying different files with zero conflicts.

### Level Gates and Handoffs

Between execution levels, a sequence of gates enforces clean handoffs:

1. **Merge Gate**: Integrate completed branches using intent-aware resolution
2. **Integration Test Gate**: Validate merged code still works together
3. **Debt Gate**: Process completed-with-debt results, propagate debt_notes downstream