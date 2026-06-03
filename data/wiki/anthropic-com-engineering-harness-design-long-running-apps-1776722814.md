---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-03T06:58:21.118500
raw_file_updated: 2026-06-03T06:58:21.118500
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-03T06:58:21.118500
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and engineering techniques used to enable [[AI agents]] to successfully complete complex, long-running tasks without human intervention. This article describes how [[Anthropic]] researchers, led by Prithvi Rajasekaran, developed a multi-agent system inspired by [[Generative Adversarial Networks]] (GANs) to improve both [[frontend design]] quality and full-stack application development. The approach separates generation from evaluation, allowing specialized agents to focus on specific aspects of task completion while providing meaningful feedback loops.

---

## Contents

1. [Overview](#overview)
2. [Limitations of Naive Approaches](#limitations-of-naive-approaches)
3. [Frontend Design Harness](#frontend-design-harness)
4. [Full-Stack Coding Architecture](#full-stack-coding-architecture)
5. [Implementation and Results](#implementation-and-results)
6. [Harness Evolution](#harness-evolution)
7. [Key Principles](#key-principles)
8. [Related Concepts](#related-concepts)

---

## Overview

### The Core Problem

[[AI models]] like [[Claude]] can produce impressive results on single-pass generation tasks, but struggle with complex, multi-step projects that require sustained coherence, quality evaluation, and iterative refinement. Traditional approaches that rely on a single agent to both generate and evaluate its own work suffer from systematic failures:

- **Context degradation**: As context windows fill during long tasks, models lose coherence and exhibit "context anxiety," prematurely wrapping up work
- **Self-evaluation bias**: Agents tend to praise their own work even when quality is mediocre, particularly on subjective tasks
- **Scope creep and incoherence**: Without structured decomposition, agents lose sight of the original specification

### The Solution: Multi-Agent Harnesses

Rather than asking a single agent to do everything, harness design distributes responsibilities across specialized agents:

- **Generator agents** focus on creating and implementing work
- **Evaluator agents** critically assess quality and identify gaps
- **Planner agents** decompose high-level requirements into actionable specifications

This separation allows each agent to be optimized for its specific role, with the evaluator tuned to be skeptical rather than lenient.

---

## Limitations of Naive Approaches

### Context Window Management

Earlier [[Anthropic]] work on [[long-running agents]] demonstrated that [[Claude Sonnet 4.5]] exhibited "context anxiety"—a tendency to prematurely conclude work as the context window fills. Two approaches exist to address this:

**Context Resets** (complete context clearing with structured handoff)
- Provides a clean slate for the next agent session
- Eliminates context anxiety but adds orchestration complexity and latency
- Necessary for Sonnet 4.5

**Context Compaction** (in-place summarization)
- Preserves continuity but doesn't eliminate context anxiety
- Less effective as a standalone solution

The introduction of [[Claude Opus 4.6]] largely eliminated context anxiety, enabling single continuous sessions without resets.

### Self-Evaluation Failure

When asked to evaluate their own work, [[AI agents]] consistently demonstrate positive bias:

- They praise mediocre outputs, particularly on subjective tasks like [[design]]
- They fail to identify bugs and usability issues in code they've written
- Their judgment is unreliable even on tasks with verifiable outcomes

**Solution**: Separate the agent doing the work from the agent judging it. While evaluator agents are still inclined toward leniency (being LLMs themselves), they can be tuned to be skeptical through careful prompting and few-shot examples.

---

## Frontend Design Harness

### The Challenge

[[Frontend design]] presents a particularly acute version of the self-evaluation problem. Without intervention, [[Claude]] gravitates toward "safe, predictable layouts that are technically functional but visually unremarkable"—what practitioners call "[[AI slop]]."

### Grading Criteria Framework

The breakthrough was converting subjective aesthetic judgments into concrete, gradable criteria:

| Criterion | Definition | Weight |
|-----------|-----------|--------|
| **Design Quality** | Coherent visual identity combining colors, typography, layout, and imagery into a distinct mood | High |
| **Originality** | Evidence of custom creative decisions rather than template layouts or unmodified components | High |
| **Craft** | Technical execution: typography hierarchy, spacing, color harmony, contrast ratios | Medium |
| **Functionality** | Usability and user task completion independent of aesthetics | Medium |

The framework explicitly penalizes generic patterns while rewarding distinctive aesthetic risk-taking.

### Generator-Evaluator Loop

**Architecture**:
1. **Generator agent** creates an HTML/CSS/JavaScript frontend based on user prompt
2. **Evaluator agent** uses [[Playwright]] MCP to interact with the live page
3. Evaluator screenshots, navigates, and carefully studies the implementation
4. Evaluator produces detailed critique against the four criteria
5. Feedback loops back to generator for next iteration
6. Process repeats 5-15 times per generation

**Key Findings**:

- Evaluator assessments improved over iterations before plateauing
- Some generations refined incrementally; others took sharp aesthetic turns
- Prompt language steered generation in unexpected ways (e.g., "museum quality" pushed designs toward specific visual convergence)
- Even first-iteration outputs exceeded baseline with no evaluator feedback
- Full runs extended 4+ hours due to real-time interaction requirements

### Notable Example: Dutch Museum Website

A prompt to create a website for a fictional Dutch art museum yielded:
- **Iterations 1-9**: Polished dark-themed landing page
- **Iteration 10**: Complete pivot to 3D spatial experience with CSS perspective, checkered floor, freely-positioned artwork, and doorway-based navigation
- Result: Creative leap beyond typical single-pass generation

---

## Full-Stack Coding Architecture

### Three-Agent System

Building on the success of the frontend harness, a three-agent architecture was developed for autonomous full-stack application development:

#### 1. Planner Agent

**Role**: Expand simple user prompts into comprehensive product specifications

**Characteristics**:
- Takes 1-4 sentence input and produces detailed multi-feature spec
- Ambitious about scope; focused on product context and high-level technical design
- Avoids over-specifying granular implementation details
- Integrates [[AI features]] into product specs (e.g., built-in Claude agents)
- Access to [[frontend design skills]] to establish visual design language

**Rationale**: Upfront planning prevents cascading errors from incorrect implementation details

#### 2. Generator Agent

**Role**: Implement features and build the application

**Characteristics**:
- Works in [[sprints]] (one feature at a time) from the spec
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint
- Uses [[Git]] for version control
- Negotiates "sprint contracts" with evaluator before implementation

**Sprint Contract Process**:
1. Generator proposes what will be built and success criteria
2. Evaluator reviews proposal to ensure correctness
3. Agents iterate until agreement reached
4. Generator builds against agreed contract
5. Work handed to evaluator for verification

**Rationale**: Bridges gap between high-level user stories and testable implementation without over-specification

#### 3. Evaluator Agent

**Role**: Quality assurance and verification

**Characteristics**:
- Uses [[Playwright]] MCP to click through running application like a user
- Tests UI features, API endpoints, and database states
- Grades sprints against criteria: product depth, functionality, visual design, code quality
- Each criterion has hard threshold; failure triggers detailed feedback
- Walks through live page, taking screenshots before scoring

**Evaluation Criteria**:
- Does the feature work as specified?
- Are there bugs or edge cases?
- Does UI match design language?
- Is code maintainable?

**Tuning Challenge**: Out-of-box, [[Claude]] is a poor QA agent. Early evaluators would:
- Identify legitimate issues then rationalize them away
- Test superficially, missing edge cases
- Approve incomplete work

Solution required multiple tuning iterations, reading logs, identifying judgment divergences, and updating prompts.

### Communication Pattern

Agents communicate via files:
- One agent writes a file with its work/analysis
- Next agent reads and responds within that file or creates new file
- Keeps work faithful to spec without over-specification

---

## Implementation and Results

### Case Study 1: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Solo Agent (Single-Pass)**:
- Duration: 20