---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-21T04:52:37.585993
raw_file_updated: 2026-04-21T04:52:37.585993
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-21T04:52:37.585993
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to reliably complete complex, long-running tasks. This article describes techniques developed at Anthropic for improving [[Claude]] performance on extended coding and design tasks, particularly through multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs). The key innovation is separating task execution from evaluation, allowing specialized agents to generate outputs while dedicated evaluator agents provide reliable feedback and quality control.

---

## Overview

Harness design has emerged as a critical discipline in [[agentic AI]] engineering. As [[large language models]] like Claude attempt increasingly complex tasks, the orchestration and decomposition of work becomes as important as the model's raw capabilities. This article documents research on building harnesses that enable Claude to produce high-quality [[frontend design]] and complete full-stack applications over multi-hour autonomous sessions.

The work addresses two fundamental challenges:
1. **Context degradation** - Models lose coherence as context windows fill during long tasks
2. **Self-evaluation bias** - Models tend to praise their own work rather than critically assess it

## Core Problems in Long-Running Tasks

### Context Anxiety and Window Management

Models like [[Claude Sonnet 4.5]] exhibit "context anxiety," a tendency to prematurely wrap up work as they approach perceived context limits. Two approaches exist to address this:

- **Compaction**: Summarizing earlier conversation history in place, allowing the same agent to continue on shortened context
- **Context resets**: Clearing the context window entirely and starting fresh with a structured handoff artifact

While compaction preserves continuity, context resets provide a clean slate that better prevents context anxiety. Testing showed that context resets were essential for Sonnet 4.5 performance, though newer models like [[Claude Opus 4.5]] reduced this behavior significantly.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently provide inflated assessments, especially on subjective tasks. This problem persists even for tasks with verifiable outcomes. The solution is architectural: **separating the agent doing the work from the agent judging it**.

The separation alone doesn't eliminate leniency, but tuning a standalone evaluator to be skeptical proves far more tractable than making a generator critical of its own work.

## Frontend Design: The GAN-Inspired Approach

### Motivation

Frontend design presents a unique challenge: the task is inherently subjective, yet quality can be meaningfully improved through structured criteria. Absent intervention, Claude gravitates toward safe, technically functional but visually unremarkable layouts.

### Design Criteria Framework

To make subjective aesthetic judgment gradable, four explicit criteria were developed:

1. **Design Quality**: Does the design feel coherent rather than fragmented? Strong work combines colors, typography, layout, and imagery into a distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Penalizes generic "AI slop" patterns and unmodified stock components.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity assessment.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The framework explicitly weighted design and originality more heavily, as Claude already excelled at craft and functionality by default.

### Implementation Architecture

The system used a **generator-evaluator loop**:

- **Generator Agent**: Creates HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator Agent**: Uses [[Playwright MCP]] to interact with live pages, screenshotting and studying implementations before scoring each criterion
- **Feedback Loop**: Evaluator feedback flows back to generator for iterative refinement

Typical runs involved 5-15 iterations per generation, with each cycle pushing the generator in more distinctive directions. Full runs stretched up to four hours.

### Key Findings

- The wording of criteria steered generators in unanticipated ways; phrases like "museum quality" pushed designs toward specific visual convergence
- Scores generally improved over iterations before plateauing, though not always linearly
- Later implementations tended to be better overall, but humans sometimes preferred middle iterations
- Implementation complexity increased across rounds as generators attempted more ambitious solutions
- Even first-iteration outputs were noticeably better than baseline with no prompting, suggesting criteria themselves guided models away from generic defaults

### Notable Example

For a Dutch art museum website, the generator produced a clean, dark-themed landing page by iteration nine. On the tenth cycle, it scrapped the approach entirely, reimagining the site as a 3D spatial experience with a checkered floor rendered in CSS perspective, artwork on walls in free-form positions, and doorway-based navigation between gallery rooms—a creative leap not seen in single-pass generation.

## Full-Stack Application Development

### Three-Agent Architecture

Building on frontend design successes, a three-agent system was developed for complete application development:

#### Planner Agent

- Takes simple 1-4 sentence prompts and expands them into full product specifications
- Deliberately ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation
- Weaves [[AI features]] into product specs
- Avoids over-specification that could cascade errors downstream

#### Generator Agent

- Implements features one at a time using sprint-based decomposition (in initial version)
- Technology stack: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- Self-evaluates work at sprint end before handing off to QA
- Uses [[Git]] for version control
- In updated versions, runs coherently without sprint decomposition

#### Evaluator Agent

- Uses [[Playwright MCP]] to interact with running applications like end users
- Tests UI features, API endpoints, and database states
- Grades against criteria covering product depth, functionality, visual design, and code quality
- Each criterion has hard thresholds; failures trigger detailed feedback

### Sprint Contracts

Before implementation, generator and evaluator negotiate a "sprint contract" defining:
- What "done" looks like for the chunk of work
- How success will be verified
- Specific testable behaviors

This bridges the gap between high-level user stories and testable implementation without over-specification.

### Communication Pattern

Agents communicate via files rather than direct conversation:
- One agent writes a file
- Another agent reads and responds in that file or creates new files
- Previous agent reads response and iterates

This keeps work faithful to specifications while allowing flexibility in implementation.

## Case Study: Retro Game Maker

### Comparison: Solo vs. Harness

**Solo Agent Run** (20 minutes, $9):
- Technically functional but spatially inefficient
- Rigid workflow requiring users to create sprites/entities before populating levels
- Core feature broken: entities appeared but didn't respond to input
- Wiring between entity definitions and game runtime was broken

**Full Harness Run** (6 hours, $200):
- Planner expanded one-sentence prompt into 16-feature spec across ten sprints
- Included sprite animation, behavior templates, sound effects, music, AI-assisted sprite generation, and shareable export
- Polish and consistency throughout
- Sprite editor richer and more fully featured
- Built-in Claude integration for game generation
- Playable game that actually worked (though with some physics edge cases)
- 20x more expensive but vastly superior quality

## Evolving the Harness: Simplification for Opus 4.6

### Motivation for Simplification

As models improve, scaffolding that was essential for earlier versions becomes unnecessary overhead. [[Claude Opus 4.6]] offered:
- Better planning capabilities
- Sustained agentic task performance
- Improved reliability in large codebases
- Better code review and debugging
- Improved long-context retrieval

### Methodical Decomposition

Rather than radical simplification, the approach was systematic: remove one component at a time and measure impact. This clarified which pieces were load-bearing.

### Key Changes

1. **Removed Sprint Construct**: Opus 4.6 handled decomposition natively; sprints became unnecessary overhead
2. **Moved Evaluator to Single Pass**: Instead of per-sprint grading, evaluation occurs at end of full build
3. **Improved AI Feature Integration**: Added prompting to help generators build proper agents with tools
4. **Context Resets Eliminated**: Opus 4.6's improvements made context anxiety largely irrelevant

### Evaluator Trade-offs

The evaluator's necessity depends on task complexity relative to model capabilities:
- **Within model capability**: Evaluator becomes unnecessary overhead
- **At edge of capability**: Evaluator provides meaningful lift
- **Beyond model capability**: Evaluator is essential

This is not a fixed yes/no decision but a function of current model performance.

## Case Study: Digital Audio Workstation

### Prompt

> Build a fully featured DAW in the browser using the Web Audio