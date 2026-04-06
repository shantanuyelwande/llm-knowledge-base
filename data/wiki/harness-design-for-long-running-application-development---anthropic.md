---
title: Harness design for long-running application development _ Anthropic
source_file: Harness design for long-running application development _ Anthropic.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:21:23.402029
raw_file_updated: 2026-04-05T20:21:23.402029
version: 1
sources:
  - file: Harness design for long-running application development _ Anthropic.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:21:23.402029
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** is an AI engineering approach that significantly improves the performance of [[Claude]] and other language models on complex, long-running tasks. By decomposing work into specialized agent roles, implementing evaluation mechanisms separate from generation, and using structured handoffs between sessions, harness design enables models to produce higher-quality applications, designs, and code than single-agent approaches. This methodology draws inspiration from [[Generative Adversarial Networks]] (GANs) and has proven effective for both subjective tasks like frontend design and objective tasks like full-stack application development.

## Overview

Harness design addresses fundamental limitations in how language models handle extended tasks. Rather than asking a single model to generate, evaluate, and iterate on complex work, harness design separates these concerns into specialized agents that work collaboratively within a structured framework. This approach has proven essential for pushing [[autonomous software engineering]] beyond baseline capabilities.

## Key Problems Addressed

### Context Management

Long-running tasks present two critical challenges related to [[context windows]]:

1. **Context Degradation**: Models lose coherence as context windows fill during lengthy tasks
2. **Context Anxiety**: Some models, notably [[Claude Sonnet 4.5]], exhibit a tendency to prematurely wrap up work as they approach perceived context limits

While [[context compaction]] (summarizing earlier conversation in place) preserves continuity, it doesn't provide models with a clean slate. **Context resets**—clearing the context window entirely and using structured handoff artifacts to carry previous state—proved more effective, though at the cost of increased orchestration complexity and token overhead.

### Self-Evaluation Bias

When asked to evaluate their own work, agents exhibit systematic bias:

- They tend to respond with confident praise even when quality is mediocre
- This problem is particularly pronounced for subjective tasks like design where no binary correctness check exists
- Even on verifiable tasks, agents sometimes demonstrate poor judgment that impedes performance

**Separating the agent doing the work from the agent judging it** proves to be a strong lever. While evaluator agents are still inclined toward generosity toward LLM-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

## Frontend Design Application

### Design Criteria Framework

The frontend design harness converts subjective aesthetic judgments into concrete, gradable criteria:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, imagery, and details to create distinct mood and identity
2. **Originality**: Evidence of custom decisions versus template layouts and library defaults. Penalizes unmodified stock components and telltale AI patterns
3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios
4. **Functionality**: Usability independent of aesthetics—can users understand the interface, find primary actions, and complete tasks?

The framework emphasizes design quality and originality over craft and functionality, since [[Claude]] naturally excels at the latter two. This deliberate weighting pushes the model toward more aesthetic risk-taking.

### Implementation Details

- **Generator Agent**: Creates HTML/CSS/JS frontends based on user prompts
- **Evaluator Agent**: Uses [[Playwright]] MCP to interact with live pages directly, navigating and screenshotting before scoring
- **Iteration Loop**: 5-15 iterations per generation, with evaluator feedback flowing back to generator
- **Strategic Decision-Making**: Generator decides whether to refine current direction or pivot to entirely different aesthetic based on evaluator scores

Results showed that evaluator assessments improved over iterations before plateauing, with some generations refining incrementally while others took sharp aesthetic turns. Notably, even first-iteration outputs were noticeably better than baseline with no prompting, suggesting the criteria language itself steered the model away from generic defaults.

## Full-Stack Application Development

### Three-Agent Architecture

The harness scales the generator-evaluator pattern to full-stack development using three specialized agents:

#### Planner Agent

- Takes a simple 1-4 sentence prompt and expands it into a full product specification
- Prompted to be ambitious about scope while staying focused on product context and high-level technical design
- Avoids granular technical details upfront to prevent cascading errors
- Weaves [[AI features]] into product specs
- Produces deliverable-focused specifications rather than implementation details

#### Generator Agent

- Works in **sprints**, picking up one feature at a time from the specification
- Implements using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint before handoff to QA
- Uses [[Git]] for version control
- Negotiates **sprint contracts** with evaluator before coding—agreeing on "done" criteria and testable implementation details

#### Evaluator Agent

- Uses [[Playwright]] MCP to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against bugs found and criteria covering:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Each criterion has hard thresholds; failure in any triggers detailed feedback for generator iteration
- Provides specific, actionable findings rather than general commentary

### Sprint Contracts

The sprint contract bridges the gap between high-level user stories and testable implementation:

1. Generator proposes what it will build and how success will be verified
2. Evaluator reviews proposal to ensure generator is building the right thing
3. Agents iterate until agreement is reached
4. Communication handled via files—agents read and respond to each other's written proposals
5. Generator builds against agreed-upon contract before handing work to QA

## Evolution Across Model Versions

### Opus 4.5 Implementation

Initial harness results demonstrated dramatic quality improvements:

| Metric | Solo Agent | Full Harness |
|--------|-----------|-------------|
| Duration | 20 minutes | 6 hours |
| Cost | $9 | $200 |
| Quality | Broken core features | Functional, polished application |

The solo agent produced a retro game maker with layout issues, rigid workflows, and non-functional game mechanics. The full harness produced a feature-rich application with proper editor functionality, working gameplay, AI-assisted design features, and shareable exports.

### Opus 4.6 Simplification

With the release of [[Claude Opus 4.6]], which improved planning, agentic task duration, codebase handling, and code review capabilities, the harness was simplified:

**Removed Components:**
- Sprint construct (model could handle longer coherent tasks)
- Context resets (improved long-context handling eliminated context anxiety)
- Per-sprint evaluations (moved to single pass at end)

**Retained Components:**
- Planner agent (prevented under-scoping)
- Evaluator agent (continued catching edge cases and incomplete features)

**Key Insight**: The evaluator's value is not fixed. It's worth the cost when tasks sit beyond what the current model does reliably solo. As models improve, the boundary of what requires evaluation moves outward.

### DAW Example Results

Using the simplified harness to build a Digital Audio Workstation:

| Phase | Duration | Cost |
|-------|----------|------|
| Planner | 4.7 min | $0.46 |
| Build (Round 1) | 2 hr 7 min | $71.08 |
| QA (Round 1) | 8.8 min | $3.24 |
| Build (Round 2) | 1 hr 2 min | $36.89 |
| QA (Round 2) | 6.8 min | $3.09 |
| Build (Round 3) | 10.9 min | $5.88 |
| QA (Round 3) | 9.6 min | $4.06 |
| **Total** | **3 hr 50 min** | **$124.70** |

The evaluator caught significant gaps: missing interactive features (clip dragging, instrument panels, visual effect editors), stubbed audio recording, and incomplete effect visualizations. These weren't edge cases but core DAW interactions.

## Design Principles

### Core Insights

1. **Task Decomposition**: Breaking complex work into tractable chunks improves agent coherence
2. **Structured Artifacts**: Using files and contracts to hand off context between sessions and agents enables multi-hour autonomous work
3. **Specialized Agents**: Assigning specific roles (planning, generation, evaluation) allows tuning each agent for its particular function
4. **Evaluation Separation**: External feedback from a dedicated evaluator is more effective than self-evaluation
5. **Prompt Engineering**: Grading criteria language directly shapes output character; careful wording steers generation in anticipated and unanticipated ways

### Harness Maintenance Philosophy

Every component in a harness encodes an assumption