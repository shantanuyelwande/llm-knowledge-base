---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-12T06:48:59.643256
raw_file_updated: 2026-06-12T06:48:59.643256
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-12T06:48:59.643256
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents how [[AgentField]] and [[SWE-AF]] successfully orchestrate 200+ autonomous [[LLM]] agents to collaboratively produce production-quality code through structured failure recovery, checkpoint-based execution, and nested control loops. The system demonstrates that architectural design and systematic failure handling outperform reliance on model capability alone.

---

## Overview

**Beyond Vibe Coding** describes a production system for coordinating multiple [[Claude Code]] instances on shared codebases to automate software engineering tasks. Rather than having human engineers guide individual agent iterations, the system abstracts the human role to high-level review and architectural approval, with autonomous agents handling line-by-line implementation, testing, and verification.

The approach emerged from building [[SWE-AF]], an open-source system for autonomous software engineering that successfully completed real-world projects:
- A diagrams-as-code CLI in Rust (15 issues, 200+ agent invocations, $116)
- A Go SDK feature (10 issues, 80+ invocations, $19)
- A Node.js benchmark (95/100 score on both cheapest and mid-tier models)

### The Core Problem: The Convergence Problem

When 30+ autonomous agents work in parallel on a shared codebase, they inevitably create incoherent results. The initial system experienced agents building entire API layers on modules that other agents never exported. Tests passed through mocking, code compiled cleanly, but the system did not function. This **convergence problem** requires systematic solutions for isolation, failure recovery, and state reconciliation.

---

## Architecture Principles

### 1. Two Modes of LLM Integration

The most critical architectural insight is that multi-agent systems require two distinct LLM integration patterns, not one.

#### Constrained Calls (`.ai()`)

**Constrained calls** are single-shot, deterministic operations with:
- Structured input and output
- No tool use
- No iteration
- Predictable latency and cost (fractions of a cent, milliseconds)

Use cases include:
- Issue routing and classification
- Risk assessment ("Is this change high-risk?")
- Guidance generation for downstream agents

Example output:
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

**Autonomous harnesses** are multi-turn, goal-driven loops with:
- Full coding environment (filesystem, test runner, git access)
- Tool use and iteration
- Goal-oriented execution until verifiable outcome
- Unpredictable cost and latency

Characteristics:
- Can run 50-150+ tool-use turns on complex issues
- Cost: $0.50 to $4+ per invocation depending on complexity
- Receives a goal and toolset, returns a verifiable result

The harness abstraction emerged from observing actual build failures rather than from theoretical design. It represents the pattern that repeatedly appeared in production: agents need a complete coding environment with built-in retry and failure recovery.

#### Integration Pattern

The two modes coexist through cheap routing decisions. A single boolean classification (`needs_deeper_qa`) determines whether an issue follows a lean two-call path (coder → reviewer) or a thorough four-call path (coder → QA and reviewer in parallel → synthesizer).

---

## 2. Failure Recovery and Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three nested control loops to handle different failure modes.

### Types of Failures

#### Deadlocks That Retrying Cannot Fix

When an agent produces code with infinite loops or deadlocks, simple retrying fails because the same agent produces the same broken code. Example: integration-tests issue that timed out after 2700 seconds in iteration 1 and 2.

**Response:** Block the issue, record typed debt, and allow dependent work to continue with knowledge of the gap.

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

#### Review Catches That Tests Miss

Tests can pass while code violates architectural conventions. Example: 119 passing tests but the app module was not exported in `lib.rs`, making it inaccessible to library consumers.

**Response:** Inner retry loop catches and fixes in iteration 2.

#### Regressions on Trivial Tasks

Autonomous agents can regress on simple tasks. Example: project-scaffold issue passed iteration 1 but iteration 2 added module declarations for non-existent code.

**Response:** Escalate to advisor loop for strategy change or scope reduction.

#### Cascading Verification Failures

Final verification can reveal multiple issues requiring sequential fixes across iterations.

### Three Nested Control Loops

#### Inner Loop (Per-Issue)

- Up to 5 iterations per issue
- Agent retries with feedback from [[QA]] and review
- Handles problems the same agent can solve with better information
- Example: missing export caught and fixed in iteration 2

#### Middle Loop (Issue Advisor)

Activates when inner loop is exhausted. Five typed recovery actions:

| Action | Response |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

Final invocation prompt explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retries.

#### Outer Loop (Replanner)

Fires when issues in a dependency level produce unrecoverable failures. Capabilities:
- See full execution state
- Skip downstream dependents
- Restructure remaining issue graph
- Reduce scope
- Abort if necessary

Previous replan decisions fed back to prevent repeating failed strategies. Default behavior on system crash: **continue** rather than abort (graceful degradation over fail-fast).

---

## 3. Durable Execution and Checkpointing

At $116 per build (diagrams project), crashes cannot mean restarting from invocation 1. The system applies high-performance computing principles to multi-agent orchestration.

### Checkpoint Everything

LLM timeouts, rate limits, network errors, and malformed output each pose crash risks. Checkpoints capture:

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

`resume_build()` loads the checkpoint, skips completed levels, and continues from exact failure point. A 30-minute build failing at minute 25 resumes from minute 25, not minute 0.

Checkpoint also captures:
- Git state (integration branch, original branch, initial commit SHA)
- Worktree directory mapping
- Allows workspace reconstruction without re-cloning

### Git Worktree Isolation

Each issue gets its own git worktree on a dedicated branch (`issue/01-project-scaffold`, etc.). Benefits:
- No lock contention
- No conflicts during parallel coding
- Parallel modification of different files
- Clean integration between levels

Example: diagrams build level 2 ran three issues in parallel (lexer, parser, validator), each in its own worktree, each modifying different files.

### Intent-Aware Merging

Between levels, a merger agent integrates completed branches into the integration branch. The merger:
- Reads architecture spec
- Consults file conflict annotations from planning phase
- Makes intent-aware resolution decisions
- Preserves both intents when two issues modify the same file

### Gate Sequence Between Levels

Every level enforces clean handoffs:

1. **Merge