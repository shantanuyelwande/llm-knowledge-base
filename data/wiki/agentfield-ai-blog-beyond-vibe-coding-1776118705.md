---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-27T05:32:04.762394
raw_file_updated: 2026-04-27T05:32:04.762394
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-27T05:32:04.762394
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Software Engineering at Scale

## Summary

This article documents lessons learned from orchestrating 200+ autonomous AI agents on shared codebases to produce production-ready code. The key findings are: (1) separating LLM integration into two distinct primitives—constrained single-shot calls and autonomous loops; (2) implementing nested failure recovery loops to handle inevitable agent failures; and (3) using checkpoint-based execution for cost-efficient long-running builds. The work demonstrates that architectural design matters more than model selection, with the same system achieving 95/100 performance on both expensive and cheap models.

---

## Overview

[[AgentField]] is an AI-native software engineering platform that abstracts the human role from real-time iteration to final architectural review. Rather than having engineers guide individual [[LLM]] interactions, the system coordinates dozens of autonomous agent instances in parallel on shared codebases, producing draft pull requests that have already passed multiple rounds of automated writing, testing, and verification before human review.

The core innovation is treating multi-agent software development as a long-running, failure-prone distributed system requiring explicit primitives for isolation, recovery, and state reconciliation—borrowed from high-performance computing patterns.

---

## Core Architecture

### Two Modes of LLM Integration

The most critical architectural decision is separating [[LLM]] access into two distinct primitives rather than giving all agents identical capabilities.

#### Constrained Single-Shot Calls (`.ai()`)

**Characteristics:**
- Single invocation, no iteration
- Structured input and output schemas
- No tool use or autonomous looping
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic outputs suitable for downstream routing

**Use cases:**
- Issue classification and routing
- Risk assessment ("Is this change high-risk?")
- Guidance generation for downstream agents
- Planning and decomposition decisions

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

**Characteristics:**
- Multi-turn, goal-driven iteration
- Full coding environment access (filesystem, test runner, [[git]])
- Tool use and autonomous decision-making
- Variable latency (minutes to hours)
- Variable cost (can exceed $4 per complex issue)
- Verifiable outcomes rather than prescribed paths

**Capabilities:**
- Read and write source code
- Execute test suites
- Discover failures and retry with new approaches
- Integrate with version control
- Make autonomous architectural decisions within scope

**Example:** A single coder harness on a complex issue in the diagrams-as-code build ran up to 150 tool-use turns and cost over $4.

### Why Separation Matters

Keeping these primitives distinct enables:
- **Cost predictability**: Cheap classification gates determine expensive work allocation
- **SLA guarantees**: Constrained calls have bounded latency; harnesses have bounded iterations
- **Retry semantics**: Retrying a 45-minute autonomous loop differs fundamentally from retrying a 200ms classification
- **Operational reasoning**: System behavior becomes predictable and analyzable

In practice, a boolean from a cheap `.ai()` call (e.g., `needs_deeper_qa`) routes issues to either a lean two-call path (coder → reviewer) or a thorough four-call path (coder → QA and reviewer in parallel → synthesizer).

---

## Failure Recovery: Three Nested Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three hierarchical recovery mechanisms.

### Inner Loop: Per-Issue Iteration (Up to 5 attempts)

**Activation:** Single issue failure
**Agents involved:** Coder, QA, Reviewer
**Recovery mechanism:** Agent retries with feedback from quality checks

**Example:** The app-module issue in the diagrams build passed all 119 tests but was missing `pub mod app;` in `lib.rs`. The reviewer blocked it. Iteration 2 fixed the export with 354 tests passing.

**Success criteria:**
- Problem is addressable by the same agent with better information
- [[QA]] and review provide actionable feedback
- Issue has not exceeded maximum iterations

### Middle Loop: Issue Advisor (When inner loop exhausted)

**Activation:** Issue fails to pass all gates after 5 iterations
**Agents involved:** Issue advisor
**Decision options:**

| Action | Meaning | Example |
|--------|---------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt | Reduce test coverage requirements |
| `RETRY_APPROACH` | Same criteria, different strategy | Try alternative library or algorithm |
| `SPLIT` | Break into smaller sub-issues | Decompose complex feature |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt | Ship with known limitations documented |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work | Restructure entire issue graph |

**Example:** The integration-tests issue timed out after 2700 seconds due to a CLI binary deadlock. The tests themselves were correct and passed code review, but the underlying binary hung. The advisor blocked the issue and recorded typed debt:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining upstream failures so they can work around known gaps instead of building on broken assumptions.

### Outer Loop: Replanner (When dependency level fails)

**Activation:** Issues in a [[dependency graph]] level produce unrecoverable failures
**Agents involved:** Replanner
**Actions:**
- Skip downstream dependents affected by upstream failures
- Restructure remaining issue graph
- Reduce overall scope
- Escalate to human review
- Abort build if unrecoverable

**State:** Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies.

**Failure mode:** If the replanner itself crashes (LLM timeout, malformed output), the system defaults to `continue` rather than `abort`. For expensive workflows, graceful degradation beats fail-fast.

### Real-World Failure Examples

**Deadlocks that retrying cannot fix:** The integration-tests issue timed out after 2700 seconds. Retrying the same agent on the same binary produced the same timeout—a problem no amount of iteration can solve.

**Review catches that tests miss:** The app-module issue had 119 passing tests and met all acceptance criteria, but the module was not exported in `lib.rs`, making it inaccessible to library consumers. Tests passed because downstream code mocked the dependency.

**Regressions on trivial tasks:** The project-scaffold issue (literally "create Cargo.toml and src/main.rs") passed on iteration 1, then regressed on iteration 2 when the coder added module declarations for non-existent code.

**Cascading verification failures:** The final-acceptance-verification issue took 3 iterations to pass. Iteration 1 found four blocking issues. Iteration 2 fixed those but introduced a new bug with `cargo fmt` checks. Iteration 3 finally succeeded.

---

## Checkpoint-Based Execution for Cost Efficiency

A 200+ invocation build costing ~$116 cannot afford to restart from invocation 1 after a failure at invocation 140. The system treats multi-agent builds as long-running, expensive processes requiring explicit durability guarantees.

### Checkpoint Structure

Checkpoints capture full execution state at level boundaries:

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

**Recovery:** `resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build that fails at minute