---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-10T05:42:34.146739
raw_file_updated: 2026-05-10T05:42:34.146739
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-10T05:42:34.146739
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents the architectural patterns and lessons learned from orchestrating 200+ autonomous AI agents to collaboratively produce production-quality code. The system, called [[SWE-AF]], demonstrates that effective [[multi-agent systems]] require two distinct modes of [[LLM integration]], three nested failure recovery loops, and checkpoint-based execution to handle the inevitable failures that occur at scale.

## Overview

[[AgentField]] is an infrastructure platform that enables teams to coordinate multiple [[Claude Code]] instances working in parallel on a shared codebase. Rather than having a single engineer iterate with one coding assistant, the system orchestrates dozens of autonomous agents that work in parallel, with human engineers reviewing finished, verified draft pull requests rather than guiding each incremental change.

The first major challenge discovered was the **convergence problem**: getting N independent autonomous processes to produce one coherent result without conflicts, missing dependencies, or broken abstractions. This required developing new primitives for [[isolation]], [[failure recovery]], and [[state reconciliation]].

## Architecture Principles

### Two Modes of LLM Integration

The most critical architectural insight is that multi-agent systems require two fundamentally different kinds of LLM access, not one unified approach.

#### Constrained Calls (.ai())

The first primitive is a **constrained call** (`.ai()`): a single-shot [[LLM]] interaction with:
- Structured input and output
- No tool use
- No iteration
- Predictable latency and cost
- Deterministic routing logic

These calls handle classification tasks like:
- "Does this issue need deeper QA?"
- "Is this change high-risk?"
- Risk assessment and issue routing

Each issue receives an `IssueGuidance` block with structured fields:
```
needs_new_tests: boolean
estimated_scope: "small" | "medium" | "large"
touches_interfaces: boolean
needs_deeper_qa: boolean
agent_guidance: string
```

A typical constrained call costs fractions of a cent and completes in milliseconds, making it viable for high-volume routing decisions.

#### Autonomous Harnesses (.harness())

The second primitive is an **autonomous harness** (`.harness()`): a multi-turn, tool-using, goal-driven agent that:
- Receives a goal and toolset
- Iterates until producing a verifiable outcome
- Has full filesystem access
- Can execute tests and build processes
- Maintains git state
- Discovers failures and retries independently

The harness emerged from observing real build failures rather than from theoretical design. It represents the abstraction teams discovered they actually needed after months of iteration.

In the diagrams-as-code build example, a single coder invocation required up to 150 tool-use turns and cost over $4 on complex issues.

### Three Nested Control Loops

Because agents fail constantly—even on trivial tasks—the system requires three hierarchical failure recovery mechanisms.

#### Inner Loop: Per-Issue Iteration

The **inner loop** runs per issue with a maximum of 5 iterations:
- Agent attempts to solve the issue
- [[QA agent]] tests the solution
- [[Code reviewer]] approves or blocks
- On rejection, agent retries with feedback
- Captures both `qa_passed` and `review_approved` states

This loop handles problems that the same agent can solve with better information, such as a missing module export that tests missed.

#### Middle Loop: Issue Advisor

The **middle loop** activates when the inner loop exhausts its iterations. An issue advisor can take five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt items |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The advisor's final invocation includes an explicit warning that this is the last chance, biasing toward acceptance or escalation rather than futile retry.

#### Outer Loop: Replanner

The **outer loop** fires when issues at a dependency level produce unrecoverable failures. The replanner:
- Views the full execution state
- Can skip downstream dependents
- Restructures the remaining issue graph
- Reduces scope or aborts if necessary
- Learns from previous replan decisions to avoid repeating failed strategies

If the replanner itself crashes, the system defaults to **continue** rather than abort, treating graceful degradation as preferable to fail-fast for expensive workflows.

### Failure Pattern Examples

#### Deadlocks Beyond Retry

When the integration-tests issue timed out after 2700 seconds due to a CLI binary infinite loop, retrying the same agent on the same binary produced identical failures. The solution was to **block** the issue, record typed debt, and let downstream work adapt around the gap.

#### Review-Caught Defects

The app-module issue passed all 119 tests and met acceptance criteria, but the code reviewer noticed the module was never exported in `lib.rs`. One missing `pub mod app;` line—invisible to automated tests but critical for library consumers. The inner loop fixed this on iteration 2.

#### Regressions on Simple Tasks

The project-scaffold issue (creating `Cargo.toml` and `src/main.rs`) passed iteration 1 but regressed in iteration 2 when the coder added module declarations for code that didn't exist yet, breaking the build.

#### Cascading Verification

The final-acceptance-verification issue required three iterations to fix four blocking issues: `set -e` crashes, macOS-specific `stat` flags failing on Linux CI, infinite recursion between test files, and missing dependency checks.

## Execution and Durability

### Checkpoint-Based Execution

For expensive builds (the diagrams project cost $116 across 200+ invocations), restarting from failure is economically impractical. The system checkpoints at every level boundary, capturing:

- Current execution level
- Completed levels
- All issues and their status
- Original plan summary
- Replan count
- Accumulated debt items
- Git state (branches, commits, worktree mappings)

When a build fails at invocation 140 of 200, `resume_build()` loads the checkpoint, skips completed work, and continues from the exact failure point. Without checkpointing, the probability of interruption approaches 1 as builds grow longer.

### Git Worktree Isolation

Each issue gets its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.), preventing lock contention and conflicts during parallel coding.

A **merger agent** integrates completed branches between execution levels, making intent-aware resolution decisions when multiple issues modify the same file. The merger reads architecture specifications and conflict annotations from the planning phase to preserve both changes' intentions.

### Gate Sequence Between Levels

Every execution level ends with a structured gate sequence:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code works together
3. **Debt gate**: Process completed-with-debt results
4. **Split gate**: Inject sub-issues if any were split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

Each level starts clean, inheriting no dirty state from predecessors.

### Unified API Interface

The control plane provides a single API endpoint regardless of how many agents are spawned or what failure recovery occurs internally:

```bash
curl -X POST http://localhost:8080/api/v1/execute/async/swe-planner.build \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "goal": "Build a diagrams-as-code CLI tool",
      "repo_url": "https://github.com/user/my-project",
      "config": {
        "runtime": "claude_code",
        "models": { "default": "sonnet", "coder": "haiku" }
      }
    }
  }'
```

The response is a 202 Accepted with an `execution_id`. The build runs asynchronously, with checkpoint recovery handling any interruptions.

## Model Selection vs. Architecture

Empirical testing revealed that **architecture beats model selection**. On a Node.js CLI benchmark, the same orchestration architecture scored 95/100 using both:
- Claude Haiku (cheapest model, ~$20 total)
- MiniMax M2.5 via OpenRouter (~$6 total)

Single-agent approaches on the same task scored 59-73.

The model configuration is a flat parameter map:
```json
{
  "runtime": "claude_code",
  "models