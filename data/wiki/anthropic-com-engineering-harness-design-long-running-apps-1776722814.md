---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-04T05:39:51.492089
raw_file_updated: 2026-05-04T05:39:51.492089
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-04T05:39:51.492089
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical approach for improving [[AI agents|agentic]] system performance on complex, long-running tasks. This article describes techniques developed at [[Anthropic]] for building multi-agent architectures that can reliably generate high-quality [[frontend design|frontend designs]] and complete full-stack applications over extended autonomous coding sessions. The core innovation involves applying [[Generative Adversarial Networks|GAN]]-inspired patterns with separate generator and evaluator agents, combined with strategic task decomposition and structured context management.

---

## Overview

Long-running autonomous software engineering presents significant challenges for [[large language models]]. As [[AI agents]] work on complex tasks over extended periods, they encounter degradation in coherence, self-evaluation bias, and scope management issues. This article, written by Prithvi Rajasekaran from [[Anthropic Labs]], documents novel harness design patterns that substantially improve performance on both subjective tasks (like [[frontend design]]) and objective tasks (like full-stack application development).

## Core Problem: Why Naive Implementations Fail

### Context Window Degradation

[[Large language models]] struggle to maintain coherence on lengthy tasks as their [[context window]] fills. Additionally, some models exhibit "context anxiety," where they prematurely wrap up work as they approach their perceived context limit.

**Solutions attempted:**
- **Compaction**: Summarizing earlier conversation portions in place, allowing the same agent to continue on shortened history
- **Context resets**: Clearing the context window entirely and starting fresh agents with structured handoffs carrying previous state

Context resets proved more effective than compaction alone, particularly with [[Claude Sonnet 4.5]], though they introduce orchestration complexity and token overhead.

### Self-Evaluation Bias

[[AI agents]] exhibit systematic bias when evaluating their own work, confidently praising mediocre outputs. This problem is especially acute for subjective tasks like [[design]], where no binary verification criteria exist. Even on objective tasks with verifiable outcomes, agents demonstrate poor judgment that impedes performance.

**Key insight**: Separating the agent performing work from the agent evaluating it provides a strong lever for addressing this issue. While evaluator agents remain susceptible to leniency toward [[AI]]-generated outputs, they can be tuned to be appropriately skeptical—a far more tractable approach than making generators self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

### Design Principles Framework

To address the challenge of evaluating subjective aesthetic quality, the author developed a framework of four grading criteria applied to both generator and evaluator agents:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, and imagery to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions versus template layouts and library defaults. Penalizes telltale signs of [[AI]]-generated patterns like generic purple gradients.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. Primarily a competence check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

The framework emphasized design quality and originality over craft and functionality, since [[Claude]] naturally excelled at the latter two.

### Generator-Evaluator Loop Architecture

The frontend design harness operated on the [[Claude Agent SDK]], implementing:

- **Generator agent**: Created HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator agent**: Used the [[Playwright MCP]] to interact with live pages, screenshotting and studying implementations before scoring each criterion with detailed critique
- **Iteration cycle**: 5-15 iterations per generation, with the generator strategically choosing to refine current direction or pivot to new aesthetic approaches

Full runs extended to four hours due to real wall-clock time spent on page navigation and evaluation. Evaluator assessments improved over iterations before plateauing, though patterns were not always linearly progressive—later iterations tended to be better overall, but users sometimes preferred intermediate versions.

### Key Findings

- **Prompt influence**: Wording of criteria steered generators in unanticipated ways (e.g., "museum quality" language pushed toward particular visual convergence)
- **First-iteration improvement**: Even without evaluator feedback, outputs were noticeably better than baseline, suggesting criteria language itself moved models away from generic defaults
- **Creative leaps**: Later iterations sometimes produced unexpected architectural innovations (e.g., reimagining a museum website as a 3D spatial experience with CSS perspective rendering)

---

## Full-Stack Coding: Three-Agent Architecture

### System Design

Building on insights from [[frontend design]] work and earlier [[long-running coding agent harness|long-running agent harnesses]], the author developed a three-agent system for autonomous full-stack development:

#### Planner Agent

- **Role**: Converts simple 1-4 sentence user prompts into comprehensive product specifications
- **Approach**: Ambitious about scope, focused on product context and high-level technical design rather than granular implementation details
- **Special capability**: Weaves [[AI]] features into product specs, creating opportunities for agentic integration
- **Rationale**: Avoids cascading errors from incorrect low-level specifications while providing clear deliverable targets

#### Generator Agent

- **Role**: Implements application features iteratively
- **Stack**: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- **Process**: Works in sprints picking one feature at a time; self-evaluates work at sprint end
- **Tools**: [[Git]] for version control
- **Constraint**: Builds against agreed-upon sprint contracts before handing off to QA

#### Evaluator Agent

- **Role**: Quality assurance through automated testing and verification
- **Testing approach**: Uses [[Playwright MCP]] to click through applications like real users, testing UI features, API endpoints, and database states
- **Evaluation criteria**: Product depth, functionality, visual design, and code quality
- **Process**: Negotiates sprint contracts with generator before implementation; detailed feedback on failures

### Sprint Contract System

A critical component of the architecture, sprint contracts bridge the gap between high-level user stories and testable implementation:

- Generator proposes what will be built and how success will be verified
- Evaluator reviews proposals to ensure correct work is being built
- Both agents iterate until agreement
- Communication via structured files passed between agents
- Prevents over-specification while maintaining specification fidelity

### Performance Metrics: Retro Game Maker Example

**Comparison of solo agent vs. full harness:**

| Harness Type | Duration | Cost | Quality |
|---|---|---|---|
| Solo agent | 20 minutes | $9 | Broken core functionality; rigid workflow; layout issues |
| Full harness | 6 hours | $200 | Polished interface; working gameplay; 16-feature specification; AI-assisted editors |

The solo run produced a non-functional game with broken entity wiring and unintuitive workflows. The harness run expanded a one-sentence prompt into a 10-sprint specification including sprite animation systems, behavior templates, sound effects, AI-assisted sprite generation, and shareable game export.

### Evaluator Effectiveness

The evaluator proved critical for catching implementation gaps:

| Contract Criterion | Finding |
|---|---|
| Rectangle fill tool allows click-drag | **FAIL** — Tool only places tiles at endpoints; `fillRectangle` function not triggered on mouseUp |
| Select and delete entity spawn points | **FAIL** — Delete handler requires both `selection` and `selectedEntityId`, but clicking entity only sets one |
| Reorder animation frames via API | **FAIL** — Route matching issue causes FastAPI to parse 'reorder' as frame_id integer |

Out-of-the-box, [[Claude]] is a poor QA agent, requiring substantial prompt tuning through iterative feedback loops. The evaluator initially identified issues but rationalized them away; later iterations required tuning for deeper edge-case testing.

---

## Harness Evolution: Opus 4.6 Optimization

### Principle of Minimal Scaffolding

As [[large language models]] improve, assumptions built into harnesses become worth stress-testing. The principle: "find the simplest solution possible, and only increase complexity when needed." Each harness component encodes assumptions about model limitations; as models improve, assumptions may become outdated.

### Removing the Sprint Construct

With [[Claude Opus 4.6]] release, the author removed sprint decomposition entirely:

**Rationale**: Opus 4.6 improvements in planning, agentic task sustenance, large codebase operation, and code review made sprint-level decomposition unnecessary for many tasks.

**Outcome**: 
- Removed sprint structure but retained planner and evaluator
- Moved evaluator to single pass at end rather than per-sprint grading
- Evaluator value now depends on task difficulty relative to model capability

**Key insight**: The evaluator is not a fixed decision but a