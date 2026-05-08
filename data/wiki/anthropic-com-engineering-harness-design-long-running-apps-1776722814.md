---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-08T04:57:23.644324
raw_file_updated: 2026-05-08T04:57:23.644324
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-08T04:57:23.644324
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical technique for enabling [[AI agents]] to produce high-quality outputs across extended, complex tasks. This approach combines multiple specialized agents—typically a generator, evaluator, and planner—with structured feedback loops to overcome limitations in [[self-evaluation]], [[context management]], and [[task decomposition]]. Originally developed for [[frontend design]], the pattern has been successfully scaled to full-stack application development, enabling autonomous software engineering over multi-hour sessions.

---

## Overview

**Harness design** refers to the architectural patterns and orchestration systems that enable [[large language models]] (LLMs) to perform effectively on long-running, complex tasks. Rather than relying on a single model instance to complete an entire project, harness design uses multiple specialized agents with different roles, each optimized for specific aspects of the work.

The fundamental insight is that [[AI agents]] struggle with two critical problems:
1. **Self-evaluation bias**: Models tend to praise their own work even when quality is mediocre
2. **Context degradation**: Performance declines as context windows fill, and models may exhibit "context anxiety" by prematurely concluding work

By separating generation from evaluation and implementing structured context management, harness design overcomes these limitations and enables significantly higher quality outputs.

---

## Key Limitations of Naive Implementations

### Context Window Challenges

Models like [[Claude Sonnet 4.5]] exhibit **context anxiety**, a tendency to wrap up work prematurely as the context window approaches perceived limits. Two approaches address this:

- **Compaction**: Summarizing earlier conversation parts in-place while maintaining the same agent session
- **Context resets**: Clearing the context window entirely and starting a fresh agent with structured handoff artifacts

[[Context resets]] proved more effective than compaction alone, as they provide a clean slate that eliminates context anxiety, though they introduce orchestration complexity and token overhead.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently exhibit [[confirmation bias]], confidently praising mediocre outputs. This problem is particularly acute for:

- **Subjective tasks** (design, aesthetics) where no verifiable test exists
- **Complex technical work** where subtle bugs may not be immediately obvious

Separating the agent performing work from the agent evaluating it proves to be a powerful intervention. While evaluator agents remain somewhat lenient toward LLM-generated outputs, they can be tuned to be appropriately skeptical through [[prompt engineering]] and [[few-shot learning]].

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically gravitates toward safe, predictable layouts that are technically functional but visually unremarkable—often called "AI slop."

### The Solution: Grading Criteria

The key insight is that while aesthetics cannot be fully reduced to numerical scores, they can be improved by encoding [[design principles]] as concrete, gradable criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, and imagery to create distinct mood and identity.

2. **Originality**: Is there evidence of custom decisions, or merely template layouts and library defaults? Human designers should recognize deliberate creative choices.

3. **Craft**: Technical execution—typography hierarchy, spacing consistency, color harmony, contrast ratios. Competence verification rather than creativity assessment.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

### Implementation

The harness used a **generator-evaluator loop** inspired by [[Generative Adversarial Networks]] (GANs):

- **Generator agent**: Created HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator agent**: Used the [[Playwright]] [[Model Context Protocol]] (MCP) to interact with live pages, take screenshots, and grade each criterion
- **Iteration**: Feedback from the evaluator drove the generator toward more distinctive designs

The evaluator was calibrated using [[few-shot examples]] with detailed score breakdowns, ensuring consistent judgment aligned with design preferences.

### Results

- Runs typically required 5-15 iterations over 4+ hours
- The evaluator's assessments improved across iterations before plateauing
- Wording of criteria steered generator behavior in unanticipated ways
- Some generations made sharp aesthetic pivots between iterations rather than incremental refinement
- Even first iterations were noticeably better than baseline, suggesting criteria themselves shape output character

**Notable example**: When prompted to create a website for a Dutch art museum, the model produced a conventional dark-themed landing page through iteration 9. On iteration 10, it completely reimagined the site as a spatial 3D experience with CSS perspective, checkered floor, freeform artwork positioning, and doorway-based navigation—a creative leap not seen in single-pass generation.

---

## Scaling to Full-Stack Application Development

### Three-Agent Architecture

The successful frontend design pattern scaled naturally to full-stack development, mapping onto the software development lifecycle where code review and QA serve the same structural role as design evaluation.

#### Planner Agent

**Role**: Expand high-level prompts into detailed product specifications

**Characteristics**:
- Takes 1-4 sentence user prompts and creates comprehensive specs
- Ambitious about scope rather than conservative
- Focuses on product context and high-level technical design
- Avoids granular technical details that could cascade errors
- Identifies opportunities to integrate [[AI features]] into product specifications

**Rationale**: Detailed upfront specs risk cascading errors, while high-level specs with clear deliverables allow downstream agents to determine implementation paths.

#### Generator Agent

**Role**: Implement features and build the application

**Characteristics**:
- Works in [[sprint]]s, implementing one feature at a time from the specification
- Technology stack: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- Uses [[Git]] for version control
- Self-evaluates work at the end of each sprint
- Hands off to QA before moving to next sprint

**Rationale**: [[Sprint-based decomposition]] helps manage scope and maintain coherence across extended builds.

#### Evaluator Agent (QA)

**Role**: Verify quality, catch bugs, and provide detailed feedback

**Characteristics**:
- Uses [[Playwright]] MCP to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades against both discovered bugs and criteria-based rubrics
- Negotiates "sprint contracts" with generator before implementation
- Provides specific, actionable feedback rather than vague critiques

**Evaluation Criteria** (adapted from frontend design):
- Product depth and feature completeness
- Functionality and usability
- Visual design
- Code quality

### Sprint Contracts

Before each sprint, generator and evaluator agents negotiate a **sprint contract** that:
- Bridges the gap between high-level user stories and testable implementation
- Specifies what the generator will build
- Defines how success will be verified
- Ensures the generator builds the right thing before implementation begins

Communication occurs through structured files, with agents reading and responding to previous outputs, maintaining clear context and accountability.

---

## Case Study: Retro Video Game Maker

### Comparison: Solo vs. Harness Approach

**Solo Agent Run**:
- Duration: 20 minutes
- Cost: $9
- Output: Application appeared functional but had critical bugs
  - Rigid workflow without UI guidance
  - Entity-game runtime wiring broken
  - Game unresponsive to input
  - Layout wasted space

**Full Harness Run** (Opus 4.5):
- Duration: 6 hours
- Cost: $200
- Output: Feature-rich, polished application
  - 16-feature spec across 10 sprints
  - Included sprite animation system, behavior templates, sound/music, AI-assisted sprite/level generation, shareable game export
  - Consistent visual identity from design spec
  - Functional sprite editor with rich tooling
  - Playable games with working physics
  - Built-in Claude integration for game generation
  - Some workflow UX gaps remained (minor issue vs. broken core functionality)

**Key insight**: 20x cost difference yielded dramatically higher quality, with the harness output actually functional while solo output had broken core features.

---

## Harness Evolution and Optimization

### Principle: Stress-Test Assumptions

Every component in a harness encodes an assumption about model limitations. As models improve, these assumptions warrant re-examination. The principle is: **find the simplest solution possible, and only increase complexity when needed**.

### Opus 4.6 Improvements

The release of [[Claude Opus 4.6]] motivated harness simplification:
- Better planning and longer agentic task sustainability
- More reliable operation in large codebases
- Improved code review and debugging capabilities
- Better long-context retrieval

These improvements meant certain harness components were