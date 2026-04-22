---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-22T04:51:47.751368
raw_file_updated: 2026-04-22T04:51:47.751368
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-22T04:51:47.751368
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Software Development with Autonomous Orchestration

## Summary

This article documents how to orchestrate multiple autonomous AI agents (200+) to collaboratively produce production-quality code through a system called SWE-AF. The key innovation separates [[LLM Integration]] into two distinct primitives: constrained single-shot calls (`.ai()`) for routing and classification, and autonomous harnesses (`.harness()`) for iterative coding tasks. The system manages agent failures through three nested control loops, uses [[Git Worktrees]] for isolation, and implements checkpoint-based recovery to survive expensive long-running builds. The architecture proves more important than model selection, with cheaper models performing equivalently to expensive ones when paired with proper orchestration.

---

## Core Architecture

### Two LLM Primitives

The foundational insight is that effective [[Multi-Agent Systems]] require two distinct modes of [[LLM Integration]], not a single unified approach.

#### Constrained Call (`.ai()`)

The **constrained call** operates as a single-shot, structured interaction:
- **Input**: Structured prompt with defined parameters
- **Output**: Predictable, typed responses (JSON schema)
- **Tools**: None - direct inference only
- **Latency**: Milliseconds
- **Cost**: Fractions of a cent
- **Use Cases**: Routing decisions, classification, planning guidance

Example guidance block produced by a constrained call:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

These calls drive downstream routing decisions with minimal cost, allowing expensive harness invocations to be allocated strategically.

#### Autonomous Harness (`.harness()`)

The **autonomous harness** provides a full coding environment with iterative problem-solving:
- **Environment**: Full filesystem access, test runner, git integration
- **Iteration**: Multi-turn tool use until goal achievement
- **Tools**: File operations, code execution, test running, git commands
- **Latency**: Minutes to hours depending on task complexity
- **Cost**: $0.50 to $4+ per invocation
- **Use Cases**: Code generation, implementation, testing, debugging

A single harness invocation may execute 50-150 tool-use turns to solve a complex issue. The system evaluates outcomes, not intermediate steps—the harness either delivers working code or fails in a way the failure-recovery system can classify and handle.

### The Convergence Problem

When multiple agents work on a shared codebase in parallel, they must produce one coherent result. The initial implementation discovered this problem sharply: one agent built an entire API layer on a module another agent never exported. Tests passed because the downstream agent mocked the dependency. Code compiled. The PR appeared clean. The system did not work.

Solving convergence requires:
- **Isolation primitives** to prevent agents from interfering with each other
- **Failure recovery mechanisms** to handle inevitable conflicts
- **State reconciliation** to merge parallel work into coherent output

---

## Failure Management

### Three Nested Control Loops

Agent failures are not edge cases in large builds—they are the normal path. A 200+ invocation build experiences failures constantly. The system addresses this through three nested control loops, each with different scope and recovery strategies.

#### Inner Loop: Per-Issue Iteration

**Scope**: Single issue, up to 5 iterations  
**Trigger**: QA or code review rejection  
**Recovery**: Same agent, same criteria, new attempt with feedback

The agent receives specific feedback about what failed (test results, review comments) and attempts to fix it. This loop handles problems where the same agent can succeed with better information.

**Example**: The `app-module` issue passed all 119 tests and met acceptance criteria, but code review identified that the module was not exported in `lib.rs`. The inner loop caught this, and iteration 2 fixed the export, resulting in 354 passing tests.

#### Middle Loop: Issue Advisor

**Scope**: Single issue, exhausted inner loop  
**Trigger**: Inner loop reaches iteration limit without success  
**Recovery**: Five typed recovery actions

When an issue cannot be fixed locally, the issue advisor activates with five possible actions:

| Action | Meaning | Use Case |
|--------|---------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt | Feature too complex for current scope |
| `RETRY_APPROACH` | Same criteria, different strategy | Wrong library or algorithm choice |
| `SPLIT` | Break into smaller sub-issues | Issue too large to solve atomically |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed debt | Acceptable quality with known limitations |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work | Upstream planning was wrong |

On its final invocation, the advisor prompt explicitly warns that this is the last chance, biasing toward acceptance or escalation rather than futile retries.

**Example**: The `integration-tests` issue timed out after 2700 seconds due to an infinite loop in the CLI binary. Retrying the same agent would produce the same timeout. The advisor blocked the issue, recorded typed debt:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

This debt record propagates to dependent issues so they can work around the gap.

#### Outer Loop: Replanner

**Scope**: Full build, dependency level failures  
**Trigger**: Unrecoverable failures escalated from middle loop  
**Recovery**: Global restructuring

The replanner sees the full execution state and can:
- Skip downstream dependents of failed issues
- Restructure the remaining issue dependency graph
- Reduce scope globally
- Abort if necessary

Previous replan decisions are fed back on subsequent invocations to prevent repeating failed strategies. If the replanner itself crashes (LLM timeout, malformed output), the system defaults to **continue** rather than abort—graceful degradation is better than fail-fast for expensive workflows.

### Failure Classification

Different failures require different responses:

**Deadlocks** (infinite loops, resource exhaustion): Cannot be fixed by retrying the same approach. Escalate to advisor for blocking or splitting.

**Review-caught issues** (missing exports, architectural problems): Tests pass but code violates conventions or structure. Inner loop can fix with feedback.

**Regressions** (previously working code breaks): Indicates agent instability or conflicting changes. May need splitting or approach change.

**Cascading failures** (fix introduces new bug): Multiple iterations required; track regression patterns to prevent repeating mistakes.

---

## Execution Durability

### Checkpoint-Based Recovery

Multi-agent builds running 200+ invocations across hours represent expensive computations. A crash at invocation 140 cannot mean restarting from invocation 1.

The system checkpoints at every level boundary, capturing:

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

**Resume capability**: `resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 does not restart from minute 0.

**Git state capture**: The checkpoint records integration branch state, original branch, initial commit SHA, and worktree directory mappings. Resumed builds reconstruct the full workspace without re-cloning.

**Probability improvement**: As builds grow longer, checkpoint recovery makes them more reliable, not more fragile. Each completed level adds a recovery point, inverting the relationship between workflow duration and failure probability.

### Isolation with Git Worktrees

Each issue receives its own [[Git Worktrees|git worktree]] on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`, etc.). This provides:

- **No lock contention**: Parallel issues modify different working directories
- **No conflicts during coding**: Each agent works independently until