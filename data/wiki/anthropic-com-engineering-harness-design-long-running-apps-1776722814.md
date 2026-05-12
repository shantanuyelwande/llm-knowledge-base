---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-12T05:43:07.297717
raw_file_updated: 2026-05-12T05:43:07.297717
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-12T05:43:07.297717
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical approach to improving [[AI agent]] performance on complex, long-running tasks. By separating concerns into specialized agent roles and implementing feedback loops inspired by [[Generative Adversarial Networks]] (GANs), developers can achieve substantially higher quality outputs in both [[frontend design]] and [[full-stack software development]]. This article documents techniques for building multi-agent systems that decompose work, evaluate outputs critically, and maintain coherence across extended execution sessions.

---

## Overview

**Harness design** refers to the architectural patterns and orchestration strategies that enable [[AI models]] to work effectively on complex, extended tasks that exceed their baseline capabilities. Rather than relying on a single agent to complete work end-to-end, harness design distributes responsibilities across specialized agents with distinct roles, creating feedback loops and quality gates that drive iterative improvement.

This approach has proven particularly effective for:
- [[Frontend design]] and user interface development
- [[Full-stack application development]]
- [[Long-running autonomous coding]] tasks
- [[Code generation]] and software engineering

The foundational insight is that [[self-evaluation]] is unreliable—models tend to overestimate the quality of their own work. Separating the agent performing work from the agent evaluating it creates a more effective feedback mechanism.

---

## The Problem with Naive Implementations

### Context Management Issues

Long-running tasks present two critical challenges related to [[context windows]]:

1. **Context Coherence Loss**: As the [[context window]] fills during extended tasks, models tend to lose coherence and consistency in their outputs.

2. **Context Anxiety**: Some models (particularly [[Claude Sonnet 4.5]]) exhibit a tendency to wrap up work prematurely as they approach their perceived [[context limit]], even when substantial work remains.

**Solutions:**
- **Context Resets**: Rather than using [[compaction]] (summarizing earlier conversation in place), completely clear the context window and use a fresh [[agent session]] with a structured handoff artifact containing the previous agent's state and next steps
- **Continuous Sessions**: Newer models like [[Claude Opus 4.6]] largely eliminate context anxiety, allowing continuous sessions with automatic [[compaction]] to manage context growth

### Self-Evaluation Limitations

When asked to evaluate their own work, [[AI agents]] consistently exhibit positive bias, praising outputs even when quality is mediocre. This problem is particularly acute for:
- **Subjective tasks** (like [[design]]) where there is no binary correctness check
- **Complex implementations** where agents may miss subtle bugs or usability issues

**Solution:** Separate the generator (agent doing work) from the evaluator (agent grading work), and tune the evaluator to be appropriately skeptical rather than lenient toward [[AI-generated]] outputs.

---

## Frontend Design: Making Subjectivity Gradable

### The Challenge

Without intervention, Claude typically produces safe, technically functional but visually unremarkable layouts. The core problem: how to provide concrete feedback on subjective qualities like "good design"?

### Grading Criteria Framework

Rather than asking "Is this design beautiful?" (unanswerable), the harness uses four concrete grading criteria:

| Criterion | Definition | Emphasis |
|-----------|-----------|----------|
| **Design Quality** | Does the design feel coherent rather than a collection of parts? Do colors, typography, layout, and imagery combine to create distinct mood and identity? | High |
| **Originality** | Evidence of custom decisions vs. template layouts and defaults? Recognition of deliberate creative choices vs. telltale AI patterns? | High |
| **Craft** | Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios | Medium |
| **Functionality** | Usability independent of aesthetics: can users understand the interface, find actions, complete tasks? | Medium |

The emphasis on design quality and originality over craft and functionality reflects Claude's natural strengths in technical competence, pushing the model toward aesthetic risk-taking.

### Implementation Architecture

The [[frontend design harness]] operates as follows:

1. **Generator Agent**: Creates HTML/CSS/JavaScript frontend based on user prompt
2. **Evaluator Agent**: 
   - Uses [[Playwright MCP]] to interact with live page directly
   - Screenshots and studies implementation before scoring
   - Provides detailed critique for each criterion
   - Feedback loops back to generator

**Iteration Pattern**: 5-15 iterations per generation, with generator choosing to either refine current direction or pivot to entirely different aesthetic based on evaluation scores.

### Key Findings

- **Prompt Engineering Impact**: Wording of criteria steers output direction (e.g., "museum quality" pushed designs toward specific visual convergence)
- **Non-Linear Improvement**: While scores generally improve over iterations, preferred outputs sometimes appear mid-sequence rather than at the end
- **Complexity Escalation**: Later iterations reach for more ambitious solutions in response to evaluator feedback
- **Baseline Lift**: Even without evaluator feedback, criteria-based prompting alone noticeably improves output over generic generation

### Example: Museum Website

A notable example involved generating a website for a Dutch art museum:
- **Iterations 1-9**: Produced clean, dark-themed landing page meeting expectations
- **Iteration 10**: Complete aesthetic pivot—reimagined site as 3D spatial experience with CSS perspective, checkered floor, artwork hung in free-form positions, doorway-based navigation between gallery rooms
- **Result**: Creative leap not typically seen in single-pass generation

---

## Full-Stack Application Development

### Architecture: Three-Agent System

The harness for [[full-stack development]] extends the [[frontend design]] approach to complete applications using three specialized agents:

#### 1. Planner Agent

**Purpose**: Expand simple user prompts into comprehensive product specifications

**Characteristics**:
- Takes 1-4 sentence prompt as input
- Expands into full product spec with multiple features and sprints
- Focuses on product context and high-level technical design (not granular implementation details)
- Weaves [[AI features]] into product specs
- Access to [[frontend design skill]] to create visual design language

**Rationale**: Prevents implementation errors from cascading when technical details are over-specified upfront; lets downstream agents determine implementation path.

#### 2. Generator Agent

**Purpose**: Implement application features in iterative sprints

**Characteristics**:
- Works one feature at a time from spec
- Uses [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack
- Self-evaluates work at end of each sprint
- Uses [[Git]] for version control
- Negotiates "sprint contracts" with evaluator before implementation

**Sprint Contract**: Agreement between generator and evaluator on:
- What "done" looks like for that chunk of work
- Testable success criteria
- Verification methods

#### 3. Evaluator Agent

**Purpose**: Verify implementation quality and catch bugs before handoff

**Characteristics**:
- Uses [[Playwright MCP]] to interact with running application like a user
- Tests UI features, API endpoints, database states
- Grades each sprint against:
  - Bugs found through testing
  - Criteria: product depth, functionality, visual design, code quality
- Each criterion has hard threshold; failure requires generator feedback and rework
- Reviews sprint contracts before implementation begins

**Testing Approach**: Active navigation and interaction rather than static screenshot analysis, enabling discovery of runtime bugs and usability issues.

### Communication Pattern

Agents communicate via files to maintain clear, auditable handoffs:
- One agent writes specification file
- Next agent reads and responds within same file or creates new file
- Previous agent reads response and continues
- Keeps work faithful to spec without over-specification

### Case Study: Retro Video Game Maker

**Prompt**: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

#### Solo Agent vs. Full Harness Comparison

| Metric | Solo Agent | Full Harness |
|--------|-----------|--------------|
| Duration | 20 minutes | 6 hours |
| Cost | $9 | $200 |
| Output Quality | Broken core functionality | Fully functional application |

**Solo Agent Issues**:
- Layout wasted space with fixed-height panels
- Workflow unclear—no UI guidance on required sequence
- Core game broken: entities appeared but didn't respond to input
- Entity-to-runtime wiring disconnected

**Full Harness Output**:
- Polished, coherent interface with consistent visual identity
- 16-feature spec across 10 sprints (vs. basic solo attempt)
- Sprite animation system, behavior templates, sound/music support
- [[AI-assisted]] sprite generator and level designer
- Game export with shareable links
- Functional sprite editor with rich tooling
- Playable game with working physics (though imperfect)
- Built-in Claude integration for generative features

**Evaluator