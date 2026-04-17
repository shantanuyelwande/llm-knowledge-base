---
title: Anthropic - Claude Skills Guide
source_file: Anthropic - Claude Skills Guide.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T21:12:48.165816
raw_file_updated: 2026-04-05T21:12:48.165816
version: 1
sources:
  - file: Anthropic - Claude Skills Guide.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T21:12:48.165816
tags: ["skills", "claude-ai", "customization", "workflows", "api", "instructions"]
related_topics: []
backlinked_by: []

---
# Claude Skills Guide

## Summary

A **skill** is a packaged set of instructions that teaches Claude how to handle specific tasks or workflows. Skills are powerful customization tools that enable consistent, repeatable workflows across [[Claude.ai]], [[Claude Code]], and the [[Claude API]]. They follow a progressive disclosure design pattern to minimize token usage while maintaining specialized expertise, and can work independently or enhance [[Model Context Protocol]] (MCP) integrations.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Fundamentals](#fundamentals)
4. [Planning and Design](#planning-and-design)
5. [Technical Requirements](#technical-requirements)
6. [Testing and Iteration](#testing-and-iteration)
7. [Distribution](#distribution)
8. [Patterns and Troubleshooting](#patterns-and-troubleshooting)

---

## Overview

### What is a Skill?

A skill is a folder containing structured instructions packaged in [[Markdown]] format with [[YAML]] frontmatter. Skills teach Claude to follow specific workflows, preferences, and domain expertise consistently across conversations. Rather than re-explaining requirements in every conversation, users define a skill once and benefit from it automatically in all future interactions.

### When to Use Skills

Skills are particularly powerful for:

- **Repeatable workflows**: Generating frontend designs from specifications, conducting research with consistent methodology, creating documents following style guides
- **Multi-step processes**: Orchestrating complex workflows that benefit from consistent execution
- **Domain expertise**: Embedding specialized knowledge and best practices
- **Tool coordination**: Combining [[Model Context Protocol]] tools with workflow guidance

### Who Should Build Skills

- Developers building custom Claude integrations
- Power users standardizing workflows
- Organizations establishing company-wide Claude practices
- MCP server creators enhancing tool access with workflow guidance

---

## Core Concepts

### Progressive Disclosure

Skills use a three-level information architecture to minimize token usage:

1. **First Level (YAML Frontmatter)**: Always loaded in Claude's system prompt. Provides just enough information for Claude to know when a skill should be used without loading the entire skill into context.

2. **Second Level (SKILL.md Body)**: Loaded when Claude determines the skill is relevant to the current task. Contains full instructions and detailed guidance.

3. **Third Level (Linked Files)**: Additional documentation bundled within the skill directory (in `references/`, `scripts/`, or `assets/`) that Claude can navigate and discover only as needed.

This architecture minimizes token consumption while maintaining specialized expertise.

### Composability

Skills are designed to work together. A single skill should:

- Work well alongside other enabled skills
- Not assume it's the only capability available
- Clearly define its scope and triggers
- Avoid overlapping with common use cases

### Portability

Skills work identically across all Claude surfaces:

- [[Claude.ai]]
- [[Claude Code]]
- [[Claude API]]

Create a skill once and deploy it everywhere without modification, provided the environment supports any required dependencies.

### Skills + MCP Integration

For [[Model Context Protocol]] builders, skills and MCP servers work together as complementary layers:

| Aspect | MCP | Skills |
|--------|-----|--------|
| **Purpose** | Connectivity | Knowledge |
| **Function** | Connects Claude to services and data | Teaches Claude how to use services effectively |
| **Access** | Real-time data and tool invocation | Workflow guidance and best practices |
| **User Impact** | "What Claude can do" | "How Claude should do it" |

Without skills, users must discover workflows themselves. With skills, pre-built workflows activate automatically, providing consistent, reliable tool usage with embedded best practices.

---

## Fundamentals

### File Structure

A skill is organized as follows:

```
your-skill-name/
├── SKILL.md                 # Required - main skill file with instructions
├── scripts/                 # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/              # Optional - documentation and guides
│   ├── api-guide.md
│   └── examples/
└── assets/                  # Optional - templates, fonts, icons
    └── report-template.md
```

### Critical Naming Rules

- **SKILL.md**: Must be exactly this name (case-sensitive). No variations like `SKILL.MD`, `skill.md`, or `Skill.md` are accepted.
- **Folder name**: Use kebab-case (e.g., `notion-project-setup`). No spaces, underscores, or capital letters.
- **No README.md**: Do not include a README inside the skill folder. All documentation goes in `SKILL.md` or `references/`. (Note: When distributing via GitHub, include a repo-level README for human visitors.)

### YAML Frontmatter

The YAML frontmatter is how Claude decides whether to load your skill. It must be correctly formatted.

#### Minimal Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

#### Required Fields

**name** (required)
- Must be in kebab-case
- No spaces or capital letters
- Should match the folder name

**description** (required)
- Must include BOTH what the skill does AND when to use it
- Maximum 1024 characters
- No XML tags (`<` or `>`)
- Should include specific trigger phrases users might say
- Should mention relevant file types if applicable

#### Optional Fields

**license**
- Use for open-source skills
- Common values: `MIT`, `Apache-2.0`

**compatibility**
- 1-500 characters
- Indicates environment requirements (intended product, required system packages, network access needs)

**metadata**
- Custom key-value pairs
- Suggested fields: `author`, `version`, `mcp-server`
- Example:
  ```yaml
  metadata:
    author: ProjectHub
    version: 1.0.0
    mcp-server: projecthub
  ```

#### Security Restrictions

Forbidden in frontmatter:
- XML angle brackets (`<` or `>`)
- Skill names containing "claude" or "anthropic" (reserved)

Reason: Frontmatter appears in Claude's system prompt, so malicious content could inject instructions.

### Writing Effective Descriptions

The description field is critical for proper skill triggering. Structure it as:

**[What it does] + [When to use it] + [Key capabilities]**

#### Good Description Examples

```yaml
description: Analyzes Figma design files and generates developer 
handoff documentation. Use when user uploads .fig files, asks for 
"design specs", "component documentation", or "design-to-code handoff".
```

```yaml
description: Manages Linear project workflows including sprint planning, 
task creation, and status tracking. Use when user mentions "sprint", 
"Linear tasks", "project planning", or asks to "create tickets".
```

```yaml
description: End-to-end customer onboarding workflow for PayFlow. 
Handles account creation, payment setup, and subscription management. 
Use when user says "onboard new customer", "set up subscription", or 
"create PayFlow account".
```

#### Poor Description Examples

- **Too vague**: "Helps with projects."
- **Missing triggers**: "Creates sophisticated multi-page documentation systems."
- **Too technical**: "Implements the Project entity model with hierarchical relationships."

---

## Planning and Design

### Start with Use Cases

Before writing any code, identify 2-3 concrete use cases your skill should enable.

#### Good Use Case Definition

```
Use Case: Project Sprint Planning

Trigger: User says "help me plan this sprint" or "create sprint tasks"

Steps:
1. Fetch current project status from Linear (via MCP)
2. Analyze team velocity and capacity
3. Suggest task prioritization
4. Create tasks in Linear with proper labels and estimates

Result: Fully planned sprint with tasks created
```

#### Key Questions

- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?

### Common Skill Use Case Categories

#### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output including documents, presentations, apps, designs, and code.

**Real example**: [[frontend-design skill]] - "Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications."

**Key techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities (no external tools required)

#### Category 