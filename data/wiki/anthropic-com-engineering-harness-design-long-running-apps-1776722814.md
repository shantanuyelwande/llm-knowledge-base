---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-07T05:36:56.470404
raw_file_updated: 2026-05-07T05:36:56.470404
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-07T05:36:56.470404
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article describes techniques developed at [[Anthropic]] for improving [[Claude]]'s performance on extended development tasks through multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs). The approach separates generation and evaluation into distinct agents, enabling iterative improvement of both [[frontend design]] and full-stack application development without human intervention.

---

## Overview

Harness design is a critical engineering discipline for building effective long-running [[agentic systems]]. While simple prompting can handle straightforward tasks, complex applications—particularly those requiring subjective judgment or extended multi-hour development cycles—benefit from structured orchestration patterns that decompose work, manage context, and provide external evaluation.

This article documents research conducted by Prithvi Rajasekaran of [[Anthropic Labs]], exploring how to push [[Claude]] beyond baseline performance on two interconnected problems:

1. Producing high-quality [[frontend design]] with distinctive aesthetics
2. Building complete, functional full-stack applications autonomously

The work demonstrates that separating the roles of **generator** (creation) and **evaluator** (assessment) agents significantly improves output quality compared to single-agent approaches, even when the evaluator is itself an [[LLM]].

---

## Core Problems with Naive Implementations

### Context Management Issues

Long-running [[AI agent]] tasks face two primary context-related challenges:

**Context Window Saturation**
As conversations extend, the [[context window]] fills with history, reducing the model's ability to process new information effectively. While [[context compaction]] (summarizing earlier conversation segments in place) helps preserve continuity, it doesn't fully solve the problem.

**Context Anxiety**
Some models, particularly [[Claude Sonnet 4.5]], exhibit a tendency to prematurely wrap up work as they approach what they perceive as their [[context limit]]. This behavior persists even with compaction.

**Context Resets as Solution**
Rather than compacting within a single session, the solution involves clearing the context window entirely and starting a fresh agent with a structured handoff. This provides a clean slate while using [[structured artifacts]] to carry forward previous agent state and next steps. However, context resets add orchestration complexity, token overhead, and latency.

### Self-Evaluation Limitations

When asked to evaluate their own work, [[AI agents]] exhibit systematic biases:

- **Overconfidence**: Models tend to praise their outputs confidently, even when quality is mediocre by human standards
- **Subjective task blindness**: For tasks without binary verification (like [[design quality]]), agents reliably skew positive in self-assessment
- **Impaired judgment**: Even on tasks with verifiable outcomes, agents sometimes exhibit poor judgment that impedes their own performance

**Separation as Mitigation**
Separating the generating agent from the evaluating agent proves to be a strong lever. While both are [[LLMs]] inclined toward leniency, tuning a standalone evaluator to be skeptical is more tractable than making a generator critical of its own work. Once external feedback exists, the generator has concrete input to iterate against.

---

## Frontend Design: Making Subjective Quality Gradable

### Design Criteria Framework

The initial harness was built for [[frontend design]], where self-evaluation issues were most visible. The key insight was that while aesthetics cannot be fully reduced to a score, they can be improved through grading criteria that encode [[design principles]].

Four grading criteria were developed:

1. **Design Quality**: Does the design feel like a coherent whole rather than a collection of parts? Strong work combines colors, [[typography]], layout, imagery, and other details to create a distinct mood and identity.

2. **Originality**: Is there evidence of custom decisions, or does the design rely on template layouts, library defaults, and recognizable AI-generated patterns? A human designer should recognize deliberate creative choices.

3. **Craft**: Technical execution including [[typography hierarchy]], spacing consistency, [[color harmony]], and contrast ratios. This is a competence check; most reasonable implementations succeed here by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

The harness emphasized design quality and originality over craft and functionality, as [[Claude]] already performed well on the latter two. The criteria explicitly penalized generic "[[AI slop]]" patterns.

### Implementation Architecture

The design harness operated on the following cycle:

1. A **generator agent** created HTML/CSS/JavaScript frontends based on user prompts
2. An **evaluator agent** received access to [[Playwright MCP]], allowing it to interact with the live page directly
3. The evaluator would navigate the page, take screenshots, study the implementation, then score each criterion with detailed critique
4. Feedback flowed back to the generator for the next iteration
5. The generator made strategic decisions: refine the current direction if scores trended well, or pivot to a different aesthetic if the approach wasn't working

Typical runs involved 5-15 iterations per generation, with full runs extending up to four hours. The evaluator's assessments improved over iterations before plateauing, with remaining headroom still available.

### Key Findings

- **Criteria-driven convergence**: The wording of criteria steered the generator in ways not fully anticipated. Phrases like "the best designs are museum quality" pushed outputs toward particular visual convergence.

- **Non-linear improvement**: While scores generally improved over iterations, patterns weren't cleanly linear. Later implementations tended to be better overall, but earlier iterations were sometimes preferable.

- **Baseline lift from criteria alone**: Even on the first iteration, outputs were noticeably better than baseline with no prompting, suggesting the criteria and associated language themselves steered the model away from generic defaults before any evaluator feedback.

- **Unexpected creativity**: The system occasionally produced creative leaps—for example, reimagining a museum website as a 3D spatial experience with CSS perspective rendering and free-form artwork positioning—that demonstrated genuine aesthetic innovation.

---

## Scaling to Full-Stack Coding

### Three-Agent Architecture

Building on the [[long-running coding agent harness]] from earlier work, a three-agent system was developed to address gaps in autonomous full-stack development:

#### Planner Agent

**Role**: Expands simple user prompts into detailed product specifications

**Characteristics**:
- Takes 1-4 sentence prompts and produces comprehensive specs
- Ambitious about scope, focused on product context and high-level technical design rather than granular implementation details
- Avoids over-specifying technical details that could cascade errors into downstream implementation
- Actively seeks opportunities to weave [[AI features]] into product specs

**Rationale**: Automating specification creation prevents users from needing to provide detailed upfront specs, while allowing the downstream agents to determine implementation paths.

#### Generator Agent

**Role**: Implements the application according to the spec

**Characteristics**:
- Works in sprints, picking up one feature at a time from the spec
- Implements using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]]
- Uses [[Git]] for version control
- Self-evaluates work at the end of each sprint before handoff to QA
- Negotiates sprint contracts with the evaluator before implementation

**Sprint Contract**:
Before each sprint, the generator and evaluator agree on:
- What will be built
- How success will be verified
- Testable implementation criteria

This bridges the gap between high-level user stories and testable implementation without over-specifying early.

#### Evaluator Agent

**Role**: Performs quality assurance and testing

**Characteristics**:
- Uses [[Playwright MCP]] to click through the running application like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and evaluation criteria
- Each criterion has hard thresholds; failure on any criterion causes the sprint to fail
- Provides detailed feedback on what went wrong

**Evaluation Criteria** (adapted from frontend design):
- Product depth
- Functionality
- Visual design
- Code quality

**Testing Methodology**: The evaluator actively navigates and exercises the application rather than reviewing static code, enabling discovery of runtime issues and user experience problems.

### Communication Pattern

Communication between agents occurs via files:
- One agent writes a file
- Another reads it and responds either within that file or with a new file
- The previous agent reads the response and continues

This approach keeps work faithful to specifications without over-constraining implementation details.

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Comparison Results**:

| Harness Type | Duration | Cost |
|---|---|---|
| Solo Agent | 20 minutes | $9 |
| Full Harness | 6