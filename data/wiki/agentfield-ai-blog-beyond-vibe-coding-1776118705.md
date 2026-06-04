---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-04T06:49:16.209295
raw_file_updated: 2026-06-04T06:49:16.209295
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-04T06:49:16.209295
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article describes the architectural patterns and lessons learned from orchestrating 200+ autonomous [[AI agents]] to collaboratively develop software, specifically through the [[AgentField]] framework and its [[SWE-AF]] implementation. It covers the critical distinction between constrained LLM calls and autonomous harnesses, failure recovery strategies across three nested control loops, and checkpoint-based execution for cost-effective long-running workflows.

---

## Overview

[[AgentField]] is an infrastructure platform for coordinating multiple autonomous [[AI agents]] on shared codebases. Rather than having a single engineer iterate with one [[Claude Code]] session, the system enables dozens of agent instances to work in parallel on different issues within the same repository. These agent instances, called **harnesses**, are full coding environments with filesystem access, test execution capabilities, and git integration.

The core challenge is the **convergence problem**: getting N autonomous processes to produce one coherent result requires explicit primitives for isolation, failure recovery, and state reconciliation. Early attempts at parallel agent coordination produced pull requests that appeared correct but contained hidden failures, such as agents building on unexported modules or creating circular dependencies.

## Key Architectural Principles

### 1. Two Modes of LLM Integration

The most critical architectural distinction is separating LLM access into two complementary primitives, rather than giving all agents identical capabilities.

#### Constrained Calls (`.ai()`)

The first mode is a **constrained single-shot call** with the following characteristics:

- **Single-turn execution**: No iteration or tool use
- **Structured input/output**: Predictable format for downstream processing
- **No tools**: Classification and routing only
- **Predictable cost and latency**: Millisecond-scale execution, fraction-of-cent cost

Constrained calls handle routing and classification decisions such as:
- "Does this issue need deeper QA?"
- "Is this change high-risk?"
- Risk assessment and scope estimation

These calls produce structured guidance blocks that drive downstream routing decisions:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (`.harness()`)

The second mode is an **autonomous loop** with these characteristics:

- **Multi-turn execution**: Iterates until goal completion
- **Tool-using**: Full access to filesystem, test runners, and git
- **Goal-driven**: Receives objectives and toolsets, iterates toward verifiable outcomes
- **Outcome-focused**: Results are checked, not execution steps

A single harness invocation on a complex issue can run up to 150 tool-use turns and cost several dollars. The harness receives a goal, reads files, writes code, runs tests, discovers failures, and attempts recovery.

#### Separation Benefits

Keeping these modes separate provides:

- **Cost efficiency**: Cheap routing decisions direct expensive autonomous work
- **Operational predictability**: SLAs, cost projections, and retry logic vary by mode
- **Flexible routing**: A single boolean from a constrained call determines whether an issue uses a lean two-call path (coder, then reviewer) or a thorough four-call path (coder, QA, reviewer in parallel, synthesizer)

### 2. Three Nested Control Loops for Failure Recovery

In a build with 200+ agent invocations, failures are the normal execution path, not edge cases. The system requires three hierarchical control loops to handle different categories of failures.

#### Inner Loop: Per-Issue Iteration

The **inner loop** operates at the issue level with up to 5 iterations maximum:

- Agent receives feedback from [[QA]] and code review
- Retries with improved information
- Handles problems the same agent can solve with better context
- Example: Missing module exports caught by review and fixed on retry

Success criteria:
- QA passes all tests
- Code review approves changes
- All acceptance criteria met

#### Middle Loop: Issue Advisor

When the inner loop exhausts its 5 iterations, the **middle loop** advisor activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap with severity rating |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The advisor explicitly signals that this is the final chance, biasing toward acceptance or escalation rather than futile retries.

#### Outer Loop: Replanner

The **outer loop** replanner fires when issues in a dependency level produce unrecoverable failures:

- Views full execution state across all issues
- Can skip downstream dependents
- Restructure remaining issue graph
- Reduce scope or abort entire build
- Previous replan decisions fed back to prevent repeating failed strategies

If the replanner itself crashes (timeout, malformed output), the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation is preferable to fail-fast behavior.

#### Failure Examples

**Deadlocks that retrying cannot fix**: The integration-tests issue timed out after 2700 seconds due to an infinite loop in the CLI binary. The tests themselves were correct and approved, but the code being tested was broken. Retrying would produce the same timeout. Solution: block the issue, record typed debt, let the build continue.

**Review catches that tests miss**: The app-module had 119 passing tests and met all acceptance criteria, but the module was not exported in `lib.rs`, making it inaccessible to library consumers. The code review caught what tests missed. Solution: inner loop retry fixed the export on iteration 2.

**Regressions on trivial tasks**: The project-scaffold issue (create Cargo.toml and src/main.rs) passed on iteration 1, then regressed on iteration 2 when the coder added module declarations for non-existent code. Solution: inner loop detected and fixed the regression.

**Cascading verification failures**: The final-acceptance-verification issue required three iterations due to cascading failures: `set -e` crashes, macOS-specific `stat` flags, infinite recursion, missing dependency checks, and `|| true` masking formatting failures.

### 3. Checkpoint-Based Execution for Cost Efficiency

With builds costing $50-$150 and running 200+ invocations, a crash at invocation 140 cannot mean restarting from invocation 1. The system treats multi-agent builds as long-running, expensive processes requiring durability from the start.

#### Checkpoint Capture

The system checkpoints at every dependency level boundary, capturing:

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

The checkpoint also captures:
- Git state (integration branch, original branch, initial commit SHA)
- Worktree directory mappings
- All completed issue results
- Typed debt records

#### Recovery and Resumption

`resume_build()` loads the checkpoint and continues from the exact failure point:

- Skips completed levels
- Reconstructs full workspace without re-cloning
- Continues with same orchestration state

Without checkpoint recovery, longer workflows accumulate more fragility. With checkpointing, longer workflows accumulate more recovery points.

#### Git Worktree Isolation

Each issue gets its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`):

- No lock contention during parallel coding
- No conflicts between concurrent modifications
- Enables finer-grained parallelization than humans typically attempt

The system consistently decomposes large epics into 50-100 issues with dependency structures that humans would avoid due to coordination costs. The orchestrator absorbs this coordination cost through automated scheduling.

#### Level Gates

Between dependency levels, a sequence of gates enforces clean handoffs:

1. **Merge gate**: Integrate completed branches using intent-aware conflict resolution
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate debt notes downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

Every level starts clean. No level