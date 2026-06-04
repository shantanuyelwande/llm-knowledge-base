---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-04T06:47:54.203982
raw_file_updated: 2026-06-04T06:47:54.203982
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-04T06:47:54.203982
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to work effectively on complex, long-running tasks. This article describes techniques developed at [[Anthropic]] for improving [[Claude]]'s performance on extended coding and design tasks, including a generator-evaluator pattern inspired by [[Generative Adversarial Networks]] (GANs). The work demonstrates how separating task execution from evaluation, decomposing complex work into manageable chunks, and using structured handoffs between agents can significantly improve output quality for both subjective tasks like [[frontend design]] and objective tasks like [[full-stack application development]].

---

## Overview

Harness design has emerged as a critical factor in achieving high-quality results from [[long-running agents]] working on complex problems. While basic [[prompt engineering]] can improve model performance, more sophisticated architectural approaches become necessary when tasks exceed what a single agent can reliably handle in one session.

This work, conducted by Prithvi Rajasekaran at [[Anthropic Labs]], addresses two interconnected challenges:

1. **Getting [[Claude]] to produce high-quality [[frontend design]]** with aesthetic sophistication beyond generic, template-based outputs
2. **Building complete [[full-stack applications]]** autonomously without human intervention across multi-hour sessions

The core insight is that separating the roles of generator (task executor) and evaluator (quality assessor) creates a feedback loop that drives better outcomes than self-evaluation alone, regardless of whether the task is subjective or objective.

---

## Core Problems with Naive Approaches

### Context Window Limitations

[[Long-running agents]] face two distinct challenges as context windows fill:

- **Context loss**: Models struggle to maintain coherence on extended tasks as conversation history grows, leading to inconsistent decisions and forgotten requirements
- **Context anxiety**: Some models (notably [[Claude Sonnet 4.5]]) exhibit a tendency to prematurely wrap up work as they approach perceived context limits

**Solutions compared:**
- **Compaction**: Summarizing earlier conversation parts in place allows the same agent to continue on shortened history, but preserves context anxiety
- **Context resets**: Clearing the context window entirely and starting fresh with a structured handoff provides a clean slate, eliminating context anxiety at the cost of orchestration complexity and token overhead

For [[Claude Sonnet 4.5]], context resets proved essential. With [[Claude Opus 4.5]] and later models, context anxiety diminished significantly, allowing continuous sessions with [[automatic compaction]].

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] exhibit systematic bias:

- **Confidence over accuracy**: Agents tend to praise mediocre outputs confidently, even when human observers recognize obvious quality issues
- **Subjective task blindness**: This problem is particularly acute for subjective domains like [[design]] where there are no binary correctness checks
- **Objective task underperformance**: Even on verifiable tasks, agents sometimes exhibit poor judgment that impedes their own performance

**Key finding**: Separating the evaluator from the generator proves to be a strong lever for addressing self-evaluation bias. While evaluators remain inclined toward leniency toward [[LLM]]-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—a phenomenon sometimes called "[[AI slop]]."

### The Solution: Generator-Evaluator Loop

The approach applies a [[Generative Adversarial Networks|GAN]]-inspired pattern to design:

1. **Generator agent**: Creates HTML/CSS/JavaScript frontends based on user prompts
2. **Evaluator agent**: Grades designs and provides detailed critique using [[Playwright MCP]] for live interaction
3. **Feedback loop**: Evaluator feedback drives iterative refinement (typically 5-15 iterations per generation)

### Design Criteria

Rather than trying to score abstract qualities like "beauty," the harness uses concrete, gradable criteria:

| Criterion | Definition | Emphasis |
|-----------|-----------|----------|
| **Design Quality** | Does the design feel like a coherent whole with colors, typography, layout, and imagery combining to create distinct mood and identity? | High |
| **Originality** | Evidence of custom decisions rather than template layouts and library defaults? Recognition of deliberate creative choices by humans? | High |
| **Craft** | Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios | Lower (Claude excels naturally) |
| **Functionality** | Usability independent of aesthetics; can users understand, find actions, and complete tasks? | Lower (Claude excels naturally) |

**Key insight**: The wording of criteria steers generator behavior in non-obvious ways. Phrases like "the best designs are museum quality" pushed designs toward particular visual convergence. Explicit penalties for "[[AI slop]]" patterns (purple gradients over white cards) drove models toward aesthetic risk-taking.

### Calibration and Results

- **Few-shot calibration**: The evaluator was calibrated using detailed score breakdowns to align judgment with specific aesthetic preferences
- **Iterative improvement**: Evaluator assessments improved over iterations before plateauing
- **Non-linear progress**: While later implementations tended to be better overall, individual preferred iterations sometimes appeared mid-sequence
- **Complexity growth**: Implementation sophistication increased across rounds as generators reached for more ambitious solutions

**Notable example**: A Dutch art museum website that, by iteration 10, completely reimagined itself as a 3D spatial experience with CSS perspective rendering, free-form artwork positioning, and doorway-based navigation—a creative leap not seen in single-pass generation.

---

## Full-Stack Application Development

### Architecture: Three-Agent System

Building on the [[generator-evaluator]] pattern, the full-stack harness introduced a three-agent architecture:

#### Planner Agent

**Purpose**: Automate specification creation from minimal input

**Responsibilities**:
- Expand 1-4 sentence user prompts into comprehensive product specifications
- Emphasize ambitious scope without over-specifying implementation details
- Focus on product context and high-level technical design
- Identify opportunities to weave [[AI features]] into product specs
- Create visual design language using the [[frontend design skill]]

**Rationale**: Detailed upfront specifications can cascade errors into downstream implementation. Better to constrain deliverables and let agents determine the path.

#### Generator Agent

**Purpose**: Implement features incrementally with self-evaluation

**Responsibilities**:
- Work in sprints (in v1) or continuously (in v2), picking up features from the spec
- Build using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Maintain [[Git]] version control
- Self-evaluate work at sprint end before handoff to QA
- Negotiate sprint contracts with evaluator before implementation

**Tech Stack**:
```
Frontend: React + Vite
Backend: FastAPI
Database: SQLite (later PostgreSQL)
Version Control: Git
```

#### Evaluator Agent

**Purpose**: Verify implementation against specifications and quality criteria

**Responsibilities**:
- Use [[Playwright MCP]] to interact with running applications like a user would
- Test UI features, API endpoints, and database states
- Grade against product depth, functionality, visual design, and code quality
- Identify and document specific bugs with code locations
- Negotiate sprint contracts before implementation begins

**Sprint Contracts**: Before each sprint, generator and evaluator agree on:
- What "done" looks like for that work chunk
- Specific testable success criteria
- Verification methods

This bridges the gap between high-level user stories and concrete, testable implementation.

### Communication Pattern

Agents communicate via files:
- One agent writes a file with its output
- Other agents read and respond in the same file or create new files
- This keeps work faithful to specifications without over-constraining implementation

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Metric | Solo Agent | Full Harness |
|--------|-----------|--------------|
| Duration | 20 min | 6 hours |
| Cost | $9 | $200 |
| Output Quality | Broken core gameplay | Fully functional game |

**Solo Agent Issues**:
- Layout wasted space with fixed-height panels
- Rigid workflow unclear to users
- Game completely broken: entities appeared but didn't respond to input
- Entity-runtime wiring disconnected with no UI indication

**Full Harness Output**:
- Polished interface with consistent visual identity
- Rich sprite editor with better tools and controls
- Built-in [[Claude integration]] for AI-assisted game generation
-