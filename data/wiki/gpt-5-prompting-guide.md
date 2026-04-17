---
title: GPT 5 PROMPTING GUIDE
source_file: GPT 5 PROMPTING GUIDE.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:31:02.699194
raw_file_updated: 2026-04-05T20:31:02.699194
version: 1
sources:
  - file: GPT 5 PROMPTING GUIDE.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:31:02.699194
tags: ["prompt-engineering", "gpt-5", "best-practices", "agentic-ai", "coding"]
related_topics: []
backlinked_by: []

---
# GPT-5 Prompting Guide

## Summary

The GPT-5 Prompting Guide is an official resource from [[OpenAI]] that provides best practices for maximizing output quality from GPT-5, OpenAI's newest flagship model. The guide covers key areas including [[agentic task performance]], [[instruction following]], [[coding optimization]], and practical techniques for controlling model behavior through prompt engineering. It emphasizes that GPT-5 represents significant improvements in reasoning, tool calling, and steerability compared to previous models.

## Overview

GPT-5 represents a substantial leap forward in agentic task performance, coding capabilities, raw intelligence, and steerability. While the model performs well "out of the box," this guide provides evidence-based prompting techniques derived from real-world applications and training experience. The guide is particularly designed for developers building [[agentic applications]] and [[tool-calling workflows]].

### Key Improvements in GPT-5

- Enhanced [[tool calling]] and instruction following
- Long-context understanding capabilities
- Improved [[agentic workflow]] predictability
- Superior coding performance across multiple domains
- Greater responsiveness to prompt-based steering

---

## Table of Contents

1. [Agentic Workflow Optimization](#agentic-workflow-optimization)
2. [Coding Performance](#coding-performance)
3. [Instruction Following](#instruction-following)
4. [API Features and Parameters](#api-features-and-parameters)
5. [Minimal Reasoning](#minimal-reasoning)
6. [Appendix: Tool Definitions](#appendix-tool-definitions)

---

## Agentic Workflow Optimization

### Agentic Eagerness and Control

GPT-5 is trained to operate across a spectrum of control—from highly autonomous decision-making to tightly constrained, well-defined tasks. The key challenge is calibrating the model's "agentic eagerness": balancing proactivity with awaiting explicit guidance.

#### Controlling Agentic Eagerness

By default, GPT-5 is thorough and comprehensive when gathering context. To reduce agentic behavior and minimize latency:

**Techniques for Less Eagerness:**

- **Lower reasoning_effort**: Reduces exploration depth while improving efficiency and latency. Many workflows achieve consistent results with `medium` or even `low` reasoning_effort settings.

- **Define clear exploration criteria**: Specify in your prompt exactly how you want the model to explore the problem space, reducing unnecessary reasoning about tangential ideas.

- **Set tool call budgets**: Establish fixed limits on tool calls, naturally varying based on desired search depth.

- **Provide escape hatches**: Include explicit clauses allowing the model to proceed under uncertainty (e.g., "even if it might not be fully correct").

**Context Gathering Strategy (Low Eagerness):**

```
Goal: Get enough context fast. Parallelize discovery and stop as soon as possible.

Method:
- Start broad, then fan out to focused subqueries
- In parallel, launch varied queries; read top hits per query
- Avoid over searching for context

Early stop criteria:
- You can name exact content to change
- Top hits converge (~70%) on one area/path
- Escalate once if signals conflict; run one refined parallel batch, then proceed
- Search depth: very low
- Absolute maximum of 2 tool calls
- Bias strongly towards providing a correct answer quickly, even if not fully certain
```

#### Encouraging Agentic Autonomy

To encourage model autonomy, persistence, and reduce clarifying questions:

**Techniques for More Eagerness:**

- **Increase reasoning_effort**: Use `high` for complex, multi-step tasks to ensure optimal outputs.

- **Use persistence prompts**: Explicitly instruct the model to continue until task completion.

- **Reduce hand-offs to users**: Discourage the model from asking for clarification or confirming assumptions.

**Persistence Instruction Example:**

```
- You are an agent - please keep going until the user's query is completely resolved
- Only terminate your turn when you are sure that the problem is solved
- Never stop or hand back to the user when you encounter uncertainty — research and solve
- Do not ask the human to confirm or clarify assumptions, as you can always adjust later
```

### Tool Preambles

GPT-5 is trained to provide clear upfront plans and consistent progress updates via "tool preamble" messages. This significantly improves user experience during long agentic rollouts.

**Best Practices for Tool Preambles:**

- Always begin by rephrasing the user's goal in a friendly, clear, and concise manner
- Immediately outline a structured plan detailing each logical step
- Finish by summarizing completed work distinctly from the upfront plan
- Adjust frequency and style based on user needs (from detailed explanations to brief summaries)

### Responses API for Agentic Workflows

OpenAI strongly recommends using the [[Responses API]] when deploying GPT-5 for agentic applications. Key benefits include:

- **Persistent reasoning context**: Reasoning persists between tool calls, improving efficiency
- **Performance gains**: Tau-Bench Retail scores increased from 73.9% to 78.2% when switching from Chat Completions
- **Token efficiency**: Previous reasoning traces are reused via `previous_response_id`, conserving CoT tokens
- **Latency improvements**: Eliminates need to reconstruct plans from scratch after each tool call
- **Cost reduction**: More efficient token usage across agentic workflows

---

## Coding Performance

GPT-5 leads all frontier models in coding capabilities. It can work in large codebases to fix bugs, handle large diffs, implement multi-file refactors, and build complete applications from scratch.

### Frontend App Development

#### Recommended Technology Stack

**Frameworks:**
- [[Next.js]] (TypeScript)
- [[React]]
- HTML

**Styling & UI:**
- [[Tailwind CSS]]
- [[shadcn/ui]]
- [[Radix Themes]]

**Icons:**
- Material Symbols
- Heroicons
- Lucide

**Animation:**
- Motion

**Fonts:**
- San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

#### Zero-to-One App Generation

GPT-5 excels at building complete applications in one shot. To maximize output quality:

**Self-Reflection Approach:**

```
- First, spend time thinking of a rubric until you are confident
- Then, think deeply about every aspect of what makes for a world-class solution
- Finally, use the rubric to internally think and iterate on the best possible implementation
```

This leverages GPT-5's thorough planning and self-reflection capabilities to improve output quality.

#### Matching Codebase Design Standards

When implementing incremental changes and refactors, code should adhere to existing style and design standards. Enhance this with explicit prompt directions summarizing:

- Engineering principles
- Directory structure
- Best practices (explicit and implicit)

**Code Editing Rules Template:**

```
Guiding Principles:
- Clarity and Reuse: Every component and page should be modular and reusable
- Consistency: The UI must adhere to a consistent design system
- Simplicity: Favor small, focused components and avoid unnecessary complexity
- Demo-Oriented: Structure should allow for quick prototyping and feature showcasing
- Visual Quality: Follow high visual quality standards

Frontend Stack Defaults:
- Framework: Next.js (TypeScript)
- Styling: TailwindCSS
- UI Components: shadcn/ui
- Icons: Lucide
- State Management: Zustand

Directory Structure:
/src
  /app                    # Application routes
  /api/<route>/route.ts   # API endpoints
  /(pages)                # Page routes
  /components/            # UI building blocks
  /hooks/                 # Reusable React hooks
  /lib/                   # Utilities (fetchers, helpers)
  /stores/                # Zustand stores
  /types/                 # Shared TypeScript types
  /styles/                # Tailwind config

UI/UX Best Practices:
- Visual Hierarchy: Limit typography to 4–5 font sizes and weights
- Color Usage: Use 1 neutral base and up to 2 accent colors
- Spacing and Layout: Always use multiples of 4 for padding and margins
- State Handling: Use skeleton placeholders or animate-pulse for loading states
- Accessibility: Use semantic HTML and ARIA roles where appropriate
```

### Collaborative Coding: Cursor's GPT-5 Integration

[[Cursor]], an AI code editor, served as a trusted alpha tester for GPT-5. Their prompt tuning work provides valuable insights for production use.

#### System Prompt and Parameter Tuning

**Balancing Verbosity:**

Cursor