---
title: GPT 5 PROMPTING GUIDE
source_file: GPT 5 PROMPTING GUIDE.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:04:32.594231
raw_file_updated: 2026-04-17T21:04:32.594231
version: 1
sources:
  - file: GPT 5 PROMPTING GUIDE.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:04:32.594231
tags: []
related_topics: []
backlinked_by: []
---
# GPT-5 Prompting Guide

## Summary

The GPT-5 Prompting Guide is an official resource from [[OpenAI]] that provides best practices for maximizing the quality of outputs from [[GPT-5]], their flagship language model. Published on August 7, 2025, the guide covers agentic task performance, instruction adherence, coding optimization, and API features. It emphasizes that GPT-5 represents significant improvements in tool calling, instruction following, and long-context understanding, making it particularly suited for [[agentic workflows]] and software development tasks.

## Overview

[[GPT-5]] is described as a substantial leap forward in agentic task performance, coding capabilities, raw intelligence, and [[steerability]]. While the model performs well "out of the box" across various domains, this guide provides evidence-based prompting techniques derived from real-world applications and training experience. The guide acknowledges that prompting is not a one-size-fits-all discipline and encourages experimentation and iteration.

## Table of Contents

1. [Agentic Workflows](#agentic-workflows)
2. [Coding Performance](#coding-performance)
3. [Instruction Following](#instruction-following)
4. [Minimal Reasoning](#minimal-reasoning)
5. [Steering and Control](#steering-and-control)
6. [Production Applications](#production-applications)
7. [Appendix](#appendix)

---

## Agentic Workflows

### Overview

GPT-5 was trained with developers in mind, focusing on improving [[tool calling]], instruction following, and long-context understanding to serve as the best foundation model for agentic applications. The guide recommends upgrading to the [[Responses API]] for agentic workflows, where [[reasoning]] is persisted between tool calls, leading to more efficient and intelligent outputs.

### Controlling Agentic Eagerness

Agentic scaffolds span a wide spectrum of control—from systems that delegate the vast majority of decision-making to the model, to those that keep the model on a tight leash with heavy programmatic logical branching. GPT-5 is trained to operate anywhere along this spectrum.

#### Prompting for Less Eagerness

By default, GPT-5 is thorough and comprehensive when gathering context in agentic environments. To reduce the scope of agentic behavior and minimize latency:

- **Lower reasoning_effort**: Reduces exploration depth while improving efficiency and latency. Many workflows can be accomplished with consistent results at medium or even low reasoning_effort.
- **Define clear exploration criteria**: Specify in your prompt how you want the model to explore the problem space, reducing unnecessary reasoning.
- **Set tool call budgets**: Establish fixed limits on the number of tool calls allowed (e.g., maximum of 2 calls).
- **Provide escape hatches**: Include clauses that allow the model to proceed under uncertainty, such as "even if it might not be fully correct."

#### Prompting for More Eagerness

To encourage model autonomy and reduce clarifying questions:

- **Increase reasoning_effort**: Use higher reasoning levels for complex, multi-step tasks.
- **Use persistence directives**: Include instructions like "You are an agent - please keep going until the user's query is completely resolved."
- **Reduce uncertainty thresholds**: Instruct the model to research and investigate rather than asking for clarification.
- **Avoid escalation requests**: Discourage the model from handing back to the user when encountering ambiguity.

### Tool Safety and Uncertainty Thresholds

Different tools should have different uncertainty thresholds for requiring user clarification. For example:
- **Low threshold tools** (e.g., checkout, payment, file deletion): Require explicit user confirmation before execution
- **High threshold tools** (e.g., search, read operations): Can operate with minimal confirmation

### Tool Preambles

GPT-5 is trained to provide clear upfront plans and consistent progress updates via "tool preamble" messages. You can steer the frequency, style, and content of these preambles:

- Rephrase the user's goal in a friendly, clear, and concise manner
- Outline a structured plan detailing each logical step
- Summarize completed work distinctly from the upfront plan

Tool preambles significantly improve user ability to follow along with increasingly complex agent work.

### Reasoning Effort Parameter

The `reasoning_effort` parameter controls how hard the model thinks and how willingly it calls tools:
- **Default**: medium
- **Recommendation**: Scale up for complex, multi-step tasks; scale down for simpler tasks
- **Best practice**: Break distinct, separable tasks across multiple agent turns, with one turn per task

### Responses API and Reasoning Context Reuse

The [[Responses API]] offers significant advantages over Chat Completions:

- **Persistent reasoning**: Reasoning is maintained between tool calls
- **Token efficiency**: Eliminates the need to reconstruct plans from scratch after each tool call
- **Performance gains**: Observed Tau-Bench Retail score increases from 73.9% to 78.2% by switching to the Responses API and using `previous_response_id`
- **Latency improvement**: Conserves CoT tokens and improves response time
- **Availability**: Available for all Responses API users, including ZDR organizations

---

## Coding Performance

### Overview

GPT-5 leads all frontier models in coding capabilities. It can work in large codebases to fix bugs, handle large diffs, implement multi-file refactors, and develop large new features. It also excels at implementing new applications from scratch, covering both [[frontend development|frontend]] and [[backend development|backend]] implementation.

### Frontend App Development

GPT-5 is trained with excellent baseline aesthetic taste alongside rigorous implementation abilities. For new apps, OpenAI recommends using:

**Frameworks**:
- [[Next.js]] (TypeScript)
- [[React]]
- HTML

**Styling / UI**:
- [[Tailwind CSS]]
- shadcn/ui
- Radix Themes

**Icons**:
- Material Symbols
- Heroicons
- Lucide

**Animation**:
- Motion

**Fonts**:
- San Serif
- Inter
- Geist
- Mona Sans
- IBM Plex Sans
- Manrope

### Zero-to-One App Generation

GPT-5 excels at building applications in one shot. Early experimentation shows that prompts asking the model to iteratively execute against self-constructed excellence rubrics improve output quality by leveraging GPT-5's thorough planning and self-reflection capabilities.

**Self-Reflection Process**:
- First, spend time thinking of a rubric until confident
- Think deeply about every aspect of what makes for a world-class application
- Use the rubric to internally think and iterate on the best possible solution

### Matching Codebase Design Standards

When implementing incremental changes and refactors in existing applications, model-written code should adhere to existing style and design standards. While GPT-5 already searches for reference context (e.g., reading package.json), behavior can be enhanced with prompt directions that summarize:

- Engineering principles
- Directory structure
- Best practices (explicit and implicit)

#### Recommended Code Editing Rules Structure

**Guiding Principles**:
- **Clarity and Reuse**: Every component and page should be modular and reusable
- **Consistency**: The user interface must adhere to a consistent design system
- **Simplicity**: Favor small, focused components and avoid unnecessary complexity
- **Demo-Oriented**: Structure should allow for quick prototyping and feature showcasing
- **Visual Quality**: Follow high visual quality standards

**Frontend Stack Defaults**:
- Framework: Next.js (TypeScript)
- Styling: TailwindCSS
- UI Components: shadcn/ui
- Icons: Lucide
- State Management: Zustand

**Directory Structure Example**:
```
/src
  /app              # Next.js app routes
  /api/<route>/     # API endpoints
  /(pages)          # Page routes
  /components/      # UI building blocks
  /hooks/           # Reusable React hooks
  /lib/             # Utilities (fetchers, helpers)
  /stores/          # Zustand stores
  /types/           # Shared TypeScript types
  /styles/          # Tailwind config
```

**UI/UX Best Practices**:
- **Visual Hierarchy**: Limit typography to 4–5 font sizes and weights for consistency
- **Color Usage**: Use 1 neutral base (e.g., `zinc`) and up to 2 accent colors
- **Spacing and Layout**: Always use multiples of 4 for padding and margins
- **State Handling**: Use skeleton placeholders or `animate-pulse` to indicate data loading
- **Accessibility**: Use semantic HTML and ARIA roles where appropriate

###