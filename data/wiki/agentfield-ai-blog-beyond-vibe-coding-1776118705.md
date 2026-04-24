---
title: agentfield-ai-blog-beyond-vibe-coding-1776118705
source_file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
source_url: https://agentfield.ai/blog/beyond-vibe-coding
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:56:41.042180
raw_file_updated: 2026-04-24T18:56:41.042180
version: 1
sources:
  - file: agentfield-ai-blog-beyond-vibe-coding-1776118705.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:56:41.042180
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Code Generation Architecture

## Summary

**Beyond Vibe Coding** documents AgentField's approach to orchestrating 200+ autonomous AI agents on shared codebases to produce production-ready pull requests. The system separates [[LLM Integration]] into two primitives—constrained single-shot calls and autonomous harnesses—implements three nested failure recovery loops, and uses checkpoint-based execution to survive expensive, long-running builds. Key findings show that architectural design and failure recovery matter more than model selection, with the same system achieving 95/100 scores across both expensive and budget models.

---

## Overview

AgentField's multi-agent orchestration system represents a shift in how AI-assisted software engineering can be structured. Rather than having individual engineers iterate with single [[AI Code Assistants|AI code assistant]] instances, the platform enables dozens of autonomous agents to coordinate on parallel tasks within a shared codebase, moving human responsibility from line-by-line iteration to architectural review.

The system emerged from practical experience building real projects:
- **Diagrams-as-code CLI** (Rust): 15 issues, 200+ agent invocations, $116 total cost
- **Go SDK feature**: 10 issues, 80+ invocations, $19 total cost
- **Node.js benchmark**: 95/100 score on both cheapest and mid-tier models

---

## Core Architecture

### Two Modes of LLM Integration

The fundamental architectural insight is that different tasks require fundamentally different kinds of [[LLM]] access. The system implements two complementary primitives:

#### Constrained Call (`.ai()`)

Single-shot, structured [[API]] calls with:
- **Inputs**: Bounded, well-defined schemas
- **Outputs**: Structured, predictable formats
- **Tools**: None—pure reasoning
- **Latency**: Milliseconds
- **Cost**: Fractions of a cent

Used for routing and classification tasks:
- "Does this issue need deeper QA?"
- "Is this change high-risk?"
- Generating issue guidance blocks with structured fields

Example guidance output:
```json
IssueGuidance:
  needs_new_tests: true
  estimated_scope: "medium"
  touches_interfaces: true
  needs_deeper_qa: true
  agent_guidance: "Complex parsing logic with edge cases"
```

#### Autonomous Harness (`.harness()`)

Multi-turn, tool-using, goal-driven loops with:
- **Environment**: Full filesystem access, test execution, git operations
- **Iteration**: Retry on failure with feedback
- **Output**: Verifiable outcomes rather than process transparency
- **Cost**: Variable, up to $4+ per invocation on complex issues
- **Turns**: Up to 150 tool-use calls per issue

The harness emerged from observing recurring patterns in build failures rather than from theoretical design. It represents the abstraction the team wished existed from the beginning.

### Failure Recovery: Three Nested Control Loops

Because failures are the normal path in 200+ invocation builds, the system implements three escalating recovery mechanisms:

#### Inner Loop (Per-Issue)

- **Scope**: Single issue, up to 5 retry iterations
- **Mechanism**: Agent receives feedback from [[QA]] and code review, attempts fixes
- **Success**: Problem solved with same agent given better information
- **Example**: Missing `pub mod` export caught by reviewer and fixed in iteration 2

#### Middle Loop (Issue Advisor)

Activates when the inner loop exhausts retries. Provides five typed recovery actions:

| Action | Purpose |
|--------|---------|
| `RETRY_MODIFIED` | Relax acceptance criteria, record gap as typed debt |
| `RETRY_APPROACH` | Keep criteria, try different strategy |
| `SPLIT` | Break issue into smaller sub-issues |
| `ACCEPT_WITH_DEBT` | Close enough; document gaps |
| `ESCALATE_TO_REPLAN` | Cannot fix locally; restructure remaining work |

The final invocation explicitly warns that this is the last chance, biasing toward acceptance or escalation.

#### Outer Loop (Replanner)

- **Trigger**: Unrecoverable failures at a dependency level
- **Scope**: Full execution state visibility
- **Actions**: Skip downstream dependents, restructure issue graph, reduce scope, abort
- **Memory**: Previous replan decisions prevent repeating failed strategies
- **Default**: Continue on LLM errors rather than fail-fast (graceful degradation)

### Failure Patterns in Practice

Real builds illustrate why single retry loops fail:

**Deadlocks that retrying cannot fix**: Integration tests timeout after 2700 seconds due to infinite loop in CLI binary. Tests pass (they're correct), but the code is broken. Retrying the same agent produces the same deadlock. Solution: block the issue, record typed debt, continue.

**Review catches that tests miss**: App module technically sound with 119 passing tests, but not exported in `lib.rs`, making it invisible to library consumers. Inner loop catches and fixes in iteration 2.

**Regressions on trivial tasks**: Project scaffold issue (create Cargo.toml and src/main.rs) passes iteration 1, regresses in iteration 2 when agent adds non-existent module declarations.

**Cascading verification failures**: Final acceptance verification requires 3 iterations to fix: `set -e` crashes, macOS-specific flags, infinite recursion, then `|| true` masking formatting issues.

---

## Execution Durability

### Checkpoint-Based Recovery

At $116 per build, restarting from scratch after a failure is economically unviable. The system checkpoints at every dependency level boundary:

```json
{
  "current_level": 3,
  "completed_levels": [0, 1, 2],
  "all_issues": [...],
  "original_plan_summary": "15 issues organized in 6 levels...",
  "replan_count": 0,
  "accumulated_debt": [...]
}
```

Checkpoints capture:
- Completed level indices
- Full issue graph with dependency structure
- Git state (integration branch, original branch, initial commit SHA, worktree mappings)
- Accumulated debt records
- Replan history

`resume_build()` loads the checkpoint, skips completed levels, and continues from the exact failure point. A 30-minute build failing at minute 25 resumes at minute 25, not minute 0.

### Git Worktree Isolation

Each issue gets a dedicated git worktree on its own branch (`issue/01-project-scaffold`, `issue/02-types-module`). This pattern:
- Eliminates lock contention during parallel coding
- Prevents conflicts until intentional merge
- Allows rollback of individual issues without affecting others

Between levels, a merger agent integrates completed branches into the integration branch using intent-aware resolution (reading architecture specs and file conflict annotations from planning phase).

### Level Gate Sequence

Every level enforces a clean handoff through five sequential gates:

1. **Merge gate**: Integrate completed branches
2. **Integration test gate**: Validate merged code works together
3. **Debt gate**: Process completed-with-debt results, propagate `debt_notes` downstream
4. **Split gate**: Inject sub-issues if any were split during execution
5. **Replan gate**: Invoke replanner if failures escalated
6. **Checkpoint**: Serialize full state to disk

---

## Planning and Parallelization

The system generates more parallelizable issue graphs than humans typically produce:

- **Human planning**: ~15-20 issues with conservative dependency structure
- **AI planning**: 50-100 issues with fine-grained parallelization

The planner decomposes epics into smaller units than humans would attempt, because humans face coordination overhead that the orchestrator absorbs automatically. Parallel worktree management is a scheduling problem, not an operational burden.

The diagrams-as-code build shows this: level 2 ran three issues in parallel (lexer, parser, validator), each in its own worktree, each modifying different files, with no lock contention.

---

## Cost and Model Selection

### Architecture Beats Model Intelligence

Contrary to expectations, smarter models do not proportionally improve results. Testing on a Node.js CLI benchmark:

- **Claude Haiku** ($20 total): 95/100
- **MiniMax M2.5** ($6 total): 95/100
- **Single-agent baselines**: 59-73/100

The same architecture achieves 95/100 regardless of model capability because verification loops and escalation hierarchies compensate for lower model intelligence through iteration.

### Model Configuration

Models are runtime parameters assigned per role:

```json
{
  "runtime": "claude_code",
  "models": {
    "default": "sonnet",
    "coder":