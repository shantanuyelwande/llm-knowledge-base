---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-09T06:15:20.657351
raw_file_updated: 2026-06-09T06:15:20.657351
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-09T06:15:20.657351
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the structured scaffolding and multi-agent architectures used to enable [[AI agents]] to complete complex, long-running tasks such as frontend design and full-stack software development. This approach, inspired by [[Generative Adversarial Networks]] (GANs), employs specialized agent personas (planner, generator, evaluator) that work together to decompose complex problems, generate solutions, and maintain quality standards across extended execution sessions. The methodology addresses key challenges in agentic systems including [[context window]] management, self-evaluation bias, and task coherence over time.

---

## Overview

Harness design is a critical technique for pushing [[AI coding agents]] beyond their baseline capabilities. Rather than relying on a single model to complete a complex task, harness design uses multiple specialized agents, structured workflows, and feedback mechanisms to achieve higher-quality outputs for long-running applications. This approach has proven particularly effective for tasks requiring both subjective judgment (like frontend design) and verifiable correctness (like software engineering).

The core insight is that by separating the roles of generation and evaluation, and by providing structured handoffs between sessions, AI systems can maintain coherence and quality across hours-long development cycles that would otherwise exceed the practical limits of a single agent.

## Historical Context

Earlier work at Anthropic on [[long-running agents]] demonstrated that harness design could substantially improve performance. The initial approach used:

- An **initializer agent** to decompose product specifications into task lists
- A **coding agent** that implemented features one at a time
- **Structured artifacts** to carry context across sessions through [[context resets]]

While effective, these early harnesses still exhibited persistent failure modes on complex tasks, particularly issues with [[context anxiety]] and unreliable self-evaluation. These limitations motivated the development of more sophisticated multi-agent architectures.

## Key Challenges Addressed

### Context Management

[[Context window]] constraints present a fundamental challenge for long-running tasks. As conversations extend, models experience two related problems:

1. **Context anxiety**: Models begin wrapping up work prematurely as they perceive their [[context window]] filling, even when more work remains
2. **Loss of coherence**: Extended context can degrade model performance on lengthy tasks

**Solution**: [[Context resets]] provide a clean slate for continuation agents, combined with structured artifacts that carry essential state forward. This approach proved more effective than [[context compaction]] (summarizing earlier conversation in place) for models like [[Claude Sonnet 4.5]], though newer models like [[Claude Opus 4.6]] largely mitigated context anxiety natively.

### Self-Evaluation Bias

Models asked to evaluate their own work tend to provide inflated assessments, confidently praising mediocre outputs. This problem is particularly acute for subjective tasks like design, where no binary correctness check exists.

**Solution**: Separating the evaluation role into a dedicated **evaluator agent** creates an external feedback mechanism. The evaluator can be specifically tuned to be skeptical, making it more tractable to achieve reliable quality assessment than making a generator self-critical.

## Architecture: Multi-Agent System

The harness design employs a three-agent architecture, each addressing specific aspects of complex task completion:

### Planner Agent

**Function**: Expands high-level user prompts into detailed product specifications

**Key characteristics**:
- Takes 1-4 sentence prompts and produces comprehensive specs
- Emphasizes ambitious scope without over-specifying implementation details
- Focuses on product context and high-level technical design
- Identifies opportunities to weave [[AI features]] into specifications
- Avoids granular technical details that could cascade errors downstream

**Rationale**: Automating the specification phase ensures consistent scope definition and prevents the generator from under-scoping based on a minimal prompt.

### Generator Agent

**Function**: Implements the product according to the specification and evaluator feedback

**Key characteristics**:
- Works in decomposed chunks (when using earlier harness versions)
- Implements features using modern stacks (React, Vite, FastAPI, SQLite/PostgreSQL)
- Performs self-evaluation before handoff
- Uses [[version control]] (git) for code management
- Iterates based on evaluator feedback

**Rationale**: Decomposing work into tractable chunks helps maintain coherence and allows the evaluator to assess well-defined units of work.

### Evaluator Agent

**Function**: Tests implementations and grades work against defined criteria

**Key characteristics**:
- Uses [[Playwright]] to interact with running applications like a user
- Tests UI features, API endpoints, and database states
- Grades against both concrete bugs found and abstract quality criteria
- Establishes **sprint contracts** before implementation begins
- Provides detailed, actionable feedback for iteration

**Rationale**: Separating evaluation from generation enables reliable quality assessment and creates a feedback loop that drives improvement.

## Frontend Design Application

The harness design approach was first validated on frontend design, where the self-evaluation problem was most pronounced.

### Design Criteria

The evaluator grades designs against four specific criteria:

1. **Design quality**: Visual coherence, mood, and identity. Do colors, typography, layout, and imagery combine effectively?
2. **Originality**: Evidence of custom decisions rather than template defaults. Are there deliberate creative choices recognizable to a human designer?
3. **Craft**: Technical execution including typography hierarchy, spacing, color harmony, and contrast ratios
4. **Functionality**: Usability independent of aesthetics. Can users understand the interface and complete tasks?

The harness emphasized **design quality** and **originality** over craft and functionality, as models naturally performed well on the latter two dimensions. The criteria explicitly penalized generic "AI slop" patterns.

### Feedback Loop

The generator-evaluator loop operated as follows:

1. Generator creates HTML/CSS/JS frontend based on prompt
2. Evaluator navigates the live page using Playwright, taking screenshots and studying implementation
3. Evaluator scores each criterion and provides detailed critique
4. Generator receives feedback and either refines the current direction or pivots to a different aesthetic
5. Loop repeats 5-15 iterations per generation

**Key findings**:
- Evaluator assessments improved over iterations before plateauing
- Later implementations tended to be better overall, though individual middle iterations were sometimes preferred
- Prompt wording of criteria strongly influenced output character
- Even first-iteration outputs improved significantly over baseline, suggesting the criteria language itself steered the model away from generic defaults

### Example: Museum Website

A notable example involved generating a website for a fictional Dutch art museum. By iteration 9, the model produced a clean, dark-themed landing page. On iteration 10, it scrapped the approach entirely and reimagined the site as a 3D spatial experience: a CSS-rendered room with checkered floor, artworks hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This creative leap demonstrated the potential of iterative refinement with external evaluation.

## Full-Stack Development Application

The GAN-inspired pattern was then applied to full-stack development, where code review and QA serve analogous roles to design evaluation.

### Architecture

The full-stack harness retained the three-agent structure but with different implementation details:

- **Planner**: Expands prompts into 16+ feature specifications across multiple sprints
- **Generator**: Implements features with negotiated sprint contracts
- **Evaluator**: Tests functionality and validates against contract criteria

**Sprint contracts** bridge the gap between high-level user stories and testable implementation. Before each sprint, generator and evaluator negotiate what "done" looks like, establishing testable success criteria before code is written.

### Performance Comparison: Solo vs. Harness

A retro video game maker was built using both a single-agent system and the full harness:

| Approach | Duration | Cost | Outcome |
|----------|----------|------|---------|
| Solo agent | 20 minutes | $9 | Functional interface but broken core gameplay |
| Full harness | 6 hours | $200 | Feature-complete, playable game |

The solo run produced an interface that appeared correct but had fundamental bugs: entity controls didn't respond to input, and the wiring between entity definitions and game runtime was broken.

The harness run, starting from the same one-sentence prompt, produced a 16-feature specification across 10 sprints, including sprite animation, behavior templates, sound effects, AI-assisted generation, and game export. The final application was visually polished, had consistent design language, and actually worked.

### Evaluator Effectiveness

The evaluator proved critical for catching implementation gaps:

| Contract Criterion | Evaluator Finding |
|-------------------|------------------|
| Rectangle fill tool allows click-drag to fill area | **FAIL** — Tool only places tiles at drag start/end points; `fillRectangle` function exists but isn't triggered properly |
| User can reorder animation frames via API | **FAIL** — FastAPI route ordering issue: `reorder` route defined after `/{frame_id}`, so 'reorder' is parsed as