---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-11T06:53:31.452131
raw_file_updated: 2026-06-11T06:53:31.452131
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-11T06:53:31.452131
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to effectively complete complex, long-running tasks. This article documents Anthropic's research into multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs), which employ separate generator and evaluator agents to improve output quality across both subjective tasks like [[frontend design]] and objective tasks like [[full-stack application development]].

---

## Overview

Harness design is a critical discipline in [[agentic AI systems]], particularly when pushing models like [[Claude]] to handle extended development tasks that exceed what single-agent approaches can accomplish. Rather than relying on a model's baseline capabilities, effective harness design decomposes complex problems into specialized agent roles, uses structured handoffs between sessions, and implements feedback loops that drive iterative improvement.

This approach emerged from research by Prithvi Rajasekaran at [[Anthropic Labs]], who discovered that naive long-running agent implementations consistently hit performance ceilings despite [[prompt engineering]] improvements. The breakthrough came from adapting principles from adversarial training: separating the agent that generates work from the agent that evaluates it, enabling more reliable quality assessment and iterative refinement.

---

## The Problem: Why Naive Implementations Fail

### Context Window Limitations

Long-running tasks expose two critical failure modes in [[large language models]]:

1. **Loss of Coherence**: As the [[context window]] fills during extended tasks, models tend to lose track of earlier decisions and constraints, leading to inconsistent implementations.

2. **Context Anxiety**: Some models, notably [[Claude Sonnet 4.5]], exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when substantial work remains.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] tend to respond with unwarranted confidence and positivity, even when quality is objectively mediocre. This is particularly problematic for:

- **Subjective tasks** (e.g., [[design]], where there is no binary correctness check)
- **Complex implementations** (where subtle bugs may not be immediately apparent)

The solution is not to make the generator more self-critical, but to separate evaluation into a dedicated agent role that can be specifically tuned for skepticism and rigor.

---

## Solution: The Multi-Agent Architecture

### Core Principles

The harness design approach rests on three key insights:

1. **Decomposition**: Breaking complex tasks into tractable chunks that individual agents can manage coherently
2. **Structured Handoffs**: Using files and explicit contracts to transfer context and state between agents
3. **Specialized Roles**: Assigning each agent a specific responsibility, allowing for targeted prompt engineering

### Context Reset vs. Compaction

Earlier research explored two approaches to managing context growth:

- **Compaction**: Summarizing earlier conversation in place so the same agent continues on shortened history
- **Context Reset**: Clearing the context window entirely and starting a fresh agent with structured state transfer

Context resets proved superior for models exhibiting context anxiety, as they provide a clean slate. However, they introduce orchestration complexity and token overhead. With newer models like [[Claude Opus 4.6]], which largely eliminated context anxiety, continuous sessions with automatic compaction became viable.

---

## Application 1: Frontend Design

### The Challenge

Without intervention, [[Claude]] gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—a phenomenon often called "[[AI slop]]."

### The Solution: Generator-Evaluator Loop

A two-agent system inspired by [[GANs]]:

**Generator Agent**: Creates HTML/CSS/JavaScript frontends based on user prompts

**Evaluator Agent**: 
- Uses [[Playwright MCP]] to interact with the live page
- Takes screenshots and studies implementations
- Scores work against explicit criteria
- Provides detailed critiques for iteration

### Grading Criteria

Rather than subjective judgments, the evaluator grades against concrete design principles:

| Criterion | Definition | Weight |
|-----------|-----------|--------|
| **Design Quality** | Does the design feel coherent? Do colors, typography, layout, and imagery combine into a distinct mood and identity? | High |
| **Originality** | Evidence of custom decisions vs. template layouts and library defaults? Avoids telltale "AI slop" patterns. | High |
| **Craft** | Technical execution: typography hierarchy, spacing, color harmony, contrast ratios | Medium |
| **Functionality** | Usability independent of aesthetics: can users understand, find actions, and complete tasks? | Medium |

### Results

- **5-15 iterations** per generation, with each cycle pushing toward more distinctive outputs
- **4-hour runs** for complete design explorations
- **Wording effects**: Phrases like "museum quality" subtly steered outputs toward particular visual convergence
- **Creative leaps**: In one case, the generator spontaneously reimagined a museum website as a 3D spatial experience with CSS perspective rendering—a creative breakthrough not seen in single-pass generation

### Key Insight

The criteria themselves act as a steering mechanism. Even on the first iteration, outputs were noticeably better than baseline, suggesting that the language and principles in the prompts directly shape model behavior before any evaluator feedback occurs.

---

## Application 2: Full-Stack Application Development

### The Three-Agent Architecture

Building on the frontend design success, a three-agent system was developed for complete application development:

#### Planner Agent

**Purpose**: Expand brief user prompts into comprehensive product specifications

**Approach**:
- Takes 1-4 sentence user prompt
- Generates 16+ feature specs across multiple sprints
- Emphasizes scope and high-level technical design over implementation details
- Avoids cascading errors from over-specified technical requirements
- Weaves [[AI integration]] opportunities into specifications

**Rationale**: Prevents errors in detailed specs from propagating downstream; lets implementation agents determine technical paths

#### Generator Agent

**Purpose**: Implement features iteratively using modern web stacks

**Approach**:
- Implements in sprints (one feature at a time)
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Maintains code with [[Git]] version control
- Self-evaluates work before handoff
- Negotiates sprint contracts with evaluator before coding

**Sprint Contract**: 
- Bridge between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews proposal to ensure generator is building the right thing
- Both agents iterate until agreement

#### Evaluator Agent

**Purpose**: Verify implementation quality through testing and QA

**Approach**:
- Uses [[Playwright MCP]] to click through running application
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and explicit criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard thresholds; failure requires generator iteration

**Communication Protocol**: Agents communicate via files, creating an asynchronous handoff system that maintains context across iterations

### Case Study: Retro Game Maker

**Prompt**: _Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode._

#### Solo Agent Approach
- **Duration**: 20 minutes
- **Cost**: $9
- **Result**: Broken core functionality; entities appeared but didn't respond to input; rigid workflow; wasted screen space

#### Full Harness Approach
- **Duration**: 6 hours
- **Cost**: $200
- **Result**: 
  - 16-feature spec across 10 sprints
  - Sprite animation system, behavior templates, sound effects, music
  - AI-assisted sprite generator and level designer
  - Game export with shareable links
  - Working gameplay with functional physics
  - Integrated [[Claude]] agent for game generation

**Quality Difference**: The 20x cost increase correlated with immediately apparent improvements in polish, coherence, and functionality. The solo run's central feature simply didn't work; the harness run produced a complete, playable application.

### Evaluator Effectiveness

The evaluator caught specific, actionable bugs:

| Contract Criterion | Evaluator Finding |
|-------------------|------------------|
| Rectangle fill tool allows click-drag | **FAIL** — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered on mouseUp |
| User can select and delete entity spawn points | **FAIL** — Delete handler requires both `selection` and `selectedEntityId`, but clicking only sets `selectedEntityId` |
| User can reorder animation frames via API | **FAIL** — Route ordering issue causes FastAPI to parse "reorder" as integer frame_id |

Early evaluator iterations suffered from poor judgment, praising mediocre