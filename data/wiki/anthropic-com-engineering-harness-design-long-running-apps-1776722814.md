---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-23T04:55:43.441341
raw_file_updated: 2026-04-23T04:55:43.441341
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-23T04:55:43.441341
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to complete complex, long-running tasks effectively. This article explores techniques developed by [[Anthropic]] for improving [[AI]] performance on extended coding and design tasks through multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs). Key innovations include separating generation from evaluation, implementing context resets, and using structured handoffs between specialized agents.

---

## Overview

Harness design is critical for achieving high-quality outputs when deploying [[AI agents]] for extended autonomous tasks. While [[prompt engineering]] and basic agent architectures can handle simple problems, complex applications—particularly those requiring subjective judgment or spanning multiple hours of computation—require more sophisticated orchestration patterns.

The work presented here addresses two persistent challenges in long-running [[AI]] applications:

1. **Context degradation**: Models lose coherence as context windows fill during extended tasks
2. **Self-evaluation bias**: Agents tend to overestimate the quality of their own work

---

## Core Problems with Naive Implementations

### Context Window Management

Long-running tasks create two related problems for [[language models]]:

**Context anxiety** occurs when models believe they are approaching their context limit and begin prematurely wrapping up work. While [[context compaction]] (summarizing earlier conversation history) can help, it doesn't provide the clean slate needed to fully resolve the issue.

**Context resets** offer a stronger solution: completely clearing the context window and starting fresh with a [[structured handoff]] that carries forward essential state. This approach:
- Eliminates context anxiety entirely
- Provides a clean slate for continued work
- Adds [[orchestration]] complexity and [[token]] overhead
- Requires well-designed [[artifacts]] to maintain continuity

Earlier work with [[Claude Sonnet 4.5]] demonstrated that context resets were essential, though newer models like [[Claude Opus 4.6]] exhibit this behavior less strongly due to improved long-context capabilities.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently overestimate quality, particularly on subjective tasks like design where no binary verification exists. This tendency persists even on objectively verifiable tasks.

**Solution**: Separating the generating agent from the evaluating agent creates external feedback that the generator can iterate against. While evaluator [[language models]] still lean toward leniency toward [[AI]]-generated outputs, tuning a standalone evaluator to be skeptical proves far more tractable than making a generator self-critical.

---

## Frontend Design: Making Subjectivity Gradable

### The Challenge

Without intervention, [[Claude]] gravitates toward safe, technically functional but visually unremarkable designs. The core insight is that while aesthetics cannot be fully reduced to objective scores, they can be improved by grounding evaluation in concrete design principles.

### Evaluation Criteria

Four grading criteria were developed to guide both generator and evaluator:

1. **Design Quality**: Does the design feel coherent rather than a collection of parts? Strong work combines colors, typography, layout, imagery, and details to create distinct mood and identity.

2. **Originality**: Evidence of custom decisions versus template layouts and library defaults. Unmodified stock components and telltale [[AI]] patterns (purple gradients, generic cards) fail this criterion.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check; most reasonable implementations pass by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks?

The harness weighted design quality and originality more heavily, as [[Claude]] already performed well on craft and functionality by default.

### Architecture and Results

**Implementation**:
- Generator agent created HTML/CSS/JavaScript frontends based on prompts
- Evaluator agent used [[Playwright MCP]] to interact with live pages before scoring
- Feedback loop ran 5-15 iterations per generation
- Full runs extended up to 4 hours

**Key Findings**:
- Evaluator assessments improved over iterations before plateauing
- Criterion wording steered outputs in unexpected ways (phrases like "museum quality" influenced aesthetic direction)
- Even first-iteration outputs exceeded baseline significantly
- Later iterations sometimes showed worse subjective quality than intermediate versions despite higher scores
- Implementation complexity increased across rounds as generators pursued more ambitious solutions

**Notable Example**: A website for a Dutch art museum evolved from a conventional dark-themed landing page to a spatial 3D experience with a checkered floor, freely positioned artwork, and room-based navigation—a creative leap not typically seen in single-pass generation.

---

## Full-Stack Application Development

### Three-Agent Architecture

Applying [[GAN]]-inspired patterns to full-stack coding required three specialized agents:

#### Planner Agent

**Role**: Expands brief prompts into comprehensive product specifications

**Characteristics**:
- Takes 1-4 sentence prompts and generates full feature lists
- Emphasizes ambitious scope while focusing on product context rather than implementation details
- Avoids over-specifying technical details that could cascade errors downstream
- Identifies opportunities to weave [[AI features]] into product specs

**Rationale**: Automating spec generation allows the system to expand scope beyond what users initially articulate, while letting downstream agents determine implementation paths.

#### Generator Agent

**Role**: Implements features in iterative sprints using modern full-stack stack

**Technology Stack**:
- Frontend: [[React]], [[Vite]]
- Backend: [[FastAPI]]
- Database: [[SQLite]] or [[PostgreSQL]]
- Version Control: [[Git]]

**Approach** (in original harness):
- Works one feature at a time from the spec
- Self-evaluates work at end of each sprint
- Negotiates "sprint contracts" with evaluator before implementation
- Hands off structured artifacts between sessions

#### Evaluator Agent (QA)

**Role**: Tests implementation against spec and quality criteria

**Methods**:
- Uses [[Playwright MCP]] to click through running applications like a user
- Tests UI features, [[API]] endpoints, and database states
- Grades against adapted design criteria (product depth, functionality, visual design, code quality)
- Each criterion has hard thresholds; failure triggers detailed feedback
- Negotiates sprint contracts before implementation begins

**Sprint Contract**: A pre-implementation agreement between generator and evaluator defining:
- What "done" looks like for that work chunk
- Testable success criteria
- Prevents over-specification while ensuring implementation fidelity

### Initial Results: Retro Game Maker

**Comparison Setup**:
- Prompt: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode"
- Solo agent run: 20 minutes, $9
- Full harness run: 6 hours, $200

**Solo Run Issues**:
- Layout wasted space with fixed-height panels
- Rigid workflow with no UI guidance for proper sequence
- Core functionality broken: entities appeared but didn't respond to input
- Entity-to-runtime wiring broken with no surface indication

**Harness Run Advantages**:
- Planner expanded one-sentence prompt into 16-feature spec across 10 sprints
- Included sprite animation system, behavior templates, sound effects, AI-assisted generation, and shareable export
- Polish and consistency throughout interface
- Sprite editor richer and more fully featured
- Built-in Claude integration for game generation
- Playable game with working physics (though with edge cases)

**Key Insight**: 20x cost differential produced immediately apparent quality differences in both functionality and design coherence.

### Evaluator Tuning

Out-of-the-box [[Claude]] performs poorly as a [[QA]] agent:
- Identifies legitimate issues then talks itself out of reporting them
- Tests superficially rather than probing edge cases
- Subtle bugs slip through undetected

**Tuning Process**:
- Read evaluator logs and identify judgment divergences
- Updated QA prompts to address specific gaps
- Required several iterations before reasonable grading
- Even after tuning, limitations remained (layout issues, unintuitive interactions, undiscovered deeply-nested bugs)

**Specific Issues Caught**:
- Rectangle fill tool only placing tiles at endpoints instead of filling region
- Entity deletion requiring contradictory conditions in code
- Route ordering causing FastAPI to misparse parameters

---

## Harness Simplification with Opus 4.6

### Removing Load-Bearing Assumptions

As models improve, harness complexity should be re-evaluated. The principle: "find the simplest solution possible, and only increase complexity when needed."

**Key Insight**: Every harness component encodes an assumption about model limitations. These assumptions warrant stress-testing as models improve.

### Sprint Construct Removal

**Original Purpose**: Decompose work into chunks for coherent model processing

**Change**: Removed sprint structure entirely with [[Opus 