---
title: Harness design for long-running application development _ Anthropic
source_file: Harness design for long-running application development _ Anthropic.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:16:21.866671
raw_file_updated: 2026-04-17T20:16:21.866671
version: 1
sources:
  - file: Harness design for long-running application development _ Anthropic.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:16:21.866671
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** is a systematic approach to structuring [[AI agent]] systems for complex, long-duration tasks in software development. Developed at Anthropic, this methodology combines multi-agent architectures inspired by [[Generative Adversarial Networks]] (GANs) with specialized agent roles to overcome limitations in [[context window]] management, self-evaluation bias, and task decomposition. The approach has proven effective for both subjective tasks like [[frontend design]] and objective tasks like [[full-stack application development]].

---

## Overview

Harness design addresses fundamental challenges in [[agentic AI]] development by structuring how [[language models]] like Claude approach extended, complex tasks. Rather than relying on a single agent to complete work from start to finish, harness design employs multiple specialized agents with distinct roles—such as planning, generation, and evaluation—that work in coordination to produce higher-quality outputs than baseline single-agent approaches.

This methodology emerged from work at Anthropic's Labs team, particularly research into improving Claude's capabilities in frontend design and autonomous software engineering. The key insight is that many failures in long-running agent tasks stem not from the model's fundamental capabilities, but from architectural and orchestration choices in how the task is structured.

---

## Core Challenges in Long-Running Tasks

### Context Window Management

One of the primary obstacles in long-running [[agentic coding]] is the degradation of model performance as the [[context window]] fills during extended sessions. Two related failure modes emerge:

**Context Anxiety**: Models like [[Claude Sonnet 4.5]] exhibit a tendency to prematurely wrap up work as they approach what they perceive as their context limit, even when significant work remains.

**Loss of Coherence**: As context accumulates, models tend to lose track of earlier decisions and architectural patterns, leading to inconsistent or conflicting implementations.

#### Context Resets vs. Compaction

Two strategies address these issues:

- **[[Compaction]]**: Summarizing earlier conversation portions in place, allowing the same agent to continue on a shortened history. While this preserves continuity, it does not provide a clean slate, and context anxiety can persist.

- **[[Context Reset]]**: Clearing the context window entirely and starting a fresh agent session, combined with structured [[artifact handoff]] that carries previous state and next steps. This provides a clean slate but adds orchestration complexity and token overhead.

Testing showed that Claude Sonnet 4.5 required context resets for strong performance on lengthy tasks, whereas later models like [[Claude Opus 4.6]] largely eliminated context anxiety behavior, making context resets unnecessary.

### Self-Evaluation Bias

When asked to evaluate their own work, [[language models]] consistently exhibit positive bias, praising outputs even when quality is mediocre. This problem is particularly pronounced for:

- **Subjective tasks** (like [[frontend design]]) where there is no binary correctness check
- **Complex objective tasks** where agents may miss subtle bugs or edge cases

The solution is to separate the agent generating work from the agent evaluating it. While evaluator agents are still inclined to be generous toward LLM-generated outputs, tuning a standalone evaluator to be appropriately skeptical is far more tractable than making a generator self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

### The Design Evaluation Framework

The first application of harness design focused on improving Claude's ability to generate high-quality frontend designs. The key insight was that while aesthetics cannot be fully reduced to a score, they can be improved through grading criteria that encode design principles.

Prithvi Rajasekaran developed four grading criteria, weighted to address Claude's baseline weaknesses:

#### Design Quality
Does the design feel like a coherent whole rather than a collection of parts? Strong work means colors, typography, layout, imagery, and other details combine to create a distinct mood and identity. This criterion addresses Claude's tendency toward generic, safe designs.

#### Originality
Is there evidence of custom decisions, or is this template layouts and AI-generated patterns? The criterion explicitly penalizes telltale signs of AI generation like "purple gradients over white cards" and encourages deliberate creative choices that a human designer would recognize.

#### Craft
Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check rather than a creativity check. Claude typically scores well here by default.

#### Functionality
Usability independent of aesthetics. Can users understand what the interface does, find primary actions, and complete tasks without guessing? Claude also typically handles this well baseline.

The weighting emphasized design quality and originality over craft and functionality, pushing the model toward more aesthetic risk-taking.

### Implementation with Generator-Evaluator Loop

The harness used the [[Claude Agent SDK]] with a [[generator-evaluator architecture]]:

1. **Generator Agent**: Created HTML/CSS/JavaScript frontends based on user prompts
2. **Evaluator Agent**: Used [[Playwright MCP]] to interact with live pages, navigating and screenshotting before scoring each criterion with detailed critique
3. **Iteration Loop**: Feedback flowed back to the generator, running 5-15 iterations per generation

The evaluator was calibrated using [[few-shot examples]] with detailed score breakdowns to ensure judgment aligned with design preferences and reduced score drift across iterations.

### Results and Observations

- Scores generally improved over iterations before plateauing
- Some generations refined incrementally; others took sharp aesthetic turns
- Prompting language directly shaped output character (e.g., phrases like "museum quality" steered toward particular visual convergence)
- Even first-iteration outputs were noticeably better than baseline with no specialized prompting
- Implementation complexity increased across rounds as generators reached for more ambitious solutions
- Notable example: A Dutch art museum website that pivoted from a conventional dark-themed landing page to a 3D spatial experience with CSS perspective and room-based navigation

---

## Full-Stack Application Development

### Three-Agent Architecture

Building on the frontend design work, Rajasekaran developed a three-agent system for complete [[full-stack development]]:

#### Planner Agent
Transforms simple user prompts (1-4 sentences) into comprehensive product specifications. Key characteristics:

- Ambitious about scope
- Focused on product context and high-level technical design rather than granular implementation details
- Avoids cascading errors from over-specified technical details
- Actively seeks opportunities to weave [[AI features]] into product specifications
- Integrates with frontend design skills to establish visual design language

#### Generator Agent
Implements the application iteratively in sprints using a modern tech stack ([[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]). Responsibilities include:

- Working one feature at a time from the specification
- Self-evaluating work at the end of each sprint
- Negotiating [[sprint contracts]] with the evaluator before implementation
- Using [[version control]] (git) for code management
- Building proper [[agents]] that can drive app functionality through tools

#### Evaluator Agent
Tests implementations thoroughly and grades against acceptance criteria. Key functions:

- Uses [[Playwright MCP]] to interact with running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades sprints against both discovered bugs and structured criteria
- Negotiates sprint contracts defining "done" before coding begins
- Provides specific, actionable feedback sufficient for the generator to address without investigation

### Sprint Contract System

Before each sprint, the generator and evaluator negotiate a [[sprint contract]] that:

- Bridges the gap between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews to ensure the generator is building the right thing
- Both iterate until agreement is reached
- Provides granular, testable criteria (e.g., 27 criteria for a single level editor sprint)

Communication occurs via files: one agent writes, the other reads and responds, maintaining context across handoffs.

### Initial Results: Retro Game Maker

A comparison between single-agent and full harness approaches on a retro video game maker prompt demonstrates the value:

| Harness Type | Duration | Cost | Quality |
|---|---|---|---|
| Solo Agent | 20 min | $9 | Broken core functionality; rigid workflow; poor UI layout |
| Full Harness | 6 hr | $200 | Functional gameplay; polished interface; rich feature set; integrated AI features |

The solo run produced an application that appeared functional initially but had broken entity-input wiring and poor usability. The harness run generated a 16-feature specification across 10 sprints, including sprite animation, behavior templates, sound effects, AI-assisted generation, and shareable exports. The final application was fully playable and included integrated Claude features for sprite and level generation.

### Evaluator Tuning and Limitations

Getting the evaluator to perform at high levels required significant tuning:

- Out of the box, Claude is a poor [[QA]] agent
- Early iterations identified legitimate issues then rationalized them away
- Evalu