---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-03T05:35:34.420683
raw_file_updated: 2026-05-03T05:35:34.420683
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-03T05:35:34.420683
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to reliably complete complex, long-running tasks. This article explores how [[Anthropic]] researchers developed multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs) to improve both [[frontend design]] quality and full-stack application development. The key innovation separates the roles of generation and evaluation into distinct agents, enabling iterative refinement and higher-quality outputs than single-agent approaches.

---

## Overview

Harness design has emerged as a critical factor in advancing [[agentic coding]] capabilities. Rather than relying on a single agent to complete complex tasks, effective harnesses decompose work into specialized roles, each addressing specific gaps in model performance.

This work, conducted by Prithvi Rajasekaran at [[Anthropic Labs]], demonstrates how novel AI engineering approaches can break through performance ceilings in both subjective domains (like design) and objective ones (like software development).

---

## The Problem with Naive Implementations

### Context Window Limitations

Long-running tasks present two persistent challenges:

1. **Context Window Degradation**: As the [[context window]] fills during extended tasks, models tend to lose coherence. This problem is distinct from simple token limits.

2. **Context Anxiety**: Some models, notably [[Claude Sonnet 4.5]], exhibit "context anxiety"—a tendency to prematurely wrap up work as they approach what they perceive as their context limit.

**Solutions**: 
- **Context Resets**: Clearing the entire context window and starting fresh with a structured handoff artifact preserves state better than compaction alone
- **Compaction**: Summarizing earlier conversation in place allows the same agent to continue, but doesn't eliminate context anxiety
- **Structured Artifacts**: Using files or data structures to carry forward previous agent state across sessions

### Self-Evaluation Bias

A second critical failure mode is **self-evaluation bias**. When asked to evaluate their own work, [[AI models]] consistently skew positive, praising mediocre outputs with confidence. This problem is particularly acute in subjective domains like [[design]] but also affects objective tasks.

**Solution**: Separating the agent doing the work from the agent evaluating it creates a feedback loop that drives improvement. While evaluator agents still exhibit some leniency toward LLM-generated outputs, they can be tuned to be appropriately skeptical through careful prompting and calibration.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without intervention, [[Claude]] typically produces safe, technically functional but visually unremarkable designs. The core problem is that subjective aesthetic judgments resist quantification.

### The Approach

The solution involved two insights:

1. **Grading Criteria as Anchors**: While aesthetics can't be fully reduced to scores, they can be improved by encoding design principles into concrete, gradable criteria
2. **Generator-Evaluator Loop**: Separating generation from evaluation creates feedback that drives the generator toward stronger outputs

### Four Grading Criteria

The harness used four criteria, weighted to emphasize areas where Claude needed improvement:

| Criterion | Definition | Weight |
|-----------|-----------|--------|
| **Design Quality** | Does the design feel like a coherent whole? Do colors, typography, layout, and imagery combine to create a distinct mood and identity? | High |
| **Originality** | Evidence of custom decisions vs. template layouts and AI-generated patterns. Are there deliberate creative choices? | High |
| **Craft** | Technical execution: typography hierarchy, spacing, color harmony, contrast ratios. Competence check. | Medium |
| **Functionality** | Usability independent of aesthetics. Can users understand, find actions, and complete tasks? | Medium |

### Implementation

- **Generator Agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator Agent**: Used [[Playwright MCP]] to interact with live pages, taking screenshots and studying implementations before scoring
- **Iteration Loop**: 5-15 iterations per generation, with evaluator feedback driving refinement
- **Wall-Clock Time**: Full runs stretched up to 4 hours

### Key Findings

- Evaluator assessments improved over iterations before plateauing
- Prompting language directly shaped output character (e.g., "museum quality" pushed toward specific visual convergence)
- Later implementations were generally better, but not always linearly—some middle iterations were preferred to final versions
- Even first-iteration outputs were noticeably better than baseline with no prompting, suggesting criteria language itself steered the model away from generic defaults

### Notable Example: Museum Website

When prompted to create a website for a Dutch art museum, the model produced a clean, dark-themed landing page by iteration nine. At iteration ten, it scrapped the approach entirely and reimagined the site as a spatial 3D experience with a checkered floor, artwork hung on walls, and doorway-based navigation—a creative leap not typically seen in single-pass generation.

---

## Full-Stack Application Development

### The Architecture

Building on earlier [[long-running harness]] work, the system employed three specialized agents:

#### Planner Agent

- **Role**: Expands simple 1-4 sentence prompts into full product specifications
- **Approach**: Ambitious on scope, focused on product context and high-level technical design rather than implementation details
- **Innovation**: Identifies opportunities to weave [[AI features]] into product specs
- **Rationale**: Avoids cascading errors from over-specified technical details

#### Generator Agent

- **Role**: Implements features in sprints using [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]]
- **Approach**: One feature at a time, with self-evaluation before handoff to QA
- **Tools**: Git for version control
- **Key Improvement**: Removed sprint construct in later versions when [[Claude Opus 4.6]] demonstrated sufficient capability

#### Evaluator Agent

- **Role**: Quality assurance through automated testing and grading
- **Tools**: [[Playwright MCP]] for clicking through running applications like a user would
- **Testing**: UI features, API endpoints, database states
- **Grading**: Against product-adapted criteria (depth, functionality, design, code quality)
- **Innovation**: **Sprint Contract** negotiation—generator and evaluator agree on "done" before coding begins

### Sprint Contracts

A critical innovation in the harness is the sprint contract mechanism:

1. **Generator proposes** what it will build and how success will be verified
2. **Evaluator reviews** the proposal to ensure the right thing is being built
3. **Both iterate** until agreement is reached
4. **Generator builds** against the agreed contract
5. **Evaluator tests** against contract criteria

This bridges the gap between high-level user stories and testable implementations without over-specifying too early.

### Communication Pattern

Agents communicate via files rather than direct conversation:
- One agent writes a file
- Another agent reads and responds in that file or creates a new file
- This keeps work faithful to specifications while maintaining flexibility

---

## Case Study: Retro Video Game Maker

### Comparison: Solo vs. Full Harness

| Aspect | Solo Agent | Full Harness |
|--------|-----------|--------------|
| **Duration** | 20 minutes | 6 hours |
| **Cost** | $9 | $200 |
| **Cost Multiplier** | — | 22x |
| **Scope** | Basic editors and play mode | 16 features across 10 sprints |
| **Quality** | Broken core gameplay | Fully functional game |

### Solo Run Results

The solo agent produced an application that appeared functional initially but had critical flaws:
- Layout wasted space with fixed-height panels
- Workflow was rigid with no UI guidance for proper sequence
- **Core feature broken**: Entities didn't respond to input; wiring between entity definitions and game runtime was broken

### Full Harness Results

The harness-generated application demonstrated:
- Polish and smoothness throughout interface
- Full viewport utilization with sensible panel sizing
- Consistent visual identity tracking design direction
- Richer sprite editor with cleaner tool palettes
- **Integrated AI features** for generating game components
- **Functional gameplay**: Users could move entities and play the game
- Minor physics edge cases (character overlapping platforms) but core functionality worked

### Evaluator Findings

The evaluator caught critical issues that would have gone unnoticed:

| Contract Criterion | Finding |
|-------------------|---------|
| Rectangle fill tool fills rectangular area | **FAIL** — Only places tiles at endpoints; `fillRectangle` function exists but isn't triggered on mouseUp |
| User can delete entity spawn points | **FAIL** — Delete handler requires both `selection` and `selectedEntityId`, but clicking only sets `selectedEntityId` |
| User can reorder animation frames via API | **FAIL** — Route