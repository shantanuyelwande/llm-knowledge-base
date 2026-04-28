---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-28T05:36:09.169815
raw_file_updated: 2026-04-28T05:36:09.169815
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-28T05:36:09.169815
tags: []
related_topics: []
backlinked_by: []
---
# Beyond Vibe Coding: Orchestrating Autonomous Agents in Production

## Summary

This article documents how [[AgentField]] successfully orchestrated over 200 autonomous [[LLM]]-powered agents to ship production code through a shared codebase. The key innovation involves separating [[LLM]] integration into two distinct primitives—constrained single-shot calls (`.ai()`) and autonomous harnesses (`.harness()`)—combined with three nested failure recovery loops and checkpoint-based execution. The approach achieved production-quality results on multiple real-world projects including a Rust CLI tool, Go SDK, and Node.js benchmark, while demonstrating that architectural design matters more than raw model capability.

## Overview

Traditional approaches to [[AI agent]] systems treat all LLM interactions uniformly, leading to unpredictable costs, latency, and failure modes. AgentField's engineering team discovered that production-grade multi-agent code generation requires fundamentally different abstractions than single-agent systems.

The core insight: moving human responsibility from the iteration loop (guiding each change) to the review loop (approving finished, verified draft PRs) requires robust primitives for [[agent coordination]], failure recovery, and state reconciliation.

## Key Architectural Principles

### Two Modes of LLM Integration

Rather than a single unified LLM interface, production systems require two complementary primitives:

#### Constrained Calls (`.ai()`)

**Purpose**: Routing and classification with predictable behavior

**Characteristics**:
- Single-shot execution with no iteration
- Structured input and output
- No tool use
- Deterministic latency (milliseconds)
- Minimal cost (fractions of a cent)
- Predictable outputs for downstream routing

**Use cases**:
- Issue classification ("Does this need deeper QA?")
- Risk assessment ("Is this change high-risk?")
- Planning and guidance generation
- Intent-aware decision making

**Example output**:
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

**Purpose**: Goal-driven iteration with full coding environment access

**Characteristics**:
- Multi-turn execution with tool use
- Full filesystem, test runner, and [[git]] access
- Iterative problem-solving until verifiable outcome
- Variable latency and cost (depends on task complexity)
- Observable execution trace

**Capabilities**:
- Read and write code files
- Execute test suites
- Discover failures and retry
- Commit and push changes
- Integrate with CI/CD systems

**Example**: A single coder harness invocation on a complex issue ran up to 150 tool-use turns, costing over $4.

### The Convergence Problem

When multiple autonomous agents operate on a shared codebase simultaneously, they risk producing code that:
- Compiles and passes tests individually
- Fails when integrated due to missing exports or broken dependencies
- Appears correct in code review but does not function

The solution requires explicit primitives for:
- **Isolation**: Separate working directories and branches
- **Failure recovery**: Typed, severity-rated debt tracking
- **State reconciliation**: Intent-aware merging and verification

## Failure Recovery: Three Nested Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. Robust multi-agent systems require three escalating levels of failure recovery:

### Inner Loop: Per-Issue Iteration (Up to 5 iterations)

**Scope**: Single issue with feedback from [[QA agent|QA]] and [[code review]] agents

**Behavior**: The same agent retries with better information

**Success criteria**: 
- All acceptance criteria met
- Tests pass
- Code review approved

**Failure handling**: Produces detailed feedback for next iteration

**Example**: The app-module issue had all 119 tests passing but was missing a `pub mod app;` export in `lib.rs`. The inner loop caught this architectural violation and fixed it in iteration 2.

### Middle Loop: Issue Advisor (Escalation when inner loop exhausted)

**Scope**: Single issue that has failed all inner loop attempts

**Typed recovery actions**:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria; record gaps as typed debt |
| `RETRY_APPROACH` | Keep criteria; try different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

**Decision making**: Final invocation prompt explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retries.

**Example**: The integration-tests issue hit an infinite loop deadlock in the CLI binary. After two failed attempts, the advisor blocked the issue and recorded it as typed debt:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

### Outer Loop: Replanner (Dependency-level restructuring)

**Scope**: Full issue graph when failures cascade across dependency levels

**Capabilities**:
- Skip downstream dependents
- Restructure remaining issue graph
- Reduce scope
- Abort if necessary
- Consume previous replan decisions to avoid repeating failed strategies

**Default behavior**: Continue rather than abort on LLM failures (graceful degradation for expensive workflows)

**Debt propagation**: Downstream agents receive `debt_notes` explaining what upstream failed to deliver, enabling workarounds instead of broken assumptions

## Production Durability: Checkpoint-Based Execution

At $116 per build (200+ invocations), restarting from failure is economically unviable. The system treats long-running multi-agent workflows like [[high-performance computing]] jobs: checkpointing is a survival requirement, not an optimization.

### Checkpoint Contents

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
  "original_plan_summary": "15 issues organized in 6 levels that maximize parallelism while respecting dependencies...",
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

### Checkpoint Recovery

- Load checkpoint at failure point
- Skip completed levels
- Resume from exact failure point
- Reconstruct full workspace without re-cloning
- A 30-minute build failing at minute 25 does not restart from minute 0

### Git Worktree Isolation

Each issue operates in its own [[git]] worktree on a dedicated branch:
- `issue/01-project-scaffold`
- `issue/02-types-module`
- `issue/03-error-module`

**Benefits**:
- No lock contention during parallel coding
- No merge conflicts until intentional integration
- Clean isolation of changes per issue

**Between-level gates**:
1. Merge gate: integrate completed branches
2. Integration test gate: validate merged code works together
3. Debt gate: process completed-with-debt results
4. Split gate: inject sub-issues if needed
5. Replan gate: invoke replanner if failures escalated
6. Checkpoint: serialize full state to disk

### Unified API Interface

The control plane provides a single endpoint regardless of which agents are spawned or how many:

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