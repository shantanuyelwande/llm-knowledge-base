---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:31:24.912526
raw_file_updated: 2026-06-07T06:31:24.912526
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:31:24.912526
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to produce production-ready code through a system called [[SWE-AF]]. The key innovations are: separating LLM integration into two distinct primitives (constrained calls and autonomous harnesses), implementing three nested failure recovery loops, and using checkpoint-based execution for cost-effective long-running workflows.

---

## Overview

[[Multi-agent systems]] for [[software engineering]] face a critical challenge: coordinating N autonomous processes to produce one coherent result. Traditional approaches that give every agent identical LLM access lead to unpredictable costs, unpredictable latency, and unrecoverable failures. AgentField's approach inverts this relationship by building operational abstractions from real failure patterns rather than theoretical requirements.

The system has been validated on real builds:
- **Diagrams-as-code CLI** (Rust): 15 issues, 200+ agent invocations, $116
- **Go SDK feature**: 10 issues, 80+ invocations, $19  
- **Node.js benchmark**: 95/100 score on both cheapest and mid-tier models

---

## Core Architecture

### Two Modes of LLM Integration

The most significant architectural decision is separating [[LLM]] access into two fundamentally different primitives, rather than providing a single general-purpose interface.

#### Constrained Calls (`.ai()`)

**Purpose**: Routing, classification, and structured decision-making

**Characteristics**:
- Single-shot, no iteration
- Structured input and output
- No [[tool use|tool-using]]
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic downstream routing

**Example Use Cases**:
- Does this issue need deeper QA?
- Is this change high-risk?
- What is the estimated scope?

A typical constrained call produces an `IssueGuidance` block with structured fields:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields enable deterministic routing. The `agent_guidance` string carries context for downstream agents without forcing parsing of free-form text.

#### Autonomous Harnesses (`.harness()`)

**Purpose**: Goal-driven iteration with full development environment access

**Characteristics**:
- Multi-turn, iterative execution
- [[Tool use|Tool-using]] enabled (filesystem, test runner, git)
- Goal-driven termination
- Variable latency (seconds to hours)
- Variable cost (cents to dollars)
- Verifiable outcomes rather than deterministic paths

**Example**: A single coder harness on a complex issue may run up to 150 tool-use turns, costing over $4, reading files, writing code, running tests, discovering failures, and iterating until producing a working implementation.

**Key Insight**: The harness abstraction did not come from studying other frameworks or anticipating developer needs. It emerged from watching real builds fail. Agents consistently needed a full coding environment with an iteration loop that could retry on failure, and no existing abstraction captured this pattern cleanly.

### Routing and Cost Efficiency

The two primitives coexist in a single system. A cheap `.ai()` classification call determines whether an issue follows a lean path (coder → reviewer) or a thorough path (coder → QA and reviewer in parallel → synthesizer):

```
if needs_deeper_qa:
  path = [coder, qa_parallel, reviewer_parallel, synthesizer]
else:
  path = [coder, reviewer]
```

This design keeps routing cheap while allowing expensive work to be allocated intelligently. The boolean from a millisecond classification call drives the entire issue execution strategy.

---

## Failure Recovery and Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three nested control loops to handle different failure modes.

### Failure Categories

#### Deadlocks That Retrying Cannot Fix

**Example**: An integration test times out after 2700 seconds because the CLI binary has an infinite loop. The inner retry loop cannot fix this because the same agent produces the same broken binary.

**Response**: Block the issue and record typed [[technical debt]]:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, allowing them to work around known gaps.

#### Review Catches That Tests Miss

**Example**: An app module passes all 119 tests and meets all acceptance criteria, but is not exported in `lib.rs`, making it inaccessible to library consumers.

**Response**: The code reviewer blocks the PR with specific feedback. The agent fixes the missing `pub mod app;` declaration on the next iteration. This is the inner retry loop working as intended.

#### Regressions on Trivial Tasks

**Example**: A project scaffold issue (create Cargo.toml and src/main.rs) passes iteration 1 with all 13 tests passing, then regresses in iteration 2 when the coder adds module declarations for code that does not exist yet.

**Response**: The system detects the regression through QA verification and feeds it back to the agent for another attempt.

#### Cascading Verification Failures

**Example**: A final-acceptance-verification issue requires three iterations:
1. Iteration 1: Identifies four blocking issues
2. Iteration 2: Fixes those but introduces a new bug with `|| true` masking failures
3. Iteration 3: Finally produces correct behavior

### Three Nested Control Loops

The system implements hierarchical failure recovery with three distinct control loops:

#### Inner Loop: Per-Issue Iteration
- **Scope**: Single issue, up to 5 iterations
- **Feedback**: QA and code review results
- **Purpose**: Allow the same agent to improve given better information
- **Handles**: Problems that the agent can solve with additional context

#### Middle Loop: Issue Advisor
- **Scope**: Activated when inner loop exhausted (5 iterations reached)
- **Actions**:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

- **Purpose**: Make principled decisions about when to stop iterating
- **Handles**: Issues that need a different approach or scope reduction

#### Outer Loop: Replanner
- **Scope**: Activated when issues in a dependency level produce unrecoverable failures
- **Visibility**: Full execution state across all issues
- **Actions**: Skip downstream dependents, restructure issue graph, reduce scope, or abort
- **Memory**: Previous replan decisions fed back on subsequent invocations
- **Resilience**: If replanner crashes, defaults to `continue` rather than abort
- **Purpose**: Adapt the remaining work to changed constraints
- **Handles**: System-level failures requiring restructuring

### Debt Tracking

Every failure is tracked as a structured [[technical debt]] item:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "...",
  "issue_name": "...",
  "severity": "high|medium|low",
  "justification": "...",
  "downstream_impact": "..."
}
```

The final PR includes a complete debt section documenting:
- What was deferred
- Why it was accepted
- What downstream issues adapted to accommodate it

This makes failure visible and auditable rather than hidden in logs.

---

## Durable Execution and Checkpointing

At $116 per build with 200+ invocations, a crash at invocation 140 cannot restart from invocation 1. The system treats multi-agent builds as long-running, expensive processes requiring checkpoint-based recovery.

### Checkpoint Structure

Every level boundary captures complete execution state:

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": [
    "