---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-11T06:03:57.939005
raw_file_updated: 2026-05-11T06:03:57.939005
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-11T06:03:57.939005
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation Architecture

## Summary

This article documents the architectural patterns and lessons learned from orchestrating 200+ autonomous [[LLM]] agents to collaboratively produce production-quality code through a structured, failure-resilient pipeline. The approach moves human responsibility from iterative guidance to final architectural review, achieving high-quality results through systematic failure recovery and verification loops rather than raw model capability.

## Overview

[[AgentField]] is an infrastructure system for coordinating multiple autonomous [[AI]] agents on shared codebases. Rather than having a single engineer iterate with one [[Claude Code]] instance, the system enables dozens of parallel agent instances (called "harnesses") to coordinate on the same repository. Each agent has full access to the filesystem, test execution, and git operations.

The core innovation is moving human engineers from the iteration loop—where they guide each change—to the review loop, where they approve finished, pre-verified draft pull requests. This shift required solving three critical problems:

1. **Operational clarity** through distinct LLM integration modes
2. **Systematic failure recovery** through nested control loops
3. **Cost-effective durability** through checkpointing and isolation

## Key Concepts

### Two Primitives for LLM Integration

The fundamental architectural mistake in multi-agent systems is treating all [[LLM]] calls identically. AgentField separates LLM integration into two distinct primitives:

#### Constrained Call (`.ai()`)

**Purpose:** Single-shot, deterministic operations with predictable behavior

**Characteristics:**
- Single turn, no iteration
- Structured input and output
- No tool use
- Millisecond latency
- Fraction-of-a-cent cost

**Use cases:**
- Routing decisions ("Does this issue need deeper QA?")
- Classification ("Is this change high-risk?")
- Planning guidance generation
- Risk assessment

**Example output:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

#### Autonomous Harness (`.harness()`)

**Purpose:** Multi-turn, goal-driven iteration with full development environment access

**Characteristics:**
- Multi-turn with iteration
- Full tool access (filesystem, test runner, git)
- Goal-oriented execution
- Variable latency (minutes to hours)
- Higher cost ($0.50-$4.26 per invocation)

**Capabilities:**
- Read and write files
- Execute tests
- Discover failures
- Iterate on solutions
- Verify outcomes

**Execution model:** Receives a goal and toolset, iterates until producing a verifiable outcome. The system checks what was delivered, not how it was achieved.

### Three Nested Failure Recovery Loops

In a 200+ invocation build, failures are the normal path, not edge cases. The system implements three hierarchical recovery loops:

#### Inner Loop: Per-Issue Iteration

**Scope:** Single issue, up to 5 iterations maximum

**Function:** Allows the same agent to retry with feedback from [[QA]] and review

**Recovery mechanism:** 
- Agent receives explicit feedback about test failures, code review comments, or architectural issues
- Agent attempts fix with improved context
- Loop continues until success or iteration limit

**Example:** The app-module issue failed iteration 1 because a module wasn't exported in `lib.rs`, despite 119 passing tests. Iteration 2 added the missing `pub mod app;` declaration.

#### Middle Loop: Issue Advisor

**Scope:** Single issue after inner loop exhaustion

**Function:** Makes typed recovery decisions with five possible actions

| Action | Behavior | Use Case |
|--------|----------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed [[debt]] | Scope reduction is acceptable |
| `RETRY_APPROACH` | Same criteria, different strategy | Previous approach was fundamentally wrong |
| `SPLIT` | Break into smaller sub-issues | Complexity exceeded agent capability |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt | Good enough solution exists |
| `ESCALATE_TO_REPLAN` | Restructure remaining work | Cannot be fixed locally |

**Key feature:** Final invocation explicitly warns this is the last chance, biasing toward acceptance or escalation rather than futile retry.

**Example:** Integration-tests issue timed out with infinite loop in CLI binary. After two failed iterations, advisor blocked the issue and recorded a typed debt item:
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

#### Outer Loop: Replanner

**Scope:** Full build after dependency level completion

**Function:** Restructures work based on accumulated failures

**Capabilities:**
- Skip downstream dependents of failed issues
- Restructure remaining issue graph
- Reduce scope
- Abort if necessary
- Prevent repeated failed strategies using decision history

**Failure mode:** If replanner crashes, system defaults to `continue` rather than abort. For expensive workflows, graceful degradation beats fail-fast.

### Debt-Based Failure Handling

Rather than retrying indefinitely or silently dropping failures, the system uses **typed debt items**—structured, severity-rated records of deferred work. Downstream agents receive `debt_notes` explaining what upstream failed to deliver, enabling them to work around known gaps instead of building on broken assumptions.

This approach:
- Makes failures explicit and traceable
- Prevents cascading failures from hidden assumptions
- Allows the build to continue and complete
- Documents exactly what was deferred and why

## Execution Architecture

### Planning and Decomposition

The planner decomposes large epics into fine-grained issue graphs with explicit dependency structures. Notably, the planner produces more parallelizable structures than humans would typically create:

- Human planners avoid 50-100 issue decompositions due to coordination overhead
- AI planner creates these structures because the orchestrator absorbs coordination cost
- Fine-grained issues enable higher parallelism and better failure isolation

**Planning output includes:**
- Dependency graph with explicit levels
- File conflict annotations
- Estimated scope for each issue
- Guidance strings for downstream agents

### Isolation with Git Worktrees

Each issue operates in its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This provides:

- **No lock contention:** Multiple issues modify different files simultaneously
- **Clean isolation:** Changes stay isolated until ready to merge
- **Parallel execution:** Dependency level runs multiple issues in parallel

**Between levels**, a merger agent integrates completed branches into the integration branch. The merger is not mechanical—it reads architecture specs and file conflict annotations to make intent-aware resolution decisions.

### Level Gates

Every dependency level completes through a sequence of gates:

1. **Merge gate:** Integrate completed branches
2. **Integration test gate:** Validate merged code works together
3. **Debt gate:** Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate:** Inject sub-issues if any issue was split
5. **Replan gate:** Invoke replanner if failures escalated
6. **Checkpoint:** Serialize full state to disk

Each gate can be configured for human approval in regulated environments. The sequence remains identical; only approval policy varies.

## Durability and Checkpointing

Long-running, expensive builds require checkpoint-based recovery. The diagrams-as-code build cost ~$116 and ran 200+ invocations—a crash at invocation 140 cannot mean restarting from invocation 1.

### Checkpoint Contents

Captured at every level boundary:

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

### Recovery Mechanism

`resume_build()` loads checkpoint, skips completed levels, and continues from exact failure point. A 30-minute build failing at minute 25 doesn't restart