---
title: The-Complete-Guide-to-Building-Skill-for-Claude_copy
source_file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:55:33.761870
raw_file_updated: 2026-04-17T20:55:33.761870
version: 1
sources:
  - file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:55:33.761870
tags: []
related_topics: []
backlinked_by: []
---
# Agent Skills for Claude

## Summary

**Agent Skills** are packaged sets of instructions that teach Claude how to handle specific tasks and workflows. Skills enable users to create consistent, reusable capabilities without re-explaining preferences and domain expertise in every conversation. They work across all Claude interfaces (Claude.ai, Claude Code, and API) and can be enhanced with [[Model Context Protocol|MCP]] integrations for tool access.

---

## Overview

A skill is fundamentally a folder containing structured documentation and optional executable code that customizes Claude's behavior for specific use cases. Rather than treating each conversation as a blank slate, skills embed organizational knowledge, best practices, and workflow guidance directly into Claude's system prompt through a three-level progressive disclosure system.

### Core Value Proposition

Skills are most powerful for:
- **Repeatable workflows** - Generating frontend designs, conducting research with consistent methodology, creating documents following style guides
- **Multi-step processes** - Coordinating actions across multiple tools or services
- **Domain expertise** - Embedding specialized knowledge that shouldn't be re-explained
- **Organizational standards** - Ensuring consistent output across teams and departments

---

## Fundamentals

### What Is a Skill?

A skill consists of:

- **SKILL.md** (required) - Main skill file containing [[YAML]] frontmatter and Markdown instructions
- **scripts/** (optional) - Executable code in Python, Bash, or other languages
- **references/** (optional) - Additional documentation loaded on-demand
- **assets/** (optional) - Templates, fonts, icons, and other resources

### Core Design Principles

#### Progressive Disclosure

Skills use a three-level system to minimize token usage while maintaining specialized expertise:

1. **First Level (YAML Frontmatter)** - Always loaded in Claude's system prompt. Provides just enough information for Claude to recognize when the skill is relevant without loading all content into context.

2. **Second Level (SKILL.md Body)** - Loaded when Claude determines the skill is relevant to the current task. Contains full instructions and guidance.

3. **Third Level (Linked Files)** - Additional bundled files that Claude can navigate and discover only as needed.

#### Composability

Skills are designed to work alongside other skills. They should not assume they are the only capability available and should integrate cleanly with other loaded skills.

#### Portability

Skills work identically across all Claude interfaces without modification, provided the environment supports any required dependencies. This enables write-once, deploy-everywhere functionality.

### Skills and MCP Integration

For developers building [[Model Context Protocol|MCP]] servers, skills provide the knowledge layer on top of tool access.

**The Kitchen Analogy:**
- **MCP** provides the professional kitchen - access to tools, ingredients, and equipment
- **Skills** provide the recipes - step-by-step instructions on how to create something valuable

| Aspect | MCP (Connectivity) | Skills (Knowledge) |
|--------|-------------------|-------------------|
| **Purpose** | Connects Claude to external services | Teaches Claude how to use services effectively |
| **Provides** | Real-time data access and tool invocation | Workflow guidance and best practices |
| **Answers** | What Claude can do | How Claude should do it |

**Benefits of combining both:**
- Pre-built workflows activate automatically when needed
- Consistent, reliable tool usage across conversations
- Best practices embedded in every interaction
- Reduced learning curve for integration users

---

## Planning and Design

### Start with Use Cases

Before writing any code, identify 2-3 concrete use cases the skill should enable. Each use case should specify:

- **Trigger** - What the user says or does
- **Steps** - Multi-step workflow required
- **Tools** - Built-in capabilities or [[Model Context Protocol|MCP]] tools needed
- **Result** - What success looks like

### Use Case Categories

Anthropic has identified three common skill categories based on real-world usage:

#### Category 1: Document & Asset Creation

**Purpose:** Creating consistent, high-quality output including documents, presentations, applications, designs, and code.

**Key Techniques:**
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities without external tools

**Example:** Frontend design skill that creates production-grade interfaces with consistent design quality.

#### Category 2: Workflow Automation

**Purpose:** Multi-step processes that benefit from consistent methodology, including coordination across multiple services.

**Key Techniques:**
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Example:** Skill-creator skill that guides users through the process of creating new skills.

#### Category 3: MCP Enhancement

**Purpose:** Workflow guidance that enhances the tool access an [[Model Context Protocol|MCP]] server provides.

**Key Techniques:**
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

**Example:** Sentry code review skill that automatically analyzes and fixes detected bugs using Sentry's error monitoring data.

### Define Success Criteria

Success metrics should be both quantitative and qualitative targets:

**Quantitative Metrics:**
- Skill triggers on 90% of relevant queries
- Completes workflow in X tool calls
- Zero failed API calls per workflow

**Qualitative Metrics:**
- Users don't need to prompt Claude about next steps
- Workflows complete without user correction
- Consistent results across sessions

---

## Technical Requirements

### File Structure

```
your-skill-name/
├── SKILL.md              # Required - main skill file
├── scripts/              # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/           # Optional - documentation
│   ├── api-guide.md
│   └── examples/
└── assets/              # Optional - templates, etc.
    └── report-template.md
```

### Critical Naming Rules

**SKILL.md:**
- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted

**Skill Folder:**
- Use kebab-case: `notion-project-setup` ✅
- No spaces, underscores, or capitals

**No README.md:**
- Don't include `README.md` inside the skill folder
- All documentation goes in `SKILL.md` or `references/`
- For GitHub distribution, use a repo-level README for human users

### YAML Frontmatter

The frontmatter is how Claude decides whether to load your skill. It is the most critical component.

**Minimal Required Format:**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Field Requirements:**

**name** (required):
- kebab-case only
- No spaces or capitals
- Should match folder name

**description** (required):
- MUST include both what the skill does AND when to use it
- Under 1024 characters
- No XML tags (`<` or `>`)
- Include specific tasks users might say
- Mention file types if relevant

**license** (optional):
- Use for open-source skills
- Common: `MIT`, `Apache-2.0`

**compatibility** (optional):
- 1-500 characters
- Indicates environment requirements and dependencies

**metadata** (optional):
- Custom key-value pairs
- Suggested: `author`, `version`, `mcp-server`

### Security Restrictions

**Forbidden in frontmatter:**
- XML angle brackets (`<` `>`)
- Skills with "claude" or "anthropic" in name (reserved)

These restrictions exist because frontmatter appears in Claude's system prompt, and malicious content could inject unauthorized instructions.

### Writing Effective Descriptions

The description field implements the first level of progressive disclosure. It should follow this structure:

**[What it does] + [When to use it] + [Key capabilities]**

**Good Examples:**

> Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

> Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

**Bad Examples:**

- Too vague: "Helps with projects."
- Missing triggers: "Creates sophisticated multi-page documentation systems."
- Too technical: "Implements the Project entity model with hierarchical relationships."

### Writing Main Instructions

After the frontmatter, write instructions in Markdown following this recommended structure:

```markdown
# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example: