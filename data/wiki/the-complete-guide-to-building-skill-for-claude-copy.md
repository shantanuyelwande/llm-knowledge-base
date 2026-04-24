---
title: The-Complete-Guide-to-Building-Skill-for-Claude_copy
source_file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:55:04.271761
raw_file_updated: 2026-04-24T18:55:04.271761
version: 1
sources:
  - file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:55:04.271761
tags: []
related_topics: []
backlinked_by: []
---
# Agent Skills for Claude

## Summary

Agent Skills are structured packages that teach Claude how to handle specific tasks and workflows. A skill is a folder containing instructions in Markdown with YAML frontmatter, optional executable scripts, reference documentation, and assets. Skills enable consistent, repeatable workflows across Claude.ai, Claude Code, and API environments without requiring repeated explanations of preferences and domain expertise.

## Overview

A **skill** is one of the most powerful ways to customize [[Claude]] for specific needs. Rather than re-explaining preferences, processes, and domain expertise in every conversation, skills allow you to teach Claude once and benefit from that knowledge across all interactions.

### Core Concept

Skills are most valuable when you have:
- **Repeatable workflows** - generating designs from specifications, conducting research with consistent methodology, creating branded documents, or orchestrating multi-step processes
- **Domain expertise** - specialized knowledge that should be applied consistently
- **Tool coordination** - workflows requiring multiple tools or [[MCP|MCP servers]] in sequence

### Relationship to MCP

[[MCP|Message Context Protocol (MCP)]] provides the **connectivity layer**, while skills provide the **knowledge layer**:

| Aspect | MCP | Skills |
|--------|-----|--------|
| Function | Connects Claude to services and tools | Teaches Claude how to use services effectively |
| Provides | Real-time data access and tool invocation | Workflows and best practices |
| Enables | What Claude can do | How Claude should do it |

Together, they transform raw tool access into reliable, optimized workflows. The analogy: MCP is the professional kitchen (tools, ingredients, equipment), while skills are the recipes (step-by-step instructions).

## File Structure and Requirements

### Directory Organization

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

### Critical Rules

**SKILL.md naming:**
- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted (`SKILL.MD`, `skill.md`, etc.)

**Folder naming:**
- Use kebab-case: `notion-project-setup` ✓
- No spaces, underscores, or capitals

**No README.md:**
- Don't include `README.md` inside the skill folder
- All documentation goes in `SKILL.md` or `references/`
- Note: When distributing via GitHub, include a repo-level README for human users

## YAML Frontmatter

The YAML frontmatter is how Claude decides whether to load your skill. This section appears in Claude's system prompt and implements the first level of [[#Progressive Disclosure|progressive disclosure]].

### Minimal Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

### Required Fields

**name:**
- kebab-case only
- No spaces or capitals
- Should match folder name

**description:**
- MUST include BOTH: what the skill does AND when to use it (trigger conditions)
- Under 1,024 characters
- No XML tags (`<` or `>`)
- Include specific tasks users might say
- Mention file types if relevant

### Optional Fields

**license:**
- Use if making skill open source
- Common values: `MIT`, `Apache-2.0`

**compatibility:**
- 1-500 characters
- Indicates environment requirements: intended product, required system packages, network access needs

**metadata:**
- Any custom key-value pairs
- Suggested fields: `author`, `version`, `mcp-server`

```yaml
metadata:
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
```

### Security Restrictions

Forbidden in frontmatter:
- XML angle brackets (`<` or `>`)
- Skills with "claude" or "anthropic" in name (reserved)

**Reason:** Frontmatter appears in Claude's system prompt. Malicious content could inject instructions.

## Core Design Principles

### Progressive Disclosure

Skills use a three-level system to minimize [[token]] usage while maintaining specialized expertise:

1. **First level (YAML frontmatter):** Always loaded in Claude's system prompt. Provides just enough information for Claude to know when each skill should be used without loading all of it into context.

2. **Second level (SKILL.md body):** Loaded when Claude thinks the skill is relevant to the current task. Contains full instructions and guidance.

3. **Third level (Linked files):** Additional files bundled within the skill directory that Claude can choose to navigate and discover only as needed.

### Composability

Claude can load multiple skills simultaneously. Your skill should work well alongside others, not assume it's the only capability available. Design with this multi-skill environment in mind.

### Portability

Skills work identically across:
- [[Claude.ai]]
- Claude Code
- [[Claude API]]

Create a skill once and it works across all surfaces without modification, provided the environment supports any dependencies the skill requires.

## Planning and Design

### Start with Use Cases

Before writing any code, identify 2-3 concrete use cases your skill should enable.

**Good use case definition includes:**
- What the user wants to accomplish
- What multi-step workflows this requires
- Which tools are needed (built-in or MCP)
- What domain knowledge or best practices should be embedded

Example:
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

### Common Skill Use Case Categories

**Category 1: Document & Asset Creation**
- Used for: Creating consistent, high-quality output (documents, presentations, apps, designs, code)
- Example: [[#frontend-design skill|frontend-design skill]]
- Key techniques: Embedded style guides, template structures, quality checklists, uses Claude's built-in capabilities

**Category 2: Workflow Automation**
- Used for: Multi-step processes requiring consistent methodology, including coordination across multiple MCP servers
- Example: skill-creator skill
- Key techniques: Step-by-step workflows with validation gates, templates, built-in review suggestions, iterative refinement loops

**Category 3: MCP Enhancement**
- Used for: Workflow guidance to enhance tool access provided by MCP servers
- Example: sentry-code-review skill (from Sentry)
- Key techniques: Coordinates multiple MCP calls in sequence, embeds domain expertise, provides context, handles common MCP issues

### Define Success Criteria

Establish how you'll know your skill is working. These are aspirational targets—rough benchmarks rather than precise thresholds.

**Quantitative metrics:**
- Skill triggers on 90% of relevant queries
- Completes workflow in X tool calls
- 0 failed API calls per workflow

**Qualitative metrics:**
- Users don't need to prompt Claude about next steps
- Workflows complete without user correction
- Consistent results across sessions

## Writing Effective Skills

### The Description Field

The description is the first level of [[#Progressive Disclosure|progressive disclosure]].

**Structure:** `[What it does] + [When to use it] + [Key capabilities]`

**Good examples:**
- "Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'."
- "Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions 'sprint', 'Linear tasks', 'project planning', or asks to 'create tickets'."

**Bad examples:**
- "Helps with projects." (too vague)
- "Creates sophisticated multi-page documentation systems." (missing triggers)
- "Implements the Project entity model with hierarchical relationships." (too technical, no user triggers)

### Writing Main Instructions

After the frontmatter, write actual instructions in Markdown.

**Recommended structure:**

```markdown
# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

### Examples

#### Example 1: [common scenario]
User says: "Set up a new