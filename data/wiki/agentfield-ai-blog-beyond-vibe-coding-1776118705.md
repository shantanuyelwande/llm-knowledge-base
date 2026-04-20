---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-20T05:18:17.808149
raw_file_updated: 2026-04-20T05:18:17.808149
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-20T05:18:17.808149
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents how [[AgentField]] orchestrates 200+ autonomous [[Large Language Model|LLM]] agents to collaboratively produce production code through a system called SWE-AF. The work introduces two key architectural primitives—constrained single-shot calls (`.ai()`) and autonomous harnesses (`.harness()`)—combined with three nested failure recovery loops to handle the complexity of coordinating multiple agents on shared codebases. The approach prioritizes architectural design and failure recovery over raw model capability, achieving comparable results across different model tiers through systematic verification and iteration.

---

## Overview

Building software with multiple autonomous [[AI agent|AI agents]] requires fundamentally different architectural patterns than single-agent systems. Traditional approaches that give every agent identical tool access and iteration capabilities create unpredictable costs, unmeasurable outcomes, and coordination failures. The AgentField team discovered through production experience that successful multi-agent code generation depends on three critical insights: separating LLM integration modes, building resilient failure recovery hierarchies, and implementing checkpoint-based execution for cost-effective long-running workflows.

## Core Architectural Principles

### Two Modes of LLM Integration

The most significant architectural mistake in multi-agent systems is providing uniform [[LLM]] access to all agents. Instead, successful orchestration requires two distinct integration patterns:

#### The Constrained Call (`.ai()`)

A **constrained call** is a single-shot LLM invocation with:
- Structured input and output schemas
- No tool use or iteration
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic outputs for routing decisions

These calls handle classification tasks like "Does this issue need deeper QA?" or "Is this change high-risk?" The system uses constrained calls to generate `IssueGuidance` blocks containing structured fields:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

These structured outputs drive routing and downstream decision-making with predictable resource consumption.

#### The Autonomous Harness (`.harness()`)

An **autonomous harness** is a multi-turn, goal-driven [[agent]] with:
- Full coding environment access (filesystem, test runners, version control)
- Tool use and iteration capability
- Open-ended iteration until verifiable outcomes are reached
- Variable cost and latency based on task complexity

Harnesses receive goals and toolsets, then iterate through reading files, writing code, running tests, discovering failures, and attempting fixes. A single harness invocation may run 150+ tool-use turns and cost several dollars on complex issues.

**Key Insight**: The constrained call is not novel—most [[agentic framework|agentic frameworks]] implement some version of it. The harness abstraction emerged from observing production failures rather than theoretical design. It captures the pattern of agents needing full development environments with failure recovery, which existing frameworks did not cleanly abstract.

### Nested Failure Recovery Loops

In multi-agent builds with 200+ invocations, failures are not edge cases but the normal execution path. The system implements three nested control loops to handle different failure classes:

#### Inner Loop: Per-Issue Iteration

The **inner loop** runs up to 5 iterations per issue, with the agent retrying based on feedback from [[Quality Assurance|QA]] and code review. This loop handles problems the same agent can solve with better information, such as:
- Missing module exports (caught by review, fixed by agent)
- Test failures with clear error messages
- Compilation errors with diagnostic output

#### Middle Loop: Issue Advisor

When the inner loop exhausts retries, an **issue advisor** activates with five typed recovery actions:

| Action | Purpose |
|--------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., alternative library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

The advisor's final invocation includes explicit warnings that this is the last opportunity, biasing decisions toward acceptance or escalation rather than futile retries.

#### Outer Loop: Replanner

The **replanner** fires when issues in a dependency level produce unrecoverable failures. It has full visibility of execution state and can:
- Skip downstream dependents
- Restructure the issue dependency graph
- Reduce scope
- Abort the build

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes, the system defaults to `continue` rather than abort—graceful degradation is preferable to fail-fast for expensive workflows.

### Practical Example: The Deadlock Pattern

A Rust CLI tool's integration-tests issue timed out after 2700 seconds. The tests themselves were correct (code review approved them), but the CLI binary had an infinite loop. Retrying would produce the same timeout:

```json
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

The system blocked the issue, recorded typed debt, and allowed the rest of the build to continue around the gap. Downstream agents received `debt_notes` explaining what upstream failed to deliver, enabling them to work around known gaps instead of building on broken assumptions.

## Cost-Effective Execution at Scale

### Checkpoint-Based Recovery

A 200-invocation build costing $116 cannot restart from scratch on failure. The system checkpoints at every level boundary, capturing:

- Current execution level
- Completed levels
- All issues in the build
- Original plan summary
- Replanning history
- Accumulated debt items
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)

`resume_build()` loads checkpoints and continues from the exact failure point. A build failing at minute 25 of a 30-minute execution resumes from minute 25, not minute 0. As builds grow longer, they accumulate more recovery points rather than more fragility.

### Parallel Isolation with Git Worktrees

Each issue receives its own [[git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This pattern:
- Eliminates lock contention during parallel coding
- Prevents merge conflicts during concurrent development
- Allows agents to modify different files independently

Between levels, a **merger agent** integrates completed branches into the integration branch. The merger is not mechanical `git merge`—it reads architecture specifications and file conflict annotations to make intent-aware resolution decisions. When two issues modify the same file, the merger understands each change's purpose and preserves both intents.

Between-level gates enforce clean handoffs:

1. **Merge gate**: integrate completed branches
2. **Integration test gate**: validate merged code still works together
3. **Debt gate**: process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: inject sub-issues if any issue was split
5. **Replan gate**: invoke replanner if failures escalated
6. **Checkpoint**: serialize full state to disk

### Unified API Interface

The control plane provides a single API endpoint regardless of which agents exist, how many spawn, or what failure recovery occurs internally:

```bash
curl -X POST http://localhost:8080/api/v1/execute/async/swe-planner.build \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "goal": "Build a diagrams-as-code CLI tool with DSL parser and SVG output",
      "repo_url": "https://github.com/user/my-project",
      "config": {
        "runtime": "claude_code",
        "models": { "default": "sonnet", "coder": "haiku" }
      }
    }
  }'
```

The response is a `202 Accepted` with an `execution_id`. Hours later, a draft [[pull request]] includes the complete codebase, test results, and a debt section documenting every scope reduction.

## Model Selection vs. Architecture

Contrary to initial assumptions, smarter models do not necessarily produce better results. On a Node.js CLI benchmark, the same architecture scored 95/100