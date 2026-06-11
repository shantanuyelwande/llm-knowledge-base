---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-11T06:55:58.343213
raw_file_updated: 2026-06-11T06:55:58.343213
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-11T06:55:58.343213
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents how [[AgentField]] and [[SWE-AF]] orchestrate 200+ autonomous [[LLM]] agents to collaboratively generate production code. The system introduces two distinct LLM integration primitives (constrained calls and autonomous harnesses), implements three nested failure recovery loops, and uses checkpoint-based execution to make expensive multi-agent builds survivable. The architecture demonstrates that systematic orchestration and verification can achieve comparable results across different model tiers, shifting the quality bottleneck from model selection to system design.

---

## Overview

The shift from single-agent to multi-agent software development requires new abstractions for orchestration, failure recovery, and state management. Traditional approaches of giving all agents identical [[LLM]] access create operational blind spots: unpredictable latency, unforecastable costs, and indeterminate retry semantics.

The AgentField team developed this system through production experience, shipping 200+ agent invocations on real projects including:
- A Rust diagrams-as-code CLI (15 issues, 200+ invocations, $116)
- A Go SDK feature (10 issues, 80+ invocations, $19)
- A Node.js benchmark (95/100 score on both cheapest and mid-tier models)

## Core Concepts

### Two Modes of LLM Integration

The foundational architectural insight is separating [[LLM]] access into two distinct primitives rather than providing uniform access to all agents.

#### Constrained Single-Shot Calls (`.ai()`)

The first primitive is the **constrained call**: single-shot, structured input/output, no tools, no iteration.

**Characteristics:**
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic output structure
- Suitable for routing and classification

**Use cases:**
- Issue triage ("Does this need deeper QA?")
- Risk assessment ("Is this change high-risk?")
- Planning and decomposition
- Guidance generation

**Example output structure:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

The second primitive is the **autonomous harness**: multi-turn, tool-using, goal-driven iteration.

**Characteristics:**
- Full coding environment (filesystem, test runner, [[git]])
- Iterative problem-solving
- Tool access and execution capability
- Variable latency and cost
- Verifiable outcomes

**Capabilities:**
- File reading and writing
- Code generation and modification
- Test execution and debugging
- Dependency discovery
- Failure analysis and recovery

**Resource consumption:**
- Single invocation can run 50-150 tool-use turns
- Cost range: $0.50-$4.26 per issue depending on complexity
- Execution time: minutes to hours

### System Architecture

#### Three Nested Control Loops

The system implements three escalating failure recovery mechanisms, each handling different failure categories.

##### Inner Loop (Per-Issue Iteration)

- **Scope:** Single issue, up to 5 iterations
- **Actors:** Coder agent, QA agent, code reviewer
- **Recovery mechanism:** Retry with feedback
- **Success criteria:** All acceptance criteria met, tests pass, code review approved

**Example:** The app-module issue was caught by code review (missing `pub mod app;` export) and fixed on iteration 2 with 354 tests passing.

##### Middle Loop (Issue Advisor)

Activates when the inner loop exhausts retries after 5 iterations.

**Typed recovery actions:**

| Action | Purpose | Outcome |
|--------|---------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria | Record gap as typed [[Technical Debt]] |
| `RETRY_APPROACH` | Same criteria, different strategy | Try alternative implementation approach |
| `SPLIT` | Decompose issue | Create sub-issues for remaining work |
| `ACCEPT_WITH_DEBT` | Close enough | Document each gap as severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally | Trigger outer loop restructuring |

**Example:** The integration-tests issue (infinite loop deadlock) was blocked after 2 iterations, recorded as high-severity debt, and the build continued with downstream issues receiving `debt_notes` about the missing integration test suite.

##### Outer Loop (Replanner)

Fires when issues in a [[Dependency Graph]] level produce unrecoverable failures.

**Capabilities:**
- Skip affected downstream dependents
- Restructure remaining issue graph
- Reduce scope
- Abort gracefully
- Learn from previous replan decisions

**Failure handling:** System defaults to `continue` rather than `abort` on LLM timeouts or malformed output, enabling graceful degradation.

#### Execution Flow Between Levels

Between each [[Dependency Graph]] level, the system enforces a clean handoff through sequential gates:

1. **Merge gate** - Integrate completed branches into integration branch
2. **Integration test gate** - Validate merged code still works together
3. **Debt gate** - Process completed-with-debt results, propagate downstream
4. **Split gate** - Inject sub-issues if any issue was split
5. **Replan gate** - Invoke replanner if failures escalated
6. **Checkpoint** - Serialize full state to disk

## Failure Categories and Recovery

### Deadlocks That Retrying Cannot Fix

**Problem:** Agent produces code with infinite loop or deadlock. Tests pass because they mock the dependency. Inner loop retries produce identical failure.

**Recovery:** Block the issue, record as typed [[Technical Debt]], let rest of build work around the gap.

**Example data structure:**
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

### Review Catches That Tests Miss

**Problem:** Code passes all tests and acceptance criteria but violates architectural constraints (e.g., module not exported in `lib.rs`).

**Recovery:** Inner loop catches on code review, agent fixes on next iteration.

**Example:** Missing `pub mod app;` in `lib.rs` made module inaccessible to library consumers despite 119 passing tests.

### Regressions on Trivial Tasks

**Problem:** Agent produces working code on iteration 1, then regresses on iteration 2 by adding non-existent module declarations.

**Recovery:** Inner loop detects regression, agent corrects on next iteration.

**Example:** Project scaffold issue (simple Cargo.toml + main.rs) passed iteration 1 but iteration 2 referenced 10 non-existent modules.

### Cascading Verification Failures

**Problem:** Final verification reveals multiple issues: shell script error handling, platform-specific flags, infinite recursion, missing dependency checks, and incorrect error suppression.

**Recovery:** Multiple iterations through inner loop, each fixing one category of failure, sometimes introducing new issues.

**Example:** Final-acceptance-verification took 3 iterations to get shell scripts, platform compatibility, and code formatting checks all correct simultaneously.

## Checkpointing and Durability

### Checkpoint-Based Execution

At $116 per build, restarting from failure is economically unviable. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint recovery at every level.

**Checkpoint captures:**
- Current execution level
- Completed levels
- Full issue list with status
- Original plan summary
- Replan count and history
- Accumulated [[Technical Debt]] items
- [[Git]] state (integration branch, original branch, commit SHA, worktree mappings)

**Resume behavior:**
- Load checkpoint from disk
- Skip completed levels
- Continue from exact failure point
- Reconstruct workspace without re-cloning

**Example:** 30-minute build failing at minute 25 resumes from minute 25, not minute 0.

### Isolation with Git Worktrees

Each issue gets a dedicated [[Git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.).

**Benefits:**
- No lock contention during parallel coding
- No conflicts between parallel issues
- Clean integration points between levels
- Enables intent-aware conflict resolution

**Merger agent:** Between levels, a merger agent integrates completed branches into the integration branch. Unlike mechanical `git merge`, it reads architecture specs and file conflict annotations to make