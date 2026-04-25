---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-25T04:41:15.588807
raw_file_updated: 2026-04-25T04:41:15.588807
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-25T04:41:15.588807
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation and Orchestration

## Summary

This article documents the architectural patterns and operational lessons learned from orchestrating 200+ autonomous [[LLM]] agents to collaboratively produce production code. Rather than relying on model capability alone, the system achieves high-quality results through structured failure recovery, checkpoint-based execution, and two distinct modes of [[LLM integration]]: constrained single-shot calls and autonomous harnesses. The approach demonstrates that architecture and orchestration patterns matter more than model selection for complex multi-agent workflows.

## Overview

[[AgentField]] and its specialized implementation [[SWE-AF]] represent a shift in how autonomous systems approach software engineering. Instead of having a single engineer iterate with a single [[Claude Code]] session, the system coordinates dozens of parallel agent instances on a shared codebase. This requires solving the **convergence problem**: how to get N autonomous processes to produce one coherent result.

The core insight is that successful multi-agent systems require:
- Two distinct [[LLM]] integration patterns, not one
- Three nested failure recovery loops
- Checkpoint-based execution for cost efficiency
- Architecture-driven design rather than model-driven assumptions

## Key Architectural Patterns

### Two Modes of LLM Integration

The system separates [[LLM]] access into two complementary primitives:

#### Constrained Single-Shot Calls (`.ai()`)

- **Purpose**: Routing, classification, and decision-making
- **Characteristics**: Single-turn, structured input/output, no tools, deterministic behavior
- **Cost**: Fractions of a cent per call
- **Latency**: Milliseconds
- **Example**: Analyzing an issue to generate `IssueGuidance` with fields like `needs_new_tests`, `estimated_scope`, `touches_interfaces`, and `agent_guidance`

The constrained call enables operational predictability. SLAs become meaningful, costs become predictable, and retry logic becomes unambiguous.

#### Autonomous Harnesses (`.harness()`)

- **Purpose**: Goal-driven problem-solving with iteration
- **Characteristics**: Multi-turn, tool-using, full coding environment access
- **Environment**: Filesystem access, test execution, git operations
- **Cost**: Variable, from $0.50 to $4+ per invocation depending on complexity
- **Process**: Receives a goal and toolset, iterates until producing verifiable outcomes

The harness abstraction emerged from observing real failures rather than from theoretical design. It represents the abstraction the team wished existed from the beginning.

### Three Nested Control Loops

When agents fail—which they do constantly in 200+ invocation builds—the system requires escalating levels of intervention:

#### Inner Loop (Per-Issue Iteration)

- **Scope**: Single issue, up to 5 iterations
- **Mechanism**: Agent retries with feedback from [[QA]] and code review
- **Example**: The `app-module` issue where a missing `pub mod app;` export was caught and fixed
- **Success Rate**: Handles problems the same agent can solve with better information

#### Middle Loop (Issue Advisor)

Activates when the inner loop exhausts all retries. Provides five typed recovery actions:

| Action | Behavior |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record gaps as typed debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

#### Outer Loop (Replanner)

- **Trigger**: Unrecoverable failures in a dependency level
- **Scope**: Full execution state visibility
- **Actions**: Skip dependents, restructure issue graph, reduce scope, or abort
- **Memory**: Previous replan decisions prevent repeated failed strategies
- **Default**: Continue on LLM failure rather than abort (graceful degradation)

### Failure Patterns and Recovery

The diagrams-as-code build revealed four classes of failures:

**Deadlocks That Retrying Cannot Fix**
- The `integration-tests` issue timed out after 2700 seconds
- Inner retry produced identical timeout
- Solution: Block the issue, record typed debt, continue build
- Debt records are structured data structures downstream agents consume

**Review Catches That Tests Miss**
- The `app-module` passed 119 tests but violated Rust conventions
- Module was not exported in `lib.rs`, making it inaccessible
- Solution: Inner loop caught and fixed on iteration 2

**Regressions on Trivial Tasks**
- The `project-scaffold` issue (create Cargo.toml and src/main.rs) regressed on iteration 2
- Agent added module declarations for non-existent code
- Demonstrates unpredictability even on simple tasks

**Cascading Verification Failures**
- The `final-acceptance-verification` issue required three iterations
- Each iteration discovered different problems: shell error handling, platform-specific flags, infinite recursion, missing dependency checks

## Cost and Efficiency

### Real-World Build Costs

| Project | Issues | Agent Invocations | Total Cost |
|---------|--------|-------------------|-----------|
| Diagrams-as-code CLI (Rust) | 15 | 200+ | $116 |
| Go SDK feature | 10 | 80+ | $19 |
| Node.js benchmark | N/A | Multiple | $6-20 |

The diagrams build cost breakdown:
- Architect: $0.83 (9 turns, 345 seconds)
- Individual coders: $0.50 to $4.26 per invocation
- Most expensive single agent: QA on integration-tests at $4.26

### Architecture Beats Model Selection

Empirical testing showed that architecture and orchestration patterns matter more than model capability:

- **Haiku (cheapest)**: 95/100 on Node.js benchmark
- **MiniMax M2.5 (~$6)**: 95/100 on same task
- **Single-agent approaches**: 59-73/100

The same architecture scored identically with both cheap and expensive models because verification loops and escalation hierarchies compensate for model capability through iteration.

## Durable Execution Through Checkpointing

Long-running, expensive builds require checkpoint-based recovery:

### Checkpoint Contents

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": [...],
  "original_plan_summary": "...",
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

The checkpoint captures:
- Progress through dependency levels
- Complete issue list and original plan
- Git state (integration branch, original branch, initial commit SHA)
- Worktree directory mappings
- Accumulated debt items

### Recovery Strategy

- Failures at invocation 140 of 200 resume from checkpoint, not from invocation 1
- Saves 30+ minutes of execution on a failed build
- At $116 per build, restart-from-scratch is economically infeasible

## Isolation and Parallelization

### Git Worktrees for Agent Isolation

Each issue gets its own git worktree on a dedicated branch (`issue/01-project-scaffold`, `issue/02-types-module`). This enables:
- True parallelism without lock contention
- Isolated changes until merge gates
- Independent test execution per issue

### Agent Planning Produces Finer Granularity

Agents decompose large epics into 50-100 issues with dependency structures humans would avoid due to coordination costs. The orchestration system absorbs this coordination cost:
- Humans managing 80 parallel branches: impractical
- Orchestrator managing 80 parallel worktrees: a scheduling problem

### Gate Sequence Between Levels

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code works together
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

Every level starts clean; no level inherits dirty state from previous ones.

## Integration and API Design

### Unified Control Plane Interface

The system provides a single API endpoint regardless of runtime or model:

```bash
curl -X POST http://localhost:8080/api/v1/execute/async/swe-planner.build \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "goal