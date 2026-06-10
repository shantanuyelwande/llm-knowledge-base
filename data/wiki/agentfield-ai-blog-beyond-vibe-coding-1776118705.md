---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-10T06:31:09.026517
raw_file_updated: 2026-06-10T06:31:09.026517
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-10T06:31:09.026517
tags: []
related_topics: []
backlinked_by: []
---
# Beyond Vibe Coding: Multi-Agent Software Development at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[LLM]] agents to collaboratively produce production-quality code through structured coordination, failure recovery, and checkpoint-based execution. The key innovation separates [[LLM Integration]] into two distinct modes: constrained single-shot calls for routing and classification, and autonomous harnesses for iterative code generation. The system demonstrates that architectural design and systematic failure handling outweigh model capability in determining multi-agent system performance.

## Overview

[[Beyond Vibe Coding]] describes the engineering approach developed by AgentField for coordinating multiple [[Claude Code]] instances on shared codebases. Rather than having human engineers iterate with individual AI assistants, the system enables dozens of autonomous agents to work in parallel on different issues while maintaining code coherence. The approach emerged from practical experience building and iterating on large-scale multi-agent systems, with lessons that apply broadly to [[AI Agent Orchestration]].

The core insight is that naive multi-agent coordination produces convergence failures—situations where individual agents produce locally correct work that fails to integrate coherently. Solving this required three key innovations: two distinct modes of [[LLM]] access, nested failure recovery loops, and checkpoint-based execution for cost resilience.

## Key Concepts and Findings

### Two Modes of LLM Integration

The most critical architectural decision separates [[LLM Integration]] into two distinct primitives rather than giving all agents uniform access:

#### Constrained Calls (.ai())

The **constrained call** pattern provides:
- Single-shot execution with no iteration
- Structured input and output schemas
- No tool use or external dependencies
- Predictable latency (milliseconds) and cost (fractions of a cent)
- Deterministic routing based on classification results

This mode handles decision-making tasks such as:
- Issue severity and scope assessment
- Risk classification ("Is this change high-risk?")
- Routing decisions ("Does this need deeper QA?")
- Planning and decomposition

Each issue receives structured guidance that downstream agents consume:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harnesses (.harness())

The **autonomous harness** pattern provides:
- Multi-turn, tool-using iteration
- Full coding environment with filesystem, test runner, and git access
- Goal-driven execution until verifiable outcome
- Unpredictable latency and cost proportional to problem complexity
- Failure recovery through retry and escalation

A single harness invocation may execute 150+ tool-use turns, cost $4 or more on complex issues, and take significant time. The harness is evaluated on outcomes, not intermediate steps.

**Design Philosophy**: Rather than inventing abstractions theoretically, AgentField extracted these primitives from recurring patterns in failing builds. The constrained call was obvious from the start; the harness emerged from months of observing how agents needed full coding environments with iteration loops.

### Nested Failure Recovery Loops

In a 200+ invocation build, failures are normal, not exceptions. The system implements three nested control loops to handle different failure modes:

#### Inner Loop: Per-Issue Iteration (up to 5 attempts)

The agent retries itself with feedback from [[QA]] and code review. This handles problems the same agent can solve with better information.

**Example**: The app-module issue in the diagrams build passed all 119 tests but failed review because the module was not exported in `lib.rs`. The inner loop caught this and iteration 2 fixed it with 354 tests passing.

#### Middle Loop: Issue Advisor

When the inner loop exhausts attempts, an issue advisor activates with five typed recovery actions:

| Action | Purpose |
|--------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The advisor's final invocation includes explicit warnings that this is the last chance, biasing toward acceptance or escalation rather than futile retries.

#### Outer Loop: Replanner

Fires when issues in a dependency level produce unrecoverable failures. The replanner sees full execution state and can:
- Skip downstream dependents
- Restructure the issue dependency graph
- Reduce scope
- Abort if necessary

Previous replan decisions feed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes, the system defaults to `continue` rather than `abort` for graceful degradation.

#### Typed Debt System

Failures are not hidden—they are recorded as structured debt items:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, enabling them to work around known gaps instead of building on false assumptions.

### Cost-Resilient Execution Through Checkpointing

A $116 multi-agent build cannot restart from scratch after a failure at invocation 140. The system implements comprehensive checkpointing at every level boundary:

#### Checkpoint Contents

The checkpoint captures:
- Current execution level and completed levels
- Full issue list and dependency graph
- Original planning summary
- Replan count and accumulated debt
- Git state (integration branch, original SHA, worktree mappings)

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

Resume operations load the checkpoint, skip completed levels, and continue from the exact failure point.

#### Git Worktree Isolation

Each issue gets its own [[Git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`). This provides:
- Complete isolation between parallel issues
- No lock contention or conflicts during coding
- Ability to parallelize more aggressively than humans would attempt
- Clear integration points between levels

The planner consistently produces finer-grained issue graphs than humans would, decomposing epics into 50-100 issues with dependency structures that maximize parallelism.

#### Gate Sequence Between Levels

Every level transition enforces clean handoffs:

1. **Merge gate**: Integrate completed branches with intent-aware conflict resolution
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate downstream
4. **Split gate**: Inject sub-issues if any were split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

### Architecture Outperforms Model Selection

Contrary to intuition, model capability does not determine multi-agent system performance. Testing on a Node.js CLI benchmark showed:

- **Claude Haiku** (cheapest model, ~$20 total): **95/100**
- **MiniMax M2.5** via OpenRouter (~$6 total): **95/100**
- Single-agent approaches: 59-73/100

The same architecture scored identically across different models because verification loops and escalation hierarchies compensate for model capability through iteration. Cheaper models simply require more inner loop cycles to reach the same outcome.

Model selection becomes a runtime parameter rather than an architectural decision:

```json
{
  "runtime": "claude_code",
  "models": {
    "default": "sonnet",
    "coder": "haiku",
    "qa": "haiku",
    "architect": "sonnet"
  }
}
```

Each role (coder, reviewer, QA, planner, merger) can be assigned independently and swapped for cost/quality optimization.

## Case