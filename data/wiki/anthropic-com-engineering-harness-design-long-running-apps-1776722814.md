---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:30:00.753930
raw_file_updated: 2026-06-07T06:30:00.753930
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:30:00.753930
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the structured architecture and orchestration patterns used to enable [[AI agents]] to work effectively on complex, multi-hour coding tasks and creative projects. By combining multiple specialized agents (planner, generator, evaluator) with careful task decomposition and context management, sophisticated applications can be built autonomously. This approach draws inspiration from [[Generative Adversarial Networks]] (GANs) and addresses key challenges in long-running agentic systems, including context window limitations and poor self-evaluation.

---

## Overview

Harness design is a critical technique for pushing [[AI coding agents]] beyond their baseline capabilities on complex tasks. Rather than relying on a single agent to handle an entire project, effective harnesses decompose work across multiple specialized agents, each addressing specific gaps in model performance. This approach has proven particularly valuable for building complete applications without human intervention, combining high-quality frontend design with functional backend systems.

The core insight is that while individual models have limitations on extended tasks, carefully orchestrated multi-agent systems can achieve results that are orders of magnitude better than single-pass generation, despite significantly higher computational costs.

## Key Problems with Naive Implementations

### Context Window and Context Anxiety

[[Long-running agents]] face two related challenges as they work on extended tasks:

1. **Context window filling**: As conversation history grows, the model's available context shrinks, eventually forcing the agent to conclude work prematurely or lose access to earlier information.

2. **Context anxiety**: Some models, notably [[Claude Sonnet 4.5]], exhibit a tendency to begin wrapping up work when they perceive they're approaching their context limit, even when substantial work remains.

**Solution**: [[Context resets]] provide a clean slate by clearing the conversation history entirely and starting a fresh agent session. Rather than [[compaction]] (summarizing earlier conversation in place), resets prevent context anxiety from persisting. However, resets require structured handoff artifacts that preserve sufficient state for the next agent to continue work effectively. This approach trades orchestration complexity and latency for improved long-task performance.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] demonstrate systematic bias toward positive assessment, even when objective quality is mediocre. This problem is particularly acute for subjective tasks like [[frontend design]], where there is no binary correctness check.

**Solution**: Separating the agent performing work from the agent evaluating it creates a stronger feedback mechanism. While external evaluators are still inclined toward leniency, they are more amenable to prompt tuning toward skepticism than generators are toward self-criticism. Once external feedback exists, generators have concrete targets to iterate against.

## Frontend Design: Making Subjective Quality Gradable

### Design Grading Criteria

To address the challenge of evaluating subjective design quality, a framework of four concrete criteria was developed:

1. **Design Quality**: Does the design feel like a coherent whole? Strong work combines colors, typography, layout, imagery, and details to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions rather than template layouts and library defaults. Avoids telltale signs of [[AI-generated content]] like generic patterns and purple gradients.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. A competence check rather than creativity check.

4. **Functionality**: Usability independent of aesthetics. Users can understand the interface, find primary actions, and complete tasks without guessing.

The framework emphasized design quality and originality over craft and functionality, since [[Claude]] naturally excels at the latter while tending toward bland outputs on the former.

### Generator-Evaluator Loop

The frontend design harness implemented a feedback loop inspired by [[Generative Adversarial Networks]]:

- **Generator agent**: Creates HTML/CSS/JavaScript frontends based on user prompts
- **Evaluator agent**: Uses [[Playwright MCP]] to interact with live pages, screenshots them, and scores each criterion with detailed critique
- **Iteration**: Generator receives evaluator feedback and refines the design, with 5-15 iterations per generation

Evaluator calibration used few-shot examples with detailed score breakdowns to ensure judgment aligned with design preferences and reduced score drift across iterations.

### Results and Observations

- Designs improved noticeably even on first iteration, suggesting that criteria wording itself steered the model away from generic defaults
- Iteration patterns were not always linearly improving; later implementations were generally better but individual iterations sometimes peaked earlier
- Implementation complexity increased across rounds as the generator pursued more ambitious solutions
- Wording in criteria (e.g., "museum quality") significantly influenced output character
- Notable example: A museum website progressed from conventional dark-themed design to an innovative 3D spatial experience with CSS perspective rendering

## Full-Stack Application Development

### Three-Agent Architecture

The principles from frontend design scaled to full-stack development through a three-agent system:

#### Planner Agent

- Takes a simple 1-4 sentence user prompt and expands it into a comprehensive product specification
- Emphasizes ambitious scope and high-level technical direction rather than granular implementation details
- Weaves [[AI features]] into product specs to enhance user workflows
- Produces specifications that guide downstream work without over-constraining implementation

#### Generator Agent

- Implements features in [[sprint]] cycles, picking up one feature at a time from the specification
- Works with modern stack: [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]]
- Performs self-evaluation at end of each sprint before handoff
- Uses [[Git]] for version control
- Negotiates sprint contracts with evaluator before implementation

#### Evaluator Agent

- Uses [[Playwright MCP]] to interact with running applications like an actual user
- Tests UI features, API endpoints, and database states
- Grades each sprint against criteria covering product depth, functionality, visual design, and code quality
- Each criterion has hard thresholds; failure on any criterion triggers detailed feedback for generator iteration
- Negotiates sprint contracts before work begins, bridging gap between user stories and testable implementation

### Sprint Contracts

Sprint contracts establish agreement between generator and evaluator on what "done" looks like before code is written. This mechanism:

- Bridges the gap between high-level user stories and testable implementation details
- Allows generator to propose what it will build and how success will be verified
- Enables evaluator to ensure the generator builds the right thing
- Prevents over-specification of implementation details upfront
- Typically contain 20+ specific, testable criteria per sprint

### Communication Pattern

Agents communicate through files rather than direct conversation:
- One agent writes a file
- Next agent reads and responds either within that file or with a new file
- Previous agent reads response and continues

This approach maintains context clarity and creates an auditable record of decisions.

## Case Study: Retro Game Maker

### Comparison: Solo vs. Full Harness

A simple prompt to "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode" was run through both approaches:

| Approach | Duration | Cost |
|----------|----------|------|
| Solo Agent | 20 min | $9 |
| Full Harness | 6 hours | $200 |

**Solo Output Issues:**
- Fixed-height panels wasted viewport space
- Rigid workflow without clear guidance on sprite/entity creation sequence
- Core game functionality broken: entities appeared but didn't respond to input
- Entity-to-runtime wiring completely non-functional

**Harness Output Advantages:**
- Polished interface with full viewport utilization
- Consistent visual identity from design spec
- Rich, feature-complete sprite editor
- Functional game editor and playable test mode
- Built-in [[Claude integration]] for AI-assisted game design
- Planner expanded 1-sentence prompt into 16-feature spec across 10 sprints

### Evaluator Feedback Examples

The evaluator caught specific, actionable issues:

| Contract Criterion | Finding |
|-------------------|---------|
| Rectangle fill tool allows click-drag to fill rectangular area | **FAIL** — Tool only places tiles at drag start/end points. `fillRectangle` function exists but isn't triggered properly on mouseUp. |
| User can select and delete placed entity spawn points | **FAIL** — Delete key handler requires both `selection` and `selectedEntityId`, but clicking entity only sets `selectedEntityId`. |
| User can reorder animation frames via API | **FAIL** — `PUT /frames/reorder` route defined after `/{frame_id}` routes, causing FastAPI to match 'reorder' as frame_id. |

## Iterating on the Harness: Simplification with Opus 4.6

### Removing the Sprint Construct

As [[Claude Opus 4.6]] was released with improvements in planning, long-context reasoning, and code review capabilities, the harness was systematically simplified:

- **Removed**: Sprint-based decomposition, which Opus 4.6 could