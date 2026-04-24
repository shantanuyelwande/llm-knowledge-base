---
title: Harness design for long-running application development _ Anthropic
source_file: Harness design for long-running application development _ Anthropic.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:54:38.841716
raw_file_updated: 2026-04-24T18:54:38.841716
version: 1
sources:
  - file: Harness design for long-running application development _ Anthropic.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:54:38.841716
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical technique for improving [[Large Language Model|LLM]] performance on complex, extended tasks. This approach combines multiple specialized [[AI Agent|agents]] with structured feedback loops to enable autonomous development of full-stack applications. The method was developed at [[Anthropic]] to overcome limitations in [[self-evaluation]] and [[context management]], drawing inspiration from [[Generative Adversarial Networks|GANs]].

## Overview

**Harness design for long-running application development** refers to the architectural patterns and techniques used to enable [[Claude]] and other language models to produce high-quality software and design work over extended periods without human intervention. Rather than relying on a single agent or model instance, effective harnesses decompose complex tasks into manageable components and employ specialized agents for different roles—such as planning, generation, and evaluation.

The key insight is that separating the agent that produces work from the agent that evaluates it creates a powerful feedback mechanism. This separation addresses two fundamental challenges:

1. **Self-evaluation bias**: Models tend to overestimate their own work quality
2. **Context degradation**: Models lose coherence and develop "context anxiety" on lengthy tasks

## Core Challenges and Solutions

### Self-Evaluation Problem

When asked to evaluate their own work, [[AI Agent|agents]] typically respond with unwarranted confidence, even when output quality is mediocre. This problem is particularly acute in subjective domains like [[Frontend Design|frontend design]], where there are no binary correctness checks.

**Solution**: Separate the generation and evaluation functions into distinct agents. The evaluator agent can be tuned to be appropriately skeptical, creating concrete feedback for the generator to iterate against. This external validation proves far more effective than attempting to make a single agent self-critical.

### Context Management Issues

Two related problems emerge as tasks extend:

- **Context window exhaustion**: As conversations grow, models lose coherence as the context window fills
- **Context anxiety**: Models begin wrapping up work prematurely as they approach perceived context limits

**Solutions**:
- **Context resets**: Clear the context window entirely and start fresh agents with structured handoff artifacts carrying previous state (differs from [[compaction]], which summarizes in place)
- **Continuous sessions**: With improved models like [[Claude Opus 4.6]], agents can maintain coherence across longer continuous sessions without resets

## Frontend Design Application

The harness design methodology was first applied to [[Frontend Design|frontend design]], where subjective quality assessment is most challenging.

### Design Evaluation Criteria

Four grading criteria were developed to make aesthetic judgments concrete and gradable:

1. **Design Quality**: Does the design feel like a coherent whole? Colors, typography, layout, imagery, and details combine to create distinct mood and identity
2. **Originality**: Evidence of custom decisions versus template layouts and library defaults; avoids telltale "AI slop" patterns
3. **Craft**: Technical execution including typography hierarchy, spacing, color harmony, and contrast ratios
4. **Functionality**: Usability independent of aesthetics; users can understand the interface and complete tasks

The methodology emphasized design quality and originality over craft and functionality, as [[Claude]] already performed well on the latter dimensions.

### Generator-Evaluator Loop

The frontend design system operated as follows:

- **Generator agent**: Creates HTML/CSS/JavaScript frontend based on user prompt
- **Evaluator agent**: Uses [[Playwright MCP]] to interact with live pages, navigate interfaces, take screenshots, and score against criteria
- **Iteration cycle**: Feedback flows back to generator for refinement; 5-15 iterations per generation
- **Strategic pivoting**: Generator decides whether to refine current direction or pivot to different aesthetic based on evaluation trends

Results showed that evaluator assessments improved over iterations before plateauing. Implementation complexity increased across rounds as the generator attempted more ambitious solutions. The wording of evaluation criteria itself steered generation in significant ways—phrases like "the best designs are museum quality" pushed designs toward particular visual convergence.

## Full-Stack Coding Architecture

The [[GAN]]-inspired pattern was scaled to full-stack application development, mapping naturally onto the software development lifecycle where code review and QA serve the same structural role as design evaluation.

### Three-Agent System

#### Planner Agent

- Takes simple 1-4 sentence user prompt
- Expands into full product specification
- Emphasizes scope and high-level technical design rather than granular implementation details
- Identifies opportunities to weave [[AI Agent|AI features]] into product specs
- Produces detailed feature lists and design language (e.g., 16-feature spec across 10 sprints)

#### Generator Agent

- Works in sprints, implementing one feature at a time from specification
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint
- Uses [[Git]] for version control
- Negotiates "sprint contracts" with evaluator before implementation begins

#### Evaluator Agent

- Uses [[Playwright MCP]] to interact with running applications like end users
- Tests UI features, API endpoints, and database states
- Grades sprints against both identified bugs and quality criteria:
  - Product depth
  - Functionality
  - Visual design
  - Code quality
- Establishes hard thresholds; failed criteria trigger detailed feedback to generator
- Participates in sprint contract negotiation to define "done" criteria before coding

### Sprint Contract Pattern

Before each sprint, generator and evaluator negotiate a contract that:

- Specifies what "done" looks like for that work chunk
- Bridges gap between high-level user stories and testable implementation
- Generator proposes what will be built and how success will be verified
- Evaluator reviews and iterates until agreement reached
- Provides concrete test criteria (e.g., "27 criteria covering the level editor")

Communication occurs via files, with agents writing and reading structured artifacts to maintain context and clarity.

## Implementation Examples

### Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

**Solo agent result** (20 minutes, $9):
- Functional but limited interface
- Rigid workflow requiring unintuitive action sequence
- Broken core gameplay: entities appeared but didn't respond to input
- Wiring between entity definitions and runtime was broken

**Full harness result** (6 hours, $200):
- Planner expanded prompt into 16-feature spec across 10 sprints
- Included sprite animation system, behavior templates, sound effects, AI-assisted sprite generator
- Game export with shareable links
- Coherent visual design language
- Functional gameplay with physics (though with some edge cases)
- Built-in [[Claude]] integration for generative features
- 20x more expensive but dramatically higher quality output

### Digital Audio Workstation (DAW)

**Prompt**: "Build a fully featured DAW in the browser using the Web Audio API."

**Updated harness results** (3 hours 50 minutes, $124.70):
- Removed sprint decomposition construct (Opus 4.6 capability improvement)
- Single QA pass at end rather than per-sprint evaluation
- Planner created comprehensive specification
- Generator maintained coherence over 2+ hour build sessions
- QA identified real gaps:
  - Feature completeness issues (clips couldn't be dragged, no instrument UI panels)
  - Audio recording stub-only implementation
  - Missing clip resize and split functionality
  - Numeric-only effect visualizations without graphical representations
- Final app included working arrangement view, mixer, transport, and agent-driven composition

## Model Improvements and Harness Evolution

### Opus 4.5 vs. Opus 4.6

[[Claude Opus 4.5]] exhibited strong [[context anxiety]], requiring [[context reset|context resets]] between sessions. [[Claude Opus 4.6]] largely eliminated this behavior, enabling:

- More careful planning
- Sustained agentic tasks for longer
- More reliable operation in larger codebases
- Better code review and debugging skills
- Improved long-context retrieval

### Simplification Strategy

As models improved, harness components that were previously load-bearing became unnecessary overhead. The principle: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing."

**Methodical simplification approach**:
1. Remove one component at a time
2. Review impact on final results
3. Keep components that add clear value
4. Planner remained valuable (prevented under-scoping)
5. Evaluator value depended on task difficulty relative to model capabilities

The evaluator's usefulness is not binary but contextual—worth the cost when tasks exceed what the model handles reliably solo.

## Key Insights and Principles

### Effective Harness Design

1. **Specialize agents by role**: Different agents for planning, generation, and evaluation capture different aspects of complex work