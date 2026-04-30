---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-30T05:35:23.915498
raw_file_updated: 2026-04-30T05:35:23.915498
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-30T05:35:23.915498
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to effectively complete complex, multi-hour autonomous software engineering tasks. By combining [[generator-evaluator architectures]] inspired by [[Generative Adversarial Networks]] (GANs), task decomposition, and structured context handoff mechanisms, harness design enables [[large language models]] like [[Claude]] to produce high-quality full-stack applications without human intervention. This approach addresses key limitations including [[context anxiety]], self-evaluation bias, and coherence degradation over extended execution periods.

---

## Overview

Harness design has emerged as a critical discipline in [[agentic AI]] development, particularly for long-running coding tasks. Rather than relying on single-pass model outputs, well-designed harnesses orchestrate multiple specialized agents to decompose complex problems, maintain coherence across extended sessions, and iteratively improve results through structured feedback loops.

The core insight underlying modern harness design is that many apparent limitations of language models can be addressed through thoughtful system architecture rather than waiting for model improvements alone. By separating concerns—such as planning, generation, and evaluation—developers can create feedback mechanisms that drive higher-quality outputs across both subjective domains (like [[frontend design]]) and objective tasks (like [[software development]]).

---

## Key Problems in Long-Running Agentic Coding

### Context Window Limitations

As [[context window]] fills during extended execution, models exhibit two related failure modes:

- **Context degradation**: Model coherence declines as the context window fills, causing agents to "go off the rails" on lengthy tasks
- **Context anxiety**: Models like [[Claude Sonnet 4.5]] exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when substantial work remains

### Context Reset vs. Compaction

Two strategies address context limitations:

**Compaction** summarizes earlier conversation sections in place, allowing the same agent to continue on a shortened history. While this preserves continuity, it does not eliminate [[context anxiety]] because the agent retains awareness of its approaching limit.

**Context reset** provides a clean slate by ending the current session and starting a fresh agent, using a structured handoff artifact to carry previous state forward. This approach eliminates context anxiety but introduces orchestration complexity and token overhead.

[[Claude Opus 4.5]] required context resets for strong performance on long tasks, while later models like [[Claude Opus 4.6]] largely eliminated this behavior, reducing the need for aggressive reset strategies.

### Self-Evaluation Bias

A second persistent challenge is **self-evaluation bias**: when asked to evaluate their own work, agents tend to respond with unwarranted confidence and positive assessments, even when output quality is mediocre to a human observer. This problem is particularly acute for subjective tasks like [[frontend design]], where verifiable tests cannot easily measure quality.

Separating the evaluating agent from the generating agent proves to be a strong lever for addressing this issue. While evaluator agents still exhibit some leniency toward LLM-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

---

## Frontend Design Harness

### The Generator-Evaluator Pattern

Inspired by [[Generative Adversarial Networks]], the frontend design harness implements a two-agent architecture:

- **Generator agent**: Creates [[HTML]]/[[CSS]]/[[JavaScript]] frontends based on user prompts
- **Evaluator agent**: Grades outputs against explicit criteria and provides detailed feedback for iteration

This structure creates a feedback loop that drives the generator toward stronger outputs, enabling iterative refinement across 5-15 cycles per generation.

### Design Evaluation Criteria

To make subjective aesthetic judgments gradable, the harness defines four explicit criteria:

1. **Design quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, and imagery to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Penalizes generic "[[AI slop]]" patterns and unmodified stock components.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The harness emphasizes design quality and originality over craft and functionality, as [[Claude]] naturally excels at the latter two. This weighting pushes the model toward greater aesthetic risk-taking and away from bland defaults.

### Implementation Details

The harness uses the [[Claude Agent SDK]] for orchestration. The evaluator agent receives the [[Playwright MCP]] to interact with live pages directly, allowing it to navigate, screenshot, and carefully study implementations before scoring. This real-time interaction adds wall-clock time (full runs stretch to 4 hours) but provides richer feedback than static evaluation.

The generator receives detailed evaluator critiques and makes strategic decisions: refine the current direction if scores trend well, or pivot to an entirely different aesthetic if the approach isn't working.

### Results and Observations

- Scores generally improve over iterations before plateauing, though the pattern is not always cleanly linear
- Later implementations tend to be better overall, but earlier iterations are sometimes preferred
- Implementation complexity increases across rounds as the generator reaches for more ambitious solutions
- The language of the criteria steers the generator in ways that weren't fully anticipated (e.g., "museum quality" pushes toward particular visual convergence)
- Even first-iteration outputs are noticeably better than baseline with no prompting, suggesting criteria and associated language themselves move the model away from generic defaults

In one notable example, a museum website generator scrapped its initial approach on the tenth iteration and reimagined the site as a 3D spatial experience with CSS perspective rendering, artwork hung in free-form positions, and doorway-based navigation—a creative leap not seen in single-pass generation.

---

## Full-Stack Development Harness

### Three-Agent Architecture

Building on the frontend design findings, the full-stack harness implements a three-agent system, each addressing specific gaps observed in prior long-running coding attempts:

#### Planner Agent

Takes a simple 1-4 sentence user prompt and expands it into a full product specification. Key characteristics:

- Ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation details
- Avoids cascading errors that occur when the planner over-specifies and gets details wrong
- Weaves [[AI features]] into product specs to enhance user workflows
- Has access to [[frontend design skill]] to create visual design language as part of the specification

#### Generator Agent

Implements the application against the spec. Key characteristics:

- Works in **sprints**, picking up one feature at a time from the specification
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint before handing off to QA
- Has access to [[Git]] for version control
- Negotiates a **sprint contract** with the evaluator before implementation begins

#### Evaluator Agent

Tests the running application and grades against explicit criteria. Key characteristics:

- Uses [[Playwright MCP]] to click through applications like a user would
- Tests [[UI]] features, [[API]] endpoints, and database states
- Grades each sprint against criteria covering product depth, functionality, visual design, and code quality
- Each criterion has hard thresholds; if any falls below the threshold, the sprint fails
- Provides detailed feedback on what went wrong for the generator to fix

### Sprint Contract Mechanism

A critical component of the harness is the **sprint contract**, which bridges the gap between high-level user stories and testable implementation:

1. Generator proposes what it will build and how success will be verified
2. Evaluator reviews the proposal to ensure the generator is building the right thing
3. Two agents iterate until agreement is reached
4. Generator builds against the agreed-upon contract
5. Evaluator tests implementation against contract criteria

This prevents over-specification while maintaining fidelity to the spec through explicit testable criteria.

### Communication via Structured Artifacts

Agents communicate through files rather than direct conversation:

- One agent writes a file
- Another agent reads it and responds either within that file or with a new file
- Previous agent reads the response in turn

This approach keeps work faithful to the spec without over-specifying implementation too early, and creates clear handoff points for [[context reset]] if needed.

---

## Case Study: Retro Video Game Maker

### Comparative Results

A simple prompt ("Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode") was tested against both a single-agent baseline and the full three-agent harness:

| Harness Type | Duration | Cost |
|---|---|---|
| Solo agent | 20 min | $9 |
| Full harness | 6 hr | $