---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-07-01T06:37:39.170408
raw_file_updated: 2026-07-01T06:37:39.170408
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-07-01T06:37:39.170408
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to perform complex, long-running tasks effectively. This article explores techniques developed by [[Anthropic]] for improving [[agentic coding]] through multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs), with applications to both [[frontend design]] and [[full-stack application development]].

---

## Introduction

Long-running autonomous software engineering tasks present unique challenges for [[large language models]]. While naive implementations of [[AI agents]] can handle simple coding tasks, they struggle with complexity, lose coherence over extended sessions, and exhibit poor self-evaluation capabilities. Harness design addresses these limitations through specialized architectural patterns that decompose work, provide external feedback loops, and manage [[context windows]] effectively.

This work, conducted by Prithvi Rajasekaran at [[Anthropic Labs]], demonstrates that a well-designed harness can produce significantly higher-quality applications than single-agent approaches, though at increased computational cost. The techniques are generalizable across different domains, from subjective design tasks to verifiable software engineering.

---

## Core Problems with Naive Implementations

### Context Management Issues

Long-running tasks present two context-related challenges:

1. **Context Window Exhaustion**: As conversations grow longer, models lose coherence and begin to lose track of earlier context.

2. **Context Anxiety**: Certain models (notably [[Claude Sonnet 4.5]]) exhibit a tendency to wrap up work prematurely as they approach their perceived [[context limit]], even when more work remains.

Two approaches exist to address these issues:

- **Compaction**: Summarizing earlier conversation history in place, allowing the same agent to continue with shortened context
- **Context Resets**: Completely clearing the context window and starting fresh with a structured handoff containing essential state

While compaction preserves continuity, it doesn't fully resolve context anxiety. Context resets provide a clean slate but introduce orchestration complexity and token overhead. Testing with Claude Sonnet 4.5 demonstrated that context resets were necessary for strong long-task performance.

### Self-Evaluation Limitations

When asked to evaluate their own work, [[AI agents]] exhibit systematic bias toward positive assessment, even when output quality is objectively mediocre. This problem is especially pronounced for:

- **Subjective tasks** (e.g., [[frontend design]]) where there is no binary correctness criterion
- **Complex tasks** where agents may miss subtle bugs or design flaws

The solution is to **separate the evaluating agent from the generating agent**, creating an external feedback mechanism that is more tractable to tune toward appropriate skepticism.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically produces frontend designs that are technically functional but visually unremarkable—safe, predictable layouts lacking distinctive character or originality.

### The Approach: Generator-Evaluator Architecture

Inspired by [[Generative Adversarial Networks]] (GANs), a two-agent system was designed:

1. **Generator Agent**: Creates HTML/CSS/JavaScript interfaces based on user prompts
2. **Evaluator Agent**: Grades designs and provides detailed feedback for iteration

### Grading Criteria

To make subjective design quality measurable, four explicit criteria were established:

| Criterion | Definition | Weight |
|-----------|-----------|--------|
| **Design Quality** | Does the design feel coherent? Do colors, typography, layout, and imagery combine to create distinct mood and identity? | High |
| **Originality** | Evidence of custom decisions vs. template layouts and AI-generated patterns? | High |
| **Craft** | Technical execution: typography hierarchy, spacing, color harmony, contrast ratios | Medium |
| **Functionality** | Usability independent of aesthetics. Can users understand and complete tasks? | Medium |

The weighting deliberately emphasized design and originality—areas where Claude struggled—while de-emphasizing craft and functionality, where the model already performed well by default.

### Implementation Details

- The evaluator was given access to the [[Playwright MCP]], allowing it to interact with live pages directly
- The generator was instructed to make strategic decisions: refine current direction if scores improved, or pivot to different aesthetics if not working
- Typical runs involved 5-15 iterations per generation, with full runs lasting up to 4 hours
- Few-shot examples with detailed score breakdowns calibrated the evaluator's judgment

### Results and Observations

- **Iterative improvement**: Evaluator assessments improved over iterations before plateauing
- **Non-linear progress**: Later implementations were generally better, but individual middle iterations were sometimes preferable
- **Increased complexity**: Generator reached for more ambitious solutions in response to feedback
- **Prompt influence**: Wording of criteria (e.g., "museum quality") steered outputs toward specific visual convergence
- **Creative leaps**: Notable example: a museum website initially developed as a traditional dark-themed site was reimagined on iteration 10 as a 3D spatial experience with CSS perspective and gallery navigation

---

## Full-Stack Coding: Three-Agent Architecture

### Architecture Overview

Building on lessons from frontend design and earlier [[long-running agent]] work, a three-agent system was developed for autonomous full-stack application development:

#### 1. Planner Agent

**Purpose**: Expand simple user prompts into comprehensive product specifications

**Key characteristics**:
- Takes 1-4 sentence prompts and expands to full specs
- Deliberately ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation details
- Identifies opportunities to weave [[AI features]] into product specs
- Reads the [[frontend design skill]] to establish visual design language

**Rationale**: High-level specs prevent cascading errors from incorrect implementation details while giving downstream agents flexibility in execution.

#### 2. Generator Agent

**Purpose**: Implement features and build working applications

**Key characteristics**:
- Works in sprints, implementing one feature at a time
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Performs self-evaluation at end of each sprint
- Uses [[Git]] for version control
- Negotiates sprint contracts with evaluator before implementation

**Sprint Contract Process**:
- Bridge between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews to ensure generator is building the right thing
- Iterates until both agents agree on concrete, testable criteria

#### 3. Evaluator Agent

**Purpose**: Test applications and provide quality feedback

**Key characteristics**:
- Uses [[Playwright MCP]] to interact with running applications as a user would
- Tests UI features, API endpoints, and database states
- Grades sprints against both discovered bugs and explicit criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard thresholds; failure on any criterion fails the sprint
- Provides detailed feedback enabling generator iteration

### Communication Pattern

Agents communicate via files rather than direct conversation:
- One agent writes a file
- Next agent reads and responds within that file or creates new file
- Previous agent reads response and continues

This approach maintains work fidelity to specifications without over-specification.

---

## Case Study: Retro Video Game Maker

### Prompt

> Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode.

### Solo Agent Baseline

| Metric | Value |
|--------|-------|
| Duration | 20 minutes |
| Cost | $9 |
| Result | Broken core functionality; entities didn't respond to input |

**Issues identified**:
- Layout wasted space with fixed-height panels
- Rigid workflow with no UI guidance for proper sequence
- Game runtime broken: entity wiring non-functional
- No surface indication of errors

### Full Harness (Opus 4.5)

| Metric | Value |
|--------|-------|
| Duration | 6 hours |
| Cost | $200 |
| Cost multiplier vs. solo | 20x |

**Planner Output**: 16-feature spec across 10 sprints including:
- Core editors and play mode
- Sprite animation system
- Behavior templates
- Sound effects and music
- AI-assisted sprite generator and level designer
- Game export with shareable links

**Results**:
- Visually polished interface with consistent design language
- Functional sprite editor with cleaner tool palettes and better controls
- Working play mode where entities responded correctly to input
- Built-in Claude integration for AI-assisted game generation
- Physics had rough edges but core functionality worked

**Remaining issues**:
- Workflow clarity: not obvious that sprites/entities should be created before populating levels
- Some physics edge cases (character overlapping platforms)
- Limitations in AI's level construction (impass