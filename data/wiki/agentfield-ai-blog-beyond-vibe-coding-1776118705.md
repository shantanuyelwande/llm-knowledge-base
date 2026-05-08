---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-08T04:57:49.272524
raw_file_updated: 2026-05-08T04:57:49.272524
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-08T04:57:49.272524
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[AI agents]] to collaboratively generate production code. The key innovation is separating [[LLM]] integration into two distinct primitives: constrained single-shot calls (`.ai()`) for routing and classification, and autonomous harnesses (`.harness()`) for iterative problem-solving. The system implements three nested failure recovery loops and checkpoint-based execution to handle the complexity of coordinating multiple agents on shared codebases. A real-world case study (diagrams-as-code CLI in Rust) demonstrates the approach across 15 issues, 200+ agent invocations, and $116 in total cost.

---

## Table of Contents

1. [Overview](#overview)
2. [The Convergence Problem](#the-convergence-problem)
3. [Two Modes of LLM Integration](#two-modes-of-llm-integration)
4. [Failure Recovery Architecture](#failure-recovery-architecture)
5. [Durable Execution and Checkpointing](#durable-execution-and-checkpointing)
6. [Architecture vs. Model Selection](#architecture-vs-model-selection)
7. [Lessons and Future Improvements](#lessons-and-future-improvements)
8. [Related Systems](#related-systems)

---

## Overview

[[AgentField]] and its specialized implementation [[SWE-AF]] represent a shift in how autonomous systems approach software engineering. Rather than having a single [[AI agent]] iterate with a human developer, the system coordinates dozens of [[Claude Code]] instances (called "harnesses") in parallel on a shared codebase. The goal is to move human responsibility from the iteration loop to the review loop—engineers review finished, verified draft pull requests rather than guiding each change.

### Key Achievement

The system produces draft pull requests where code has already undergone multiple rounds of:
- Automated writing
- Testing
- Peer review
- Verification

Only a small percentage of epics required code changes from the human reviewer. The human role shifted from line-by-line iteration to architectural sign-off.

---

## The Convergence Problem

When 30+ autonomous agents work in parallel on a shared codebase, coordination failures emerge that single-agent systems never encounter. The initial attempt revealed a critical issue: one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. Code compiled. The pull request looked clean. **The system did not work.**

This is the **convergence problem**: getting N autonomous processes to produce one coherent result requires explicit primitives for:
- [[Isolation]] between agent workspaces
- [[Failure recovery]] mechanisms
- [[State reconciliation]] across parallel work

---

## Two Modes of LLM Integration

The most common architectural mistake in multi-agent systems is giving every agent identical [[LLM]] access. This prevents operational reasoning about the system:

- Cannot set [[SLA|SLAs]]
- Cannot predict costs
- Cannot build reliable retry logic
- Retry meaning varies by call type

### The Solution: Two Primitives

#### 1. Constrained Call (`.ai()`)

**Purpose**: Routing, classification, and decision-making

**Characteristics**:
- Single-shot execution
- Structured input and output
- No tool use or iteration
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic downstream behavior

**Example Output**:
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive routing decisions. The `agent_guidance` string carries context for downstream agents.

#### 2. Autonomous Harness (`.harness()`)

**Purpose**: Multi-turn problem-solving with full development environment

**Characteristics**:
- Multi-turn tool-using interaction
- Goal-driven iteration
- Full filesystem access
- Test execution capability
- Git integration
- Verifiable outcomes
- Variable cost and latency (up to 150 tool-use turns, $4+ per invocation)

**Workflow**:
1. Receive a goal and toolset
2. Read files, write code, run tests
3. Discover failures and iterate
4. Produce verifiable outcome
5. System checks deliverable, not process

### Design Philosophy

These primitives did not come from studying other frameworks or hypothetically anticipating needs. They emerged from watching production builds fail. The harness abstraction took months of failed iterations to recognize as the missing primitive.

---

## Failure Recovery Architecture

In a 200+ invocation build, failures are the normal path, not edge cases. The system requires three nested control loops to handle the diversity of failure modes.

### Failure Categories and Examples

#### Deadlocks That Retrying Cannot Fix

**Example**: Integration test issue that timed out after 2700 seconds due to an infinite loop in the CLI binary.

```
{
  "iteration": 2,
  "action": "block",
  "summary": "Issue is stuck in a loop. Tests timeout after 2700s in iteration 2, 
    same failure as iteration 1 despite attempted CLI binary fix.",
  "qa_passed": false,
  "review_approved": true,
  "review_blocking": false
}
```

**Response**: Block the issue and record typed debt rather than retrying, which would waste budget.

#### Review Catches That Tests Miss

**Example**: App module with 119 passing tests and met acceptance criteria, but the module was never exported in `lib.rs`, making it inaccessible to library consumers.

```
{
  "iteration": 1,
  "summary": "App module is technically sound with all 119 tests passing... 
    However, the app module is not exported in lib.rs, making it inaccessible 
    to library consumers.",
  "qa_passed": true,
  "review_approved": false,
  "review_blocking": true
}
```

**Response**: Inner retry loop catches and fixes this on iteration 2.

#### Regressions on Trivial Tasks

**Example**: Project scaffold issue that passed iteration 1 with 13 tests passing, then regressed in iteration 2 by adding non-existent module declarations.

```
{
  "iteration": 2,
  "summary": "main.rs references 10 non-existent modules, causing cargo build 
    to fail. This is a regression from iteration 1.",
  "qa_passed": false,
  "review_blocking": true
}
```

**Response**: Demonstrates that autonomous code generation fails unpredictably, even on trivial tasks.

#### Cascading Verification Failures

**Example**: Final acceptance verification that required three iterations to fix platform-specific issues, infinite recursion, and format checking errors.

### Three Nested Control Loops

![Nested Loop Architecture](/nested-control-loops)

#### Inner Loop: Per-Issue Iteration
- **Scope**: Single issue, up to 5 iterations
- **Participants**: Coder agent, QA agent, reviewer agent
- **Feedback**: QA and review findings drive retry attempts
- **Success Condition**: Issue passes QA and review
- **Handles**: Problems that the same agent can solve with better information

#### Middle Loop: Issue Advisor
- **Trigger**: Inner loop exhausted (5 iterations reached)
- **Participants**: Advisor agent with five typed recovery actions
- **Actions**:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

- **Final Invocation**: Prompt explicitly warns this is the last chance, biasing toward acceptance or escalation

#### Outer Loop: Replanner
- **Trigger**: Unrecoverable failures in a dependency level
- **Participants**: Replanner agent with full execution state visibility
- **Capabilities**:
  - Skip downstream dependents
  - Restructure issue graph
  - Reduce scope
  - Abort build
- **Memory**: Previous replan decisions feed back to prevent repeating failed strategies
- **Graceful Degradation**: If replanner crashes (timeout, malformed output), system defaults to `continue` rather than `abort`

### Typed Debt Items

Failed issues are recorded as structured debt, not log messages:

```json
{