---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-02T06:47:21.634619
raw_file_updated: 2026-06-02T06:47:21.634619
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-02T06:47:21.634619
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and agent orchestration strategies used to enable [[AI agents]] to successfully complete complex, long-running tasks like full-stack application development. This article describes research from [[Anthropic]] demonstrating how multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs) can improve both subjective outputs (like [[frontend design]]) and objective outcomes (like [[software development]]) by separating generation from evaluation functions.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Problem: Limitations of Naive Implementations](#core-problem)
3. [Frontend Design Harness](#frontend-design-harness)
4. [Full-Stack Coding Architecture](#full-stack-coding-architecture)
5. [Iterating and Simplifying](#iterating-and-simplifying)
6. [Key Lessons](#key-lessons)
7. [Related Concepts](#related-concepts)

---

## Overview

Long-running [[autonomous agent]] tasks—particularly those spanning multiple hours and thousands of tokens—present unique challenges for [[large language models]] (LLMs). While [[prompt engineering]] and basic harness design can improve performance, more complex applications require sophisticated multi-agent architectures that decompose work, provide structured feedback, and maintain coherence across extended sessions.

This work, conducted by Prithvi Rajasekaran at [[Anthropic]], demonstrates that applying [[GAN]]-inspired patterns—where a generator agent creates outputs and a separate evaluator agent provides critical feedback—substantially improves the quality of both subjective creative work and objective technical implementations.

---

## Core Problem: Limitations of Naive Implementations

### Context Window and Coherence Issues

As [[context window]] length increases during long-running tasks, models experience two primary failure modes:

**Context Anxiety**: Models like [[Claude Sonnet 4.5]] exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when substantial work remains. This is distinct from actual context window exhaustion.

**Context Decay**: Models lose coherence and consistency as earlier parts of conversations are pushed out of active context, leading to contradictory decisions, repeated work, or architectural drift.

#### Solutions: Context Resets vs. Compaction

- **Compaction**: Summarizing earlier conversation history in-place to free up context space. Preserves continuity but doesn't eliminate context anxiety.
- **Context Resets**: Clearing the context window entirely and starting fresh with a structured handoff artifact containing the previous agent's state and next steps. Provides a clean slate but adds orchestration complexity and latency.

[[Claude Opus 4.5]] required context resets for optimal performance on long tasks, while [[Claude Opus 4.6]] largely eliminated context anxiety natively, reducing the need for this overhead.

### Self-Evaluation Bias

When asked to evaluate their own work, agents consistently exhibit **self-evaluation bias**—they praise outputs even when quality is objectively mediocre. This problem is particularly acute for:

- **Subjective tasks** (like [[frontend design]]) where there is no binary correctness check
- **Complex technical work** where agents fail to recognize subtle bugs or architectural issues

**Solution**: Separating the agent performing work (generator) from the agent evaluating it (evaluator) proves to be a strong lever. While evaluators remain somewhat lenient toward LLM outputs, they can be tuned to skepticism far more effectively than making a generator self-critical.

---

## Frontend Design Harness

### The Challenge

Without intervention, [[Claude]] typically produces technically functional but visually unremarkable frontend designs—safe, predictable layouts that lack distinctive character or originality.

### Approach: Operationalizing Aesthetics

The key insight is that while aesthetics cannot be fully reduced to a score, they can be improved through concrete grading criteria that encode design principles. The harness uses four grading criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Colors, typography, layout, imagery, and details combine to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Penalizes "AI slop" patterns like purple gradients over white cards.

3. **Craft**: Technical execution—typography hierarchy, spacing consistency, color harmony, contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface and complete tasks?

The harness weighted design quality and originality more heavily, pushing the model away from bland defaults toward more distinctive aesthetic choices.

### Architecture

- **Generator Agent**: Creates HTML/CSS/JavaScript frontend based on user prompt
- **Evaluator Agent**: Uses [[Playwright]] [[MCP]] to interact with the live page, screenshot and study implementation, then score each criterion with detailed critique
- **Feedback Loop**: Evaluator feedback flows back to generator for next iteration; 5-15 iterations per generation

### Calibration

The evaluator was calibrated using **few-shot examples** with detailed score breakdowns, ensuring judgment aligned with designer preferences and reducing score drift across iterations.

### Results

- Iterations improved before plateauing, with remaining headroom
- Wording of criteria steered generator in unanticipated ways (e.g., "museum quality" pushed toward particular visual convergence)
- Even first iteration showed improvement over baseline, suggesting criteria language itself steers models away from generic defaults
- Notable example: Dutch art museum website evolved from conventional dark-themed landing page to creative 3D spatial experience with CSS perspective rendering

---

## Full-Stack Coding Architecture

### Building on Prior Work

Earlier [[Anthropic]] research on [[long-running coding agents]] demonstrated that decomposing work into tractable chunks and using structured artifacts for context handoff improved performance. This work extended that foundation to a three-agent system.

### Three-Agent System

#### 1. Planner Agent

**Purpose**: Automate the specification phase, expanding brief user prompts into comprehensive product specs.

**Characteristics**:
- Takes 1-4 sentence prompts and expands to full product specification
- Ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation details
- Instructed to weave [[AI features]] into product specs
- Access to [[frontend design skill]] to create visual design language

**Rationale**: Constraining deliverables in spec rather than implementation details allows downstream agents to solve problems flexibly.

#### 2. Generator Agent

**Purpose**: Implement features incrementally using agreed-upon contracts.

**Characteristics**:
- Works in **sprints**, picking one feature at a time from spec
- Stack: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- Access to [[Git]] for version control
- Self-evaluates work at end of each sprint before QA handoff
- **Sprint Contract Negotiation**: Before each sprint, generator and evaluator agree on what "done" looks like, including testable success criteria

**Rationale**: High-level specs need bridging to testable implementation; negotiated contracts prevent misalignment.

#### 3. Evaluator Agent (QA)

**Purpose**: Verify implementation against requirements and catch bugs before handoff.

**Characteristics**:
- Uses [[Playwright]] [[MCP]] to click through running application as a user would
- Tests UI features, API endpoints, and database states
- Grades against both discovered bugs and criteria adapted from frontend experiment:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard threshold; any failure causes sprint to fail with detailed feedback
- Detailed issue reporting with specific code locations and fixes

**Tuning Challenge**: Out-of-box, Claude is a poor QA agent. Early runs showed:
- Identifying legitimate issues then talking itself into approving anyway
- Superficial testing missing edge cases and subtle bugs
- Required multiple rounds of prompt iteration to achieve reasonable judgment

### Communication Protocol

Agents communicate via **files**: one agent writes a file, another reads and responds either within that file or with new file. This keeps work faithful to spec without over-specification.

### Initial Results (Opus 4.5)

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness Type | Duration | Cost |
|---|---|---|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Run Issues**:
- Layout wasted space with fixed-height panels
- Rigid workflow without UI guidance
- Core game broken: entities appeared but didn't respond to input
- Entity-runtime wiring fundamentally broken

**Full Harness Advantages**:
- Polish and smoothness immediately apparent
- Canvas used full viewport, sensible panel sizing
- Consistent visual identity tracking design spec