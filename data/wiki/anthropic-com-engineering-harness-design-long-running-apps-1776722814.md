---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-10T05:42:06.928178
raw_file_updated: 2026-05-10T05:42:06.928178
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-10T05:42:06.928178
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to successfully complete complex, long-running tasks. This article describes techniques developed at [[Anthropic]] for improving [[Claude]]'s performance on extended coding and design projects, including [[multi-agent systems]], [[evaluator-generator loops]], and [[context management]] strategies.

---

## Overview

Harness design is a critical component of [[agentic AI]] development, particularly for tasks that exceed what a single model pass can accomplish reliably. Rather than relying on a model's baseline capabilities, harness design uses structural patterns—such as task decomposition, specialized agent roles, and feedback loops—to guide models toward higher-quality outputs on complex problems.

This article documents research conducted by Prithvi Rajasekaran of [[Anthropic Labs]] on applying harness design principles to two domains: [[frontend design]] and [[full-stack application development]]. The work demonstrates that well-designed harnesses can produce dramatically superior results compared to single-pass model generations, though at increased computational cost.

---

## Key Problems with Naive Implementations

### Context Management Issues

Long-running tasks present two primary challenges for [[language models]]:

1. **Context window saturation**: As conversations grow longer, models lose coherence as the context window fills with previous messages and outputs.

2. **Context anxiety**: Some models (particularly [[Claude Sonnet 4.5]]) exhibit a tendency to prematurely wrap up work as they approach their perceived context limit, even when substantial work remains.

Two approaches address these issues:

- **Compaction**: Summarizing earlier conversation history in place, allowing the same agent to continue with a shortened history. This preserves continuity but doesn't eliminate context anxiety.

- **Context resets**: Completely clearing the context window and starting a fresh agent session with a structured handoff artifact containing previous state. This provides a clean slate but adds orchestration complexity and latency.

Testing showed that [[Claude Sonnet 4.5]] required context resets to maintain performance on lengthy tasks, while newer models like [[Claude Opus 4.5]] reduced this requirement substantially.

### Self-Evaluation Limitations

When asked to evaluate their own work, [[AI agents]] consistently exhibit positive bias, praising mediocre outputs even when quality is obviously substandard. This problem is particularly acute for subjective tasks like design, where no binary verification exists.

**Solution**: Separating the [[evaluation]] function into a dedicated agent creates a feedback loop where the generator can iterate against concrete external feedback rather than its own inflated self-assessment. While evaluator agents still exhibit some leniency toward model-generated outputs, tuning them to be skeptical proves far more tractable than making generators self-critical.

---

## Frontend Design: Making Subjective Quality Gradable

### Approach

The first domain tested was [[frontend design]], where the self-evaluation problem was most visible. The baseline approach produced technically functional but visually unremarkable designs that gravitated toward safe, predictable layouts.

Two key insights shaped the solution:

1. **Codifying aesthetic principles**: While beauty cannot be fully reduced to a score, design quality can be improved through grading criteria that encode specific design principles and preferences.

2. **Separating generation from evaluation**: Creating a feedback loop between a dedicated generator and evaluator drives the generator toward stronger outputs.

### Grading Criteria

Four criteria were developed to guide both generator and evaluator:

| Criterion | Definition |
|-----------|-----------|
| **Design Quality** | Does the design feel coherent rather than a collection of parts? Do colors, typography, layout, imagery, and details combine to create distinct mood and identity? |
| **Originality** | Is there evidence of custom decisions, or reliance on templates and defaults? Can a human designer recognize deliberate creative choices? |
| **Craft** | Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios. A competence check rather than creativity check. |
| **Functionality** | Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks? |

**Weighting**: Design quality and originality were emphasized over craft and functionality, since [[Claude]] already performed well on technical competence by default. The criteria explicitly penalized generic "[[AI slop]]" patterns, pushing the model toward aesthetic risk-taking.

### Implementation

The harness was built on the [[Claude Agent SDK]] with the following components:

- **Generator agent**: Created HTML/CSS/JS frontends based on user prompts
- **Evaluator agent**: Used [[Playwright MCP]] to interact with live pages, screenshotting and studying implementations before scoring each criterion and writing detailed critiques
- **Feedback loop**: Evaluator feedback flowed back to generator for iteration

**Iteration pattern**: Runs typically executed 5-15 iterations per generation, with each cycle pushing the generator in more distinctive directions as it responded to critiques. Full runs extended up to four hours.

The generator was also instructed to make strategic decisions after each evaluation: refine the current direction if scores trended well, or pivot to an entirely different aesthetic if the approach wasn't working.

### Results

Several patterns emerged:

- **Prompt-guided convergence**: Criteria wording steered outputs in unanticipated ways. Phrases like "the best designs are museum quality" pushed designs toward particular visual convergence.

- **Non-linear improvement**: While scores generally improved over iterations, the pattern wasn't cleanly linear. Later implementations tended to be better overall, but earlier iterations were sometimes preferable individually.

- **Complexity increase**: Implementation complexity tended to increase across rounds as the generator reached for more ambitious solutions.

- **Immediate baseline improvement**: Even on the first iteration, outputs were noticeably better than baseline with no prompting, suggesting criteria and associated language steered the model away from generic defaults before any evaluator feedback.

**Example**: For a Dutch art museum website, the ninth iteration produced a clean, dark-themed landing page. The tenth cycle scrapped this approach entirely, reimagining the site as a spatial experience—a 3D room with checkered floor rendered in CSS perspective, artwork hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This creative leap had not been seen in single-pass generations.

---

## Full-Stack Coding: Three-Agent Architecture

### Building on Prior Work

Previous research on [[long-running coding agents]] demonstrated that decomposing builds into tractable chunks and using structured artifacts for context handoff significantly improved performance. However, those approaches still hit limitations on complex tasks, with agents "going off the rails" as context filled.

The new harness extended this foundation with a three-agent system addressing specific gaps:

### Agent Architecture

#### Planner Agent

- **Role**: Expands simple user prompts (1-4 sentences) into full product specifications
- **Constraints**: Focuses on product context and high-level technical design rather than granular implementation details
- **Rationale**: Prevents cascading errors from over-specified technical details
- **Special capability**: Identifies opportunities to weave [[AI features]] into product specs

#### Generator Agent

- **Role**: Implements features from the specification
- **Approach**: Works in [[sprints]], picking up one feature at a time
- **Stack**: [[React]], [[Vite]], [[FastAPI]], [[SQLite]]/[[PostgreSQL]]
- **Tools**: [[Git]] for version control
- **Workflow**: Self-evaluates work at end of each sprint before handing off to QA

#### Evaluator Agent

- **Role**: Catches bugs and verifies quality through user interaction testing
- **Tools**: [[Playwright MCP]] for clicking through running applications
- **Testing approach**: Tests UI features, API endpoints, and database states like a real user
- **Grading**: Evaluates against both discovered bugs and criteria covering product depth, functionality, visual design, and code quality
- **Thresholds**: Each criterion has hard thresholds; failure on any criterion causes sprint failure with detailed feedback

### Sprint Contracts

Before each sprint, generator and evaluator negotiate a **sprint contract** that:

1. Bridges the gap between high-level user stories and testable implementation
2. Specifies what "done" looks like for that chunk of work
3. Defines how success will be verified

The generator proposes implementation and verification approach; the evaluator reviews to ensure the right thing is being built. They iterate until agreement is reached.

**Communication**: Handled via files—agents write and read files rather than direct conversation, keeping work faithful to spec without over-specification.

### Initial Results (Opus 4.5)

#### Test Case: Retro Video Game Maker

**Prompt**: _Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode._

**Performance Comparison**:

| Harness Type | Duration | Cost |
|--------------|----------|------|
| Solo agent | 20 min | $9 |
| Full harness | 6 hr | $200 |