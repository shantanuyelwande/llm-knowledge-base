---
title: GPT 5 PROMPTING GUIDE
source_file: GPT 5 PROMPTING GUIDE.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:04:30.668599
raw_file_updated: 2026-04-24T19:04:30.668599
version: 1
sources:
  - file: GPT 5 PROMPTING GUIDE.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:04:30.668599
tags: []
related_topics: []
backlinked_by: []
---
# GPT-5 Prompting Guide

## Summary

The GPT-5 Prompting Guide is an official resource from [[OpenAI]] that provides best practices and techniques for maximizing the performance of [[GPT-5]], their flagship language model. Published on August 7, 2025, the guide covers [[agentic task]] optimization, instruction adherence, coding performance, and advanced [[prompt engineering]] strategies. It emphasizes that GPT-5 represents significant improvements in agentic behavior, code generation, reasoning capabilities, and instruction following compared to previous models.

---

## Table of Contents

1. [Overview](#overview)
2. [Agentic Task Performance](#agentic-task-performance)
3. [Coding Capabilities](#coding-capabilities)
4. [Instruction Following](#instruction-following)
5. [API Features and Parameters](#api-features-and-parameters)
6. [Advanced Prompting Techniques](#advanced-prompting-techniques)
7. [Tool Integration Examples](#tool-integration-examples)

---

## Overview

[[GPT-5]] is designed with developers in mind, focusing on three core improvements:

- **Tool Calling**: Enhanced ability to reliably invoke and chain tool calls
- **Instruction Following**: Precise adherence to complex, multi-step instructions
- **Long-Context Understanding**: Better comprehension of extended conversations and large codebases

The guide emphasizes that while GPT-5 performs excellently "out of the box," applying targeted prompting strategies can significantly improve output quality across domains. The authors recommend using the [[Responses API]] for agentic workflows, which persists reasoning between tool calls for improved efficiency.

---

## Agentic Task Performance

### Overview

GPT-5 is trained to operate across a broad spectrum of agentic autonomy—from making high-level decisions under ambiguous circumstances to handling tightly-defined, focused tasks. The key challenge is calibrating the model's "agentic eagerness": the balance between proactivity and awaiting explicit guidance.

### Controlling Agentic Eagerness

#### Prompting for Less Eagerness

When you need to reduce scope and minimize latency, the guide recommends:

1. **Lower Reasoning Effort**: Use `reasoning_effort: low` or `reasoning_effort: medium` to reduce exploration depth while improving efficiency
2. **Clear Exploration Criteria**: Define explicit criteria for problem-space exploration to reduce unnecessary reasoning
3. **Tool Call Budgets**: Set fixed limits on tool calls (e.g., maximum 2 calls) to enforce focused behavior
4. **Escape Hatches**: Provide clauses allowing the model to proceed under uncertainty, such as "even if it might not be fully correct"

**Context Gathering Strategy**:
- Start broad, then fan out to focused subqueries
- Launch varied queries in parallel; read top hits per query
- Avoid over-searching; use targeted searches when needed
- Stop when: you can name exact content to change, or top hits converge (~70%) on one area

#### Prompting for More Eagerness

When you want to encourage autonomy and thorough task completion:

1. **Increase Reasoning Effort**: Set `reasoning_effort: high` for complex, multi-step tasks
2. **Persistence Instructions**: Use explicit directives like "keep going until the user's query is completely resolved"
3. **Avoid Handoffs**: Instruct the model not to ask for clarification or defer to the user when encountering uncertainty
4. **Research Autonomously**: Encourage the model to investigate and deduce rather than escalate

### Tool Preambles

GPT-5 is trained to provide clear upfront plans and consistent progress updates via "tool preambles"—intermediate messages that explain the agent's strategy and progress. These significantly improve user experience, especially for longer-running tasks.

**High-Quality Preamble Structure**:
- Rephrase the user's goal clearly and concisely
- Outline a structured plan with logical steps
- Summarize completed work distinctly from the upfront plan

### Reasoning Effort Parameter

The `reasoning_effort` parameter controls how deeply the model thinks and how willing it is to call tools:

- **Default**: `medium`
- **Recommendation**: Scale up for complex, multi-step tasks; scale down for simple, focused tasks
- **Best Practice**: Break distinct, separable tasks across multiple agent turns (one turn per task)

### Responses API for Agentic Workflows

The [[Responses API]] offers significant advantages over [[Chat Completions]]:

- **Reasoning Persistence**: Previous reasoning is retained between tool calls via `previous_response_id`
- **Performance Gains**: Observed improvements of 4.3% (73.9% → 78.2%) on Tau-Bench Retail scores
- **Token Efficiency**: Conserves [[Chain-of-Thought]] (CoT) tokens by eliminating plan reconstruction after each tool call
- **Latency Reduction**: Faster response times due to more efficient reasoning reuse

---

## Coding Capabilities

### Overview

GPT-5 leads all frontier models in [[code generation]] and [[software engineering]] tasks. It excels at:

- Working in large codebases to fix bugs and handle large diffs
- Implementing multi-file refactors and large new features
- Building entire applications from scratch (frontend and backend)
- Maintaining consistency with existing code style and standards

### Recommended Technology Stack

For optimal results with GPT-5, use:

**Frameworks**:
- [[Next.js]] (TypeScript)
- [[React]]
- HTML

**Styling & UI**:
- [[Tailwind CSS]]
- [[shadcn/ui]]
- [[Radix Themes]]

**Icons**:
- Material Symbols
- Heroicons
- Lucide

**Animation**:
- Motion

**Fonts**:
- San Serif, Inter, Geist, Mona Sans, IBM Plex Sans, Manrope

**State Management**:
- Zustand

### Frontend App Development

#### Zero-to-One App Generation

GPT-5 excels at building applications in a single pass. To maximize quality:

1. **Self-Reflection Rubrics**: Ask the model to iteratively execute against self-constructed excellence rubrics
2. **Planning Phase**: Spend time thinking through a rubric for what constitutes world-class implementation
3. **Iteration**: Use the rubric to internally think and iterate on the best possible solution

#### Matching Codebase Design Standards

When implementing incremental changes in existing applications:

1. **Automatic Context Search**: GPT-5 automatically searches for reference context (e.g., reading `package.json`)
2. **Explicit Standards Documentation**: Provide a structured summary of:
   - Engineering principles
   - Directory structure
   - Best practices (explicit and implicit)

**Example Code Editing Rules Structure**:

```
<code_editing_rules>
<guiding_principles>
  - Clarity and Reuse: Modular, reusable components
  - Consistency: Adherence to design system
  - Simplicity: Small, focused components
  - Demo-Oriented: Quick prototyping capability
  - Visual Quality: High visual standards
</guiding_principles>

<frontend_stack_defaults>
  - Framework: Next.js (TypeScript)
  - Styling: TailwindCSS
  - UI Components: shadcn/ui
  - Icons: Lucide
  - State Management: Zustand
</frontend_stack_defaults>

<ui_ux_best_practices>
  - Visual Hierarchy: 4-5 font sizes/weights
  - Color Usage: 1 neutral base + up to 2 accents
  - Spacing: Multiples of 4 for padding/margins
  - State Handling: Skeleton placeholders, animate-pulse
  - Accessibility: Semantic HTML, ARIA roles
</ui_ux_best_practices>
</code_editing_rules>
```

### Cursor's GPT-5 Integration

[[Cursor]], the AI code editor, conducted extensive testing with GPT-5 and published detailed findings on prompt optimization:

#### System Prompt and Parameter Tuning

**Initial Challenge**: The model produced verbose outputs with status updates that disrupted user flow, while code was sometimes hard to read due to terseness.

**Solution**: 
- Set `verbosity: low` to keep text outputs brief
- Modified prompts to strongly encourage verbose outputs in coding tools only
- Result: Balanced format with efficient status updates and readable code diffs

#### Addressing Premature Task Termination

**Challenge**: GPT-5 occasionally deferred to users for clarification before taking action, creating friction in longer tasks.

**Solution**:
- Include detailed product behavior information
- Highlight specific features (e.g., Undo/Reject code, user preferences