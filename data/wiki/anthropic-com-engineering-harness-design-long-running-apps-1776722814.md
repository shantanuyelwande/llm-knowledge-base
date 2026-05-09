---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-09T05:26:20.810457
raw_file_updated: 2026-05-09T05:26:20.810457
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-09T05:26:20.810457
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to reliably complete complex, long-running tasks. This article explores how [[Anthropic]] researchers developed multi-agent systems combining generator and evaluator agents to improve performance on both subjective tasks (like [[frontend design]]) and objective tasks (like [[full-stack application development]]). The work demonstrates that separating evaluation from generation, decomposing complex tasks, and using structured handoffs between [[context windows]] significantly improves output quality for autonomous software engineering.

---

## Overview

Harness design has emerged as a critical area in [[AI engineering]] for developing reliable systems that can handle extended, complex tasks. Traditional single-agent approaches often struggle with maintaining coherence over long execution periods and accurately self-evaluating their own work. This article documents research by Prithvi Rajasekaran at [[Anthropic Labs]] on creating multi-agent architectures inspired by [[Generative Adversarial Networks]] (GANs) to overcome these limitations.

The research demonstrates applications across two distinct domains:
- **Frontend design**: Creating visually distinctive, high-quality user interfaces
- **Full-stack development**: Building complete, functional web applications over multi-hour autonomous sessions

---

## Key Problems in Naive Implementations

### Context Window Degradation

Long-running tasks expose two critical limitations in [[language models]]:

1. **Context coherence loss**: As the [[context window]] fills during extended tasks, models tend to lose coherence and make inconsistent decisions.

2. **Context anxiety**: Some models (notably [[Claude Sonnet 4.5]]) exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when significant work remains.

**Solutions attempted:**
- **Context compaction**: Summarizing earlier conversation portions in-place to preserve continuity
- **Context resets**: Clearing the context window entirely and starting fresh with structured handoffs to carry previous state

Context resets proved more effective than compaction alone, though they add orchestration complexity, token overhead, and latency.

### Self-Evaluation Bias

A persistent problem across both subjective and objective tasks: when asked to evaluate their own work, [[AI agents]] tend to respond with confident praise even when quality is mediocre. This self-evaluation bias is particularly pronounced for:

- **Subjective tasks** (design): No binary verification method exists; aesthetic judgments are inherently evaluative
- **Objective tasks** (coding): Even with verifiable outcomes, agents sometimes exhibit poor judgment that impedes performance

**Key insight**: Separating the agent that generates work from the agent that evaluates it creates a stronger feedback mechanism than attempting to make generators self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—what practitioners term "AI slop."

### Solution: Grading Criteria Framework

To make subjective aesthetic judgment gradable, the research developed four explicit criteria:

1. **Design quality**: Does the design feel like a coherent whole with unified mood and identity? Do colors, typography, layout, and imagery combine effectively?

2. **Originality**: Is there evidence of custom decisions, or just template layouts and library defaults? Can a human designer recognize deliberate creative choices?

3. **Craft**: Technical execution—typography hierarchy, spacing consistency, color harmony, contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand what the interface does and complete tasks?

The research emphasized **design quality and originality** over craft and functionality, since [[Claude]] already performed well on the latter by default.

### Architecture: Generator-Evaluator Loop

The harness used two specialized agents:

- **Generator agent**: Created HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator agent**: Used [[Playwright]] to interact with live pages, taking screenshots and carefully studying implementations before producing detailed critiques

The evaluator graded each criterion and wrote specific feedback. The generator then iterated, either refining the current direction or pivoting to entirely different aesthetics. Typical runs involved 5-15 iterations, with full cycles taking up to four hours.

### Key Finding: Prompt Wording Shapes Output

The specific language in criteria descriptions significantly influenced generator behavior. Phrases like "the best designs are museum quality" pushed designs toward particular visual convergence, suggesting that prompting directly shaped output character before any evaluator feedback occurred.

### Example: Dutch Art Museum Website

In one notable case:
- **Iterations 1-9**: Clean, dark-themed landing page for a fictional museum—visually polished but conventional
- **Iteration 10**: Complete aesthetic pivot to a spatial experience—a 3D room with checkered floor rendered in CSS perspective, artwork hung freely on walls, doorway-based navigation between gallery rooms

This creative leap demonstrated the potential of the generator-evaluator loop to drive innovation beyond baseline expectations.

---

## Full-Stack Coding: Scaling to Complete Applications

### Architecture: Three-Agent System

Building on [[earlier harness work]], the research developed a three-agent architecture:

#### 1. Planner Agent

**Purpose**: Automate the specification phase

**Approach**:
- Takes simple 1-4 sentence prompts and expands them into full product specifications
- Instructed to be ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation details
- Identifies opportunities to weave AI features into product specs

**Rationale**: Avoiding detailed technical specification upfront prevents errors from cascading into implementation. Leaves implementation details to downstream agents.

#### 2. Generator Agent

**Purpose**: Implement features in a structured, manageable way

**Approach** (Opus 4.5 version):
- Works in **sprints**, implementing one feature at a time from the specification
- Uses React, Vite, [[FastAPI]], and SQLite (later [[PostgreSQL]]) stack
- Self-evaluates work at end of each sprint before handoff to QA
- Uses [[Git]] for version control

**Approach** (Opus 4.6 version):
- Sprint construct removed due to improved model capabilities
- Single continuous build session
- Improved AI feature integration using proper agent tooling

#### 3. Evaluator Agent

**Purpose**: Catch bugs and verify specification compliance

**Approach**:
- Uses [[Playwright]] to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against criteria adapted from frontend design work:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard thresholds; failure in any criterion fails the sprint

**Sprint Contracts**: Before implementation, generator and evaluator negotiate a "sprint contract" that:
- Defines what "done" looks like for that work chunk
- Bridges the gap between high-level user stories and testable implementation
- Generator proposes what it will build and how success will be verified
- Evaluator reviews proposal to ensure generator is building the right thing
- Both iterate until agreement is reached

### Communication Pattern

Agents communicate via files:
- One agent writes a file
- Another agent reads it and responds within that file or creates a new file
- Previous agent reads response and continues

This approach keeps work faithful to specifications without over-specifying implementation.

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Results Comparison**:

| Harness | Duration | Cost |
|---------|----------|------|
| Solo agent | 20 min | $9 |
| Full harness (Opus 4.5) | 6 hr | $200 |

**Solo output issues**:
- Layout wasted space with fixed-height panels
- Rigid workflow without UI guidance
- Central feature broken: entities didn't respond to input
- Code wiring between entity definitions and game runtime was broken

**Full harness output**:
- 16-feature spec across 10 sprints
- Included sprite animation system, behavior templates, sound effects, AI-assisted sprite generator, game export
- Consistent visual identity throughout
- Sprite editor was richer with cleaner tool palettes and better controls
- Built-in Claude integration for generating game components
- Core gameplay actually functional with entity movement and interaction

**Evaluator findings example**:

| Criterion | Finding |
|-----------|---------|
| Rectangle fill tool | **FAIL** — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered properly on mouseUp |
| Delete entity spawn points | **FAIL** — Delete key handler requires both `selection` and `selectedEntityId` to be set, but clicking entity only sets `selectedEntityId` |
| Reorder animation