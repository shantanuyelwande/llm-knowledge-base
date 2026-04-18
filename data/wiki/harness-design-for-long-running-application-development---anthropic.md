---
title: Harness design for long-running application development _ Anthropic
source_file: Harness design for long-running application development _ Anthropic.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:55:09.797988
raw_file_updated: 2026-04-17T20:55:09.797988
version: 1
sources:
  - file: Harness design for long-running application development _ Anthropic.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:55:09.797988
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration systems used to enable [[AI agents]] to perform complex, long-running tasks with improved coherence, quality, and reliability. This article describes work by Anthropic researchers on applying multi-agent architectures inspired by [[Generative Adversarial Networks]] (GANs) to both [[frontend design]] and [[autonomous software engineering]]. The key innovation separates task execution from evaluation, allowing feedback loops that drive higher-quality outputs than single-agent systems.

---

## Overview

Harness design is a critical component of [[agentic AI]] development that addresses fundamental limitations in how [[large language models]] (LLMs) perform extended tasks. Rather than relying on single-pass generation or self-evaluation (which tends to produce mediocre results), effective harnesses decompose complex work into specialized agent roles with structured handoffs between them.

The research demonstrates that well-designed harnesses can produce full-stack applications spanning multiple hours of autonomous development, with significantly higher quality than baseline single-agent approaches—though at substantially higher computational cost.

---

## Core Problems with Naive Implementations

### Context Management Issues

Long-running tasks expose two critical limitations in model behavior:

1. **Context Window Degradation**: As the [[context window]] fills during extended tasks, models tend to lose coherence and make poor decisions. Models may also exhibit **context anxiety**—a tendency to prematurely wrap up work as they approach perceived context limits.

2. **Solutions**:
   - **Context Resets**: Clearing the context window entirely and starting fresh with a structured handoff preserves state while giving the agent a clean slate. This approach is more effective than [[compaction]], which summarizes earlier conversation history in place.
   - **Continuous Sessions**: With improved models like [[Claude Opus 4.6]], continuous sessions with automatic compaction can handle longer tasks without explicit resets.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] exhibit systematic bias toward positive assessment, even when output quality is objectively mediocre. This problem is particularly pronounced in subjective domains like [[design]], where there are no binary correctness checks.

**Key insight**: Separating the agent performing work from the agent evaluating it creates a strong lever for quality improvement. While evaluator agents remain somewhat lenient toward LLM-generated outputs, tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work.

---

## Frontend Design: Making Subjectivity Gradable

### Design Evaluation Criteria

To address the challenge of evaluating subjective aesthetic quality, the research developed four grading criteria that could be applied consistently:

1. **Design Quality**: Does the design feel cohesive rather than a collection of disconnected parts? Do colors, typography, layout, and imagery combine to create distinct mood and identity?

2. **Originality**: Is there evidence of custom decisions, or are these template layouts and AI-generated patterns? Human designers should recognize deliberate creative choices; unmodified stock components and telltale signs of AI generation (like purple gradients) fail this criterion.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check rather a creativity check.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

The research emphasized **design quality** and **originality** over craft and functionality, since Claude already performed well on technical competence. The criteria explicitly penalized generic "AI slop" patterns.

### Generator-Evaluator Loop

The frontend design harness operated as follows:

- A **generator agent** created HTML/CSS/JS frontends based on user prompts
- An **evaluator agent** with access to [[Playwright MCP]] interacted with live pages, screenshotting and studying implementations before scoring each criterion with detailed critique
- Feedback flowed back to the generator for iterative refinement
- Typical runs involved 5-15 iterations per generation, with each cycle taking real wall-clock time (full runs up to 4 hours)
- The generator made strategic decisions after each evaluation: refine the current direction if scores improved, or pivot to a different aesthetic if the approach wasn't working

### Results and Insights

- Evaluator assessments improved over iterations before plateauing, with headroom remaining for further improvement
- The wording of criteria steered generator behavior in ways not fully anticipated (e.g., phrases like "museum quality" pushed toward particular visual convergence)
- Scores didn't always improve linearly; later implementations were generally better but individual middle iterations were sometimes preferable
- Implementation complexity increased across rounds as generators reached for more ambitious solutions
- Even first-iteration outputs were noticeably better than baseline, suggesting criteria and associated language steered the model away from generic defaults before evaluator feedback

**Notable example**: A Dutch art museum website that evolved from a conventional dark-themed landing page into a 3D spatial experience with a checkered floor, artwork hung on walls, and doorway-based navigation between gallery rooms—a creative leap not seen in single-pass generation.

---

## Full-Stack Coding Architecture

### Three-Agent System

Building on the frontend design insights, the research developed a three-agent architecture for autonomous full-stack development:

#### Planner Agent
- Takes a simple 1-4 sentence user prompt and expands it into a full product specification
- Instructed to be ambitious about scope while staying focused on product context and high-level technical design rather than implementation details
- Avoids over-specifying technical details that could cascade errors downstream
- Integrates opportunities to weave [[AI features]] into product specs

#### Generator Agent
- Implements features one at a time from the spec (sprint-based in original version)
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint before handoff to QA
- Has access to [[git]] for version control
- In later iterations, builds applications without sprint decomposition

#### Evaluator Agent
- Uses [[Playwright MCP]] to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against both identified bugs and quality criteria covering product depth, functionality, visual design, and code quality
- Each criterion has a hard threshold; failure requires generator iteration
- Negotiates **sprint contracts** with the generator before implementation begins, defining what "done" looks like and testable success criteria

### Communication and Handoffs

Communication between agents occurs via files:
- One agent writes a file; another reads and responds
- Responses may occur within the same file or in new files for asynchronous handoffs
- This approach maintains faithfulness to specifications without over-specification of implementation

### Evaluator Tuning

Getting the evaluator to perform effectively required significant work:

- Out of the box, Claude is a poor QA agent, identifying issues then talking itself into approving work anyway
- Early evaluators tested superficially rather than probing edge cases, allowing subtle bugs to slip through
- Tuning involved reading evaluator logs, finding judgment divergences, and updating prompts iteratively
- Several rounds of development were needed before evaluator grading became reasonable
- Even after tuning, output showed limits in QA capabilities: small layout issues, unintuitive interactions, and undiscovered bugs in nested features

**Representative issues caught by evaluators**:
- Rectangle fill tool only placing tiles at drag endpoints instead of filling regions
- Delete key handler requiring both `selection` and `selectedEntityId` when only one should be needed
- FastAPI route ordering causing 'reorder' to be matched as a frame_id integer

---

## Initial Results: Retro Game Maker

### Experimental Setup

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness Type | Duration | Cost |
|---|---|---|
| Solo (single-agent) | 20 min | $9 |
| Full harness (three-agent) | 6 hr | $200 |

### Solo Run Limitations

- Layout wasted space with fixed-height panels
- Workflow was rigid and didn't guide users through proper sequence
- **Critical failure**: Game was broken—entities appeared but didn't respond to input
- Code showed broken wiring between entity definitions and game runtime

### Full Harness Results

- Planner expanded one-sentence prompt into 16-feature spec across ten sprints
- Included core editors, animation system, behavior templates, sound/music, AI-assisted sprite generator, level designer, and shareable game exports
- Visual design language integrated into spec via frontend design skill
- Immediately showed more polish: canvas used full viewport, panels sized sensibly, consistent visual identity
- Sprite editor richer and more featured than solo run
- **Critical success**: Play mode actually worked—users could move entities and play games
- Physics had rough edges (character overlapping platforms)