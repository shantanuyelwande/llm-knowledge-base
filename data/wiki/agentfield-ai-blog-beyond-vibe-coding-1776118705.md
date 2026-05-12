---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-12T05:43:32.767610
raw_file_updated: 2026-05-12T05:43:32.767610
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-12T05:43:32.767610
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively generate production code. The key insight is that successful multi-agent systems require two distinct modes of [[LLM]] integration (constrained single-shot calls and autonomous loops), three nested failure recovery loops, and checkpoint-based execution for durability. The approach was validated through [[SWE-AF]], an open-source system that generated complete pull requests with minimal human iteration required.

---

## Overview

[[AgentField]] developed a novel approach to [[autonomous code generation]] where multiple [[AI agents]] work in parallel on a shared codebase, coordinating through git worktrees and structured communication protocols. Rather than having one engineer guide a single coding session, the system manages dozens of concurrent agent instances, each operating on isolated branches that merge through an intent-aware gate system.

The key achievement: draft pull requests that have already undergone multiple rounds of automated writing, testing, review, and verification before human review. The human role shifted from line-by-line iteration guidance to architectural sign-off.

---

## Fundamental Architecture

### The Two Modes of LLM Integration

The most critical architectural decision is separating LLM access into two distinct primitives:

#### 1. Constrained Single-Shot Calls (`.ai()`)

**Purpose:** Routing, classification, and structured decision-making

**Characteristics:**
- Single turn, no iteration
- Structured input and output
- No tool use
- Predictable latency and cost
- Output suitable for downstream routing logic

**Use Cases:**
- Issue guidance classification ("Does this need deeper QA?")
- Risk assessment ("Is this change high-risk?")
- Dependency analysis
- Planning decisions

**Cost Profile:** Fractions of a cent, milliseconds latency

**Example Output:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### 2. Autonomous Loops (`.harness()`)

**Purpose:** Full software development tasks with iteration and tool use

**Characteristics:**
- Multi-turn, goal-driven
- Full tool access (filesystem, test runner, git)
- Iterative refinement on failure
- Unpredictable latency and cost
- Verifiable outcomes (passing tests, working code)

**Use Cases:**
- Implementing features
- Writing and debugging code
- Running test suites
- Discovering and fixing failures

**Cost Profile:** Dollars per invocation, minutes to hours per task

**Key Difference from `.ai()`:**
The harness was not derived from studying other frameworks. It emerged from observing actual build failures and recognizing that agents needed a full coding environment with iteration capability. It represents an abstraction discovered through implementation rather than anticipated through design.

### Why Separation Matters

Unified LLM access creates operational blindness:
- Cannot set SLAs on response time
- Cannot predict costs reliably
- Cannot design consistent retry logic
- Cannot reason about system behavior

The two-mode approach enables:
- Cheap, fast routing decisions
- Expensive, thorough work execution
- Clear cost attribution
- Predictable system behavior

---

## Failure Recovery and Control Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three nested control loops, each handling different failure types.

### Inner Loop: Per-Issue Iteration

**Scope:** Single issue, up to 5 iterations

**Mechanism:** Agent receives feedback from [[QA]] and code review, then retries with better information

**Success Criteria:**
- All acceptance criteria met
- Tests passing
- Code review approved

**Example:** The app-module issue in the diagrams build had all 119 tests passing but was missing a `pub mod app;` export in `lib.rs`. The module was invisible to consumers despite being technically correct. The inner loop caught this on iteration 2 and fixed it.

**Failure Handling:** If the inner loop exhausts iterations, escalate to the middle loop

### Middle Loop: Issue Advisor

**Scope:** Single issue, after inner loop exhaustion

**Activation Trigger:** Issue fails to pass after 5 inner loop iterations

**Available Actions:**

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Keep criteria, try different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Prompt Bias:** Final invocation explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retries

**Debt Recording:** All gaps are recorded as typed, structured data:
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

**Example:** The integration-tests issue in the diagrams build timed out after 2700 seconds. The tests were correct; the CLI binary had an infinite loop. Retrying would never help because the same agent would produce the same deadlock. The advisor blocked it, recorded typed debt, and let the rest of the build work around the gap.

### Outer Loop: Replanner

**Scope:** Entire remaining build, triggered by unrecoverable failures at a dependency level

**Triggers:**
- Multiple issues in a level producing unrecoverable failures
- Debt accumulation exceeding thresholds
- Structural impossibilities discovered during execution

**Capabilities:**
- Skip downstream dependents no longer viable
- Restructure remaining issue graph
- Reduce overall scope
- Abort if necessary

**State Propagation:** Previous replan decisions fed back on subsequent invocations to prevent repeating failed strategies

**Failure Handling:** If the replanner itself crashes (timeout, malformed output), default to **continue** rather than abort. For expensive workflows, graceful degradation is better than fail-fast.

### Control Loop Integration

The three loops work together hierarchically:

1. **Inner loop handles:** Problems the same agent can solve with better feedback
2. **Middle loop handles:** Issues that need a different approach or scope adjustment
3. **Outer loop handles:** Structural problems requiring work reorganization

This hierarchy prevents both infinite retry loops and premature abandonment of viable work.

---

## Durability and Checkpointing

At $116 per build with 200+ invocations, a crash at invocation 140 cannot mean restarting from invocation 1. The system treats multi-agent builds as long-running, expensive processes requiring survival-grade infrastructure.

### Checkpoint Structure

Checkpoints capture full execution state at every level boundary:

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

**Captured Information:**
- Current execution level
- Completed levels (can skip on resume)
- Full issue list
- Original plan summary
- Replan history
- Accumulated debt items
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)

**Resume Capability:** `resume_build()` loads the checkpoint, skips completed levels, and continues from exact failure point

**Probability Model:** Without checkpointing, interruption probability approaches 1 as builds grow longer. Checkpointing inverts this: longer workflows accumulate more recovery points, not more fragility.

### Git Worktree Isolation

Each issue operates in its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.), providing:
- Complete filesystem isolation
- No lock contention
- No conflicts during parallel coding
-