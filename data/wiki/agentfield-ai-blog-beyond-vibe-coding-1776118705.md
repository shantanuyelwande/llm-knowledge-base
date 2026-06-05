---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-05T06:30:42.050786
raw_file_updated: 2026-06-05T06:30:42.050786
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-05T06:30:42.050786
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation at Scale

## Summary

This article documents the architectural patterns and lessons learned from orchestrating 200+ autonomous [[AI agents]] to collaboratively generate production code. The system demonstrates that proper architecture and failure recovery mechanisms can outperform single-agent approaches and achieve comparable results across different [[large language models]] (LLMs). Key innovations include two distinct modes of [[LLM]] integration, three nested failure recovery loops, and checkpoint-based execution for cost-effective long-running workflows.

---

## Overview

[[AgentField]] is an infrastructure platform for multi-agent AI systems that emerged from practical experience building [[SWE-AF]], a system for autonomous software engineering. Rather than having individual engineers iterate with single [[Claude Code]] sessions, the platform coordinates dozens of parallel agent instances on shared codebases, moving human responsibility from the iteration loop to the final review phase.

The core challenge addressed by this work is the **convergence problem**: ensuring N autonomous processes produce one coherent result rather than conflicting implementations. Early attempts at parallel agent coordination resulted in code that passed tests but was fundamentally broken—agents built implementations on top of modules that other agents never exported.

## Key Architectural Principles

### 1. Two Modes of LLM Integration

Rather than giving all agents identical [[LLM]] access, the system separates integration into two complementary primitives:

#### Constrained Single-Shot Calls (`.ai()`)

- **Characteristics**: Single-turn, structured input/output, no tool use, no iteration
- **Purpose**: Routing, classification, and decision-making
- **Cost**: Fractions of a cent per call
- **Latency**: Milliseconds
- **Use Cases**: 
  - Determining if an issue needs deeper [[quality assurance|QA]]
  - Assessing change risk level
  - Routing work to appropriate agents

Each issue receives a structured `IssueGuidance` block with fields like `needs_new_tests`, `estimated_scope`, and `agent_guidance` that drive downstream decisions.

#### Autonomous Harnesses (`.harness()`)

- **Characteristics**: Multi-turn, tool-using, goal-driven iteration
- **Purpose**: Complete coding tasks with full development environment
- **Capabilities**: 
  - Filesystem access
  - Test execution
  - Git operations
  - Iterative refinement
- **Cost**: Variable, up to $4+ per complex issue
- **Outcome**: Verifiable results, not specific implementation paths

The harness abstraction emerged from observing recurring failure patterns rather than from theoretical design. It represents the abstraction the team wished they had started with.

### 2. Three Nested Failure Recovery Loops

Failures are normal in large-scale multi-agent systems, not edge cases. The system implements graduated response mechanisms:

#### Inner Loop (Per-Issue Iteration)
- **Scope**: Up to 5 retry attempts per issue
- **Mechanism**: Agent receives feedback from [[quality assurance|QA]] and code review
- **Success Condition**: Issue passes acceptance criteria
- **Example**: Missing module export caught and fixed automatically

#### Middle Loop (Issue Advisor)
Activates when inner loop exhaustion occurs. Five typed recovery actions:

| Action | Response |
|--------|----------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Same criteria, different strategy (e.g., alternative library) |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; record each gap as typed, severity-rated debt |
| `ESCALATE_TO_REPLAN` | Cannot be fixed locally; restructure remaining work |

#### Outer Loop (Replanner)
- **Scope**: Full execution state visibility
- **Capabilities**: Skip downstream dependents, restructure issue graph, reduce scope, abort if necessary
- **Memory**: Previous replan decisions prevent repeating failed strategies
- **Default Behavior**: Continue rather than abort on LLM failures for graceful degradation

### 3. Durable Execution Through Checkpointing

At $116 per complete build, failures cannot trigger full restart from the beginning. The system implements high-performance computing-style checkpointing:

#### Checkpoint Contents
- Current execution level and completed levels
- Full issue list and original plan summary
- Replan count and accumulated debt records
- Git state (integration branch, worktree mappings, commit SHAs)

#### Recovery Mechanism
`resume_build()` loads the checkpoint, skips completed work, and continues from exact failure point. A 30-minute build failing at minute 25 resumes at minute 25, not minute 0.

## Isolation and Coordination

### Git Worktree Pattern

Each issue receives a dedicated git worktree on a branch (e.g., `issue/01-project-scaffold`). This provides:
- **Isolation**: No lock contention or conflicts during parallel coding
- **Parallelism**: Multiple issues can modify different files simultaneously
- **Clarity**: Each issue's changes are self-contained until integration

### Merger Agent

Between execution levels, a merger agent integrates completed branches into an integration branch. Unlike mechanical `git merge`, the merger:
- Reads the architecture specification
- Understands file conflict annotations from planning phase
- Makes intent-aware resolution decisions
- Preserves both intents when multiple issues modify the same file

### Level Gates

Between every execution level, a sequence of gates ensures clean handoff:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code still works together
3. **Debt gate**: Process completed-with-debt results, propagate debt notes downstream
4. **Split gate**: Inject sub-issues if any issue was split
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

## Real-World Failure Examples

### Case 1: Deadlocks That Retrying Cannot Fix

**Problem**: Integration test issue timed out after 2700 seconds. Tests were correct and passed code review, but the CLI binary had an infinite loop. Retrying the same agent produced the same timeout.

**Solution**: Block the issue and record typed debt:
```json
{
  "type": "dropped_acceptance_criterion",
  "criterion": "integration tests pass end-to-end",
  "issue_name": "integration-tests",
  "severity": "high",
  "justification": "CLI binary deadlocks on invocation; test suite correct but binary needs runtime debugging beyond automated repair"
}
```

### Case 2: Review Catches That Tests Miss

**Problem**: App module had 119 passing tests and met all acceptance criteria, but the module was not exported in `lib.rs`, making it inaccessible to library consumers.

**Solution**: Code reviewer blocked the issue. Agent fixed with one line (`pub mod app;`) in iteration 2, with 354 tests passing.

### Case 3: Regressions on Trivial Tasks

**Problem**: Project scaffold issue (creating `Cargo.toml` and `src/main.rs`) passed iteration 1 but regressed in iteration 2 when the agent added module declarations for non-existent code.

**Lesson**: Autonomous code generation fails unpredictably, even on simple tasks.

### Case 4: Cascading Verification Failures

**Problem**: Final acceptance verification required 3 iterations to resolve `set -e` crashes, macOS-specific flag issues, infinite recursion, and incorrect `cargo fmt` checks.

**Pattern**: Complex verification tasks require multiple iterations even after individual issues pass.

## Planning and Decomposition

[[AI agents]] consistently produce finer-grained, more parallelizable issue graphs than humans would attempt. The planner decomposes large epics into 50-100 issues with dependency structures that maximize parallelism while respecting constraints.

In the diagrams build:
- 15 issues across 6 dependency levels
- Level 2 ran 3 issues (lexer, parser, validator) in parallel
- No lock contention or conflicts during coding

This level of coordination would be impractical for human teams, but it becomes a scheduling problem for orchestration systems.

## Cost and Model Performance

### Architecture Outperforms Model Selection

Benchmark results (Node.js CLI todo app, same architecture):
- **Claude Haiku** (cheapest): 95/100
- **MiniMax M2.5** (~$6 total): 95/100
- **Single-agent approaches**: 59-73/100

The same architecture scored identically with both the cheapest and mid-tier models because verification loops and escalation hierarchies compensate for model capability through iteration.

### Cost Breakdown

**Diagrams build** ($116 total, 200+ invocations):
- Architect: $0.83 (9 turns, 345 seconds)
-