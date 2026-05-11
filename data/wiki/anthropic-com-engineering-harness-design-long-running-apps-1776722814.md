---
title: anthropic-com-engineering-harness-design-long-running-apps-1776722814
source_file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-11T06:03:30.454019
raw_file_updated: 2026-05-11T06:03:30.454019
version: 1
sources:
  - file: anthropic-com-engineering-harness-design-long-running-apps-1776722814.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-11T06:03:30.454019
tags: []
related_topics: []
backlinked_by: []
---
# Harness Design for Long-Running Application Development

## Summary

Harness design is a critical approach to improving [[AI agent]] performance in complex, long-running tasks. This article documents research by [[Anthropic]] on using multi-agent architectures inspired by [[Generative Adversarial Networks]] (GANs) to enable [[Claude]] to produce high-quality [[frontend design|frontend designs]] and build complete [[full-stack applications]] autonomously. The work demonstrates how separating generator and evaluator agents, combined with strategic task decomposition and structured handoff mechanisms, can dramatically improve output quality compared to single-agent approaches.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Problems with Naive Implementations](#core-problems-with-naive-implementations)
3. [Frontend Design Application](#frontend-design-application)
4. [Full-Stack Coding Architecture](#full-stack-coding-architecture)
5. [Harness Iterations and Improvements](#harness-iterations-and-improvements)
6. [Key Findings and Lessons](#key-findings-and-lessons)
7. [Related Concepts](#related-concepts)

---

## Overview

Harness design refers to the architectural patterns and orchestration strategies used to structure [[AI agent|AI agents]] for complex, long-running tasks. Rather than relying on a single agent to complete an entire task, effective harnesses decompose work into specialized agents, each addressing specific aspects of the problem.

The research presented here focuses on two interconnected challenges:

- **Subjective quality tasks**: Generating high-quality [[frontend design|frontend designs]] where aesthetic judgment is required
- **Objective correctness tasks**: Building complete [[software applications]] where functionality must be verified

By applying similar architectural principles across both domains, the research demonstrates that multi-agent harnesses can achieve substantially better results than baseline approaches, despite higher computational costs.

### Key Achievement

A three-agent harness (planner, generator, evaluator) successfully built complex [[full-stack applications]] over multi-hour autonomous coding sessions, producing feature-rich applications with integrated [[AI agent|AI features]]. Compared to a single-agent baseline, the harness approach produced demonstrably superior results in both design quality and functional correctness.

---

## Core Problems with Naive Implementations

### Context Window Limitations

[[Large language model|Large language models]] face significant challenges when working on extended tasks:

1. **Context Anxiety**: Models like [[Claude Sonnet 4.5]] exhibit a tendency to wrap up work prematurely as they approach their perceived [[context window]] limit, even when substantial work remains.

2. **Context Decay**: As the [[context window]] fills with conversation history, models tend to lose coherence and make increasingly poor decisions.

**Solution**: [[Context reset|Context resets]] provide a cleaner solution than [[context compaction]]. Rather than summarizing earlier conversation in place, context resets clear the window entirely and use structured artifacts to hand off state to a fresh agent session. This eliminates context anxiety while maintaining continuity through explicit handoff mechanisms.

### Self-Evaluation Bias

When asked to evaluate their own work, [[AI agent|AI agents]] exhibit systematic bias:

- **Positive Skew**: Models tend to praise their own outputs, even when quality is objectively mediocre
- **Subjective Domain Severity**: The problem is most pronounced in subjective domains like [[design]] where there are no binary correctness checks
- **Objective Domain Persistence**: Even in domains with verifiable outcomes, agents demonstrate poor judgment that impedes task completion

**Solution**: Separating the agent performing work (generator) from the agent evaluating it (evaluator) creates a feedback loop that drives quality improvement. An external evaluator can be tuned to be appropriately skeptical in ways that are difficult to achieve with a self-evaluating agent.

---

## Frontend Design Application

### Making Subjectivity Gradable

The research began with [[frontend design]], where subjective quality judgments are essential but difficult to operationalize. Two key insights shaped the approach:

1. While aesthetics cannot be fully reduced to numerical scores, they can be improved through explicit grading criteria that encode design principles
2. Separating generation from evaluation creates a feedback loop that drives the generator toward stronger outputs

### Design Grading Criteria

Four grading criteria were developed to guide both generator and evaluator agents:

#### Design Quality
Does the design feel like a coherent whole rather than a collection of disconnected parts? Strong work combines colors, [[typography]], layout, imagery, and other details to create a distinct mood and identity.

#### Originality
Is there evidence of custom creative decisions, or does the work rely on template layouts and library defaults? Human designers should recognize deliberate choices. Unmodified stock components and telltale signs of AI generation (e.g., purple gradients over white cards) fail this criterion.

#### Craft
Technical execution of [[typography]] hierarchy, spacing consistency, [[color harmony]], and contrast ratios. This is a competence check—most reasonable implementations pass by default, and failing indicates broken fundamentals.

#### Functionality
Usability independent of aesthetics. Can users understand the interface, find primary actions, and complete tasks without guessing?

### Emphasis Strategy

The harness deliberately weighted design quality and originality more heavily than craft and functionality, since [[Claude]] already performed well on technical competence. This emphasis pushed the model toward aesthetic risk-taking rather than safe, generic defaults.

### Evaluation Mechanism

The evaluator agent was given access to the [[Playwright]] [[Model Context Protocol|MCP]], enabling it to:

- Navigate the live page directly rather than scoring static screenshots
- Interact with the interface as a user would
- Take screenshots and study implementation details before scoring
- Produce detailed critiques grounded in observed behavior

Each evaluation cycle typically took real wall-clock time due to interactive testing, with full runs stretching to four hours.

### Results and Observations

- **Iterative Improvement**: Evaluator assessments improved over iterations before plateauing, with remaining headroom
- **Aesthetic Divergence**: Some generations refined incrementally; others took sharp aesthetic turns between iterations
- **Prompt Influence**: Criteria wording steered generators in unexpected ways (e.g., "museum quality" pushed toward particular visual convergence)
- **Non-Linear Progress**: Later implementations were generally better, but individual iterations sometimes surpassed the final output
- **Complexity Growth**: Implementation complexity increased across rounds as generators reached for more ambitious solutions
- **First-Iteration Lift**: Even without evaluator feedback, outputs were noticeably better than baseline, suggesting criteria and language themselves steered the model away from generic defaults

#### Notable Example: Museum Website

When prompted to create a website for a Dutch art museum, the generator produced a clean, dark-themed landing page through iteration nine. On iteration ten, it abandoned this approach entirely and reimagined the site as a spatial experience: a 3D room with checkered floor rendered in [[CSS]] perspective, artwork hung on walls in free-form positions, and doorway-based navigation between gallery rooms. This creative leap demonstrated the potential of the multi-agent approach to drive innovation beyond what single-pass generation typically achieves.

---

## Full-Stack Coding Architecture

### Scaling the GAN-Inspired Pattern

The generator-evaluator loop naturally maps onto the [[software development lifecycle]], where [[code review]] and [[quality assurance]] serve analogous structural roles to design evaluation.

### Three-Agent System

The full-stack harness expanded to three specialized agents, each addressing specific gaps observed in prior runs:

#### Planner Agent

**Purpose**: Automate the step of detailed specification, which previously required manual user input.

**Input**: Simple 1-4 sentence product prompt

**Output**: Comprehensive product specification including:
- Feature list across multiple sprints
- High-level technical design (not granular implementation details)
- Visual design language
- Integrated [[AI agent|AI features]] woven throughout the spec

**Design Philosophy**: The planner emphasizes scope and product context while avoiding over-specification of implementation details. This prevents cascading errors from incorrect technical specifications while allowing the generator flexibility in execution.

#### Generator Agent

**Purpose**: Implement features incrementally using the sprint-based approach, with integrated self-evaluation.

**Workflow**:
- Work in sprints, implementing one feature at a time
- Self-evaluate work at the end of each sprint
- Hand off to [[quality assurance|QA]] for independent verification
- Use [[git]] for version control

**Technology Stack**: [[React]], [[Vite]], [[FastAPI]], [[SQLite]] (later [[PostgreSQL]])

**Sprint Contract Mechanism**: Before implementation, generator and evaluator negotiate a sprint contract that defines:
- What "done" looks like for the chunk of work
- Testable success criteria
- How verification will occur

This bridges the gap between high-level user stories and testable implementation without over-specifying details upfront.

#### Evaluator Agent

**Purpose**: Catch bugs and ensure quality through independent testing and verification.

**Capabilities**:
- Uses [[Playwright]] [[Model Context Protocol|MCP]] to click through running applications like a user