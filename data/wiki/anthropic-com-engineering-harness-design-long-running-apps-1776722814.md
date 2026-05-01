---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:46:28.360441
raw_file_updated: 2026-05-01T05:46:28.360441
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:46:28.360441
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to successfully complete complex, long-running tasks. This article describes innovative multi-agent approaches that combine generator and evaluator agents—inspired by [[Generative Adversarial Networks]] (GANs)—to improve both frontend design quality and full-stack software development. The work demonstrates how separating task execution from evaluation, combined with strategic decomposition and context management, can dramatically improve the coherence and quality of autonomous software engineering.

---

## Overview

Harness design has become critical to achieving high performance at the frontier of [[agentic coding]]. Traditional single-agent approaches to complex tasks often fail due to two persistent problems:

1. **Context degradation** — As context windows fill during long tasks, [[AI models]] lose coherence and may exhibit "context anxiety," prematurely wrapping up work
2. **Self-evaluation bias** — Agents asked to evaluate their own work tend to respond positively regardless of actual quality

This article presents solutions developed by Anthropic's Labs team, including architectural patterns that use multiple specialized agents and structured handoffs to address these limitations.

---

## The Problem with Naive Implementations

### Context Management Issues

Earlier harness work at Anthropic used an initializer agent to decompose product specs into task lists, with a coding agent implementing features one at a time. While this approach showed promise, limitations persisted for complex tasks.

**Context Resets vs. Compaction**

The key insight was distinguishing between two approaches to managing long contexts:

- **Compaction**: Summarizing earlier conversation parts in place, allowing the same agent to continue on shortened history
- **Context Resets**: Clearing the context window entirely and starting a fresh agent with structured handoff artifacts

[[Claude Sonnet 4.5]] exhibited "context anxiety" strongly enough that compaction alone proved insufficient. Context resets provided a clean slate but added [[orchestration]] complexity, token overhead, and latency. Later model improvements ([[Claude Opus 4.6]]) largely eliminated this behavior, enabling different harness designs.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently:

- Praise mediocre outputs confidently
- Struggle particularly on subjective tasks (like design) without binary verification criteria
- Exhibit poor judgment even on tasks with verifiable outcomes

Separating the agent doing work from the agent judging it proved to be a strong lever. While the evaluator remains an LLM inclined toward generosity, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

---

## Frontend Design: Making Subjective Quality Gradable

### The Approach

The first application of the generator-evaluator pattern targeted frontend design, where self-evaluation issues were most visible. The challenge: convert subjective aesthetic judgments into concrete, gradable criteria.

### Design Criteria

Four grading criteria were developed and shared with both generator and evaluator agents:

1. **Design Quality** — Does the design feel like a coherent whole? Do colors, typography, layout, and imagery combine to create a distinct mood and identity?

2. **Originality** — Is there evidence of custom decisions, or reliance on template layouts and library defaults? Penalizes telltale "AI slop" patterns like purple gradients over white cards.

3. **Craft** — Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios. Competence check rather than creativity check.

4. **Functionality** — Can users understand the interface, find primary actions, and complete tasks without guessing?

Design quality and originality were weighted more heavily, as [[Claude]] already scored well on craft and functionality by default. This pushed the model toward more aesthetic risk-taking.

### Implementation

The harness was built using the [[Claude Agent SDK]]:

- **Generator agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator agent**: Used [[Playwright MCP]] to interact with live pages, taking screenshots and studying implementations before scoring
- **Feedback loop**: Evaluator feedback flowed back to generator for iteration

Runs typically involved 5-15 iterations, with each cycle pushing the generator in more distinctive directions. Full runs extended up to four hours.

### Results and Observations

- Evaluator assessments improved over iterations before plateauing
- Some generations refined incrementally; others took sharp aesthetic turns
- Prompting language steered generators in unanticipated ways (e.g., "museum quality" designs converged toward specific visual styles)
- Even first iterations were noticeably better than baseline with no prompting
- Implementation complexity increased across rounds as generators reached for more ambitious solutions

**Notable Example**: A Dutch art museum website that, by iteration 10, abandoned its initial dark-themed landing page and reimagined the site as a 3D spatial experience with CSS perspective, free-form artwork positioning, and doorway-based navigation.

---

## Scaling to Full-Stack Coding

### Architecture

Building on earlier long-running harness work, a three-agent system was developed:

#### Planner Agent

- **Function**: Expands simple 1-4 sentence prompts into full product specifications
- **Constraints**: Stays focused on product context and high-level technical design rather than granular implementation details
- **Innovation**: Identifies opportunities to weave [[AI features]] into product specs
- **Rationale**: Avoids cascading errors from over-specified technical details

#### Generator Agent

- **Function**: Implements features in [[sprint]]-based iterations
- **Stack**: React, Vite, [[FastAPI]], SQLite (later PostgreSQL)
- **Process**: Self-evaluates work at end of each sprint before handoff to QA
- **Tools**: Git for version control
- **Scope**: Works one feature at a time for coherent scope management

#### Evaluator Agent

- **Function**: Catches bugs through user-like interaction testing
- **Tools**: [[Playwright MCP]] for clicking through running applications
- **Testing**: Exercises UI features, API endpoints, and database states
- **Grading**: Against both discovered bugs and adapted design criteria
- **Thresholds**: Hard thresholds on all criteria; failure triggers detailed feedback

### Sprint Contracts

Before each sprint, generator and evaluator negotiate a **sprint contract**:

- Bridges gap between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews to ensure generator builds the right thing
- Both iterate until agreement

Communication occurs via files, keeping work faithful to spec without over-specification.

### Initial Results: Retro Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness | Duration | Cost |
|---------|----------|------|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Quality Difference**: Immediately apparent. Solo run had broken core functionality (entities didn't respond to input). Full harness produced:

- Polished interface using full viewport
- Consistent visual identity
- Rich, fully-featured sprite editor
- Built-in [[Claude integration]] for AI-assisted game design
- Functional playable mode with working physics

**Limitations**: Workflow clarity issues, minor physics bugs, and some AI-generated level design limitations remained.

### Evaluator Performance

The evaluator required significant tuning to perform effectively. Out of the box, [[Claude]] proved to be a poor QA agent:

- Identified legitimate issues but rationalized them away
- Tested superficially rather than probing edge cases
- Showed leniency toward LLM-generated outputs

Through iterative prompt refinement, the evaluator improved substantially. Example findings from the game maker project:

| Criterion | Finding |
|-----------|---------|
| Rectangle fill tool | **FAIL** — Tool only places tiles at drag start/end points instead of filling region. `fillRectangle` function exists but isn't triggered properly on mouseUp. |
| Entity selection/deletion | **FAIL** — Delete handler requires both `selection` and `selectedEntityId` set, but clicking entity only sets `selectedEntityId`. |
| Animation frame reordering | **FAIL** — `PUT /frames/reorder` route defined after `/{frame_id}` routes. FastAPI matches "reorder" as integer, returns 422 error. |

---

## Iterating on the Harness: Simplification

As models improve, harness assumptions become worth stress-testing. Every component encodes an assumption about what the model cannot do alone.

### Principle: Complexity as Necessary Evil

The underlying principle: "Find the simplest solution possible, and only increase complexity when needed." This applies to harness maintenance as new models emerge.

### Removing the Sprint Construct

With [[Claude Opus 4.6