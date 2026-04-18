---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:57:09.508997
raw_file_updated: 2026-04-17T20:57:09.508997
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:57:09.508997
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents the architectural patterns and lessons learned from orchestrating 200+ autonomous [[AI agent|AI agents]] to collaboratively produce production code. The system, called [[SWE-AF]], demonstrates how proper abstractions for [[LLM integration]], [[failure recovery]], and [[state management]] can enable autonomous software engineering at scale. Key insights include the necessity of two distinct LLM primitives, a three-level nested failure hierarchy, and checkpoint-based execution for cost-effective long-running builds.

---

## Overview

[[AgentField]] is an infrastructure platform that enables teams to coordinate multiple [[autonomous agents]] working on shared codebases. Rather than having individual engineers iterate with single [[AI coding assistant|AI coding assistants]], the system orchestrates dozens of [[Claude Code]] instances in parallel, each operating on isolated branches of a [[git]] repository while maintaining coherence through structured coordination.

The fundamental shift in responsibility is from **iteration** to **review**: instead of engineers guiding each incremental change, they review completed, verified draft [[pull requests]] that have already undergone multiple rounds of automated writing, testing, and verification.

## Core Architecture

### Two Modes of LLM Integration

The most critical architectural insight is that multi-agent systems require two fundamentally different types of [[LLM]] access, not one:

#### Constrained Single-Shot Calls (`.ai()`)

- **Characteristics**: Single-turn, structured input/output, no tool use, no iteration
- **Purpose**: Routing, classification, and decision-making
- **Cost**: Fractions of a cent, milliseconds latency
- **Use cases**: 
  - Determining issue scope and complexity
  - Risk assessment ("Is this change high-risk?")
  - Routing decisions based on structured criteria
  - Generating guidance blocks with typed fields

Example guidance output:
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Loops (`.harness()`)

- **Characteristics**: Multi-turn, tool-using, goal-driven iteration
- **Purpose**: Performing actual work (coding, testing, debugging)
- **Cost**: Higher per invocation ($0.50-$4.26 per issue depending on complexity)
- **Capabilities**:
  - File system access
  - Test execution
  - Git operations
  - Iterative refinement based on failures
  - Up to 150 tool-use turns on complex issues

The harness abstraction emerged from observing real failures rather than from theoretical design. It represents the minimal set of capabilities needed for autonomous code generation in a controlled environment.

### The Convergence Problem

When multiple autonomous agents work on a shared codebase in parallel, they must produce one coherent result. Early attempts failed dramatically: agents would build code that compiled and passed tests locally while being fundamentally broken when integrated. One agent built an entire [[API layer]] on a module another agent never exported. Tests passed because the downstream agent mocked the dependency.

This "convergence problem" requires explicit primitives for:
- **Isolation**: Agents must work without interfering with each other
- **Failure recovery**: Failures must be categorized and handled appropriately
- **State reconciliation**: The system must maintain a coherent view of dependencies and completed work

## Failure Handling and Recovery

In a 200+ invocation build, failures are not edge cases—they are the normal path. The system implements a three-level nested hierarchy of failure recovery:

### The Three Nested Control Loops

#### Inner Loop: Per-Issue Iteration (up to 5 attempts)

The agent retries itself with feedback from [[QA]] and code review. This loop handles problems the same agent can solve with better information.

**Example**: An app module was technically correct with 119 passing tests and all acceptance criteria met, but the module was not exported in `lib.rs`, making it inaccessible to library consumers. The reviewer blocked the change, and iteration 2 fixed the export with 354 passing tests.

#### Middle Loop: Issue Advisor

When the inner loop exhausts its attempts, an issue advisor activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Example**: An integration-tests issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The tests themselves were correct and passed review, but the code they tested was broken. Retrying would never help because the same agent would produce the same broken binary. The system blocked the issue and recorded it as typed debt:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

#### Outer Loop: Replanner

When issues at a dependency level produce unrecoverable failures, a replanner fires with access to the full execution state. It can:
- Skip downstream dependents
- Restructure the remaining issue graph
- Reduce scope
- Abort if necessary

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, allowing them to work around known gaps instead of building on invalid assumptions.

### Typed Debt System

Rather than silently dropping failures or burning budget on futile retries, the system records failures as **typed, severity-rated debt items**. These are structured data, not log messages:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "..."
}
```

This allows downstream agents to consume and work around known gaps explicitly, and lets the final reviewer understand exactly what was deferred and why.

## Execution Durability and Checkpointing

A 200+ invocation build costing $116 cannot restart from scratch on any failure. The system implements [[checkpoint]]-based execution—a pattern from [[high-performance computing]]:

### Checkpoint Contents

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

The checkpoint captures:
- Completed work at each dependency level
- Full git state (branches, commits, worktree mappings)
- Accumulated debt items
- Replan history to prevent repeated failed strategies

A build failing at minute 25 of a 30-minute execution resumes from the exact failure point without re-cloning or re-running completed work.

### Git Worktree Isolation

Each issue operates in its own [[git worktree]] on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This provides:
- Zero lock contention during parallel coding
- Clean isolation of changes per issue
- Ability to run 3+ issues simultaneously in the same repository

Between levels, a **merger agent** integrates completed branches into an integration branch. The merger is not mechanical `git merge`; it reads architecture specs and file conflict annotations to make intent-aware resolution decisions.

### Gate Sequence Between Levels

Every level transition enforces a clean handoff:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

## Planning and Parallelization

The planning phase produces finer-grained, more parallelizable issue graphs than humans typically create. The system has generated epics decomposed into 50-100 issues with dependency structures that would be impractical to coordinate manually. The coordination cost—managing 80 parallel branches—is exactly what the orchestrator absorbs.

A human managing 80 