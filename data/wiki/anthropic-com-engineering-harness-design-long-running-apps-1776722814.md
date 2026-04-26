---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-26T05:16:50.337393
raw_file_updated: 2026-04-26T05:16:50.337393
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-26T05:16:50.337393
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding systems used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article explores techniques developed at [[Anthropic]] for improving [[agentic coding]] performance through multi-agent systems, context management, and structured evaluation frameworks. Key innovations include applying [[Generative Adversarial Networks|GAN]]-inspired generator-evaluator patterns to both frontend design and full-stack software development.

---

## Overview

Harness design is critical for achieving high performance in frontier [[agentic AI]] applications. Rather than relying on single-pass model outputs, effective harnesses decompose complex tasks into structured workflows with specialized agent roles, persistent evaluation mechanisms, and strategic context management.

This approach emerged from work at [[Anthropic]] on two interconnected challenges:
- Producing high-quality [[frontend design]] outputs from AI models
- Building complete applications autonomously over extended sessions

The resulting techniques proved transferable across subjective domains (design) and objective domains (software engineering), suggesting broader principles applicable to diverse long-running tasks.

---

## The Problem: Why Naive Implementations Fall Short

### Context Window Limitations

[[Large language models]] struggle with lengthy tasks as [[context window|context windows]] fill. Two specific failure modes emerge:

1. **Loss of Coherence**: As conversation history grows, models lose track of earlier decisions and constraints, leading to inconsistent implementations.

2. **Context Anxiety**: Some models (particularly [[Claude Sonnet 4.5]]) exhibit behavior where they begin prematurely wrapping up work as they approach perceived context limits, even when substantial work remains.

**Solutions Compared**:
- **Compaction**: Summarizing earlier conversation in place allows the same agent to continue on shortened history. Preserves continuity but doesn't address context anxiety.
- **Context Resets**: Clearing the context window entirely and starting a fresh agent with structured handoff artifacts. Provides a clean slate but adds orchestration complexity and token overhead.

For Claude Sonnet 4.5, context resets proved essential. With [[Claude Opus 4.6]], improved capabilities reduced the necessity of this pattern.

### Self-Evaluation Bias

[[AI agents]] exhibit systematic bias when evaluating their own work:
- Agents confidently praise mediocre outputs
- Problem is especially pronounced for subjective tasks (e.g., design) lacking binary verification
- Even on objective tasks with verifiable outcomes, agents demonstrate poor judgment while executing work

**Key Finding**: Separating the agent producing work from the agent evaluating it creates a strong lever for improvement. While external evaluators remain somewhat generous toward [[language model]]-generated outputs, tuning a standalone evaluator to be skeptical proves far more tractable than making a generator self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

### The Core Insight

Aesthetic quality cannot be fully reduced to numeric scores, yet can be improved through grading criteria encoding design principles and preferences. The question "Is this design beautiful?" is difficult to answer consistently, but "Does this follow our design principles?" provides concrete grading targets.

### Evaluation Criteria

Four grading criteria were developed to guide both generator and evaluator agents:

1. **Design Quality**: Does the design feel like a coherent whole rather than disconnected parts? Strong work combines colors, typography, layout, and imagery to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and defaults. Human designers should recognize deliberate creative choices; unmodified stock components and telltale [[AI generation]] patterns (e.g., purple gradients over white cards) fail this criterion.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity check; most reasonable implementations score well by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

**Weighting Strategy**: Design quality and originality were weighted more heavily than craft and functionality, since Claude naturally excels at the latter two. This weighting pushed the model toward aesthetic risk-taking and away from generic "[[AI slop]]" patterns.

### Implementation and Results

The feedback loop was built on the [[Claude Agent SDK]], with:
- **Generator agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator agent**: Used [[Playwright]] [[MCP]] to interact with live pages, screenshot, and score against criteria before providing detailed critique
- **Iteration cycle**: 5-15 iterations per generation, with each cycle pushing toward more distinctive designs

**Key Observations**:
- Evaluator assessments improved over iterations before plateauing
- Improvement patterns were non-linear; later iterations were generally better but not always preferred individually
- Wording in criteria steered outputs in unanticipated ways (e.g., "museum quality" language pushed designs toward specific visual convergence)
- First iteration outputs were noticeably better than baseline with no prompting, suggesting criteria language itself shaped model behavior
- Notable example: A Dutch art museum website evolved from conventional dark theme to creative 3D spatial experience with CSS perspective rendering and gallery room navigation

---

## Full-Stack Application Development

### Three-Agent Architecture

Building on earlier [[long-running agent harness]] work, a three-agent system was designed to address specific gaps:

#### Planner Agent

**Purpose**: Automate specification from simple user prompts

**Responsibilities**:
- Expands 1-4 sentence prompts into full product specifications
- Ambitious about scope, focused on product context and high-level technical design
- Avoids granular technical details that could cascade errors downstream
- Identifies opportunities to weave [[AI features]] into product specs
- Leverages [[frontend design skill]] to create visual design language for specs

**Rationale**: Detailed upfront specs prevent downstream errors; high-level specs allow agents to solve problems as they work.

#### Generator Agent

**Purpose**: Implement features iteratively

**Responsibilities**:
- Works in [[sprint|sprints]], picking one feature at a time from specification
- Implements using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint
- Uses [[git]] for version control
- Negotiates sprint contracts with evaluator before implementation

**Sprint Contract**: Bridge between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews proposal to ensure correct work is being built
- Agents iterate until agreement reached
- Communication via files, allowing asynchronous handoff

#### Evaluator Agent

**Purpose**: Quality assurance through active testing

**Responsibilities**:
- Uses [[Playwright]] [[MCP]] to click through running applications like users would
- Tests UI features, API endpoints, and database states
- Grades each sprint against bugs found and criteria covering:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard threshold; failure on any criterion requires generator iteration
- Provides detailed feedback on what went wrong

**Tuning Requirements**: Evaluators required significant prompt engineering:
- Out-of-the-box, Claude is a poor QA agent
- Early runs showed evaluators identifying issues then talking themselves into approval
- Superficial testing allowed subtle bugs to slip through
- Multiple tuning iterations needed to align evaluator judgment with desired standards
- Even after tuning, limitations remained: layout issues, unintuitive interactions, undiscovered deeply-nested bugs

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Comparison Results**:

| Harness Type | Duration | Cost |
|---|---|---|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hr | $200 |

**Solo Agent Output Issues**:
- Layout wasted space with fixed-height panels
- Rigid workflow without UI guidance
- Central gameplay feature broken: entities appeared but didn't respond to input
- Entity-runtime wiring broken with no surface indication

**Full Harness Output Advantages**:
- Polished interface with sensible panel sizing
- Consistent visual identity tracking design spec
- Richer sprite editor with cleaner tool palettes and better controls
- Built-in [[Claude]] integration for generating game components
- Functional gameplay with working physics
- 16-feature specification across 10 sprints including animation systems, behavior templates, sound, AI-assisted generation, and shareable exports

**Remaining Gaps**: Workflow still didn't clarify sprite/entity creation prerequisites; some physics edge cases (character overlapping platforms); limitations in level design preventing progression.

### Harness Evolution and Simplification

As [[Claude Opus 4.6]] released with improved capabilities, the harness was re