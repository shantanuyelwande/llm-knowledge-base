---
title: GPT 5 PROMPTING GUIDE
source_file: GPT 5 PROMPTING GUIDE.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:25:43.480743
raw_file_updated: 2026-04-17T20:25:43.480743
version: 1
sources:
  - file: GPT 5 PROMPTING GUIDE.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:25:43.480743
tags: []
related_topics: []
backlinked_by: []
---
# GPT-5 Prompting Guide

## Summary

The **GPT-5 Prompting Guide** is an official resource from [[OpenAI]] documenting best practices for maximizing the performance of [[GPT-5]], their flagship large language model. Published August 7, 2025, the guide covers optimization techniques across [[agentic workflows]], [[coding tasks]], [[instruction following]], and [[tool calling]]. It emphasizes that effective prompting requires iterative experimentation and provides concrete examples from production deployments, including insights from [[Cursor]], an AI code editor.

---

## Overview

[[GPT-5]] represents a substantial advancement in [[agentic task performance]], [[coding capabilities]], raw intelligence, and steerability. While the model performs well without optimization, this guide provides evidence-based prompting techniques derived from training and real-world application experience. The guide is designed for developers building [[agentic applications]] and [[software engineering]] tools.

### Key Principles

- Prompting is not one-size-fits-all; experimentation and iteration are essential
- Different use cases require different calibrations of model behavior
- The [[Responses API]] is recommended for agentic workflows over Chat Completions
- Contradictory or vague instructions are particularly damaging to GPT-5's performance

---

## Agentic Workflow Optimization

### Controlling Agentic Eagerness

GPT-5 is trained to operate across a spectrum of [[agentic scaffolds]], from highly autonomous decision-making to tightly constrained, task-focused behavior. The model's default behavior is thorough and comprehensive in gathering context.

#### Prompting for Less Eagerness

To reduce scope and minimize latency in agentic tasks:

- **Lower reasoning_effort**: Reduces exploration depth while improving efficiency and latency. Many workflows perform consistently at `medium` or even `low` reasoning_effort settings.
- **Define clear criteria**: Explicit exploration boundaries in prompts reduce unnecessary tool-calling and tangential research.
- **Set tool call budgets**: Fixed limits on tool invocations constrain search depth naturally based on desired exploration scope.
- **Provide escape hatches**: Include clauses allowing the model to proceed under uncertainty, such as "even if it might not be fully correct."

**Context Gathering Example:**
```
Goal: Get enough context fast. Parallelize discovery and stop as soon as you can.

Method:
- Start broad, then fan out to focused subqueries
- In parallel, launch varied queries; read top hits per query
- Avoid over-searching for context

Early stop criteria:
- You can name exact content to change
- Top hits converge (~70%) on one area/path
- Escalate once: if signals conflict, run one refined parallel batch, then proceed
```

#### Prompting for More Eagerness

To encourage [[model autonomy]], increase tool-calling persistence, and reduce clarifying questions:

- **Increase reasoning_effort**: Allocates more computational resources to thorough task completion
- **Remove uncertainty barriers**: Explicitly instruct the model to research and resolve ambiguities without deferring to users
- **Emphasize persistence**: Use language like "keep going until the user's query is completely resolved"
- **Prevent premature termination**: Clarify that the model should never hand back to the user when encountering uncertainty

### Tool Preambles

[[GPT-5]] is trained to provide clear upfront plans and consistent progress updates via "tool preamble" messages. These messages improve user experience during long-running agentic tasks by explaining what the model is doing and why.

**High-Quality Preamble Prompt:**
```
- Always begin by rephrasing the user's goal in a friendly, clear, and concise way
- Then, immediately outline a structured plan detailing each logical step you'll take
- Finish by summarizing completed work distinctly from your upfront plan
```

You can control the frequency, style, and content of preambles through explicit prompting—from detailed explanations of each tool call to brief upfront plans.

### Reasoning Effort Parameter

The `reasoning_effort` parameter controls how deeply the model thinks and its willingness to call tools:

- **Default**: `medium`
- **Recommendation**: Scale up or down based on task difficulty
- **Complex tasks**: Use higher reasoning for multi-step problems
- **Performance peak**: Achieved by breaking separable tasks across multiple agent turns

### Responses API and Reasoning Context Reuse

The [[Responses API]] is strongly recommended for GPT-5 agentic applications because:

- **Persistent reasoning**: Reasoning is maintained between tool calls, improving efficiency
- **Token conservation**: Previous reasoning traces can be referenced via `previous_response_id`, eliminating reconstruction of plans after each tool call
- **Performance gains**: Statistically significant improvements observed (e.g., Tau-Bench Retail score increase from 73.9% to 78.2%)
- **Lower costs**: More efficient token usage compared to [[Chat Completions]]

---

## Coding Performance Optimization

### Frontend App Development

GPT-5 excels at implementing complete applications from scratch with excellent aesthetic sensibility. For optimal results, use:

**Recommended Framework Stack:**
- **Frameworks**: Next.js (TypeScript), React, HTML
- **Styling/UI**: Tailwind CSS, shadcn/ui, Radix Themes
- **Icons**: Material Symbols, Heroicons, Lucide
- **Animation**: Motion
- **Fonts**: San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

#### Zero-to-One App Generation

For building applications from scratch, GPT-5 benefits from prompts requesting iterative execution against self-constructed excellence rubrics:

```
<self_reflection>
- First, spend time thinking of a rubric until you are confident
- Then, think deeply about every aspect of what makes for a world-class solution
- Finally, use the rubric to internally think and iterate on the best possible output
</self_reflection>
```

This approach leverages GPT-5's thorough planning and [[self-reflection]] capabilities.

#### Matching Codebase Design Standards

When implementing incremental changes in existing codebases, GPT-5 should adhere to existing style and design standards. Enhance this behavior with prompt directions summarizing:

- **Guiding principles**: Clarity, reuse, consistency, simplicity, demo-orientation, visual quality
- **Frontend stack defaults**: Framework, styling, UI component choices, state management
- **Directory structure**: Organized `/src` layout with `/app`, `/api`, `/components`, `/hooks`, `/lib`, `/stores`, `/types`, `/styles`
- **UI/UX best practices**: Visual hierarchy, color usage, spacing, state handling, accessibility

**Code Editing Rules Example:**
```
<code_editing_rules>
<guiding_principles>
- Clarity and Reuse: Every component should be modular and reusable
- Consistency: Adhere to a consistent design system
- Simplicity: Favor small, focused components
- Demo-Oriented: Allow quick prototyping and feature showcasing
- Visual Quality: Follow high visual quality standards
</guiding_principles>
</code_editing_rules>
```

### Cursor's Production Integration

[[Cursor]], an AI code editor, served as a trusted alpha tester for GPT-5. Their prompt tuning work provides insights into production-grade optimization:

#### System Prompt and Parameter Tuning

**Verbosity Balance**: Cursor initially found GPT-5 produced verbose status updates that disrupted user flow, while code outputs were terse with poor variable naming. They resolved this by:

- Setting `verbosity` API parameter to `low` for brief text outputs
- Modifying prompts to strongly encourage verbose outputs in coding tools only
- Result: Efficient status updates combined with readable code diffs

**Autonomy and Clarification**: Cursor found GPT-5 occasionally deferred to users for clarification prematurely. They addressed this by:

- Including detailed product behavior information
- Specifying Cursor-specific features (Undo/Reject code, user preferences)
- Result: Longer horizon tasks completed with minimal interruption

**Context Gathering Refinement**: Cursor discovered that prompts effective with earlier models needed adjustment for GPT-5:

**Ineffective (with GPT-5):**
```
<maximize_context_understanding>
Be THOROUGH when gathering information. Make sure you have the FULL picture before proceeding.
</maximize_context_understanding>
```

This caused GPT-5 to overuse tools and call search repetitively when internal knowledge was sufficient.

**Effective (refined):**
```
<context_understanding>
If you've performed an edit that may partially fulfill the USER's query, you can proceed.
Bias towards not asking the user for help if you can find the answer yourself.
</context_understanding>
```

**Structured XML