---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-05T05:19:11.521385
raw_file_updated: 2026-05-05T05:19:11.521385
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-05T05:19:11.521385
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article describes how [[Anthropic]] developed multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs) to improve both [[frontend design]] quality and [[autonomous software engineering]]. The key innovation separates task execution from evaluation, allowing independent agents to generate work and critique it, creating feedback loops that drive better outputs than single-agent approaches.

## Overview

Harness design is critical to achieving high performance in [[agentic coding]] at the frontier of AI capabilities. Traditional single-agent approaches struggle with complex, long-running tasks due to [[context window]] limitations and poor self-evaluation. This work, conducted by Prithvi Rajasekaran of [[Anthropic Labs]], demonstrates how multi-agent architectures with specialized roles can overcome these limitations and produce production-quality applications.

The research builds on earlier work in [[long-running coding agent harness|long-running agent harnesses]] and [[frontend design skill|frontend design skills]], identifying two core problems that naive implementations face:

1. **Context degradation** - Models lose coherence over lengthy tasks and exhibit "context anxiety"
2. **Self-evaluation bias** - Agents praise their own work even when quality is mediocre

## Key Problems with Naive Implementations

### Context Window Limitations

Long-running tasks cause models to lose coherence as the [[context window]] fills. [[Claude Sonnet 4.5]] exhibited particularly strong "context anxiety," where the model begins wrapping up work prematurely as it approaches its perceived context limit.

**Solutions:**
- **Context resets** (clearing the context window entirely) rather than compaction (summarizing earlier content in place)
- Using [[structured artifacts]] to hand off context between sessions
- Relying on newer models like [[Claude Opus 4.6]] that handle longer contexts more naturally

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] tend to respond with unwarranted confidence, even when quality is obviously mediocre. This problem is particularly acute for subjective tasks like design where there is no binary correctness check.

**Solution:** Separate the agent doing the work from the agent judging it, creating an external feedback loop that is more tractable to tune than making a generator critical of its own work.

## The Generator-Evaluator Pattern

Inspired by [[Generative Adversarial Networks]] (GANs), a two-agent structure creates a feedback loop:

- **Generator agent**: Produces the actual work (code, design, etc.)
- **Evaluator agent**: Independently assesses output quality and provides detailed feedback

This separation is more effective than self-evaluation because:
- The evaluator can be specifically tuned to be skeptical
- The generator has concrete feedback to iterate against
- The feedback loop drives improvement over multiple iterations

## Frontend Design Application

### Grading Criteria

To make subjective design quality measurable, four grading criteria were developed:

1. **Design Quality** - Does the design feel like a coherent whole? Do colors, typography, layout, and imagery combine to create a distinct mood and identity?
2. **Originality** - Evidence of custom decisions rather than template layouts and defaults? Recognition of deliberate creative choices?
3. **Craft** - Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios
4. **Functionality** - Usability independent of aesthetics; can users understand, find actions, and complete tasks?

Design quality and originality were weighted more heavily, as Claude already excelled at craft and functionality by default.

### Implementation

The [[Claude Agent SDK]] was used to build the loop:

1. **Generator** creates HTML/CSS/JS frontend from user prompt
2. **Evaluator** uses [[Playwright MCP]] to interact with live page, screenshot, and study implementation
3. Evaluator scores each criterion and writes detailed critique
4. Generator receives feedback and iterates (5-15 iterations per generation)
5. Generator makes strategic decisions to refine direction or pivot aesthetic

**Results:** Over iterations, evaluator assessments improved before plateauing. Some generations refined incrementally; others took sharp aesthetic turns. Even first iterations were noticeably better than baseline with no prompting, suggesting the criteria language itself steers the model away from generic defaults.

### Notable Example

A website for a Dutch art museum evolved from a clean, dark-themed landing page (iteration 9) to a spatial 3D experience (iteration 10) with a checkered floor rendered in CSS perspective, artwork hung on walls in free-form positions, and doorway-based navigation—representing the kind of creative leap rarely seen from single-pass generation.

## Full-Stack Coding Architecture

Building on frontend design insights, a three-agent system was created for autonomous full-stack development:

### Planner Agent

- Takes simple 1-4 sentence user prompt
- Expands into full product specification
- Prompted to be ambitious about scope
- Focuses on product context and high-level technical design rather than implementation details
- Identifies opportunities to weave [[AI agents|AI features]] into product specs
- Uses [[frontend design skill]] to create visual design language

**Rationale:** Avoids cascading errors from over-specified technical details; lets downstream agents figure out implementation path.

### Generator Agent

- Works in [[sprint]]-based iterations (in earlier versions)
- Implements one feature at a time from specification
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Includes [[Git]] for version control
- Self-evaluates work at end of each sprint
- Negotiates sprint contracts with evaluator before coding

### Evaluator Agent

- Uses [[Playwright MCP]] to click through running application like a user
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and quality criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard threshold; sprint fails if any falls below
- Provides detailed feedback for generator to fix

### Sprint Contracts

Before each sprint, generator and evaluator negotiate a contract defining:
- What will be built
- How success will be verified
- Testable implementation criteria

This bridges the gap between high-level user stories and concrete implementation without over-specification.

### Communication Protocol

Agents communicate via files:
- One agent writes a file
- Another agent reads and responds
- Keeps work faithful to specification without over-specifying implementation too early

## Case Study: Retro Game Maker

### Comparison: Solo vs. Full Harness

**Prompt:** _Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode._

| Harness Type | Duration | Cost |
|---|---|---|
| Solo (single agent) | 20 min | $9 |
| Full harness (3 agents) | 6 hr | $200 |

### Solo Run Results

- Appeared to meet basic expectations initially
- Significant issues upon interaction:
  - Wasted space with fixed-height panels
  - Rigid workflow without UI guidance
  - **Core feature broken**: Entities appeared but didn't respond to input
  - Entity-to-runtime wiring was broken with no surface indication

### Full Harness Results

- Planner expanded prompt into 16-feature spec across 10 sprints
- Included: core editors, animation system, behavior templates, sound/music, AI-assisted sprite generator, level designer, game export
- Advantages over solo:
  - Consistent visual identity tracking design spec
  - Richer, more fully-featured sprite editor
  - Built-in Claude integration for generating game parts
  - **Core feature works**: Game is actually playable
  - Physics implementation present (though rough)

**Trade-off:** Still had usability gaps (workflow not intuitive) and edge cases (level design constraints), but fundamental functionality worked.

## Iterating on the Harness

As models improve, assumptions about what scaffolding is necessary become outdated. The principle: "find the simplest solution possible, and only increase complexity when needed."

### Removal of Sprint Construct

With [[Claude Opus 4.6]] release, which improved planning, long-context work, and code review capabilities, the sprint structure was removed:

- **Result:** Model could handle decomposition natively without explicit sprint scaffolding
- **Planner retained:** Without it, generator under-scoped work
- **Evaluator moved:** From per-sprint grading to single pass at end
- **New approach:** Evaluator cost is only justified when task sits beyond what current model does reliably solo

### Case Study: Digital Audio Workstation (DAW)

**Prompt:** _Build a fully featured DAW in the browser using the Web Audio API._

| Phase | Duration | Cost |
|---|---|---|
|