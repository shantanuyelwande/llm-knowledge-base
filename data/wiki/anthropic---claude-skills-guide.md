---
title: Anthropic - Claude Skills Guide
source_file: Anthropic - Claude Skills Guide.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:06:05.167393
raw_file_updated: 2026-04-17T21:06:05.167393
version: 1
sources:
  - file: Anthropic - Claude Skills Guide.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:06:05.167393
tags: []
related_topics: []
backlinked_by: []
---
# Claude Skills Guide

## Summary

A comprehensive guide to building, testing, and distributing **skills** for Claude—reusable instruction sets that teach Claude to handle specific tasks and workflows consistently. Skills are packaged as simple folders containing a SKILL.md file with YAML frontmatter, optional scripts, references, and assets. They work across Claude.ai, Claude Code, and the API, enabling users to customize Claude for their specific needs without re-explaining preferences in every conversation.

---

## Table of Contents

1. [Overview](#overview)
2. [Fundamentals](#fundamentals)
3. [Planning and Design](#planning-and-design)
4. [Testing and Iteration](#testing-and-iteration)
5. [Distribution and Sharing](#distribution-and-sharing)
6. [Patterns and Troubleshooting](#patterns-and-troubleshooting)
7. [Resources](#resources)

---

## Overview

### What is a Skill?

A **skill** is a set of instructions packaged as a simple folder that teaches [[Claude]] how to handle specific tasks or workflows. Rather than re-explaining preferences, processes, and domain expertise in every conversation, skills allow you to teach Claude once and benefit every time.

Skills are particularly powerful for:
- Generating frontend designs from specifications
- Conducting research with consistent methodology
- Creating documents following team style guides
- Orchestrating multi-step processes
- Coordinating with [[Model Context Protocol (MCP)]] integrations

### Who Should Build Skills?

- Developers who want Claude to follow specific workflows consistently
- Power users seeking to standardize Claude's behavior
- Teams looking to establish organization-wide standards for Claude usage
- [[MCP]] server builders enhancing tool access with workflow guidance

### Key Benefits

- **Consistency**: Claude follows the same process every time
- **Efficiency**: Eliminates repetitive explanations and prompt engineering
- **Portability**: Works identically across Claude.ai, Claude Code, and the API
- **Composability**: Multiple skills can load simultaneously without conflicts
- **Token Optimization**: Progressive disclosure minimizes context usage

---

## Fundamentals

### Skill Structure

A skill is a folder containing:

```
your-skill-name/
├── SKILL.md              # Required - main skill file
├── scripts/              # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/           # Optional - documentation
│   ├── api-guide.md
│   └── examples/
└── assets/              # Optional - templates, fonts, icons
    └── report-template.md
```

#### Critical Naming Rules

- **Folder name**: Use kebab-case (e.g., `notion-project-setup` ✅)
  - No spaces, underscores, or capitals
- **Main file**: Must be exactly `SKILL.md` (case-sensitive)
  - No variations like `SKILL.MD` or `skill.md`
- **No README.md**: All documentation goes in SKILL.md or references/

### Core Design Principles

#### Progressive Disclosure

Skills use a three-level system to minimize token usage:

1. **YAML Frontmatter** (always loaded): Provides just enough information for Claude to know when to use the skill without loading all content
2. **SKILL.md Body** (loaded when relevant): Full instructions and guidance
3. **Linked Files** (loaded as needed): Additional documentation, templates, and resources

#### Composability

Skills are designed to work alongside other skills. A well-designed skill:
- Doesn't assume it's the only capability available
- Coordinates with other tools and skills
- Explicitly handles edge cases involving multiple skills

#### Portability

Skills work identically across all Claude surfaces (Claude.ai, Claude Code, API) without modification, provided the environment supports any required dependencies.

### YAML Frontmatter: The Critical Component

The YAML frontmatter determines whether Claude loads your skill. It must appear at the top of SKILL.md, enclosed in triple dashes.

#### Required Fields

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

#### Field Specifications

**name** (required)
- kebab-case only
- No spaces or capitals
- Should match folder name

**description** (required)
- Must include both: what the skill does AND when to use it
- Under 1024 characters
- No XML tags (< or >)
- Include specific trigger phrases users might say
- Mention file types if relevant

**license** (optional)
- Use for open-source skills
- Common values: MIT, Apache-2.0

**compatibility** (optional)
- 1-500 characters
- Indicates environment requirements (product, system packages, network access)

**metadata** (optional)
- Custom key-value pairs
- Suggested: author, version, mcp-server

#### Security Restrictions

Forbidden in frontmatter:
- XML angle brackets (< >)
- Skills named with "claude" or "anthropic" prefix (reserved)

### Writing Effective Descriptions

The description is the first level of progressive disclosure. Structure it as:

**[What it does] + [When to use it] + [Key capabilities]**

#### Good Examples

```
Analyzes Figma design files and generates developer handoff 
documentation. Use when user uploads .fig files, asks for 
"design specs", "component documentation", or "design-to-code 
handoff".
```

```
Manages Linear project workflows including sprint planning, 
task creation, and status tracking. Use when user mentions 
"sprint", "Linear tasks", "project planning", or asks to 
"create tickets".
```

#### Bad Examples

- Too vague: "Helps with projects."
- Missing triggers: "Creates sophisticated multi-page documentation systems."
- Too technical: "Implements the Project entity model with hierarchical relationships."

### Writing Main Instructions

After frontmatter, structure instructions in Markdown using this template:

```markdown
---
name: your-skill
description: [description]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

## Examples

### Example 1: [common scenario]
User says: "Set up a new marketing campaign"

Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters

Result: Campaign created with confirmation link

## Troubleshooting

### Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

#### Best Practices for Instructions

- **Be specific and actionable**: Include exact commands, parameters, and expected outputs
- **Include error handling**: Document common issues and solutions
- **Reference bundled resources clearly**: Link to documentation in references/
- **Use progressive disclosure**: Keep SKILL.md focused on core instructions; move detailed docs to references/

---

## Planning and Design

### Start with Use Cases

Before writing code, identify 2-3 concrete use cases your skill should enable.

#### Good Use Case Definition

```
Use Case: Project Sprint Planning

Trigger: User says "help me plan this sprint" or "create 
sprint tasks"

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
- Which tools are needed (built-in or [[MCP]])?
- What domain knowledge or best practices should be embedded?

### Common Skill Use Case Categories

#### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output including documents, presentations, apps, designs, and code.

**Real example**: Frontend design skill

**Key techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities

#### Category 2: Workflow Automation

**Used for**: Multi-step processes benefiting from consistent methodology, including coordination across multiple [[MCP]] servers.

**Real example**: skill-creator skill

**Key techniques**:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

#### Category 3: MCP Enhancement

**Used for**: Workflow guidance to enhance tool access an [[MCP]] server provides.

**Real example**: sentry-code-review skill (from Sentry)

**Key techniques**:
- Coordinates multiple [[M