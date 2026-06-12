---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-12T06:46:28.391597
raw_file_updated: 2026-06-12T06:46:28.391597
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-12T06:46:28.391597
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to complete complex, long-running tasks effectively. This article describes techniques developed at [[Anthropic]] for building multi-agent systems that can generate high-quality [[frontend design|frontend designs]] and full-stack applications over extended autonomous development sessions. Key innovations include [[generator-evaluator architecture|generator-evaluator patterns]] inspired by [[Generative Adversarial Networks]], [[context reset]] strategies, and [[sprint-based decomposition]] for managing scope and coherence.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Problems in Long-Running Tasks](#core-problems-in-long-running-tasks)
3. [Frontend Design Application](#frontend-design-application)
4. [Full-Stack Coding Architecture](#full-stack-coding-architecture)
5. [Harness Iteration and Optimization](#harness-iteration-and-optimization)
6. [Key Takeaways](#key-takeaways)
7. [Related Concepts](#related-concepts)

---

## Overview

Harness design emerged as a critical approach to pushing [[Claude]] and other large language models beyond their baseline capabilities on complex, sustained tasks. Rather than relying solely on model improvements, effective harness design uses orchestration, multi-agent structures, and specialized feedback loops to achieve results that would be impossible with a single-pass generation.

The work described here addresses two interconnected challenges:

1. **Subjective quality tasks** (frontend design) where aesthetic judgment is required
2. **Verifiable correctness tasks** (software engineering) where functional accuracy is essential

Both domains benefit from similar architectural patterns, suggesting that harness design principles are broadly applicable across different problem spaces.

---

## Core Problems in Long-Running Tasks

### Context Window Limitations

As [[context window|context windows]] fill during extended tasks, [[AI agents]] face two primary challenges:

- **Context anxiety**: Models like [[Claude Sonnet]] 4.5 exhibit a tendency to wrap up work prematurely as they approach their perceived context limit, reducing output quality
- **Coherence loss**: Extended conversations can lead to the model losing track of earlier decisions and requirements

### Solutions: Context Reset vs. Compaction

**Context compaction** summarizes earlier conversation history in place, allowing the same agent to continue with a shortened history. While this preserves some continuity, it doesn't address context anxiety.

**Context reset** clears the context window entirely and starts a fresh agent session, using [[structured artifacts]] to hand off state and next steps. This provides a clean slate and eliminates context anxiety, but adds orchestration complexity, token overhead, and latency.

For [[Claude Opus]] 4.5 and earlier models, context resets proved essential. [[Claude Opus]] 4.6 largely eliminated context anxiety, enabling continuous sessions without resets.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently exhibit positive bias, confidently praising mediocre outputs. This problem is particularly acute in subjective domains like design, where there is no binary verification mechanism.

**Key insight**: Separating the agent doing the work from the agent evaluating it dramatically improves judgment quality. While evaluators remain inherently lenient toward LLM-generated content, they can be tuned through prompting to be appropriately skeptical, and the generator benefits from concrete external feedback to iterate against.

---

## Frontend Design Application

### Design Criteria Framework

To make subjective aesthetic judgments gradable, the research developed four explicit design criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, imagery, and details into a distinct mood and identity, avoiding generic aesthetics.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Penalizes telltale signs of AI generation (e.g., purple gradients over white cards) and rewards deliberate creative choices.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. Competence check rather than creativity check—most reasonable implementations succeed here by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The framework weighted design quality and originality more heavily, as [[Claude]] naturally excels at craft and functionality but tends toward bland, generic outputs without explicit guidance toward aesthetic risk-taking.

### Generator-Evaluator Loop

The frontend design harness implemented a feedback loop using the [[Claude Agent SDK]]:

1. **Generator agent** creates HTML/CSS/JavaScript frontends based on user prompts
2. **Evaluator agent** uses [[Playwright MCP]] to interact with the live page, screenshotting and studying the implementation before scoring each criterion
3. Evaluator provides detailed critique based on the four criteria
4. Generator receives feedback and decides whether to refine the current direction or pivot to a different aesthetic
5. Loop repeats for 5-15 iterations per generation

#### Key Findings

- Evaluator assessments improved over iterations before plateauing, with visible headroom remaining
- Wording of criteria steered generators in unanticipated ways (e.g., "museum quality" pushed toward visual convergence)
- First-iteration outputs were noticeably better than baseline, suggesting criteria themselves guide the model away from generic defaults
- Later iterations weren't always better than intermediate ones; implementation complexity increased across rounds
- Creative leaps occurred mid-iteration (e.g., reimagining a museum website as a 3D spatial experience in CSS)

---

## Full-Stack Coding Architecture

### Three-Agent System

Building on earlier long-running harness work, the full-stack architecture employed three specialized agents:

#### Planner Agent

**Role**: Expand simple user prompts into comprehensive product specifications

- Takes 1-4 sentence user prompts and produces detailed feature lists and technical direction
- Emphasizes ambitious scope while focusing on product context and high-level design rather than granular implementation details
- Avoids over-specifying implementation details that could cascade errors downstream
- Identifies opportunities to weave [[AI agent]] features into product specs
- Leverages [[frontend design skill]] to establish visual design language

#### Generator Agent

**Role**: Implement features in the agreed-upon [[technology stack]]

- Works in [[sprint-based decomposition|sprints]], implementing one feature at a time
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at sprint end before handing off to [[QA]]
- Uses [[Git]] for version control
- Negotiates sprint contracts with the evaluator before implementation

#### Evaluator Agent

**Role**: Verify implementation against specifications and quality standards

- Uses [[Playwright MCP]] to click through running applications like a user would
- Tests UI features, [[API]] endpoints, and database states
- Grades each sprint against:
  - Bugs discovered during testing
  - Criteria adapted from frontend work (product depth, functionality, visual design, code quality)
- Each criterion has hard thresholds; failure in any criterion fails the sprint
- Negotiates sprint contracts with the generator before work begins
- Provides detailed feedback for generator iteration

### Sprint Contract System

Before each sprint, generator and evaluator negotiate a **sprint contract** specifying:

- What will be built
- How success will be verified
- Testable implementation criteria

This bridges the gap between high-level user stories and verifiable implementations without over-specifying technical details prematurely. Communication occurs via files: agents write and read files sequentially, maintaining clear handoffs.

### Comparative Results

**Retro Video Game Maker** (two approaches):

| Metric | Solo Agent | Full Harness |
|--------|-----------|--------------|
| **Duration** | 20 minutes | 6 hours |
| **Cost** | $9 | $200 |
| **Feature Completeness** | Limited | Comprehensive (16 features across 10 sprints) |
| **Core Functionality** | Broken (non-functional game) | Working (playable game with physics) |
| **Visual Polish** | Clunky, inconsistent | Professional appearance with design language |
| **AI Integration** | None | Built-in Claude integration for generation |

The solo agent produced an interface that appeared functional but had fundamental bugs preventing core gameplay. The full harness produced a substantially more complete application with functional game mechanics, though with refinable edge cases.

### QA Effectiveness

The evaluator agent successfully identified specific, actionable issues:

| Contract Criterion | Evaluator Finding |
|-------------------|------------------|
| Rectangle fill tool allows click-drag to fill area | **FAIL** — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered properly on mouseUp |
| User can select and delete entity spawn points | **FAIL** — Delete key handler requires both `selection` and `