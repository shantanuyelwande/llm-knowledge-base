---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-10T06:29:49.255810
raw_file_updated: 2026-06-10T06:29:49.255810
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-10T06:29:49.255810
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to complete complex, long-running tasks effectively. This approach combines multiple specialized agents—such as planners, generators, and evaluators—to decompose problems, maintain coherence across extended sessions, and iteratively improve outputs. Inspired by [[Generative Adversarial Networks]] (GANs), harness design has proven effective for both [[frontend design]] and [[full-stack application development]], with demonstrated improvements in output quality, feature completeness, and functional correctness.

---

## Overview

Harness design is a critical technique for pushing [[AI agents]] beyond their baseline capabilities on complex tasks. Rather than relying on a single agent to complete an entire project, harness design uses multiple specialized agents working in coordination, each addressing specific gaps in model performance.

The approach emerged from practical limitations observed in earlier [[long-running agent]] experiments. While [[prompt engineering]] and [[context engineering]] provided initial improvements, they eventually hit performance ceilings. Harness design breaks through these ceilings by introducing structural decomposition and specialized feedback loops that guide models toward higher-quality outputs.

## Core Problems and Solutions

### Context Degradation in Long Tasks

Models struggle to maintain coherence as context windows fill during extended tasks. Two related issues emerge:

- **Context window saturation**: As conversation history grows, models lose track of earlier context and may become inconsistent
- **Context anxiety**: Some models (notably [[Claude Sonnet 4.5]]) exhibit premature task completion as they approach perceived context limits

**Solutions:**
- **Context resets**: Clearing the conversation history entirely and using [[structured artifacts]] to hand off state between sessions, providing a clean slate for continued work
- **Automatic compaction**: Summarizing earlier conversation portions in-place to maintain continuity while reducing history length (less effective than full resets for context anxiety)

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] exhibit systematic bias toward positive assessment, even when outputs are objectively mediocre. This problem is particularly acute for subjective tasks like [[frontend design]] where no binary verification exists.

**Solution:**
Separating the agent performing work from the agent evaluating it creates external feedback loops that are more tractable to tune than self-critique. While evaluator agents still show leniency toward LLM-generated outputs, this tendency is more correctable through prompt engineering than making generators self-critical.

## Frontend Design Application

### Grading Criteria Framework

The first application of harness design focused on [[frontend design]], where subjective quality was the primary challenge. Rather than attempting to quantify beauty directly, four concrete design principles were established:

1. **Design Quality**: Coherence across colors, typography, layout, and imagery creating distinct mood and identity
2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults; penalizes telltale AI patterns
3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios
4. **Functionality**: Usability and clarity independent of aesthetics

The criteria emphasized design quality and originality over craft and functionality, as models naturally excelled at the latter two while defaulting to generic outputs on the former.

### Generator-Evaluator Loop

The harness architecture for frontend design:

1. **Generator agent**: Creates HTML/CSS/JavaScript frontends based on user prompts
2. **Evaluator agent**: Uses [[Playwright]] MCP to interact with live pages, take screenshots, and grade each criterion with detailed critiques
3. **Feedback loop**: Evaluator feedback returns to generator for iterative refinement (typically 5-15 iterations per generation)

The evaluator was calibrated using few-shot examples with detailed score breakdowns to align judgment with design preferences and reduce score drift across iterations.

### Results

- Iterations showed consistent improvement in design scores before plateauing
- Evaluator feedback drove aesthetic evolution, from incremental refinement to sharp directional pivots
- Prompt wording influenced output character; phrases like "museum quality" steered toward particular visual convergence
- Even first-pass outputs exceeded baseline without evaluator feedback, suggesting criteria themselves guide models away from generic defaults

## Full-Stack Application Development

### Three-Agent Architecture

Building on frontend design insights, harness design for full-stack development introduced a three-agent system addressing specific gaps:

#### Planner Agent
- **Function**: Expands simple user prompts (1-4 sentences) into comprehensive product specifications
- **Scope**: Ambitious feature scope with focus on product context and high-level technical design
- **Approach**: Avoids granular technical details that could cascade into downstream errors; identifies opportunities to integrate AI features
- **Output**: Full product spec with visual design language guidance

#### Generator Agent
- **Function**: Implements features from the specification in sprints
- **Stack**: React, Vite, FastAPI, and SQLite/PostgreSQL
- **Process**: Works one feature at a time with self-evaluation before handoff
- **Tools**: Git version control for tracking changes
- **Optimization**: Self-evaluates work at end of each sprint before QA

#### Evaluator Agent (Quality Assurance)
- **Function**: Validates implementation against specification and quality criteria
- **Method**: Uses [[Playwright]] MCP to click through running applications as users would
- **Testing scope**: UI features, API endpoints, database states, and edge cases
- **Grading**: Evaluates against product depth, functionality, visual design, and code quality
- **Validation**: Each criterion has hard thresholds; failures trigger detailed feedback

### Sprint Contracts

Before implementation, generator and evaluator agents negotiate **sprint contracts** that:
- Define what "done" looks like for each work chunk
- Bridge gap between high-level user stories and testable implementation
- Specify testable behaviors for verification
- Prevent over-specification while ensuring alignment

Communication occurs through files: agents write files, read responses, and iterate until agreement.

### Context Management

The initial harness (using [[Claude Opus 4.5]]) required context resets between sessions due to model context anxiety. Later iterations with [[Claude Opus 4.6]] eliminated this requirement, as the improved model could sustain agentic tasks for longer without premature completion. The harness shifted from per-sprint evaluation to single-pass evaluation at the end.

## Case Studies

### Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness Type | Duration | Cost |
|---|---|---|
| Solo agent | 20 minutes | $9 |
| Full harness | 6 hours | $200 |

**Solo output limitations**:
- Rigid workflow without user guidance
- Broken entity-to-runtime wiring
- Non-functional game despite polished interface

**Harness output advantages**:
- Full viewport utilization with sensible panel sizing
- Consistent visual identity
- Richer sprite editor with better tools
- Functional gameplay with working physics
- Built-in Claude integration for AI-assisted content generation
- 16-feature specification across 10 sprints

### Digital Audio Workstation (DAW)

**Prompt**: "Build a fully featured DAW in the browser using the Web Audio API."

**Simplified harness** (Opus 4.6, no sprint decomposition):
- Planner: 4.7 minutes, $0.46
- Build (Round 1): 2 hr 7 min, $71.08
- QA (Round 1): 8.8 minutes, $3.24
- Build (Round 2): 1 hr 2 min, $36.89
- QA (Round 2): 6.8 minutes, $3.09
- Build (Round 3): 10.9 minutes, $5.88
- QA (Round 3): 9.6 minutes, $4.06
- **Total**: 3 hr 50 min, $124.70

**QA findings** caught critical gaps:
- Non-interactive timeline (clips couldn't be moved)
- Missing instrument UI panels
- Stub-only audio recording
- Unimplemented clip resizing and splitting
- Numeric sliders instead of graphical effect visualizations

**Final output** included:
- Functional arrangement view, mixer, and transport
- Working agent-driven song composition
- Autonomous tool usage for melody, drums, and effects
- Functional music production primitives

## Harness Evolution and Optimization

### Iterative Simplification

As models improve, harness components become less load-bearing. The principle: "find the simplest solution possible, and only increase complexity when needed."

**Optimization approach**:
- Remove one component at a time
- Evaluate impact on final output
- Stress-test assumptions about model limitations
- Recognize that model improvements can make previous scaffolding unnecessary

### Key