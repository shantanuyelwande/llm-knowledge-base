---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-25T04:40:50.286384
raw_file_updated: 2026-04-25T04:40:50.286384
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-25T04:40:50.286384
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article explores how [[Anthropic]] engineers developed multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs) to improve [[Claude]]'s performance on frontend design and autonomous software engineering tasks. The key innovation involves separating generator and evaluator agents to create feedback loops that drive better outputs, combined with strategic decomposition and context management techniques.

---

## Introduction

Long-running autonomous software engineering presents unique challenges for large language models. While single-pass generations can produce functional outputs, they often lack coherence, polish, and correctness when working on complex tasks. Harness design—the practice of building orchestrated multi-agent systems around language models—provides a systematic approach to overcome these limitations.

This work, conducted by the [[Anthropic]] Labs team, demonstrates that careful harness architecture can dramatically improve application quality across subjective domains like design and objective domains like software engineering, though at increased computational cost.

---

## The Problem with Naive Implementations

### Loss of Coherence Over Time

[[Long-running agents]] face two primary failure modes when executing extended tasks:

1. **Context window degradation**: As conversation history grows, models lose coherence and exhibit "[[context anxiety]]"—a tendency to wrap up work prematurely as they approach perceived context limits.

2. **Self-evaluation bias**: When asked to evaluate their own work, models exhibit systematic positive bias, confidently praising mediocre outputs. This problem is especially acute for subjective tasks like [[frontend design]] where no binary verification exists.

### Solutions and Trade-offs

**Context resets** (clearing the context window and starting fresh) prove more effective than compaction (summarizing earlier conversation in place). While resets provide a clean slate and eliminate context anxiety, they introduce orchestration complexity, token overhead, and latency.

[[Claude Sonnet 4.5]] exhibited context anxiety strongly enough to require context resets for effective performance, while later models like [[Claude Opus 4.6]] largely eliminate this behavior natively, allowing continuous sessions with automatic compaction.

---

## Frontend Design: Making Subjective Quality Gradable

### The Core Insight

Subjective quality can be improved through concrete, gradable criteria that encode design principles. Rather than asking "is this design beautiful?" (unanswerable), the system asks "does this follow our principles for good design?" (verifiable).

### Grading Criteria

The evaluator agent grades frontend designs against four weighted criteria:

- **Design Quality**: Coherence of the whole—do colors, typography, layout, imagery, and details combine to create distinct mood and identity?
- **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Penalizes telltale "[[AI slop]]" patterns like purple gradients over white cards.
- **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. Competence check rather than creativity check.
- **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

Design quality and originality receive heavier weighting, as [[Claude]] naturally performs well on craft and functionality.

### The Generator-Evaluator Loop

Using the [[Claude Agent SDK]], a generator agent creates HTML/CSS/JavaScript frontends while an evaluator agent:
- Interacts with live pages using [[Playwright]] MCP
- Screenshots and studies implementations before scoring
- Provides detailed critiques for iteration

Typical runs involve 5-15 iterations, with each cycle pushing the generator toward more distinctive directions. Full runs stretched up to four hours.

### Key Findings

- **Prompt wording shapes output**: Phrases like "museum quality" steered designs toward specific visual convergence
- **Non-linear improvement**: While scores generally improved, later iterations weren't always preferred by humans
- **Baseline improvement**: Even first iterations outperformed baselines with no prompting, suggesting criteria themselves guide the model away from generic defaults
- **Creative leaps**: The system occasionally produced unexpected creative solutions (e.g., a 3D CSS-rendered gallery space instead of traditional landing page)

---

## Full-Stack Coding: Three-Agent Architecture

### Scaling the GAN-Inspired Pattern

The generator-evaluator pattern scales naturally to [[full-stack development]], mapping onto the software development lifecycle where code review and QA serve the evaluator role.

### System Architecture

The harness consists of three specialized agents:

#### Planner Agent
- **Role**: Expands simple 1-4 sentence prompts into full product specifications
- **Focus**: Ambitious scope and high-level technical design rather than granular implementation details
- **AI Integration**: Identifies opportunities to weave [[AI features]] into product specs
- **Rationale**: Avoids cascading errors from over-specification; allows downstream agents to solve implementation details

#### Generator Agent
- **Role**: Implements application features following the spec
- **Approach**: Sprint-based development (one feature at a time)
- **Stack**: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- **Tools**: Git version control, self-evaluation at sprint end
- **Contract Negotiation**: Agrees with evaluator on "done" criteria before implementation

#### Evaluator Agent
- **Role**: Quality assurance through active testing and verification
- **Testing Method**: Uses [[Playwright]] MCP to click through running applications like a user
- **Grading**: Evaluates against both discovered bugs and design criteria
- **Contract Review**: Validates sprint contracts before implementation begins

### Sprint Contracts

Before each sprint, generator and evaluator negotiate a **sprint contract** that:
- Bridges the gap between high-level user stories and testable implementations
- Defines what "done" looks like for that work chunk
- Specifies verifiable success criteria
- Prevents both over-specification and scope ambiguity

Communication occurs via files, with agents reading and responding through file-based handoffs to maintain context clarity.

### Example: Retro Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness Type | Duration | Cost |
|---|---|---|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Output Issues**:
- Rigid, space-wasting layout
- Unclear workflow requiring trial-and-error
- Broken game mechanics (entities appeared but didn't respond to input)
- Fundamental wiring issues between entity definitions and game runtime

**Full Harness Output**:
- Polish and visual consistency
- Richer, more fully-featured editors
- Functional core gameplay
- Integrated [[Claude]] features for AI-assisted sprite and level generation
- Playable game with functional physics (though with some edge cases)

### QA Effectiveness

The evaluator catches meaningful gaps that generators miss:

| Contract Criterion | Evaluator Finding |
|---|---|
| Rectangle fill tool allows click-drag to fill rectangular area | **FAIL** — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered on mouseUp |
| User can select and delete placed entity spawn points | **FAIL** — Delete key handler requires both `selection` and `selectedEntityId` set, but clicking only sets `selectedEntityId` |
| User can reorder animation frames via API | **FAIL** — Route ordering causes FastAPI to match 'reorder' as frame_id integer, returning 422 error |

**Tuning Challenge**: Out-of-the-box, [[Claude]] is a poor QA agent. Early runs showed the model identifying issues then talking itself into accepting them anyway. Effective QA required multiple tuning iterations based on analyzing evaluator logs and identifying divergences from human judgment.

---

## Iterating on the Harness: Simplification with Model Improvements

### Core Principle

Every harness component encodes an assumption about what the model cannot do alone. As models improve, these assumptions become stale and should be stress-tested. The goal is "find the simplest solution possible, and only increase complexity when needed."

### Removing the Sprint Construct

With the release of [[Claude Opus 4.6]], which "plans more carefully, sustains agentic tasks for longer, can operate more reliably in larger codebases, and has better code review and debugging skills," the sprint decomposition became unnecessary.

**Changes**:
- Removed sprint-based decomposition
- Retained planner (prevents under-scoping) and evaluator (catches edge cases)
- Moved evaluator to single-pass at end rather than per-sprint grading
- Added prompting for proper agent construction within generated apps

**Result**: Opus 4.6 could run coherently for 2+ hours without sprint structure, though the evaluator