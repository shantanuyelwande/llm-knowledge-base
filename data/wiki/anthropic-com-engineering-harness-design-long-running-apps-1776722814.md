---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-08T06:49:41.838332
raw_file_updated: 2026-06-08T06:49:41.838332
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-08T06:49:41.838332
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design refers to the architectural patterns and scaffolding used to enable [[AI agents]] to perform complex, multi-hour autonomous tasks like [[full-stack application development]]. This article documents Anthropic's approach to building effective harnesses by separating concerns into specialized agent roles—planner, generator, and evaluator—inspired by [[Generative Adversarial Networks]] (GANs). The key innovation is using external evaluation rather than self-evaluation to provide reliable feedback that drives iterative improvement in both [[frontend design]] and code quality.

---

## Overview

Harness design represents a critical frontier in [[agentic AI]] engineering. While [[Claude]] and other large language models can produce impressive results in single-pass generations, they struggle with sustained coherence and quality judgment over long-running tasks. This article explores how specialized harness architectures can overcome these limitations by decomposing complex problems into tractable chunks with clear feedback loops.

The work documented here addresses two persistent challenges:

1. **Loss of coherence over extended tasks** - Models lose focus as [[context windows]] fill with information
2. **Poor self-evaluation** - Models tend to overestimate the quality of their own work, particularly on subjective tasks

## Core Problems with Naive Implementations

### Context Management Issues

[[Long-running agents]] face a fundamental challenge: as context windows fill, model performance degrades. Two related phenomena occur:

**Context Anxiety**: Models begin prematurely concluding their work as they approach perceived context limits, even when substantial work remains.

**Context Resets vs. Compaction**: 
- [[Compaction]] summarizes earlier conversation history in-place, allowing the same agent to continue on a shortened history
- [[Context resets]] clear the context window entirely and start a fresh agent with a structured handoff artifact containing the previous agent's state

While compaction preserves continuity, it doesn't eliminate context anxiety. Context resets provide a clean slate but add orchestration complexity and token overhead. Testing with [[Claude Sonnet 4.5]] showed context anxiety was severe enough that compaction alone proved insufficient—context resets became essential to harness design.

### Self-Evaluation Failures

Models exhibit systematic bias when evaluating their own work:

- **Subjective domains** (like [[frontend design]]): Agents confidently praise mediocre outputs, gravitating toward "safe, predictable layouts that are technically functional but visually unremarkable"
- **Objective domains** (like software testing): Even with verifiable outcomes, agents show poor judgment that impedes performance, missing bugs and logical errors

**Solution**: Separating the agent doing the work from the agent evaluating it proves to be a strong lever. While evaluator agents still exhibit some leniency toward [[LLM]]-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

## Frontend Design: Quantifying Subjective Quality

### The Challenge

Getting [[Claude]] to produce distinctive, high-quality [[frontend design|frontend designs]] proved difficult. Without intervention, the model produced technically correct but visually unremarkable interfaces.

### Design Criteria Framework

To make subjective aesthetic judgments gradable, four evaluation criteria were established:

**Design Quality**: Does the design feel like a coherent whole? Colors, typography, layout, imagery, and other details should combine to create a distinct mood and identity rather than appearing as disconnected parts.

**Originality**: Is there evidence of custom creative decisions, or just template layouts and library defaults? Telltale signs of generic [[AI]]-generated patterns (like purple gradients over white cards) indicate failure in this criterion.

**Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check—most reasonable implementations succeed here by default.

**Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

Emphasis was placed on **design quality and originality** over craft and functionality, since [[Claude]] already excelled at the latter two. The criteria explicitly penalized generic "[[AI slop]]" patterns.

### Generator-Evaluator Loop Architecture

The implementation used:

1. **Generator agent**: Created HTML/CSS/JavaScript frontends based on user prompts
2. **Evaluator agent**: Used [[Playwright MCP]] to interact with live pages, take screenshots, and grade each criterion with detailed critique
3. **Feedback loop**: 5-15 iterations per generation, with the generator refining or pivoting aesthetic direction based on evaluator feedback

**Key findings**:
- The evaluator's assessments improved over iterations before plateauing
- Wording in criteria steered generator output in anticipated and unanticipated ways (e.g., "museum quality" pushed toward specific visual convergence)
- Later implementations tended to be better overall, though not always linearly—sometimes middle iterations were preferable
- Even first-iteration outputs were noticeably better than baseline, suggesting the criteria themselves steered the model away from generic defaults

**Example**: A website for a fictional Dutch art museum initially produced a clean, dark-themed landing page. On the tenth iteration, the generator scrapped this entirely and reimagined the site as a 3D spatial experience with CSS perspective, creating doorway-based navigation between gallery rooms—a creative leap not seen in single-pass generation.

## Full-Stack Application Development

### Three-Agent Architecture

Building on insights from frontend design work, a three-agent system was created for autonomous [[full-stack application development]]:

#### Planner Agent

**Role**: Converts simple user prompts (1-4 sentences) into comprehensive product specifications.

**Characteristics**:
- Ambitious about scope
- Focuses on product context and high-level technical design rather than granular implementation details
- Identifies opportunities to weave [[AI features]] into product specs
- Avoids over-specification that could cascade errors downstream

**Rationale**: Detailed technical specifications created by the planner that prove incorrect can cause cascading errors in implementation. Better to constrain deliverables and let agents figure out implementation paths.

#### Generator Agent

**Role**: Implements application features in sprints, working with specified tech stacks (React, Vite, FastAPI, SQLite/PostgreSQL).

**Characteristics**:
- Works one feature at a time
- Implements with version control ([[Git]])
- Self-evaluates work at end of each sprint
- Negotiates "sprint contracts" with the evaluator before implementation

**Sprint Contract Mechanism**: Before each sprint, generator and evaluator agree on:
- What specific features will be built
- How success will be verified
- Testable criteria for completion

This bridges the gap between high-level user stories and testable implementation without over-specifying early.

#### Evaluator Agent

**Role**: Quality assurance through active testing and verification against sprint contracts.

**Capabilities**:
- Uses [[Playwright MCP]] to click through running applications like a user
- Tests UI features, [[API]] endpoints, and database states
- Grades sprints against both discovered bugs and explicit criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Provides detailed feedback when sprints fail any criterion

**Development**: Out-of-the-box, [[Claude]] proved to be a poor QA agent, identifying issues then talking itself into approving mediocre work. Significant tuning was required:
- Reading evaluator logs and comparing against human judgment
- Updating prompts to address divergences
- Iterating multiple rounds before achieving acceptable grading standards

### Case Study: Retro Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Comparison Results**:

| Harness Type | Duration | Cost |
|---|---|---|
| Solo (single agent) | 20 min | $9 |
| Full harness | 6 hr | $200 |

**Solo Run Issues**:
- Layout wasted space with fixed-height panels
- Workflow was rigid and unintuitive
- Core gameplay was broken—entities appeared on screen but didn't respond to input
- Entity-to-runtime wiring was disconnected with no error indication

**Full Harness Results**:
- Polished, coherent interface with consistent visual identity
- Full-featured sprite editor with cleaner tools and better controls
- Functional gameplay—entities responded to input and physics worked
- Integrated [[Claude]] features allowing game generation through natural language prompting
- 16-feature spec across 10 sprints, including sprite animation, behavior templates, sound effects, AI-assisted generation, and shareable exports

The quality difference was immediately apparent despite 20x higher cost.

### Iterating Toward Simplicity

As [[Claude Opus 4.6]] became available with improvements in planning, long-context reasoning, and debugging, the harness was re-evaluated. The principle applied: "find the simplest solution possible, and only increase complexity when needed