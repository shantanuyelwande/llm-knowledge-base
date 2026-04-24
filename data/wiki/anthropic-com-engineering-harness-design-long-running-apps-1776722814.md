---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T04:59:16.183783
raw_file_updated: 2026-04-24T04:59:16.183783
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T04:59:16.183783
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to successfully complete complex, long-running tasks. This article describes techniques developed at [[Anthropic]] for improving [[Claude]]'s ability to build complete applications autonomously, combining multi-agent architectures inspired by [[Generative Adversarial Networks]] with structured context management and evaluation frameworks.

---

## Introduction

Long-running application development presents unique challenges for [[language models]]. As context windows fill and task complexity increases, models tend to lose coherence, exhibit "context anxiety" (prematurely concluding work), and struggle with self-evaluation. This article documents approaches developed by Prithvi Rajasekaran at [[Anthropic Labs]] to overcome these limitations through innovative harness design, demonstrating substantial improvements in both [[frontend design]] quality and full-stack application development.

---

## Core Problems with Naive Implementations

### Context Management Issues

Traditional approaches to long-running tasks face two primary challenges:

**Context Window Degradation**: As the context window fills during extended work sessions, models lose coherence and struggle to maintain consistency with earlier decisions.

**Context Anxiety**: Some models, particularly [[Claude Sonnet 4.5]], exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when substantial work remains.

While [[context compaction]] (summarizing earlier conversation segments in place) provides some relief, it fails to address context anxiety because the agent retains awareness of its position in the context window. **Context resets**—clearing the context entirely and starting fresh with a structured handoff containing previous state—proved more effective, though at the cost of additional [[token]] overhead and orchestration complexity.

### Self-Evaluation Limitations

A second critical issue is agent self-evaluation. When asked to assess their own work, [[AI agents]] tend to respond with unwarranted confidence, praising mediocre outputs. This problem is particularly acute for subjective tasks like [[frontend design]] where no binary correctness check exists.

**Key insight**: Separating the agent performing work from the agent evaluating it dramatically improves assessment quality. While evaluator agents retain some leniency toward [[language model]]-generated outputs, they can be tuned to skepticism far more effectively than generators can be trained to self-criticize.

---

## Frontend Design: Making Subjectivity Gradable

### Design Criteria Framework

The initial harness experiments focused on [[frontend design]], where subjective quality was most problematic. To address this, four concrete grading criteria were developed to guide both generator and evaluator agents:

1. **Design Quality**: Does the design feel coherent rather than fragmented? Strong outputs combine color, typography, layout, and imagery into a distinct mood and identity.

2. **Originality**: Does the design show evidence of deliberate creative choices, or does it rely on template layouts and unmodified components? The criterion explicitly penalizes generic "AI slop" patterns like purple gradients over white cards.

3. **Craft**: Technical execution quality including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This represents competence verification rather than creativity assessment.

4. **Functionality**: Usability independent of aesthetics—can users understand the interface, find primary actions, and complete tasks without confusion?

The evaluator was calibrated using few-shot examples with detailed score breakdowns, ensuring consistent judgment aligned with design preferences.

### Generator-Evaluator Loop Architecture

The frontend design harness implemented a [[GAN]]-inspired loop:

- A **generator agent** created HTML/CSS/JavaScript frontends based on user prompts
- An **evaluator agent** received [[Playwright]] [[Model Context Protocol]] (MCP) access, enabling it to interact with live pages directly
- The evaluator would navigate pages, take screenshots, and score each criterion with detailed critique
- Feedback flowed back to the generator for the next iteration
- The generator made strategic decisions: refine current direction if scores trended positively, or pivot to entirely different aesthetics if approaches weren't working

Typical runs involved 5-15 iterations per generation, with each cycle pushing toward more distinctive outputs. Full runs extended up to four hours due to real wall-clock time required for page navigation and evaluation.

### Key Findings

- **Prompt wording shaped outputs significantly**: Phrases like "the best designs are museum quality" pushed toward particular visual convergence, demonstrating that criteria language directly influenced output character.

- **Improvement was non-linear**: While scores generally improved across iterations before plateauing, individual preferred iterations often appeared mid-sequence rather than at the end.

- **Complexity increased over iterations**: Generators reached for more ambitious solutions in response to evaluator feedback, progressively implementing sophisticated interactions.

- **First-iteration improvement was substantial**: Even without evaluator feedback, outputs were noticeably better than baseline with no prompting, suggesting criteria themselves steered models away from generic defaults.

---

## Full-Stack Application Development

### Three-Agent Architecture

Building on frontend design insights, a three-agent system was developed for autonomous full-stack application development:

#### Planner Agent

Transforms simple 1-4 sentence prompts into comprehensive product specifications. The planner:

- Expands scope ambitiously while focusing on product context and high-level technical design rather than granular implementation details
- Avoids over-specifying technical details upfront to prevent cascading errors
- Identifies opportunities to weave [[AI features]] into product specifications
- Accesses the [[frontend design skill]] to incorporate visual design language

**Rationale**: Detailed upfront specifications, if incorrect, cascade errors into downstream implementation. Constraining deliverables while allowing flexible implementation paths produces better results.

#### Generator Agent

Implements the application using a [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack. The generator:

- Works in sprints (in the initial architecture), implementing one feature at a time
- Performs self-evaluation at sprint end before handing off to QA
- Has access to [[Git]] for version control
- Negotiates sprint contracts with the evaluator before implementation

#### Evaluator Agent

Performs quality assurance through active testing. The evaluator:

- Uses [[Playwright]] MCP to click through running applications like end users would
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and criteria covering product depth, functionality, visual design, and code quality
- Establishes sprint contracts with the generator, negotiating what "done" looks like before code is written

### Sprint Contract Mechanism

Before implementation, generator and evaluator negotiate a **sprint contract** that:

- Bridges the gap between high-level user stories and testable implementation
- Specifies what the generator will build and how success will be verified
- Includes specific, gradable criteria (e.g., 27 criteria for a level editor sprint)
- Provides the evaluator with concrete benchmarks for assessment

Communication occurs via files, with agents reading and responding to each other's documents, maintaining faithful adherence to specifications without over-constraining implementation.

### Retro Game Maker Case Study

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness | Duration | Cost |
|---------|----------|------|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Agent Results**: The interface appeared functional initially but exhibited critical failures:
- Layout wasted space with fixed-height panels
- Rigid workflow didn't guide users toward proper sequence (create sprites/entities before populating levels)
- Core gameplay was broken—entities appeared but didn't respond to input
- Code wiring between entity definitions and game runtime was severed

**Full Harness Results**: The planner expanded the prompt into a 16-feature spec across ten sprints, including:
- Sprite animation system
- Behavior templates
- Sound effects and music
- AI-assisted sprite generator and level designer
- Game export with shareable links

The resulting application demonstrated:
- Consistent visual identity tracking design language from specification
- Richer, more fully-featured editors with cleaner tool palettes
- Built-in [[Claude]] integration for generating game components through prompting
- Functional gameplay where entities actually responded to input
- Minor physics edge cases (character overlapping platforms) but core mechanics worked

### Evaluator Quality Standards

The evaluator identified specific, actionable bugs such as:

| Criterion | Finding |
|-----------|---------|
| Rectangle fill tool allows click-drag to fill area | FAIL — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered properly on mouseUp |
| User can select and delete entity spawn points | FAIL — Delete key handler requires both `selection` and `selectedEntityId` to be set, but clicking entity only sets `selectedEntityId` |
| User can reorder animation frames via API | FAIL — `PUT /frames/reorder` route defined after `/{