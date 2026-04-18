---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:18:20.608889
raw_file_updated: 2026-04-17T20:18:20.608889
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:18:20.608889
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively write, test, and review production code. The system introduces two core LLM integration primitives (constrained calls and autonomous harnesses), implements three nested failure recovery loops, and uses checkpoint-based execution to make expensive multi-agent builds survivable. Key findings show that [[system architecture]] matters more than model selection, and that carefully designed failure handling and state management enable complex coordination without human intervention during the execution phase.

---

## Overview

**Beyond Vibe Coding: How We Ship Production Code with 200 Autonomous Agents** is a technical case study by Santosh Kumar Radha (Co-founder & CTO at AgentField) describing the design and operational lessons from running large-scale multi-agent software engineering workflows.

The core insight is a shift in human responsibility: instead of engineers iterating line-by-line with a single [[AI assistant]], the system produces draft [[pull requests]] that have already passed multiple rounds of automated writing, testing, review, and verification. Human engineers move from the iteration loop to the review loop, approving finished work rather than guiding each step.

## The Core Problem: The Convergence Problem

When multiple autonomous agents work in parallel on a shared codebase, a critical issue emerges: **convergence**. The system's first production run with 30+ parallel agents produced a pull request where one agent built an entire API layer on a module that another agent never exported. Tests passed because dependencies were mocked. Code compiled. The architecture was broken.

This revealed that coordinating N autonomous processes into one coherent result requires:
- Primitives for [[isolation]]
- [[Failure recovery]] mechanisms
- [[State reconciliation]] systems

## Two Modes of LLM Integration

The system separates LLM access into two distinct primitives, each with different operational characteristics.

### 1. Constrained Calls (`.ai()`)

A **constrained call** is:
- Single-shot execution
- Structured input and output
- No tool use
- No iteration
- Predictable latency and cost

**Purpose**: Routing and classification decisions.

**Example use case**: "Does this issue need deeper QA?" answered in milliseconds for fractions of a cent.

**Output structure**: Each issue receives an `IssueGuidance` block containing:
- `needs_new_tests`: boolean
- `estimated_scope`: "small" | "medium" | "large"
- `touches_interfaces`: boolean
- `needs_deeper_qa`: boolean
- `agent_guidance`: string with context for downstream agents

This structured output allows downstream code to make routing decisions based on predictable, typed information.

### 2. Autonomous Harnesses (`.harness()`)

An **autonomous harness** is:
- Multi-turn execution
- Tool-using and goal-driven
- Full coding environment (filesystem, test runner, git)
- Iterates until producing a verifiable outcome
- Variable latency and cost

**Purpose**: Complex problem-solving that requires exploration and iteration.

**Example**: A single coder invocation on a complex issue in the diagrams-as-code build ran up to 150 tool-use turns and cost over $4.

**Capabilities**:
- Read and write files
- Run tests
- Execute arbitrary commands
- Discover failures and retry
- Access full git operations

The harness abstraction emerged from observing repeated patterns in production failures, not from theoretical design. It represents the abstraction the team wishes it had started with.

### Integration Pattern

The two primitives coexist. A boolean from a cheap `.ai()` call (`needs_deeper_qa`) determines routing:
- **Lean path**: coder → reviewer (2 calls)
- **Thorough path**: coder → QA and reviewer (parallel) → synthesizer (4 calls)

This keeps routing cheap while allowing expensive work to be proportional to need.

## Three Nested Failure Recovery Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three nested control loops to handle different failure types.

### Inner Loop: Per-Issue Iteration (up to 5 iterations)

The agent retries itself with feedback from [[QA]] and [[code review]].

**Example**: The `app-module` issue passed all 119 tests but failed review because the module was not exported in `lib.rs`. The inner loop caught this on iteration 2, added the export, and achieved 354 passing tests.

**Handles**: Problems the same agent can solve with better information.

### Middle Loop: Issue Advisor (5 typed recovery actions)

When the inner loop exhausts retries, an issue advisor activates with five possible actions:

| Action | Meaning |
|--------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria; record gap as typed [[technical debt]] |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., "use different library") |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Example**: The `integration-tests` issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The tests themselves were correct (review approved them), but retrying would never help. The advisor blocked the issue, recorded a typed debt item, and allowed the rest of the build to continue.

**Handles**: Failures that require changing strategy or scope.

### Outer Loop: Replanner (system-level restructuring)

When issues in a [[dependency graph|dependency level]] produce unrecoverable failures, a replanner fires with full execution state visibility.

**Capabilities**:
- Skip downstream dependents
- Restructure remaining issue graph
- Reduce scope
- Abort (if necessary)
- Prevent repeating failed strategies

**Default behavior**: If the replanner crashes (timeout, malformed output), the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation is better than fail-fast.

### Failure Examples from Production

#### Deadlocks That Retrying Cannot Fix

The `integration-tests` issue in the diagrams build timed out after 2700 seconds. The tests were well-written and passed review, but the underlying CLI binary had an infinite loop. Retrying the same agent on the same binary would produce the same timeout.

**Resolution**: Block the issue, record typed debt, continue the build.

#### Review Catches That Tests Miss

The `app-module` issue had 119 passing tests and met all acceptance criteria, but the code reviewer caught that the module was not exported in `lib.rs`. One missing `pub mod app;` line made the module invisible to library consumers.

**Resolution**: Inner loop fixed the export on iteration 2 with 354 passing tests.

#### Regressions on Trivial Tasks

The `project-scaffold` issue (literally "create Cargo.toml and src/main.rs") passed iteration 1 with 13 passing tests and review approval. Iteration 2 regressed: `main.rs` referenced 10 non-existent modules.

**Resolution**: The agent's attempt to be helpful introduced new bugs, caught by QA on iteration 2.

#### Cascading Verification Failures

The `final-acceptance-verification` issue required 3 iterations:
1. Iteration 1: Found four blocking issues (`set -e` crashes, macOS-specific `stat` flags, infinite recursion, missing dependency checks)
2. Iteration 2: Fixed those but introduced `|| true` making `cargo fmt` always pass
3. Iteration 3: Finally correct

**Resolution**: Multiple iterations through the inner loop, each fixing detected issues.

## Checkpoint-Based Execution

A 200-invocation build at $116 cost cannot restart from scratch on failure. The system treats multi-agent builds as long-running, expensive processes requiring durability primitives.

### Checkpoint Content

The checkpoint captures:
- Current execution level
- Completed levels
- All issues in the build
- Original plan summary
- Replan count
- Accumulated [[technical debt]]
- Git state (integration branch, original branch, initial SHA, worktree mappings)

**Example from diagrams build**:
```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": [
    "project-scaffold", "types-module", "error-module",
    "lexer", "parser", "validator",
    "layout-engine", "svg-renderer", "ascii-renderer",
    "smoke-test", "app-module", "cli-module",
    "integration-tests", "documentation", "final-acceptance-