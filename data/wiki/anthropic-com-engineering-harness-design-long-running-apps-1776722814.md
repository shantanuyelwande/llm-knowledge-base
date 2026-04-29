---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-29T05:31:35.320204
raw_file_updated: 2026-04-29T05:31:35.320204
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-29T05:31:35.320204
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to effectively complete complex, long-running tasks. This article describes techniques developed at [[Anthropic]] for building multi-agent systems that combine generative and evaluative components—inspired by [[Generative Adversarial Networks]]—to produce high-quality [[frontend design|frontend designs]] and full-stack [[software engineering|software applications]] through autonomous coding sessions lasting multiple hours.

---

## Overview

Harness design has emerged as a critical discipline in [[agentic AI]] development, particularly for tasks that exceed what single-pass model invocations can reliably accomplish. Rather than relying solely on model capability, effective harnesses decompose complex problems into specialized agent roles, implement feedback loops, and use structured handoffs to maintain coherence across long execution sequences.

The work described here addresses two persistent challenges in long-running autonomous coding:

1. **Loss of coherence** as context windows fill during extended tasks
2. **Self-evaluation bias**, where agents fail to critically assess their own work

---

## Core Problems with Naive Implementations

### Context Window Management

Long-running tasks present a fundamental challenge: as conversation history grows, models may experience performance degradation. Two approaches exist to address this:

**Context Compaction**
- Earlier conversation segments are summarized in-place
- Preserves continuity within the same agent session
- Does not resolve "context anxiety"—the tendency for models to prematurely conclude work as they approach perceived context limits

**Context Resets**
- The context window is cleared entirely and a fresh agent session begins
- Requires structured artifacts to carry state and next steps between sessions
- Provides a clean slate that eliminates context anxiety
- Introduces orchestration complexity, token overhead, and latency

Research showed that [[Claude Sonnet 4.5]] exhibited context anxiety strongly enough that compaction alone was insufficient. Context resets became essential for maintaining coherent multi-hour coding sessions, though newer models like [[Claude Opus 4.6]] largely eliminated this behavior natively.

### Self-Evaluation Bias

When asked to evaluate their own work, [[language models]] tend to respond with unwarranted confidence and praise, even when output quality is mediocre. This problem is particularly acute for subjective tasks like [[design]], where no binary verification exists. However, it also affects objective tasks by impairing the agent's judgment during execution.

**Solution: Separating Generator and Evaluator**

Decoupling the agent producing work from the agent assessing it creates a powerful lever. While evaluators remain inclined toward leniency with [[LLM]]-generated outputs, tuning a standalone evaluator to be appropriately skeptical is far more tractable than making a generator self-critical. Once external feedback exists, the generator has concrete targets to iterate against.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] gravitates toward safe, predictable layouts that are technically functional but visually unremarkable. Aesthetics cannot be fully reduced to scores, yet design quality can be improved through grading criteria that encode design principles.

### Grading Criteria Framework

Four criteria were developed to guide both generator and evaluator agents:

**Design Quality**
- Does the design feel like a coherent whole rather than disconnected parts?
- Colors, typography, layout, imagery, and details combine to create distinct mood and identity
- Emphasis: High weight in evaluation

**Originality**
- Evidence of custom decisions versus template layouts and defaults
- Human designers should recognize deliberate creative choices
- Penalizes unmodified stock components and telltale "AI patterns" (e.g., purple gradients over white cards)
- Emphasis: High weight in evaluation

**Craft**
- Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios
- Competence check rather than creativity check
- Most implementations score well by default
- Emphasis: Lower weight in evaluation

**Functionality**
- Usability independent of aesthetics
- Can users understand the interface, find primary actions, complete tasks?
- Emphasis: Lower weight in evaluation

The emphasis on design quality and originality over craft and functionality pushed the model toward aesthetic risk-taking, as [[Claude]] already excelled at the latter two dimensions.

### Implementation

**Architecture**
- Generator agent creates HTML/CSS/JS frontend from user prompt
- Evaluator receives [[Playwright]] MCP to interact with live page directly
- Evaluator navigates, screenshots, and studies implementation before scoring
- Feedback flows back to generator for iteration

**Calibration**
- Evaluator tuned using few-shot examples with detailed score breakdowns
- Ensures alignment with designer preferences
- Reduces score drift across iterations

**Results**
- 5-15 iterations per generation, each typically pushing output in more distinctive direction
- Full runs stretched up to 4 hours
- Scores generally improved over iterations before plateauing
- Pattern was not always cleanly linear; middle iterations sometimes superior to final ones
- Implementation complexity tended to increase across rounds
- Even first iteration notably better than baseline with no prompting

### Notable Example: Museum Website

When prompted to create a website for a Dutch art museum, the model produced a clean, dark-themed landing page by iteration nine. On the tenth cycle, it scrapped the approach entirely and reimagined the site as a spatial experience: a 3D room with checkered floor rendered in CSS perspective, artwork hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This represented the kind of creative leap not typically seen from single-pass generation.

---

## Scaling to Full-Stack Coding

The GAN-inspired generator-evaluator pattern maps naturally onto the [[software development]] lifecycle, where [[code review]] and [[quality assurance|QA]] serve equivalent structural roles.

### Three-Agent Architecture

**Planner Agent**
- Takes simple 1-4 sentence user prompt
- Expands into full product specification
- Ambitious about scope; focused on product context and high-level technical design rather than granular implementation details
- Avoids over-specifying implementation details that could cascade errors downstream
- Weaves AI features into product specifications

**Generator Agent**
- Works in sprints (original harness) or continuously (refined harness)
- Implements features one at a time from specification
- Tech stack: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- Self-evaluates work at end of each sprint
- Uses [[git]] for version control
- Negotiates sprint contracts with evaluator before implementation

**Evaluator Agent**
- Uses [[Playwright]] MCP to test running application like a user would
- Clicks through features, tests [[API]] endpoints, verifies database states
- Grades sprints against both discovered bugs and predefined criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard threshold; failure requires detailed feedback
- Negotiates sprint contracts defining "done" before coding begins

### Sprint Contracts

The gap between high-level user stories and testable implementation is bridged through sprint contracts:

- Generator proposes what will be built and how success will be verified
- Evaluator reviews proposal to ensure generator builds the right thing
- Agents iterate until agreement reached
- Communication via files: agents write files other agents read and respond to
- Keeps work faithful to spec without over-specifying implementation

### Initial Results: Retro Video Game Maker

**Prompt:** "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness | Duration | Cost |
|---------|----------|------|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Run Issues:**
- Layout wasted space with fixed-height panels
- Workflow was rigid and unintuitive
- Core game mechanic broken: entities appeared but didn't respond to input
- Entity-to-runtime wiring was broken with no surface indication of problem

**Full Harness Results:**
- Immediate polish and smoothness
- Canvas used full viewport with sensible panel sizing
- Consistent visual identity tracking design specification
- Richer sprite editor with cleaner tool palettes, better color picker, usable zoom
- Built-in Claude integration for generating game components
- Functional game that could actually be played
- Physics had rough edges but core mechanics worked

**Evaluator Performance**

Out of the box, [[Claude]] is a poor [[quality assurance|QA]] agent. Initial runs showed:
- Identification of legitimate issues followed by rationalization that they weren't important
- Superficial testing rather than edge case exploration
- Subtle bugs slipping through

Tuning required:
- Reading evaluator logs and finding judgment divergences
- Updating QA prompt to address identified issues
- Several iteration cycles before reasonable grading achieved

Even with tuning, limits remained