---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-06T05:59:26.679263
raw_file_updated: 2026-06-06T05:59:26.679263
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-06T05:59:26.679263
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical approach to improving [[AI agent]] performance on complex, long-running tasks. By combining [[multi-agent systems]] with specialized evaluation mechanisms, developers can enable AI models to build complete full-stack applications autonomously. This article documents techniques pioneered at [[Anthropic]] for frontend design optimization and autonomous software engineering, including the use of [[generator-evaluator architectures]] inspired by [[Generative Adversarial Networks]].

---

## Overview

Harness design refers to the structural scaffolding and orchestration patterns that enable [[large language models]] (LLMs) to perform effectively on extended, complex tasks. Rather than relying on single-pass generation, well-designed harnesses decompose problems, provide feedback loops, and manage context constraints to achieve outputs that exceed what baseline models can produce alone.

This approach is particularly valuable for:
- **Long-running autonomous coding** spanning multiple hours
- **Subjective quality tasks** like [[frontend design]]
- **Complex full-stack application development**
- **Multi-session workflows** requiring context management

---

## Key Challenges with Naive Implementations

### Context Window Management

Models struggle to maintain coherence as context windows fill during lengthy tasks. Two primary failure modes emerge:

1. **Context Anxiety**: Models begin wrapping up work prematurely as they approach their perceived [[context limit]], reducing output quality
2. **Context Drift**: Performance degrades as the conversation history grows, leading to inconsistent or off-track implementations

**Solution Approaches:**
- **Context Resets**: Clearing the context window and starting fresh with structured handoffs (more effective but adds complexity)
- **Compaction**: Summarizing earlier conversation in place (preserves continuity but may not fully eliminate context anxiety)

[[Opus 4.5]] exhibits context anxiety strongly enough that context resets become essential, while [[Opus 4.6]] largely mitigates this behavior natively.

### Self-Evaluation Limitations

Models demonstrate systematic bias when evaluating their own work:
- Confidently praise mediocre outputs
- Struggle with subjective quality assessment (e.g., "is this design beautiful?")
- Exhibit poor judgment on verifiable tasks, impeding iteration

**Key Insight**: Separating the agent performing work from the agent evaluating it provides a strong lever for improvement. While evaluator LLMs remain inclined toward generosity, they can be tuned to skepticism more effectively than generators can be made self-critical.

---

## Generator-Evaluator Architecture

Inspired by [[Generative Adversarial Networks]] (GANs), this architecture pairs specialized agents with complementary roles.

### Core Pattern

```
Generator Agent → Produces Output → Evaluator Agent → Provides Feedback → Generator Iterates
```

The separation creates a feedback loop that drives outputs toward higher quality through concrete, actionable critique rather than relying on self-assessment.

### Application to Frontend Design

#### Grading Criteria

Making subjective quality measurable requires encoding design principles into concrete criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, imagery, and details to create distinct mood and identity
2. **Originality**: Evidence of custom decisions rather than template layouts or library defaults; absence of telltale AI-generated patterns
3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios
4. **Functionality**: Usability independent of aesthetics; users can understand the interface, find primary actions, and complete tasks

**Weighting Strategy**: Emphasizing design quality and originality over craft and functionality, since models typically excel at craft and functionality by default but struggle with distinctive, polished design.

#### Implementation

- **Generator**: Creates HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator**: Uses [[Playwright MCP]] to interact with live pages, screenshot implementations, and provide detailed critiques
- **Iteration Loop**: Runs 5-15 cycles per generation, with each iteration responding to evaluator feedback
- **Execution Time**: Full runs can extend 4+ hours

#### Key Findings

- Evaluator assessments improve over iterations before plateauing
- Later implementations tend to be better overall, though not always linearly
- Implementation complexity increases across rounds as generators attempt more ambitious solutions
- Prompt wording steers generator behavior significantly (e.g., "museum quality" influences visual convergence)
- Even first-iteration outputs exceed baseline with no evaluator feedback, suggesting criteria wording itself improves performance

---

## Full-Stack Application Development

Applying the generator-evaluator pattern to autonomous coding yields a three-agent architecture addressing the complete development lifecycle.

### Three-Agent System

#### 1. Planner Agent

**Purpose**: Automate specification creation from simple user prompts

**Responsibilities**:
- Expand 1-4 sentence prompts into comprehensive product specifications
- Maintain ambitious scope while focusing on product context and high-level technical design
- Avoid over-specifying implementation details that could cascade errors downstream
- Integrate AI features into product specifications

**Rationale**: Prevents the generator from under-scoping work while avoiding detailed technical errors that would compound through implementation.

#### 2. Generator Agent

**Purpose**: Implement features through iterative development

**Responsibilities**:
- Work in sprints, implementing one feature at a time
- Build using modern stacks (React, Vite, FastAPI, SQLite/PostgreSQL)
- Self-evaluate work at sprint completion
- Maintain version control with git
- Negotiate sprint contracts with evaluator before implementation

**Stack Components**:
- **Frontend**: React with Vite
- **Backend**: FastAPI
- **Database**: SQLite or PostgreSQL
- **Version Control**: Git

#### 3. Evaluator Agent

**Purpose**: Verify quality through active testing and grading

**Responsibilities**:
- Use [[Playwright MCP]] to interact with running applications like users would
- Test UI features, API endpoints, and database state
- Grade against criteria including product depth, functionality, visual design, and code quality
- Identify specific bugs with actionable feedback
- Negotiate sprint contracts defining "done" before implementation begins

**Sprint Contract Process**:
1. Generator proposes what will be built and success criteria
2. Evaluator reviews proposal to ensure alignment with spec
3. Agents iterate until agreement reached
4. Generator implements against agreed contract
5. Evaluator tests and provides detailed feedback

**Evaluation Approach**: Each criterion has hard thresholds; failure on any criterion triggers detailed feedback for generator iteration.

### Communication Pattern

Agents communicate via files rather than direct conversation:
- One agent writes a file
- Another agent reads and responds (either in-place or with new file)
- Previous agent reads response and continues

This approach maintains faithful spec adherence without over-specification.

---

## Harness Evolution and Optimization

### Initial Implementation (Opus 4.5)

**Architecture**: Planner → Generator (sprint-based) → Evaluator (per-sprint)

**Performance Metrics** (Retro Game Maker):
- **Duration**: 6 hours
- **Cost**: $200
- **Quality**: Significantly superior to single-agent baseline ($9, 20 min)

**Key Characteristics**:
- Sprint decomposition essential due to context anxiety
- Per-sprint evaluation catches real bugs
- Expensive but produces functional, feature-rich applications

### Simplified Implementation (Opus 4.6)

**Improvements in Opus 4.6**:
- Better planning capabilities
- Longer sustained agentic task performance
- More reliable operation in large codebases
- Improved code review and debugging
- Superior long-context retrieval

**Architectural Changes**:
- Removed sprint construct entirely
- Moved evaluation to single pass at end of run
- Added improved AI feature integration prompting
- Maintained planner (prevents under-scoping)

**Performance Metrics** (Digital Audio Workstation):
- **Duration**: 3 hours 50 minutes
- **Cost**: $124.70
- **Quality**: Functional DAW with integrated agent capabilities

**Breakdown**:
- Planner: 4.7 min ($0.46)
- Build Round 1: 2 hr 7 min ($71.08)
- QA Round 1: 8.8 min ($3.24)
- Build Round 2: 1 hr 2 min ($36.89)
- QA Round 2: 6.8 min ($3.09)
- Build Round 3: 10.9 min ($5.88)
- QA Round 3: 9.6 min ($4.06)

### Lessons in Harness Optimization

**Key Principle**: Every harness component encodes an assumption about model limitations. These assumptions warrant stress-testing as:
1. They may be incorrect
2. They become stale as models improve

**Methodical Approach