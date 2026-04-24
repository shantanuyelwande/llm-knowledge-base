---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:08:07.602877
raw_file_updated: 2026-04-24T19:08:07.602877
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:08:07.602877
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

**Harness design** refers to the architectural patterns and orchestration strategies used to enable [[AI agents]] to complete complex, long-running tasks effectively. This article explores techniques for improving [[agentic coding]] performance through multi-agent systems inspired by [[Generative Adversarial Networks]] (GANs), with applications to both [[frontend design]] and full-stack software development.

---

## Overview

Harness design has emerged as a critical factor in achieving high-quality outputs from [[language models]] when tackling complex, multi-hour development tasks. Rather than relying on single-agent systems, effective harnesses decompose work into specialized roles—typically a **generator** agent that produces code and a **evaluator** agent that provides quality feedback and verification.

The key insight underlying modern harness design is that [[context engineering]] and task decomposition can overcome fundamental limitations in model performance, including:

- **Context anxiety**: Models' tendency to prematurely conclude work as they approach perceived context limits
- **Self-evaluation bias**: Models' reluctance to critically assess their own outputs
- **Coherence loss**: Degradation in output quality as context windows fill during long tasks

---

## Problem Space: Why Naive Implementations Fall Short

### Context Management Issues

Early attempts at long-running [[agentic coding]] encountered two persistent failure modes:

**Context Anxiety and Coherence Loss**

As the [[context window]] fills during extended tasks, models exhibit degradation in performance. [[Claude]] Sonnet 4.5 demonstrated particularly strong "context anxiety"—a tendency to wrap up work prematively as it approached its perceived context limit. While [[context compaction]] (summarizing earlier conversation history in place) preserves some continuity, it doesn't provide the clean slate that models need to reset their anxiety patterns.

**Context Resets vs. Compaction**

[[Context reset|Context resets]] proved more effective than compaction for long-running tasks. A context reset involves:

1. Clearing the context window entirely
2. Starting a fresh agent session
3. Using structured [[artifact]] handoffs to carry previous state and next steps

This approach eliminates context anxiety but introduces orchestration complexity, token overhead, and latency costs. However, with [[Claude]] Opus 4.5, context resets became essential to maintaining performance on complex multi-hour builds.

### Self-Evaluation Bias

When asked to evaluate their own work, [[language models]] exhibit systematic positive bias—confidently praising outputs even when quality is objectively mediocre. This problem is particularly acute for subjective tasks like [[frontend design]], where there is no binary correctness check.

The solution is **agent separation**: creating a dedicated evaluator agent distinct from the generator. While both are LLMs with inherent generosity toward LLM-generated outputs, a standalone evaluator can be tuned to be appropriately skeptical through careful [[prompt engineering]].

---

## Frontend Design: Making Subjective Quality Gradable

### The Challenge

Without targeted intervention, [[Claude]] gravitates toward safe, technically functional but visually unremarkable layouts. The core problem is that aesthetics cannot be fully reduced to numerical scores, yet consistent improvement requires concrete grading criteria.

### Grading Framework

The approach uses four design criteria that encode both principles and preferences:

**Design Quality**
Whether the design feels like a coherent whole rather than disconnected parts. Strong work combines colors, typography, layout, imagery, and details to create a distinct mood and identity.

**Originality**
Evidence of custom decisions versus template layouts and library defaults. The criterion explicitly penalizes generic "[[AI slop]]" patterns (e.g., purple gradients over white cards) and rewards deliberate creative choices.

**Craft**
Technical execution including typography hierarchy, spacing consistency, color harmony, and contrast ratios. This competence check typically comes naturally to models; failures indicate broken fundamentals.

**Functionality**
Usability independent of aesthetics. Users should understand what the interface does, find primary actions, and complete tasks without guessing.

### Implementation

The harness emphasizes design quality and originality over craft and functionality, since models already perform well on the latter two by default. The evaluator uses [[Playwright]] MCP to:

- Interact with live pages directly
- Take screenshots during navigation
- Study implementations before scoring
- Provide detailed critiques for iteration

Each generation runs 5-15 iterations, with feedback flowing back to the generator for refinement. Strategic decision-making allows the generator to either refine the current direction or pivot to entirely different aesthetics if the approach isn't working.

### Results

Across runs, evaluator assessments improve over iterations before plateauing, though the improvement pattern is not always linear. Later implementations tend to be better overall, but sometimes earlier iterations are preferred. The generator increases implementation complexity in response to feedback, reaching for more ambitious solutions.

Notably, even first-iteration outputs significantly exceed baseline performance without evaluation feedback, suggesting that the criteria and associated language themselves steer models away from generic defaults before any evaluator iteration occurs.

---

## Full-Stack Coding: Three-Agent Architecture

### System Design

Building on earlier [[long-running harness]] work, a three-agent system addresses specific gaps:

**Planner Agent**

Takes a simple 1-4 sentence user prompt and expands it into a comprehensive product specification. The planner is instructed to:

- Be ambitious about scope
- Focus on product context and high-level technical design
- Avoid granular technical details that could cascade errors
- Identify opportunities to weave [[AI agent]] features into the spec

This automation replaces the requirement for users to provide detailed upfront specs.

**Generator Agent**

Implements features one at a time in sprints, using a [[React]], [[Vite]], [[FastAPI]], and [[SQLite]]/[[PostgreSQL]] stack. The generator:

- Works in sprints picking features from the spec
- Self-evaluates work at sprint end
- Uses [[Git]] for version control
- Negotiates sprint contracts with the evaluator

**Evaluator Agent**

Tests the running application like a user would, using [[Playwright]] MCP to:

- Click through UI features
- Test API endpoints
- Verify database states
- Grade against both discovered bugs and quality criteria

The evaluator uses a **sprint contract**—an agreed-upon definition of "done" negotiated before implementation. This bridges the gap between high-level user stories and testable implementation details.

### Communication Pattern

Agents communicate via files: one agent writes a file, another reads and responds, creating clear handoff points and maintaining context across agent boundaries.

### Case Study: Retro Game Maker

**Solo Harness Performance**
- Duration: 20 minutes
- Cost: $9
- Result: Interface appeared functional but contained critical bugs—entities appeared on screen but didn't respond to input, with broken wiring between entity definitions and game runtime

**Full Harness Performance**
- Duration: 6 hours
- Cost: $200
- Result: Polished, fully functional application with:
  - Proper visual identity consistent with design spec
  - Rich sprite editor with cleaner tool palettes
  - Built-in [[Claude]] integration for AI-assisted game design
  - Working gameplay with proper entity behavior

The 20x cost increase yielded dramatically superior output quality and completeness.

---

## Harness Evolution: Optimization for Newer Models

### Initial Simplification Attempts

Early attempts to radically simplify the harness while maintaining performance failed, making it difficult to identify which components were truly load-bearing. A methodical approach of removing one component at a time proved more effective.

### Impact of Model Improvements

The release of [[Claude]] Opus 4.6 provided motivation to re-examine harness complexity. Opus 4.6's improvements included:

- More careful planning
- Sustained performance on longer agentic tasks
- Better operation in larger codebases
- Improved code review and debugging
- Enhanced long-context retrieval

These capabilities meant several harness components were no longer necessary.

### Removing Sprint Decomposition

The sprint construct had decomposed work into chunks for coherent model execution. With Opus 4.6's improved capabilities, the generator could handle full application builds without this decomposition. This change:

- Eliminated explicit sprint structure
- Maintained planner and evaluator roles
- Moved evaluator to single-pass at run end
- Reduced cost and complexity

The practical implication is that evaluator necessity depends on task difficulty relative to current model capabilities. For tasks within the model's reliable performance boundary, the evaluator becomes overhead. For tasks at or beyond that boundary, the evaluator continues providing real value.

### Digital Audio Workstation Case Study

**Task**: Build a fully featured DAW in the browser using Web Audio API

**Performance**
- Duration: 3 hours 50 minutes
- Cost: $124.70
- Breakdown:
  - Planner: 4.7 min ($0.46)
  - Build Round 1: 2 hr 7 min ($71.08)
  - QA Round 1