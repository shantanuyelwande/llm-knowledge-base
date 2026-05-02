---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:16:10.698487
raw_file_updated: 2026-05-02T05:16:10.698487
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:16:10.698487
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents architectural patterns for orchestrating multiple [[autonomous agents]] to collaboratively produce production-quality code. The system demonstrates how 200+ [[LLM]]-powered agents can coordinate on a shared codebase through careful separation of concerns, nested failure recovery loops, and checkpoint-based execution. Key findings show that [[system architecture]] and [[failure recovery]] matter more than model selection for achieving high-quality results at scale.

---

## Overview

[[AgentField]] is an infrastructure framework that enables teams to move human engineers from direct iteration loops to architectural review roles. Instead of a single engineer guiding one [[Claude Code]] session through incremental changes, the system orchestrates dozens of autonomous agent instances working in parallel on a shared codebase.

The core insight emerged from early attempts: when multiple autonomous processes operate on the same repository, simple retry logic is insufficient. A pull request that compiles and passes tests can still be fundamentally broken—one agent may build functionality on top of modules that other agents never exported. This is the **convergence problem**: getting N independent processes to produce one coherent result requires explicit primitives for [[isolation]], [[failure recovery]], and [[state reconciliation]].

---

## Two Fundamental LLM Integration Modes

The most critical architectural decision is separating [[LLM integration]] into two distinct primitives rather than giving all agents identical access patterns.

### Constrained Single-Shot Call (`.ai()`)

The first mode is a **constrained call**: single-turn, structured input/output, no tool use, no iteration.

**Characteristics:**
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)
- Deterministic output structure
- No retry loops or tool use

**Use cases:**
- [[Routing]] decisions ("Does this issue need deeper QA?")
- [[Classification]] tasks ("Is this change high-risk?")
- [[Planning]] and decomposition
- [[Risk assessment]]

**Example output:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

Downstream code switches on these structured fields to route work appropriately. This separation ensures routing decisions remain cheap while expensive work is reserved for complex tasks.

### Autonomous Harness (`.harness()`)

The second mode is an **autonomous loop**: multi-turn, tool-using, goal-driven iteration.

**Characteristics:**
- Full coding environment ([[filesystem]] access, test execution, [[git]])
- Iterative problem-solving
- Variable latency and cost
- Tool use and feedback loops
- Verifiable outcomes

**Capabilities:**
- Read and modify source files
- Execute test suites
- Run build commands
- Discover failures and retry
- Integrate with [[version control]]

**Typical cost:** $0.50 to $4.26 per invocation depending on complexity

The harness abstraction emerged from observing real build failures rather than hypothetical design exercises. It represents the minimal set of capabilities needed for autonomous code generation at scale.

### Routing Based on Risk

The two modes coexist in the same system. A boolean flag from a cheap `.ai()` call determines execution path:

```
if needs_deeper_qa:
  path = [coder, qa, reviewer, synthesizer]  # 4 calls
else:
  path = [coder, reviewer]                    # 2 calls
```

Routing is cheap; work is expensive. Keeping them separate enables both flexibility and cost efficiency.

---

## Failure Recovery: Three Nested Control Loops

In large builds (200+ invocations), failures are the normal path, not edge cases. A single retry loop cannot handle the diversity of failure modes. The system implements three nested control loops, each with distinct responsibilities.

### Inner Loop: Per-Issue Iteration

**Scope:** Single issue, up to 5 iterations  
**Participants:** Coder, QA agent, Code reviewer  
**Recovery:** Retry with feedback

The inner loop handles problems that the same agent can solve given better information. For example:

- **Missing export issue:** Coder produces 119 passing tests but forgets `pub mod app;` in `lib.rs`. Code reviewer catches this architectural violation. Iteration 2 adds the export; all 354 tests pass.
- **Structural problems:** Agent produces correct tests but broken implementation. QA identifies the gap. Agent retries with explicit error feedback.

**Key principle:** If an agent can fix a problem given better information about what went wrong, the inner loop handles it.

### Middle Loop: Issue Advisor

**Scope:** When inner loop exhausted (5 iterations)  
**Participants:** Issue advisor agent  
**Recovery actions:**

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as [[typed debt]] |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., "use different library") |
| `SPLIT` | Decompose into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close with explicit debt items for each gap |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Example failure:** Integration tests timeout after 2700 seconds due to infinite loop in CLI binary. Retrying produces identical timeout. The advisor blocks the issue, records typed debt, and allows dependent work to continue:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents receive `debt_notes` explaining what upstream failed to deliver, so they build around known gaps rather than on broken assumptions.

### Outer Loop: Replanner

**Scope:** When issues produce unrecoverable failures  
**Participants:** Replanner agent, full execution state  
**Capabilities:**
- Skip dependent issues that cannot proceed
- Restructure remaining issue graph
- Reduce scope across multiple issues
- Prevent repeated failed strategies

**Default behavior:** If the replanner itself crashes (timeout, malformed output), the system continues rather than aborts. For expensive workflows, graceful degradation beats fail-fast.

### Failure Mode Examples

**Deadlock that retrying cannot fix:**
- Integration tests timeout due to binary infinite loop
- Tests are well-written; code is broken
- Retrying produces identical failure
- Solution: Block, record debt, continue

**Review catches what tests miss:**
- 119 tests pass, acceptance criteria met
- Code reviewer identifies missing `pub mod` export
- Module invisible to library consumers
- Solution: Inner loop iteration 2 fixes export

**Regression on trivial tasks:**
- Simple "create Cargo.toml and src/main.rs" issue
- Iteration 1: passes all tests, review approved
- Iteration 2: main.rs references non-existent modules
- Solution: Inner loop detects and fixes regression

**Cascading verification failures:**
- Final acceptance verification takes 3 iterations
- Iteration 1: `set -e` crashes, infinite recursion
- Iteration 2: `|| true` makes cargo fmt always pass
- Iteration 3: correct implementation
- Solution: Nested loops detect and repair cascading issues

---

## Durable Execution and Checkpointing

Multi-agent builds running 200+ invocations at ~$116 per build cannot restart from scratch on failure. The system treats long-running builds like [[high-performance computing]] workloads: checkpointing is a survival requirement, not an optimization.

### Checkpoint Scope

Every level boundary captures full system state:

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

**What is captured:**
- Completed and in-progress dependency levels
- Full issue list and execution state
- [[Git]] state (integration branch, original branch, commit SHA)
- Worktree