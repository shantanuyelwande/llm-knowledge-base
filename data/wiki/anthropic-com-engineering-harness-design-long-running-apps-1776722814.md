---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-05T06:29:19.978291
raw_file_updated: 2026-06-05T06:29:19.978291
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-05T06:29:19.978291
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration frameworks used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article explores how multi-agent systems with specialized roles—particularly [[generator-evaluator]] architectures inspired by [[Generative Adversarial Networks]]—can overcome limitations in single-agent systems when building large-scale applications. The work demonstrates practical improvements in both [[frontend design]] generation and [[autonomous software engineering]] through careful prompt engineering, context management, and structured feedback loops.

---

## Overview

Harness design has emerged as a critical discipline in [[agentic AI]] development, particularly for tasks that exceed what individual language models can reliably accomplish in a single pass. Rather than relying solely on model capability improvements, harness design uses orchestration, specialized agent roles, and structured feedback to push models beyond their baseline performance on complex problems.

This approach was developed and documented by Prithvi Rajasekaran at [[Anthropic]] Labs, who applied harness design principles to two distinct domains: subjective [[frontend design]] tasks and objective [[full-stack software engineering]].

---

## Core Problems with Naive Implementations

### Context Management Issues

Long-running tasks expose fundamental limitations in how language models handle extended context:

- **Context window saturation**: As conversations lengthen, models lose coherence as the context window fills with previous interactions
- **Context anxiety**: Some models, particularly [[Claude Sonnet 4.5]], exhibit a tendency to prematurely conclude work as they approach their perceived context limits
- **Compaction vs. resets**: While [[context compaction]] summarizes earlier conversation history in place, [[context resets]] provide a clean slate by clearing the context window entirely and using structured handoffs to preserve state

Context resets proved superior to compaction for Sonnet 4.5, though they introduce additional orchestration complexity, token overhead, and latency.

### Self-Evaluation Bias

A critical failure mode emerges when agents are asked to evaluate their own work:

- Agents tend to respond with **confident self-praise** even when output quality is objectively mediocre
- This problem is particularly acute for **subjective tasks** like design, where no binary correctness check exists
- Even on tasks with verifiable outcomes, agents exhibit poor judgment that impedes performance during task execution
- **Separating generation from evaluation** proves to be a strong lever for addressing this bias

While evaluator agents remain inclined to be generous toward LLM-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

---

## Frontend Design: Making Subjectivity Gradable

### The Challenge

Without intervention, [[Claude]] typically gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—often exhibiting patterns associated with "[[AI slop]]."

### The Solution: Grading Criteria

The breakthrough came from encoding design principles into concrete, gradable criteria that could guide both generator and evaluator agents:

1. **Design Quality**: Does the design feel like a coherent whole rather than a collection of parts? Strong work combines colors, typography, layout, and imagery to create a distinct mood and identity.

2. **Originality**: Is there evidence of custom decisions, or only template layouts and library defaults? Human designers should recognize deliberate creative choices; unmodified stock components indicate failure.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check; most reasonable implementations succeed here by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

**Weighting strategy**: Design quality and originality were emphasized over craft and functionality, since Claude already scored well on the latter by default. This explicit penalization of generic patterns pushed the model toward more aesthetic risk-taking.

### Implementation Details

- **Generator agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator agent**: Used [[Playwright MCP]] to interact with live pages directly before scoring each criterion and writing detailed critiques
- **Iteration loop**: 5-15 iterations per generation, with each cycle pushing the generator in a more distinctive direction
- **Calibration**: Few-shot examples with detailed score breakdowns ensured evaluator judgment aligned with preferences and reduced score drift
- **Duration**: Full runs stretched up to four hours due to real wall-clock time for page navigation

### Key Findings

- Evaluator assessments improved over iterations before plateauing, with remaining headroom
- Pattern was not cleanly linear; later implementations tended to be better overall, but middle iterations were sometimes preferable
- Implementation complexity increased across rounds as the generator reached for more ambitious solutions
- Even first-iteration outputs were noticeably better than baseline with no prompting, suggesting the criteria and associated language steered the model away from generic defaults before evaluator feedback
- Prompting language had unexpected effects (e.g., "museum quality" pushed designs toward particular visual convergence)

### Notable Example: Dutch Art Museum

In one example, the generator initially produced a clean, dark-themed landing page aligned with expectations. On the tenth iteration, it scrapped the approach entirely and reimagined the site as a spatial 3D experience—a room with checkered floor rendered in CSS perspective, artwork hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This represented the kind of creative leap rarely seen from single-pass generation.

---

## Full-Stack Coding: Scaling the Multi-Agent Pattern

### Architecture Overview

Building on the [[GAN]]-inspired generator-evaluator pattern, the full-stack harness employed a three-agent system, each addressing specific gaps observed in prior runs:

#### Planner Agent

**Role**: Automate specification generation from simple prompts

- Takes 1-4 sentence user prompts and expands them into full product specifications
- Focuses on product context and high-level technical design rather than granular implementation details
- Avoids over-specifying technical details upfront to prevent cascading errors
- Identifies opportunities to weave [[AI agent]] features into product specs
- Access to [[frontend design skill]] to establish visual design language for the application

#### Generator Agent

**Role**: Implement features in manageable sprints

- Works in **sprint-based iterations**, picking one feature at a time from the specification
- Technology stack: [[React]], [[Vite]], [[FastAPI]], [[SQLite]] (later [[PostgreSQL]])
- Uses [[Git]] for version control
- Self-evaluates work at sprint end before handoff to QA
- Proposes sprint contracts negotiated with evaluator before coding begins

#### Evaluator Agent

**Role**: Verify quality and catch bugs through active testing

- Uses [[Playwright MCP]] to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and defined criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard thresholds; failing any one criterion fails the sprint
- Provides detailed feedback for generator iteration

### Sprint Contract Pattern

Before each sprint, generator and evaluator negotiate a **sprint contract** that:

- Bridges the gap between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews the proposal to ensure the generator builds the right thing
- Agents iterate until agreement is reached
- Generator then builds against the agreed contract before QA handoff

Communication occurs via files: one agent writes a file, another reads and responds either within that file or with a new file.

### Case Study: Retro Video Game Maker

**Prompt**: _Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode._

#### Solo Agent Performance (20 minutes, $9)

- Initial interface seemed aligned with expectations
- **Critical failures emerged during testing**:
  - Layout wasted space with fixed-height panels
  - Workflow was rigid and unintuitive
  - Core gameplay was broken: entities appeared on screen but didn't respond to input
  - Entity-runtime wiring was broken with no surface indication of the problem

#### Full Harness Performance (6 hours, $200)

- **20x more expensive but immediately superior quality**
- Planner expanded one-sentence prompt into 16-feature spec across ten sprints
- Features beyond solo attempt: sprite animation system, behavior templates, sound effects, AI-assisted generation, game export with shareable links
- **Polish and coherence**: Canvas used full viewport, sensible panel sizing, consistent visual identity
- **Functional gameplay**: Entities responded to input, physics worked (though with minor rough edges)
- **AI integration**: Built-in Claude integration enabled game generation through prompting, significantly speeding workflow
- **Evaluator value**: Caught specific bugs with detailed findings (e.g., route matching issues, handler condition bugs)

#### Evaluator Findings