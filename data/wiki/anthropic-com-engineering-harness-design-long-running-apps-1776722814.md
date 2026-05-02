---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:15:44.889822
raw_file_updated: 2026-05-02T05:15:44.889822
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:15:44.889822
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and scaffolding used to enable [[AI agents]] to effectively build complex applications over extended periods. This article explores how [[Anthropic]] engineers developed novel harness architectures inspired by [[Generative Adversarial Networks]] (GANs) to improve [[Claude]]'s performance on both subjective tasks like [[frontend design]] and objective tasks like [[full-stack software development]]. The work demonstrates that separating evaluation from generation, decomposing complex tasks, and using [[context engineering]] techniques can produce significantly higher-quality outputs than naive single-agent approaches.

---

## Overview

Harness design has emerged as a critical practice at the frontier of [[agentic coding]]. Rather than relying on a single [[language model]] to complete complex tasks in isolation, effective harnesses employ multiple specialized agents working in coordination, structured handoffs between sessions, and systematic evaluation mechanisms. This approach enables [[AI systems]] to build complete, functional applications that would exceed the capabilities of baseline models.

The key insight is that harness complexity should be justified by concrete performance gains. As models improve, harnesses should be continuously re-evaluated and simplified, removing components that are no longer load-bearing while adding new capabilities that become possible with enhanced model abilities.

---

## The Problem: Why Naive Implementations Fall Short

### Context Window Limitations

[[Long-running tasks]] present fundamental challenges for [[language models]]. As context windows fill during extended work sessions, models exhibit two related failure modes:

1. **Loss of Coherence**: Models tend to lose track of earlier decisions and context as the conversation history grows, leading to inconsistent implementations and poor architectural decisions.

2. **Context Anxiety**: Some models, particularly [[Claude Sonnet 4.5]], exhibit "context anxiety"—a tendency to wrap up work prematurely as they approach their perceived context limit, even when substantial work remains.

### Context Resets vs. Compaction

Two approaches exist for managing context growth:

- **Compaction**: Summarizing earlier parts of the conversation in place, allowing the same agent to continue on a shortened history. While this preserves continuity, it doesn't eliminate context anxiety.

- **Context Resets**: Clearing the context window entirely and starting a fresh agent, combined with [[structured artifacts]] that carry the previous agent's state. This provides a clean slate but adds orchestration complexity and token overhead.

The [[Anthropic]] team found that [[Claude Sonnet 4.5]] required context resets to perform well on lengthy tasks, while newer models like [[Claude Opus 4.6]] largely eliminated this behavior natively.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agents]] consistently exhibit positive bias, praising outputs even when quality is mediocre. This problem is particularly acute for subjective tasks like [[design]] where no binary verification criterion exists. Separating the agent performing work from the agent evaluating it proves to be a strong lever for addressing this issue.

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

[[Claude]] naturally gravitates toward safe, predictable layouts that are technically functional but visually unremarkable. To push beyond this baseline, the team needed a method to make subjective aesthetic judgments gradable and actionable.

### Design Grading Criteria

Four explicit criteria were developed to guide both generator and evaluator agents:

1. **Design Quality**: Does the design feel like a coherent whole rather than a collection of parts? Strong work combines colors, typography, layout, imagery, and other details to create a distinct mood and identity.

2. **Originality**: Is there evidence of custom creative decisions, or does the design rely on template layouts and library defaults? The criterion explicitly penalizes "AI slop" patterns like purple gradients over white cards.

3. **Craft**: Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This is a competence check; most reasonable implementations succeed here by default.

4. **Functionality**: Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

The team weighted design quality and originality more heavily than craft and functionality, since [[Claude]] already performed well on the latter two dimensions by default.

### The Generator-Evaluator Loop

The harness operated as follows:

1. A **generator agent** created HTML/CSS/JavaScript frontends based on user prompts
2. An **evaluator agent** used [[Playwright MCP]] to interact with the live page directly
3. The evaluator scored each criterion and provided detailed critique
4. Feedback flowed back to the generator for iteration
5. The generator made strategic decisions: refine the current direction if scores improved, or pivot to an entirely different aesthetic if the approach wasn't working

Runs typically involved 5-15 iterations, with each cycle pushing the generator in more distinctive directions. Full runs stretched up to four hours.

### Key Findings

- The wording of evaluation criteria steered generator output in unanticipated ways (e.g., including "museum quality" in criteria pushed designs toward particular visual convergence)
- Even on the first iteration, outputs were noticeably better than baseline, suggesting criteria language itself shaped behavior
- Iteration patterns were not always linearly improving; later implementations were generally better overall, but specific middle iterations sometimes proved superior
- The generator demonstrated creative leaps—in one case, reimagining a museum website as a 3D spatial experience with CSS perspective rendering

---

## Scaling to Full-Stack Coding

### Three-Agent Architecture

Building on insights from the [[frontend design]] work, the team developed a three-agent system for autonomous [[full-stack development]]:

#### Planner Agent

- Takes a simple 1-4 sentence prompt and expands it into a full product specification
- Deliberately ambitious about scope, focusing on product context and high-level technical design rather than granular implementation details
- Avoids over-specifying technical details upfront to prevent cascading errors
- Identifies opportunities to weave [[AI features]] into product specifications
- Reads and applies [[frontend design skills]] to create visual design language

#### Generator Agent

- Works in [[sprints]], implementing one feature at a time from the specification
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Maintains version control with [[Git]]
- Self-evaluates work at the end of each sprint before handing off to QA
- Negotiates a "sprint contract" with the evaluator before implementation begins

#### Evaluator Agent

- Uses [[Playwright MCP]] to click through running applications like a user would
- Tests UI features, API endpoints, and database states
- Grades each sprint against both discovered bugs and explicit criteria
- Evaluates: product depth, functionality, visual design, and code quality
- Each criterion has a hard threshold; failure in any area triggers detailed feedback

### Sprint Contracts

Before each sprint, the generator and evaluator negotiate a **sprint contract** that specifies:

- What the generator will build
- How success will be verified
- Testable implementation criteria

This bridges the gap between high-level user stories and testable implementation, keeping work faithful to specifications without over-constraining the implementation approach.

### Communication Pattern

Agents communicate via files:
- One agent writes a file
- Another agent reads and responds within that file or with a new file
- The previous agent reads the response and continues

This asynchronous pattern maintains clear context and decision trails.

---

## Case Study: Retro Game Maker

### Comparison: Solo vs. Harness

The team compared a single-agent baseline against the full three-agent harness using the prompt: *"Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."*

| Harness | Duration | Cost |
|---------|----------|------|
| Solo | 20 min | $9 |
| Full harness | 6 hr | $200 |

**Solo Run Results:**
- Application appeared functional initially
- Layout wasted space with fixed-height panels
- Workflow was rigid and unintuitive
- **Critical failure**: Game entities appeared on screen but didn't respond to input
- Core wiring between entity definitions and game runtime was broken

**Harness Run Results:**
- Planner expanded prompt into 16-feature spec across 10 sprints
- Included sprite animation system, behavior templates, sound effects, AI-assisted sprite generator, and game export
- Visual design language applied consistently throughout
- Sprite editor was richer with cleaner tool palettes and better color picker
- **Critical success**: Entities responded to input; gameplay functioned
- Built-in [[Claude integration]] allowed generating game components through prompting
- Minor issues remained (e.g., physics edge cases, level design limitations)

---

## Iterating and Simplifying the Harness

### Principle: Stress-Test Assumptions

Every component in a harness encodes an assumption about what the model cannot do independently. These assumptions should be continuously stress-tested because: