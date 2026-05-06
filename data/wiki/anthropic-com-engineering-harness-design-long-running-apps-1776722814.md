---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-06T05:34:10.934802
raw_file_updated: 2026-05-06T05:34:10.934802
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-06T05:34:10.934802
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical approach to improving [[AI agent]] performance on complex, long-running tasks. By separating generation and evaluation functions into specialized agents and implementing structured task decomposition, developers can achieve significantly better results than single-agent systems. This article documents techniques pioneered at [[Anthropic]] for building multi-agent systems that maintain coherence across extended sessions, with applications ranging from [[frontend design]] to full-stack [[software development]].

---

## Introduction

Long-running [[agentic systems]] face persistent challenges: models lose coherence as context windows fill, agents struggle with self-evaluation, and complex tasks often result in incomplete or buggy implementations. Through experimentation with [[Claude]] across frontend design and full-stack coding tasks, researchers at Anthropic developed a multi-agent harness architecture inspired by [[Generative Adversarial Networks]] (GANs) that substantially improves output quality.

The core insight is that separating the agent that generates work from the agent that evaluates it creates a powerful feedback loop. An external evaluator can be tuned to provide reliable, critical feedback in ways that are difficult to achieve through self-evaluation alone.

---

## Key Challenges with Naive Implementations

### Context Window Limitations

[[Long-running tasks]] expose a fundamental limitation in current language models: coherence degrades as the [[context window]] fills. Two related failure modes emerge:

- **Context anxiety**: Models exhibit a tendency to wrap up work prematurely as they approach their perceived context limit, cutting tasks short even when more work remains
- **Loss of coherence**: Extended conversations lead to drift, inconsistency, and poor decision-making as earlier context becomes unavailable

**Solution approach**: Rather than using [[context compaction]] (summarizing earlier conversation in place), implementing [[context resets]] provides agents with a clean slate. The previous agent's state is captured in structured [[artifacts]] that the next agent reads to resume work. While this adds orchestration complexity and token overhead, it proved essential for models like Claude Sonnet 4.5 that exhibited strong context anxiety. Notably, newer models like [[Claude Opus 4.6]] largely eliminated this behavior, reducing the need for context resets.

### Self-Evaluation Bias

Agents asked to evaluate their own work consistently exhibit positive bias, praising outputs even when quality is mediocre. This problem is particularly acute in subjective domains like [[design]] where no binary correctness check exists.

**Solution approach**: Separating generation from evaluation creates a structural solution. An external evaluator, while still inclined toward leniency as an LLM, can be tuned to be appropriately skeptical through careful [[prompt engineering]]. Once external feedback exists, the generator has concrete, actionable input to iterate against.

---

## Frontend Design: Making Subjective Quality Measurable

### Grading Criteria Framework

The first application of the generator-evaluator pattern was [[frontend design]], where subjective taste had previously prevented reliable evaluation. The solution was to translate aesthetic judgment into concrete, gradable criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, and imagery to create distinct mood and identity, rather than appearing as disconnected parts.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Telltale signs of generic [[AI-generated]] patterns (purple gradients, stock components) indicate failure in this criterion.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The framework weighted design quality and originality more heavily than craft and functionality, as Claude naturally performed well on the latter two. This deliberately pushed the model toward aesthetic risk-taking rather than safe, generic solutions.

### Implementation Details

The harness used the [[Claude Agent SDK]] with a [[generator]] and [[evaluator]] agent:

- **Generator**: Created HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator**: Used [[Playwright MCP]] to interact with live pages, taking screenshots and studying implementations before scoring each criterion with detailed critique
- **Iteration loop**: 5-15 iterations per generation, with the generator making strategic decisions to either refine the current direction or pivot to entirely different aesthetics based on evaluator feedback

### Results and Observations

- Evaluator assessments improved over iterations before plateauing, with headroom remaining for further refinement
- Wording in the criteria steered generation in unanticipated ways (e.g., "museum quality" language pushed toward specific visual convergence)
- Score improvement was not always linear; middle iterations were sometimes preferable to final ones
- Implementation complexity increased across rounds as generators attempted more ambitious solutions
- Even first-iteration outputs were noticeably better than baseline, suggesting criteria language itself steered models away from generic defaults before evaluator feedback

**Notable example**: A museum website prompt that, by iteration nine, produced a polished dark-themed landing page. On the tenth iteration, the generator scrapped the approach entirely and reimagined it as a 3D spatial experience with CSS perspective rendering, free-form artwork positioning, and doorway-based navigation—a creative leap not typical of single-pass generation.

---

## Full-Stack Coding: Three-Agent Architecture

Building on frontend design insights, the harness was scaled to full-stack development using a three-agent system addressing specific gaps observed in prior work.

### Agent Roles

**Planner Agent**

Transforms simple 1-4 sentence prompts into comprehensive product specifications:
- Expands scope ambitiously while focusing on product context and high-level technical design rather than implementation details
- Avoids over-specification that could cascade errors downstream
- Identifies opportunities to weave [[AI features]] into product specs
- Generates visual design language for consistent application appearance

**Generator Agent**

Implements features using a sprint-based approach:
- Works one feature at a time from the spec using React, Vite, [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at the end of each sprint before handoff to QA
- Uses [[Git]] for version control
- Builds integrated [[Claude]] features when specified

**Evaluator Agent**

Performs quality assurance through active testing:
- Uses [[Playwright MCP]] to click through running applications like a user would
- Tests UI features, [[API]] endpoints, and database states
- Grades sprints against product depth, functionality, visual design, and code quality
- Establishes [[sprint contracts]] before implementation—negotiated agreements on what "done" looks like
- Provides specific, actionable feedback on failures

### Sprint Contracts

A critical innovation in the full-stack harness is the sprint contract mechanism. Before each sprint:

1. **Generator proposes** what will be built and how success will be verified
2. **Evaluator reviews** to ensure the generator is building the right thing
3. **Both iterate** until agreement is reached
4. **Generator builds** against the agreed-upon contract
5. **Evaluator tests** against the contract criteria

This bridges the gap between high-level user stories and testable implementations without over-specifying implementation details prematurely.

### Communication Pattern

Agents communicate via files rather than direct conversation:
- One agent writes a file
- Another agent reads and responds either in that file or with a new file
- Previous agent reads the response and continues

This asynchronous pattern keeps work faithful to specifications while maintaining flexibility.

### Initial Results: Retro Game Maker

**Comparison metrics**:

| Harness Type | Duration | Cost |
|---|---|---|
| Solo (single-agent) | 20 minutes | $9 |
| Full harness (three-agent) | 6 hours | $200 |

**Solo run output**:
- Appeared functional at first glance
- Layout wasted space with fixed-height panels
- Workflow was rigid and unintuitive
- Core gameplay was broken: entities appeared but didn't respond to input
- Code wiring between entity definitions and game runtime was broken

**Full harness output**:
- Polished interface with consistent visual identity
- Canvas used full viewport with sensible panel sizing
- Richer, more fully-featured sprite editor
- Built-in Claude integration for generating game components
- Functional gameplay with working physics (though with some rough edges)
- Generated from 16-feature spec across 10 sprints

The 20x cost increase yielded dramatically higher quality, with the core application features actually working versus being completely broken in the solo run.

### Evaluator Tuning Requirements

Achieving reliable QA required substantial prompt engineering:

- **Out-of-box performance**: Claude identified legitimate issues but then rationalized them away, approved substandard work, and tested superficially
- **Tuning process**: Iterative refinement based on divergence between evaluator judgment and human assessment
- **Result**: After several refinement cycles, evaluator grading became reasonable,