---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-28T05:35:43.163908
raw_file_updated: 2026-04-28T05:35:43.163908
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-28T05:35:43.163908
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration frameworks used to manage long-running [[AI agent]] tasks, particularly in [[agentic coding]] applications. This article describes techniques developed at [[Anthropic]] for improving [[Claude]]'s performance on complex, extended tasks by combining [[multi-agent systems]], [[context management]], and structured evaluation loops inspired by [[Generative Adversarial Networks]] (GANs).

---

## Overview

Harness design is critical for achieving high-quality outputs in frontier [[AI engineering]] work. Traditional single-agent approaches to complex tasks often fail due to context limitations, self-evaluation bias, and loss of coherence over extended execution periods. This article presents research by Prithvi Rajasekaran from [[Anthropic Labs]] demonstrating how specialized multi-agent architectures can overcome these limitations in both [[frontend design]] and full-stack [[software engineering]] applications.

The core innovation involves separating generation from evaluation—a pattern borrowed from [[Generative Adversarial Networks]]—where a generator agent produces work while an independent evaluator agent provides critical feedback, preventing the self-evaluation bias that plagues single-agent systems.

---

## Key Problems with Naive Implementations

### Context Window Degradation

Long-running [[AI agent]] tasks suffer from two related problems as the context window fills:

1. **Loss of coherence**: Models lose track of earlier decisions and design patterns, leading to inconsistent implementations
2. **Context anxiety**: Some models (notably [[Claude Sonnet 4.5]]) exhibit premature work completion behavior as they approach perceived context limits

**Solutions considered:**
- **Compaction**: Summarizing earlier conversation turns in-place to free context space
- **Context resets**: Clearing the context window entirely and using structured handoff artifacts to transfer state to a fresh agent session

[[Claude Opus 4.5]] and later versions largely eliminated context anxiety, making context resets less essential than they were for Sonnet 4.5.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI models]] consistently exhibit positive bias—praising outputs even when quality is mediocre. This problem is particularly acute in subjective domains like [[frontend design]] where no binary correctness check exists.

**Key insight**: Separating the agent doing work from the agent evaluating it proves substantially more effective than attempting to make a single agent self-critical. An external evaluator can be tuned to be skeptical through [[prompt engineering]], whereas making a generator critical of its own output is far more difficult.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically produces technically functional but visually unremarkable designs—safe, predictable layouts that fail to demonstrate originality or distinctive aesthetic choices.

### Solution: Generator-Evaluator Architecture

The approach applies [[Generative Adversarial Networks]] principles to [[frontend design]]:

**Four grading criteria** were developed to make subjective aesthetic judgment measurable:

| Criterion | Definition |
|-----------|-----------|
| **Design quality** | Does the design feel like a coherent whole? Do colors, typography, layout, and imagery combine to create distinct mood and identity? |
| **Originality** | Evidence of custom decisions rather than template defaults? Can a human designer recognize deliberate creative choices? |
| **Craft** | Technical execution: typography hierarchy, spacing, color harmony, contrast ratios. A competence check rather than creativity check. |
| **Functionality** | Usability independent of aesthetics. Can users understand the interface and complete tasks? |

Design quality and originality were weighted more heavily, as [[Claude]] already performed well on craft and functionality by default.

### Implementation Details

- **Generator agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator agent**: Used [[Playwright MCP]] to interact with live pages, taking screenshots and navigating before scoring
- **Feedback loop**: 5-15 iterations per generation, with evaluator feedback driving refinement
- **Calibration**: Few-shot examples with detailed score breakdowns ensured evaluator judgment aligned with human preferences

### Results

The iterative refinement process produced noticeable improvements in design distinctiveness and polish. In one notable example, the generator initially produced a conventional dark-themed museum website, then on the tenth iteration completely reimagined the site as a 3D spatial experience with CSS perspective, free-form artwork positioning, and doorway-based navigation—a creative leap not achieved in baseline single-pass generation.

---

## Full-Stack Coding: Three-Agent Architecture

### Architecture Overview

Building on earlier work with [[long-running coding agents]], a three-agent system addressed specific gaps in autonomous software engineering:

#### Planner Agent

**Purpose**: Expand brief user prompts into detailed product specifications

**Responsibilities**:
- Takes 1-4 sentence user prompts and expands to full product spec
- Maintains ambitious scope while focusing on product context and high-level technical design
- Avoids over-specifying implementation details that could cascade errors downstream
- Weaves [[AI features]] into product specs where appropriate
- Reads and applies [[frontend design skills]] to create visual design language

**Key insight**: Constraining agents on deliverables rather than implementation paths allows downstream agents to find optimal solutions.

#### Generator Agent

**Purpose**: Implement features according to the product specification

**Responsibilities**:
- Works in [[sprint]]-based iterations (in v1 harness)
- Picks up one feature at a time from the spec
- Implements using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Performs self-evaluation at end of each sprint
- Maintains version control with [[Git]]

**Sprint contract negotiation**: Before implementation, generator and evaluator agree on:
- What "done" looks like for that feature chunk
- How success will be verified
- Testable acceptance criteria

This bridges the gap between high-level user stories and testable implementation without over-specification.

#### Evaluator Agent

**Purpose**: Verify implementation against specification and identify bugs

**Responsibilities**:
- Uses [[Playwright MCP]] to interact with running applications as a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against criteria adapted from frontend work:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Identifies specific, actionable bugs with code locations
- Provides detailed feedback on failures

**Tuning challenge**: Out-of-box [[Claude]] performs poorly as a QA agent, identifying issues then talking itself into approving mediocre work. Effective evaluation required multiple iteration cycles reading evaluator logs and updating prompts to address judgment gaps.

### Communication Pattern

Agents communicate via files:
- One agent writes a file
- Next agent reads and responds in-place or with new file
- Maintains clear handoff artifacts
- Enables asynchronous coordination without real-time orchestration

### Initial Results: Retro Game Maker

**Test prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Approach | Duration | Cost |
|----------|----------|------|
| Single agent | 20 min | $9 |
| Full harness | 6 hours | $200 |

**Comparison**:
- **Solo output**: Technically functional but with broken game mechanics, rigid workflow, poor layout, and non-responsive entities
- **Harness output**: Polished interface, full-featured editors, working gameplay, integrated [[AI features]] for sprite and level generation, proper visual design language

The 20x cost increase yielded dramatically superior output quality in both functionality and usability.

---

## Iterating and Simplifying the Harness

### Design Principle

Every component in a harness encodes an assumption about what the model cannot do alone. These assumptions should be stress-tested regularly because:
1. Assumptions may be incorrect
2. Assumptions become stale as models improve

As stated in [[Building Effective Agents]]: "Find the simplest solution possible, and only increase complexity when needed."

### Removing Sprint Structure

With the release of [[Claude Opus 4.6]], which demonstrated:
- Better planning capability
- Sustained agentic task performance
- Improved code review and debugging
- Better long-context retrieval

The sprint decomposition became unnecessary. [[Opus 4.6]] could handle coherent multi-hour builds without intermediate checkpoints.

**Changes made**:
- Removed sprint-based iteration structure
- Kept planner (prevents under-scoping) and evaluator (catches edge cases)
- Moved evaluator to single pass at end rather than per-sprint grading
- Added prompting improvements for [[AI feature]] integration

### Updated Results: Digital Audio Workstation (DAW)

**Test prompt**: "Build a fully featured DAW in the browser using the Web Audio API."

| Phase | Duration |