---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-22T04:51:21.755190
raw_file_updated: 2026-04-22T04:51:21.755190
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-22T04:51:21.755190
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** is an architectural approach for improving the performance of [[AI agents]] on complex, long-running tasks. Developed by [[Anthropic]] researchers, this methodology applies [[generator-evaluator]] patterns inspired by [[Generative Adversarial Networks]] (GANs) to coordinate multiple specialized agents working on different aspects of a problem. The approach has proven effective for both [[frontend design]] tasks and full-stack [[autonomous software engineering]], significantly improving output quality compared to single-agent baselines.

---

## Overview

Harness design addresses fundamental limitations in how [[language models]] perform on extended tasks. Rather than relying on a single agent to complete complex work, harness design decomposes problems across multiple specialized agents, each addressing specific gaps in model performance. This approach emerged from practical experience with [[long-running agents]] and represents a significant evolution in [[AI engineering]] practices.

The methodology was pioneered by Prithvi Rajasekaran at [[Anthropic Labs]] and published in March 2026.

## Core Problems Addressed

### Context Window Degradation

As [[context windows]] fill during long tasks, [[language models]] experience two related phenomena:

- **Context anxiety**: Models begin prematurely concluding work as they approach perceived context limits
- **Loss of coherence**: Task performance degrades as the conversation history grows longer

While [[context compaction]] (summarizing earlier conversation to free space) preserves continuity, it doesn't provide a clean slate. **Context resets**—clearing the context window entirely and passing state via structured handoffs—proved more effective for models like [[Claude Sonnet 4.5]], though later models like [[Claude Opus 4.6]] largely eliminated this behavior.

### Self-Evaluation Bias

When asked to evaluate their own work, [[language models]] exhibit systematic bias toward positive assessment. This is particularly problematic for:

- **Subjective tasks** (like [[frontend design]]) where no binary correctness metric exists
- **Complex implementations** where subtle bugs may not be immediately apparent

Separating the agent performing work from the agent evaluating it creates a feedback loop that drives improvement, as the generator has concrete external feedback to iterate against.

## Architecture: Generator-Evaluator Pattern

The harness design pattern borrows from [[Generative Adversarial Networks]] (GANs), applying a **generator** and **evaluator** structure to software development:

- **Generator Agent**: Creates the primary work product (code, design, etc.)
- **Evaluator Agent**: Tests and grades the generator's output against defined criteria
- **Feedback Loop**: Evaluator feedback drives iterative improvement

This separation proves tractable to tune: making a standalone evaluator skeptical is far easier than making a generator self-critical.

## Frontend Design Application

### Grading Criteria Framework

To make subjective aesthetic judgment gradable, researchers developed four evaluation criteria:

1. **Design Quality**: Does the design feel coherent rather than a collection of parts? Do colors, typography, layout, and imagery combine to create a distinct mood and identity?

2. **Originality**: Is there evidence of custom decisions, or does it rely on template layouts and library defaults? Can humans recognize deliberate creative choices?

3. **Craft**: Technical execution of typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity assessment.

4. **Functionality**: Usability independent of aesthetics. Can users understand what the interface does and complete tasks without guessing?

### Implementation Details

- Generator agents created HTML/CSS/JavaScript frontends based on user prompts
- Evaluators used [[Playwright MCP]] to interact with live pages directly, taking screenshots and studying implementations before scoring
- Iterations ran 5-15 cycles per generation, with each cycle pushing toward more distinctive designs
- Full runs stretched up to four hours
- Generator made strategic decisions: refine current direction if scores trended well, or pivot to entirely different aesthetics if approaches weren't working

### Results

The evaluator's assessments improved over iterations before plateauing. Notably:

- Even first iterations outperformed baselines with no prompting, suggesting criteria and language themselves steered models away from generic defaults
- Later implementations were generally better overall, though not always linearly—humans sometimes preferred middle iterations
- Implementation complexity increased across rounds as generators reached for more ambitious solutions
- In one example, a Dutch art museum website evolved from a conventional dark-themed landing page into a creative 3D spatial experience with CSS perspective rendering and gallery room navigation

## Full-Stack Coding Application

### Three-Agent Architecture

Extending the pattern to autonomous software engineering, researchers developed a three-agent system:

#### Planner Agent
- Takes simple 1-4 sentence prompts and expands them into full product specifications
- Prompted to be ambitious about scope while staying focused on product context and high-level technical design rather than granular implementation details
- Explicitly tasked to identify opportunities for weaving [[AI features]] into product specs
- Prevents cascading errors from overly-specific upfront specifications

#### Generator Agent
- Implements features from the specification
- Works in sprints (in earlier versions) or continuously (in later versions)
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint
- Uses [[Git]] for version control
- In later iterations, builds agents that can drive the app's own functionality through tools

#### Evaluator Agent
- Uses [[Playwright MCP]] to test applications like a user would
- Clicks through running applications, testing UI features, API endpoints, and database states
- Grades against both discovered bugs and criteria covering product depth, functionality, visual design, and code quality
- Implements **sprint contracts**: agreements on what "done" looks like before code is written, bridging gap between user stories and testable implementation
- Communicates via files: agents read and respond to previous agent's work through structured file exchanges

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness | Duration | Cost |
|---------|----------|------|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Agent Output Issues**:
- Fixed-height panels wasted viewport space
- Rigid workflow with no UI guidance for required sequence
- Core gameplay broken: entities appeared but didn't respond to input
- Wiring between entity definitions and runtime was broken

**Full Harness Output Advantages**:
- Planner expanded one-sentence prompt into 16-feature spec across ten sprints
- Included sprite animation system, behavior templates, sound effects, AI-assisted sprite generator and level designer, and shareable game export
- Visual design language integrated from [[frontend design skill]]
- App showed polish, consistent visual identity, and responsive interface
- Sprite editor richer and more fully featured
- Built-in [[Claude]] integration for generating game components through prompting
- Core gameplay functional: entities responded to input, could navigate levels

### Evaluator Effectiveness

The evaluator identified specific, actionable issues:

| Contract Criterion | Evaluator Finding |
|-------------------|-------------------|
| Rectangle fill tool allows click-drag to fill rectangular area | **FAIL** — Tool only places tiles at drag start/end points. `fillRectangle` function exists but isn't triggered properly on mouseUp. |
| User can select and delete placed entity spawn points | **FAIL** — Delete key handler requires both `selection` and `selectedEntityId` to be set, but clicking entity only sets `selectedEntityId`. |
| User can reorder animation frames via API | **FAIL** — `PUT /frames/reorder` route defined after `/{frame_id}` routes, causing FastAPI to match 'reorder' as frame_id integer. |

Achieving this level of evaluation required significant tuning—out of the box, [[Claude]] was a poor QA agent, identifying issues then talking itself into accepting them anyway, and testing superficially rather than probing edge cases.

## Harness Evolution and Optimization

### Simplification Principles

As models improved, researchers found that every harness component encodes an assumption about model limitations. These assumptions are worth stress-testing because they may be incorrect or become stale as models improve. The principle: **find the simplest solution possible, and only increase complexity when needed**.

### Removing the Sprint Construct

With [[Claude Opus 4.6]], which demonstrated superior planning, sustained agentic task performance, and better code review capabilities, researchers simplified the harness:

- **Removed**: Sprint-based decomposition (model could handle longer coherent work)
- **Kept**: Planner (prevented under-scoping) and evaluator (caught edge cases)
- **Modified**: Evaluator moved to single end-of-run pass rather than per-sprint grading
- **Result**: Evaluator value became task-dependent; useful when task sits