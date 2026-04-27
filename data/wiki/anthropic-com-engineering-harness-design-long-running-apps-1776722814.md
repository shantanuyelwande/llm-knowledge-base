---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-27T05:31:38.778310
raw_file_updated: 2026-04-27T05:31:38.778310
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-27T05:31:38.778310
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design represents a critical approach to improving [[AI agent]] performance on complex, long-duration tasks. This methodology combines multiple specialized agents in a coordinated architecture to overcome inherent limitations in model self-evaluation and task coherence. By separating concerns into planning, generation, and evaluation functions—inspired by [[Generative Adversarial Networks]] (GANs)—developers can achieve significantly higher quality outputs in both [[Frontend Design|frontend design]] and [[Full-Stack Development|full-stack software engineering]] tasks.

## Overview

**Source:** [Anthropic Engineering Blog](https://www.anthropic.com/engineering/harness-design-long-running-apps)  
**Author:** Prithvi Rajasekaran (Anthropic Labs)  
**Published:** March 24, 2026

Harness design addresses fundamental challenges in long-running [[agentic coding]] systems. Rather than relying on a single model to complete complex tasks autonomously, this approach uses multiple specialized agents working in concert, with structured handoffs and evaluation mechanisms to maintain quality and coherence across extended sessions.

## Core Problems and Solutions

### The Self-Evaluation Problem

One of the most persistent issues in autonomous systems is that [[Language Models|models]] tend to evaluate their own work leniently. When asked to assess outputs they've generated, models typically provide positive feedback even when quality is objectively mediocre—a problem particularly pronounced in subjective domains like [[design]].

The key insight is that **separating the generation agent from the evaluation agent creates a stronger feedback mechanism**. While both are still [[Language Models|LLMs]] inclined toward generosity, a standalone evaluator can be tuned to be appropriately skeptical, providing concrete feedback the generator can iterate against.

### Context Window Limitations

Long-running tasks expose two distinct failure modes:

1. **Context Anxiety**: Models like [[Claude Sonnet 4.5]] exhibit premature task completion as they approach their perceived context limit, wrapping up work before it's truly finished.

2. **Coherence Loss**: Extended tasks cause models to lose coherence as the [[context window]] fills with conversation history.

While **context compaction** (summarizing earlier conversation in-place) preserves continuity, it doesn't provide the clean slate needed to eliminate context anxiety. **Context resets**—completely clearing the context window and using structured handoffs to carry state forward—proved more effective, though at the cost of increased orchestration complexity and token overhead.

With newer models like [[Claude Opus 4.6]], context anxiety became less pronounced, allowing simpler harness designs without explicit resets.

## Frontend Design Application

### Methodology

The first application of the generator-evaluator pattern targeted [[Frontend Design|frontend design]], where subjective quality assessment was most challenging. The approach converted abstract aesthetic judgments into concrete, gradable criteria:

#### Four Design Criteria

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, imagery, and details into a distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. The design should show deliberate creative choices, avoiding telltale "AI slop" patterns.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The harness weighted design quality and originality more heavily, as Claude naturally scored well on craft and functionality by default.

### Implementation

Using the [[Claude Agent SDK]], the system operated as follows:

- **Generator Agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator Agent**: Used [[Playwright]] [[Model Context Protocol|MCP]] to interact with live pages, taking screenshots and studying implementations before scoring and providing detailed critique
- **Feedback Loop**: 5-15 iterations per generation, with the generator making strategic decisions to either refine the current direction or pivot to entirely different aesthetics

Full runs extended to four hours, with evaluator assessments improving through iterations before plateauing. The wording of evaluation criteria itself influenced generator outputs in unexpected ways—phrases like "the best designs are museum quality" steered designs toward particular visual convergence.

### Results

In one notable example, a Dutch art museum website evolved through nine iterations of refinement before the tenth iteration abandoned the approach entirely, reimagining the site as a 3D spatial experience with CSS perspective, free-form artwork positioning, and doorway-based navigation—a creative leap not typically seen in single-pass generation.

## Full-Stack Coding Architecture

### Three-Agent System

Building on lessons from [[Frontend Design|frontend design]], the harness for full-stack development employed three specialized agents:

#### Planner Agent

**Purpose**: Automate specification creation from minimal user input

- Takes 1-4 sentence prompts and expands them into full product specifications
- Emphasizes ambitious scope and high-level technical design over granular implementation details
- Avoids cascading errors from over-specified technical details
- Identifies opportunities to weave [[AI agent|AI features]] into product specs
- Access to [[Frontend Design|frontend design]] skills for visual language definition

**Rationale**: Prevents the generator from under-scoping work when given raw prompts, ensuring more feature-rich applications.

#### Generator Agent

**Purpose**: Implement features according to specifications and contracts

- Works in sprints (in earlier versions) or continuously (in later versions with improved models)
- Implements applications using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]]
- Self-evaluates work at sprint completion before handing off to evaluation
- Uses [[Git]] for version control
- Responds to evaluator feedback with specific, actionable bug fixes

#### Evaluator Agent

**Purpose**: Verify functionality and quality through active testing

- Uses [[Playwright]] [[Model Context Protocol|MCP]] to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades against both discovered bugs and criteria covering product depth, functionality, visual design, and code quality
- Establishes sprint contracts before implementation begins, negotiating what "done" looks like
- Produces specific, actionable feedback rather than vague criticism

### Sprint Contracts

A critical innovation was the **sprint contract**—an agreement between generator and evaluator before coding begins. This bridges the gap between high-level user stories and testable implementation:

- Generator proposes what will be built and how success will be verified
- Evaluator reviews the proposal to ensure the generator builds the right thing
- Both iterate until agreement is reached
- Generator implements against the agreed-upon contract
- Evaluator verifies completion using specific, pre-agreed criteria

This approach maintained fidelity to specifications without over-specifying implementation details prematurely.

### Communication Pattern

Agents communicated via files rather than direct message passing:
- One agent writes a file with proposed work or findings
- Another agent reads and responds in the same file or creates a new file
- This pattern maintained clear context and created auditable handoffs

## Case Study: Retro Game Maker

### Comparison: Solo vs. Harness Approach

**Task**: Create a 2D retro game maker with level editor, sprite editor, entity behaviors, and playable test mode

| Metric | Solo Agent | Full Harness |
|--------|-----------|--------------|
| Duration | 20 minutes | 6 hours |
| Cost | $9 | $200 |
| Features | Basic | 16 features across 10 sprints |
| Functionality | Core game broken (entities non-responsive) | Fully playable game |
| Polish | Layouts wasted space, workflow unclear | Consistent visual identity, polished interface |

### Solo Agent Output Issues

- Fixed-height panels wasted viewport space
- Rigid workflow with no UI guidance toward necessary steps
- Core game functionality broken: entities appeared but didn't respond to input
- Broken wiring between entity definitions and game runtime with no surface indication of problems

### Harness Output Advantages

- Full viewport utilization and sensible panel sizing
- Consistent visual design language from specification
- Rich, fully-featured sprite editor with cleaner tool palettes and better controls
- Built-in Claude integration for AI-assisted game generation
- Functional game mechanics with working physics
- 16-feature specification including sprite animation, behavior templates, sound effects, music, AI-assisted design, and shareable game export

## Case Study: Digital Audio Workstation (DAW)

### Updated Harness (Version 2)

With [[Claude Opus 4.6]] providing improved capabilities, the harness was simplified:

- **Removed**: Sprint decomposition structure (model now handles longer coherent sessions)
- **Kept**: Planner and evaluator agents (continued to add obvious value)
- **Added**: Better prompting for proper [[AI agent]] construction within generated applications
- **Modified**: Evaluator moved to single