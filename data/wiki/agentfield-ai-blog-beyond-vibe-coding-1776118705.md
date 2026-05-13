---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-13T05:54:20.041197
raw_file_updated: 2026-05-13T05:54:20.041197
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-13T05:54:20.041197
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

**Beyond Vibe Coding** documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively produce production-ready code through a system called [[SWE-AF]]. The approach separates LLM integration into two distinct primitives—constrained classification calls and autonomous development harnesses—and implements three nested failure recovery loops to handle the inherent unpredictability of multi-agent systems. Rather than relying on model intelligence alone, the architecture achieves 95/100 quality scores on both cheap and expensive models through systematic verification, isolation, and checkpoint-based execution.

---

## Table of Contents

1. [Core Architecture](#core-architecture)
2. [Two LLM Integration Primitives](#two-llm-integration-primitives)
3. [Failure Recovery and Control Loops](#failure-recovery-and-control-loops)
4. [Durable Execution Through Checkpointing](#durable-execution-through-checkpointing)
5. [Practical Results](#practical-results)
6. [Design Principles](#design-principles)
7. [Limitations and Future Work](#limitations-and-future-work)

---

## Core Architecture

[[AgentField]] developed SWE-AF to move human engineers from the iteration loop to the review loop. Instead of one engineer guiding a single [[Claude Code]] session, the system spawns dozens of autonomous agent instances—called "harnesses"—that coordinate in parallel on a shared codebase.

The fundamental challenge is the **convergence problem**: getting N autonomous processes to produce one coherent result requires primitives for [[isolation]], [[failure recovery]], and [[state reconciliation]]. The first production run revealed this starkly: 30+ agents produced a PR that compiled and passed tests but was fundamentally broken—one agent built an API layer on a module that another agent never exported.

### Key Innovation: Harnesses

A **harness** is a full coding environment with:
- Filesystem access
- Test execution capabilities
- Git integration
- Multi-turn iteration loops

This abstraction emerged from observing real build failures rather than from theoretical design. It became one of two foundational [[AgentField]] primitives.

---

## Two LLM Integration Primitives

The most common architectural mistake in multi-agent systems is treating all [[LLM]] calls identically. AgentField separates them into two complementary modes:

### 1. Constrained Single-Shot Call (`.ai()`)

**Characteristics:**
- Single-turn interaction
- Structured input and output
- No tool use
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic routing

**Use Cases:**
- Classification ("Does this issue need deeper QA?")
- Risk assessment ("Is this change high-risk?")
- Routing decisions

**Output Example:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields drive operational routing. The `agent_guidance` string carries context for downstream agents.

### 2. Autonomous Harness (`.harness()`)

**Characteristics:**
- Multi-turn iteration
- Tool-using capability
- Goal-driven execution
- Verifiable outcomes
- Variable latency (minutes to hours)
- Variable cost (dollars per invocation)

**Capabilities:**
- Read and write files
- Execute tests
- Discover failures
- Retry with feedback
- Integrate with git workflows

**Example:** In the diagrams-as-code build, a single coder harness invocation ran up to 150 tool-use turns and cost over $4 on a complex issue.

### Separation of Concerns

The two primitives coexist strategically. A cheap `.ai()` classification determines whether an issue follows a:
- **Lean path:** coder → reviewer (2 calls)
- **Thorough path:** coder → QA + reviewer (parallel) → synthesizer (4 calls)

This separation keeps routing cheap while allowing expensive work to concentrate where needed.

---

## Failure Recovery and Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. AgentField implements three nested control loops to handle different failure classes:

### The Inner Loop: Per-Issue Retry (up to 5 iterations)

**Purpose:** Allow the same agent to improve given feedback

**Activation:** When QA or review identifies fixable problems

**Example:** The `app-module` issue passed all 119 tests but wasn't exported in `lib.rs`. The reviewer blocked it. Iteration 2 added `pub mod app;` and passed 354 tests.

**Success Condition:** Issue meets all acceptance criteria and passes review

**Failure Escalation:** After 5 iterations, escalate to the middle loop

### The Middle Loop: Issue Advisor

**Purpose:** Determine recovery strategy when inner loop exhausts

**Activation:** After inner loop reaches iteration limit

**Recovery Actions:**

| Action | Behavior | Use Case |
|--------|----------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt | Scope reduction possible |
| `RETRY_APPROACH` | Same criteria, different strategy | Wrong library/approach chosen |
| `SPLIT` | Break into smaller sub-issues | Issue too complex |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt | Acceptable partial completion |
| `ESCALATE_TO_REPLAN` | Restructure remaining work | Blocking dependency chain |

**Example:** The `integration-tests` issue timed out after 2700 seconds with an infinite loop in the CLI binary. The tests were well-written and passed code review, but the binary itself was broken. Retrying would never help. The advisor blocked it and recorded:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

### The Outer Loop: Replanner

**Purpose:** Handle unrecoverable failures at dependency level boundaries

**Activation:** When multiple issues in a level produce blocking failures

**Capabilities:**
- Skip downstream dependents
- Restructure remaining issue graph
- Reduce scope
- Abort build if necessary

**State Tracking:** Previous replan decisions are fed back to prevent repeating failed strategies

**Default Behavior:** If the replanner itself crashes (LLM timeout, malformed output), continue rather than abort. For expensive workflows, graceful degradation beats fail-fast.

### Failure Example: Cascading Verification

The `final-acceptance-verification` issue demonstrates the loop hierarchy in action:

- **Iteration 1:** Found 4 blocking issues (`set -e` crashes, macOS-specific `stat` flags, infinite recursion, missing dependency checks)
- **Iteration 2:** Fixed those but introduced new bug where `cargo fmt` check used `|| true`, making it always pass
- **Iteration 3:** Finally correct

The inner loop caught and fixed progressively discovered problems until the issue passed.

---

## Durable Execution Through Checkpointing

At $116 per build with 200+ invocations, a crash at invocation 140 cannot mean restarting from invocation 1. AgentField treats multi-agent builds as long-running, expensive processes requiring checkpoint-based recovery.

### What Gets Checkpointed

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

The checkpoint captures:
- Current execution level
- Completed levels
- Full issue list
- Original plan summary
- Replan history
- Accumulated debt items
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)

### Resume Capability

`resume_build()` loads the checkpoint and continues from the exact failure point without re-cl