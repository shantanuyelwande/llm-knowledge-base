---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-05T05:19:38.670229
raw_file_updated: 2026-05-05T05:19:38.670229
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-05T05:19:38.670229
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Software Engineering with Autonomous Code Orchestration

## Summary

This article describes how [[AgentField]] orchestrates 200+ autonomous [[LLM]]-powered agents to collaboratively develop production software through a system called [[SWE-AF]]. Rather than relying on a single intelligent model, the approach uses architectural patterns including nested failure recovery loops, [[checkpoint-based execution]], and two distinct modes of [[LLM integration]] to achieve high-quality code generation at manageable cost. The system moves human engineers from line-by-line iteration to architectural review, with the orchestration handling verification, testing, and failure recovery automatically.

---

## Overview

Traditional approaches to [[AI-assisted software development]] rely on a single developer iterating with one [[code generation]] session. AgentField's approach inverts this model: dozens or hundreds of autonomous [[code agents]] work in parallel on a shared codebase, coordinating through structured interfaces and automated verification loops.

The fundamental challenge, called the **convergence problem**, emerges when multiple autonomous processes must produce a single coherent result. Early attempts failed when agents built incompatible implementations—code that compiled and passed isolated tests but could not work together because one agent relied on an API another agent never exported.

### Key Achievement

The system successfully ran 200+ agent invocations on a Rust [[CLI]] project with 15 issues, producing a draft pull request requiring minimal human review, at a cost of $116. Similar results achieved 95/100 on a Node.js benchmark using both expensive and cheap models, proving that architecture matters more than model selection.

---

## Two Modes of LLM Integration

The most significant architectural insight is that multi-agent systems require two fundamentally different types of [[LLM]] access, not one.

### The Constrained Call: `.ai()`

The first mode is a **constrained single-shot call**, implemented as `.ai()` in AgentField:

- **Characteristics**: Single-turn, no tool use, structured input and output
- **Purpose**: Routing, classification, and planning decisions
- **Cost**: Fractions of a cent
- **Latency**: Milliseconds
- **Use cases**: 
  - Determining if an issue needs deeper QA
  - Assessing risk level of changes
  - Classifying issue complexity
  - Generating routing guidance

These calls produce structured outputs that downstream code can act upon:

```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The predictability of constrained calls enables [[SLA]] guarantees, cost prediction, and reliable [[retry logic]].

### The Autonomous Loop: `.harness()`

The second mode is an **autonomous harness**, implemented as `.harness()`:

- **Characteristics**: Multi-turn, tool-using, goal-driven iteration
- **Purpose**: Complex problem-solving with full development environment
- **Tools**: Filesystem access, test execution, [[git]] integration
- **Iteration**: Retries until verifiable outcome achieved
- **Cost**: Dollars per invocation (up to $4+ on complex issues)
- **Latency**: Minutes to hours
- **Outcome**: Code, tests, and verified results

The harness provides a complete coding environment where agents read files, write code, run tests, discover failures, and iterate. Unlike constrained calls, harnesses are opaque—the system verifies the output, not the process.

### Integration Pattern

The two modes coexist in the same system. A cheap `.ai()` call makes a routing decision (e.g., `needs_deeper_qa: true`), which determines whether an issue follows a lean two-call path or a thorough four-call path with parallel QA and review. Routing is inexpensive; work is expensive.

---

## Three Nested Failure Loops

In a 200+ invocation build, failures are normal, not edge cases. The system requires three nested control loops to handle different failure types.

### Inner Loop: Per-Issue Iteration

The **inner loop** runs per issue, up to 5 iterations maximum:

- Runs the same agent on the same issue with feedback from [[QA]] and code review
- Handles problems the agent can solve with better information
- Example: Missing `pub mod` export that tests passed but violated Rust conventions

**Iteration record example:**
```json
{
  "iteration": 1,
  "action": "fix",
  "summary": "App module not exported in lib.rs",
  "qa_passed": true,
  "review_approved": false,
  "review_blocking": true
}
```

### Middle Loop: Issue Advisor

When the inner loop exhausts retries, the **issue advisor** activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record severity-rated gaps |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The advisor's final invocation includes an explicit warning that it is the last chance, biasing toward acceptance or escalation rather than futile retries.

**Example of blocking with debt:**
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks; test suite correct but binary needs runtime debugging"
}
```

Blocked issues record typed debt that downstream agents receive as `debt_notes`, allowing them to work around known gaps instead of assuming unavailable interfaces.

### Outer Loop: Replanner

The **outer loop** fires when issues produce unrecoverable failures:

- Sees full execution state across all issues
- Can skip downstream dependents
- Restructures remaining issue graph
- Reduces scope or aborts
- Remembers previous replan decisions to prevent repeating failed strategies

If the replanner itself crashes, the system defaults to **continue** rather than abort. For expensive workflows, graceful degradation beats fail-fast.

### Failure Type Examples

**Deadlocks that retrying cannot fix**: A test suite was well-written and passed review, but the CLI binary it tested had an infinite loop. Retrying the same agent produced the same deadlock. Solution: Block the issue, record debt, let the build continue.

**Review catches that tests miss**: A module was technically sound with 119 passing tests but was not exported in `lib.rs`, making it inaccessible to consumers. Solution: Inner loop caught it; iteration 2 fixed the export.

**Regressions on trivial tasks**: A simple scaffolding task (create `Cargo.toml` and `src/main.rs`) passed iteration 1 but regressed in iteration 2 when the agent added non-existent module declarations. Solution: Inner loop detected regression; iteration 3 succeeded.

**Cascading verification failures**: Final acceptance verification took three iterations, fixing platform-specific bugs, infinite recursion, and format check issues sequentially.

---

## Checkpoint-Based Execution for Expensive Workflows

At $116 per build, a crash at invocation 140 cannot mean restarting from invocation 1. Inspired by [[high-performance computing]] practices, the system checkpoints at every level boundary.

### Checkpoint Contents

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

**Git state preservation**: Checkpoints capture git integration branch, original branch, initial commit SHA, and worktree directory mappings, allowing resumed builds to reconstruct the workspace without re-cloning.

### Isolation with Git Worktrees

Each issue receives a dedicated [[git worktree]] on an isolated branch (