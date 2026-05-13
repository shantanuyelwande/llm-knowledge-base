---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-13T05:53:55.321867
raw_file_updated: 2026-05-13T05:53:55.321867
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-13T05:53:55.321867
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design represents a structured approach to improving [[AI agent]] performance on complex, long-running tasks through specialized multi-agent architectures. Drawing inspiration from [[Generative Adversarial Networks]] (GANs), this methodology separates task execution from evaluation, enabling more effective feedback loops and higher-quality outputs. The approach has demonstrated significant improvements in both [[frontend design]] generation and full-stack [[software development]] when compared to single-agent baselines.

---

## Overview

**Harness design** is a software engineering discipline focused on architecting optimal environments for [[AI agents]] to perform extended, complex tasks. Rather than relying on a single agent to complete work autonomously, harness design employs multiple specialized agents with distinct roles, each addressing specific gaps in model performance.

The core insight is that [[self-evaluation]] in AI models tends to be unreliable—agents typically praise their own work even when quality is mediocre. By separating the agent performing work from the agent evaluating it, developers can create objective feedback mechanisms that drive iterative improvement.

### Key Innovation: The Generator-Evaluator Pattern

The generator-evaluator pattern, inspired by [[Generative Adversarial Networks]], creates a feedback loop where:

- A **generator** agent produces outputs
- An **evaluator** agent independently assesses quality
- Evaluation results guide the generator toward improved iterations

This separation proves more effective than asking a single agent to self-evaluate, as the evaluator can be specifically tuned to be skeptical and apply consistent grading criteria.

---

## Problem Statement: Why Naive Implementations Fall Short

### Context Window Limitations

[[AI agents]] executing lengthy tasks face two persistent challenges related to [[context windows]]:

1. **Context Anxiety**: Models like [[Claude Sonnet 4.5]] exhibit a tendency to prematurely conclude work as they approach their perceived context limit, even when tasks remain incomplete.

2. **Context Coherence Loss**: As context windows fill with conversation history, models lose coherence on complex tasks, producing lower-quality outputs.

#### Context Resets vs. Compaction

Two approaches address context limitations:

- **Compaction**: Summarizing earlier conversation portions in-place, allowing the same agent to continue with shortened history
- **Context Resets**: Completely clearing the context window and starting a fresh agent session with structured handoff artifacts

While compaction preserves continuity, it doesn't eliminate context anxiety. Context resets provide a clean slate but introduce orchestration complexity and token overhead. Testing showed context resets were essential for [[Claude Sonnet 4.5]] performance on long tasks.

### Self-Evaluation Bias

Agents asked to evaluate their own work consistently exhibit positive bias, particularly on [[subjective tasks]] like [[design]]. This occurs even on tasks with verifiable outcomes, where agents may make poor judgments that impede task completion.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—what practitioners term "AI slop."

### Solution: Grading Criteria Framework

To enable consistent evaluation of subjective design quality, four grading criteria were developed:

#### 1. Design Quality
Whether the design feels like a coherent whole rather than disconnected parts. Strong work combines colors, typography, layout, imagery, and other details to create a distinct mood and identity.

#### 2. Originality
Evidence of custom decisions versus template layouts and library defaults. Human designers should recognize deliberate creative choices. Generic AI patterns (e.g., purple gradients over white cards) fail this criterion.

#### 3. Craft
Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This competence check typically comes naturally to [[Claude]].

#### 4. Functionality
Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

### Implementation

The harness emphasized design quality and originality over craft and functionality, as [[Claude]] already performed well on the latter pair. This weighting pushed the model toward aesthetic risk-taking rather than generic defaults.

The evaluator was calibrated using few-shot examples with detailed score breakdowns, ensuring judgment alignment and reducing score drift across iterations.

### Results

Running 5-15 iterations per generation, the evaluator would:

- Navigate the live application using [[Playwright MCP]]
- Screenshot and study implementations before scoring
- Provide detailed critique flowing back to the generator

Across runs, evaluator assessments improved over iterations before plateauing. Notably, the wording of evaluation criteria steered outputs in unanticipated ways—phrases like "the best designs are museum quality" pushed designs toward particular visual convergence.

#### Notable Example: Dutch Art Museum

A prompt to create a website for a Dutch art museum produced a clean, dark-themed landing page by iteration nine. On iteration ten, the generator completely reimagined the approach as a spatial experience: a 3D room with checkered floor rendered in CSS perspective, artwork hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This creative leap exemplified the pattern's effectiveness.

---

## Full-Stack Coding: The Three-Agent Architecture

### Architecture Overview

Building on earlier [[long-running agent harness]] work, a three-agent system addressed specific gaps observed in prior runs:

#### Agent 1: Planner
Expands simple user prompts (1-4 sentences) into comprehensive product specifications. The planner:

- Maintains ambitious scope while focusing on product context and high-level technical design
- Avoids over-specifying granular technical details that could cascade into errors
- Identifies opportunities to weave [[AI features]] into product specs
- Generates visual design language using the [[frontend design skill]]

#### Agent 2: Generator
Implements the application according to the product spec. The generator:

- Works in sprints, implementing one feature at a time
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Performs self-evaluation at sprint end before handoff to QA
- Leverages [[Git]] for version control
- Negotiates sprint contracts with the evaluator before implementation

#### Agent 3: Evaluator
Tests the running application like a user would, using [[Playwright MCP]] to:

- Click through UI features, test API endpoints, verify database states
- Grade each sprint against product depth, functionality, visual design, and code quality
- Establish hard thresholds for each criterion
- Provide detailed feedback when criteria fail

### Sprint Contract Negotiation

Before each sprint, generator and evaluator negotiate a **sprint contract** defining:

- What "done" looks like for that work chunk
- Specific implementation details bridging user stories and testable implementation
- Success verification criteria

This bridges the gap between high-level specs and testable implementation without over-specifying early.

### Communication Pattern

Agents communicate via files: one agent writes a file, another reads and responds within that file or creates a new file. This keeps work faithful to specifications without premature implementation details.

---

## Case Study: Retro Video Game Maker

### Comparison: Solo vs. Harness

**Prompt**: _Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode._

| Harness Type | Duration | Cost |
|---|---|---|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

### Solo Agent Results

Initial output appeared functional but revealed critical issues:

- **Layout inefficiency**: Fixed-height panels left most viewport empty
- **Workflow rigidity**: UI didn't guide users toward necessary sequences (creating sprites/entities before populating levels)
- **Broken core functionality**: Entities appeared but didn't respond to input; entity-to-runtime wiring was broken

### Harness Results

The planner expanded the one-sentence prompt into a 16-feature spec across ten sprints, including:

- Core editors and play mode
- Sprite animation system
- Behavior templates
- Sound effects and music
- AI-assisted sprite generator and level designer
- Game export with shareable links

**Key improvements**:

- Polished, consistent visual identity tracking design spec
- Full viewport utilization with sensible panel sizing
- Richer sprite editor with cleaner tool palettes and better controls
- Built-in [[Claude]] integration for generating game components
- **Functional gameplay**: Users could actually move entities and play created levels

**Remaining gaps** (reflecting model limitations rather than harness design):

- Workflow still didn't clearly indicate sprite/entity creation prerequisites
- Physics had rough edges (character overlapping with platforms)
- Level design constraints sometimes created unpassable obstacles

---

## Harness Iteration and Simplification

As models improve, assumptions encoded in harness designs become outdated. The principle is: **find the simplest solution possible, and only increase complexity when needed**.

### Removing the Sprint Construct

With