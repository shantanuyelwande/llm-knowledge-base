---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-03T05:36:00.813485
raw_file_updated: 2026-05-03T05:36:00.813485
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-03T05:36:00.813485
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Software Development Architecture

## Summary

This article describes the architectural patterns and orchestration strategies used by AgentField to coordinate 200+ autonomous [[LLM]] agents working in parallel on a shared codebase. The key innovation is separating [[LLM integration]] into two distinct primitives—constrained single-shot calls and autonomous harnesses—combined with three nested failure recovery loops and checkpoint-based execution to produce production-ready code at scale.

---

## Overview

[[Autonomous agents]] working on software development require fundamentally different orchestration patterns than single-agent systems. Traditional approaches that apply the same [[LLM]] integration method to all tasks fail to scale when dozens of agents must coordinate on a shared codebase. This article covers the three core lessons learned from running 200+ agent invocations on real production builds, including a Rust CLI tool, Go SDK features, and Node.js applications.

The core insight is that **architecture matters more than model selection**. The same control loop structure achieved 95/100 on both expensive and budget models, suggesting that verification loops and escalation hierarchies compensate for raw model capability through structured iteration.

---

## 1. Two Modes of LLM Integration

### The Problem with Uniform Integration

The most critical architectural mistake is giving every agent the same kind of [[LLM]] access. When all calls can use any tool, take any amount of time, and produce any shape of output, the system becomes operationally opaque:

- **Unpredictable costs**: A call might take 200ms or 45 minutes
- **Unmeasurable SLAs**: Retry logic becomes meaningless without knowing what you're retrying
- **Loss of routing capability**: No way to distinguish cheap classification from expensive problem-solving

### The Two-Primitive Solution

#### `.ai()` - Constrained Single-Shot Calls

The first primitive is a **constrained call** with these properties:

- Single-shot execution (no iteration)
- Structured input and output
- No tool use or external calls
- Predictable latency (milliseconds)
- Predictable cost (fractions of a cent)

**Use cases:**
- Routing decisions ("Does this issue need deeper QA?")
- Risk classification ("Is this change high-risk?")
- Structured analysis that drives downstream behavior

**Example output:**
```
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases, run QA in parallel"
```

The structured fields enable downstream routing. The `agent_guidance` string provides context for autonomous agents.

#### `.harness()` - Autonomous Loops

The second primitive is an **autonomous harness** with these properties:

- Multi-turn execution with iteration
- Full tool access (filesystem, test runners, [[git]], compilers)
- Goal-driven operation (receives objective, returns verifiable result)
- Variable latency and cost depending on problem complexity
- Failure recovery and retry logic built in

**Use cases:**
- Code generation and implementation
- Test writing and validation
- Debugging and problem-solving
- Architectural decisions requiring exploration

In real builds, a single harness invocation might run 50-150 tool-use turns and cost $0.50-$4.26 depending on issue complexity.

### Integration Pattern

The two primitives coexist in the same system. A cheap `.ai()` call determines routing:

```
if needs_deeper_qa == true:
  run [coder, qa_parallel, reviewer_parallel, synthesizer]
else:
  run [coder, reviewer]
```

This separation keeps routing overhead minimal while allowing expensive work to be thorough.

---

## 2. Failure Recovery and Escalation Hierarchies

### The Convergence Problem

When 30+ autonomous agents work on a shared codebase, the first major failure is the **convergence problem**: getting N independent processes to produce one coherent result. The classic example:

- Agent A builds an API layer and exports it from `module.rs`
- Agent B builds a consumer that imports from `module.rs`
- Tests pass because Agent B mocks the dependency
- Code compiles
- The system does not work

Solving this requires primitives for isolation, failure recovery, and state reconciliation.

### Three Nested Control Loops

The system uses three escalating levels of failure recovery, each with different responsibilities:

#### Inner Loop: Per-Issue Iteration (Up to 5 attempts)

The agent retries itself with feedback from [[QA]] and code review.

**Example: App Module Export**
- Iteration 1: 119 passing tests, all criteria met, but module not exported in `lib.rs`
- QA passed, but reviewer blocked on convention violation
- Iteration 2: Added `pub mod app;` line, 354 tests passing, approved

This loop handles problems the same agent can solve with better information.

#### Middle Loop: Issue Advisor (Recovery Actions)

When the inner loop exhausts retries, an advisor activates with five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., different library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

**Example: Integration Tests Deadlock**
- Issue: CLI binary has infinite loop, tests timeout after 2700 seconds
- Iteration 1-2: Inner loop retries fail; same timeout both times
- Advisor action: `block` (unrecoverable failure)
- Result: Record typed debt item, continue build with workaround

The advisor's final invocation receives an explicit warning that this is the last chance, biasing it toward acceptance or escalation rather than futile retry.

#### Outer Loop: Replanner (Dependency-Level Recovery)

When issues in a dependency level produce unrecoverable failures, the replanner fires with full execution state visibility:

- Skip downstream dependents that depend on failed issues
- Restructure the remaining issue graph
- Reduce scope
- Abort if necessary

Previous replan decisions feed back on subsequent invocations to prevent repeating failed strategies.

**Graceful degradation default**: If the replanner crashes due to [[LLM]] timeout or malformed output, the system defaults to **continue** rather than abort. For expensive workflows, partial success beats total failure.

### Typed Debt Tracking

Rather than silently dropping failures, the system records them as typed, severity-rated data structures:

```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

Downstream agents consume `debt_notes` and work around known gaps instead of building on false assumptions. The final PR includes a debt section documenting every scope reduction, enabling human review to understand what was deferred and why.

---

## 3. Durable Execution and Cost Management

### The Checkpointing Strategy

At $116 per build (200+ invocations), restarting from scratch after a crash is economically unviable. The system checkpoints at every level boundary.

**Checkpoint captures:**
- Current execution level and completed levels
- Full issue list and dependency structure
- Original plan summary
- Accumulated debt items
- Git state (branches, worktrees, original commit SHA)

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": ["project-scaffold", "types-module", ...],
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A build that fails at minute 25 of 30 does not restart from minute 0.

### Git Worktree Isolation

Each issue gets its own [[git]] worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`). This pattern, borrowed from developer workflows, provides:

- **No lock contention**: Parallel issues modify different worktrees
- **Clean isolation**: Changes stay isolated until ready to merge
- **Automatic conflict detection**: Planning phase identifies file conflicts upfront

In the diagrams build, level 2 ran three issues in parallel (lexer, parser,