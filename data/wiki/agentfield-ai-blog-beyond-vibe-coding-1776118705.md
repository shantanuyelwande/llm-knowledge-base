---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-21T04:53:05.551238
raw_file_updated: 2026-04-21T04:53:05.551238
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-21T04:53:05.551238
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents AgentField's approach to orchestrating 200+ autonomous AI agents on shared codebases to produce production-ready pull requests. Rather than having individual engineers iterate with single AI sessions, the system coordinates parallel agent instances with structured failure recovery, checkpoint-based execution, and hierarchical control loops. Key innovations include separating [[LLM Integration]] into constrained single-shot calls and autonomous harnesses, implementing three nested failure loops for graceful degradation, and using git worktrees for agent isolation.

---

## Overview

AgentField is an [[AI-native engineering]] team that developed a system for orchestrating multiple [[Claude Code]] instances to collaboratively build software features. The core insight is that moving human responsibility from iteration loops to review loops—where engineers approve finished, verified draft pull requests rather than guiding individual changes—requires new abstractions for [[Multi-agent Orchestration|orchestration]], failure recovery, and state management.

The system has been tested on real production builds:
- A [[Rust]] diagrams-as-code CLI: 15 issues, 200+ agent invocations, $116 total cost
- A Go SDK feature: 10 issues, 80+ invocations, $19 total cost  
- A Node.js benchmark: 95/100 score on both cheapest and mid-tier models

## Core Architecture

### Two Modes of LLM Integration

The most critical architectural decision is separating [[LLM Integration]] into two distinct primitives rather than giving all agents identical access patterns.

#### Constrained Single-Shot Calls (`.ai()`)

The first primitive handles **routing and classification** with predictable characteristics:
- Single-turn execution with no tool use
- Structured input and output
- Millisecond latency, fraction-of-cent cost
- Deterministic retry semantics

During the planning phase, each issue receives an `IssueGuidance` block:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

These structured fields drive downstream routing decisions. A boolean like `needs_deeper_qa` determines whether an issue follows a lean two-call path (coder → reviewer) or a thorough four-call path (coder → QA and reviewer in parallel → synthesizer).

#### Autonomous Harnesses (`.harness()`)

The second primitive provides **multi-turn, goal-driven iteration**:
- Full [[Coding Environment|coding environments]] with filesystem access, test execution, and git
- Tool-using iteration loops that continue until producing verifiable outcomes
- Unpredictable latency and cost (single issues can consume 150+ tool-use turns and $4+)
- Outcome-focused rather than process-focused (you verify what was delivered, not how)

The harness abstraction emerged from observing production failures rather than from theoretical design. It captures the pattern of agents needing full development environments with retry-on-failure capabilities and git integration—a pattern not cleanly abstracted in other frameworks.

### The Convergence Problem

The first major failure occurred when 30+ harnesses ran in parallel on a shared codebase. The resulting pull request appeared correct until code review revealed that one agent had built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. This **convergence problem**—getting N autonomous processes to produce one coherent result—requires primitives for:
- Isolation between parallel agents
- Failure recovery and state reconciliation
- Intent-aware merging of concurrent changes

## Failure Recovery: Three Nested Loops

In a 200+ invocation build, failures are the normal execution path, not edge cases. The system implements three hierarchical control loops to handle different failure modes:

### Inner Loop: Per-Issue Iteration

Runs up to 5 iterations per issue, with the agent receiving feedback from [[QA Agent|QA]] and [[Code Review Agent|review]] stages. Handles problems that the same agent can solve with better information.

**Example**: The `app-module` issue produced 119 passing tests and met all acceptance criteria in iteration 1, but code review blocked it because the module was not exported in `lib.rs`. Iteration 2 fixed the single missing line (`pub mod app;`) with 354 tests passing.

### Middle Loop: Issue Advisor

Activates when the inner loop exhausts 5 iterations. Provides five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

The final invocation explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retries.

**Example**: The `integration-tests` issue timed out after 2700 seconds due to an infinite loop in the CLI binary. Retrying would produce the same timeout. The advisor blocked the issue and recorded structured debt:

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

Fires when issues in a dependency level produce unrecoverable failures. Has visibility into the full execution state and can:
- Skip downstream dependents
- Restructure the remaining issue graph
- Reduce scope
- Abort the build

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes ([[LLM Timeout|LLM timeouts]], malformed output), the system defaults to **continue** rather than abort—graceful degradation is preferable to fail-fast for expensive workflows.

### Debt Propagation

When upstream issues complete with debt, downstream issues receive `debt_notes` explaining what was not delivered and why. This allows dependent agents to work around known gaps instead of building on assumptions that no longer hold:

```json
{
  "issue_name": "integration-tests",
  "debt_notes": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair. Dependent issues should mock the CLI rather than invoke it directly."
}
```

## Durable Execution: Checkpointing and Isolation

Multi-agent builds are expensive ($116 for the diagrams project) and long-running (30+ minutes). A crash at invocation 140 cannot mean restarting from invocation 1. The system brings [[Checkpointing|checkpoint]]-based recovery from [[High-Performance Computing]] into multi-agent orchestration.

### Checkpoint Everything

The system checkpoints at every dependency level boundary. A typical checkpoint captures:

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

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. The checkpoint also captures git state (integration branch, original branch, initial commit SHA, worktree directory mapping) so resumed builds reconstruct the full workspace without re-cloning.

Longer workflows accumulate more recovery points, inverting the relationship between scale and fragility. Durable execution makes expensive builds survivable.

### Git Worktree Isolation

Each issue gets its own [[Git Worktree|git worktree]] on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). In parallel execution, multiple issues can safely modify different files without lock contention or conflicts.

Agents also plan more finely-grained issue decomposition than humans would attempt. The diagrams build decomposed a single epic into 15 issues with 6 dependency levels, with level 2 running three issues in parallel (lexer, parser, validator) each in its own worktree.

### Integration Between Levels

A **merger agent** integrates completed branches into the integration branch between dependency levels. Unlike mechanical `git merge`, the merger:
- Reads the architecture spec from planning
- Understands file conflict annotations