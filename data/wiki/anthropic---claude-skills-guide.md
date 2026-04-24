---
title: Anthropic - Claude Skills Guide
source_file: Anthropic - Claude Skills Guide.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:06:04.161541
raw_file_updated: 2026-04-24T19:06:04.161541
version: 1
sources:
  - file: Anthropic - Claude Skills Guide.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:06:04.161541
tags: []
related_topics: []
backlinked_by: []
---
# Claude Skills Guide

## Summary

**Claude Skills** are structured packages of instructions that teach Claude how to handle specific tasks and workflows consistently. Skills enable users to customize Claude for their needs without re-explaining preferences and domain expertise in every conversation. They work across Claude.ai, Claude Code, and the API, and can be enhanced with [[Model Context Protocol|MCP]] integrations for tool access.

---

## Overview

A skill is fundamentally a folder containing instructions in Markdown with YAML frontmatter, plus optional executable scripts, reference documentation, and assets. Skills represent one of the most powerful customization mechanisms for [[Claude AI|Claude]], enabling repeatable workflows across document creation, process automation, and tool integration.

### Purpose and Value

Skills address a core limitation of conversational AI: the need to re-establish context and instructions with every new conversation. By packaging domain knowledge, best practices, and step-by-step workflows into reusable skills, users can:

- Teach Claude once and benefit consistently across many conversations
- Maintain standardized processes across teams and organizations
- Reduce token consumption by avoiding repeated explanations
- Enable complex multi-step workflows without manual guidance at each step

### Target Users

Skills are designed for:
- **Developers** building consistent, repeatable workflows with Claude
- **Power users** wanting Claude to follow specific methodologies
- **Organizations** standardizing Claude usage across teams
- **MCP builders** enhancing tool integrations with workflow guidance

---

## Core Architecture

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
└── assets/              # Optional - templates, fonts, icons
    └── report-template.md
```

### Required Components

**SKILL.md** is the only required file. It must:
- Be named exactly `SKILL.md` (case-sensitive)
- Contain YAML frontmatter with metadata delimiters (`---`)
- Include a `name` field in kebab-case
- Include a `description` field explaining what the skill does and when to use it

### Naming Conventions

- **Folder names**: kebab-case (e.g., `notion-project-setup`)
- **File name**: Exactly `SKILL.md` with no variations
- **No README.md** inside the skill folder (documentation goes in SKILL.md or `references/`)

---

## Design Principles

### Progressive Disclosure

Skills implement a three-level information hierarchy to minimize token usage while maintaining specialized expertise:

1. **YAML Frontmatter** (always loaded): Minimal metadata telling Claude whether the skill is relevant to the current task
2. **SKILL.md Body** (conditionally loaded): Full instructions loaded when Claude determines the skill applies
3. **Linked Files** (on-demand): Additional documentation loaded only as needed

This approach prevents skill content from unnecessarily consuming context tokens in conversations where the skill isn't relevant.

### Composability

Skills are designed to work alongside each other. A well-designed skill:
- Doesn't assume it's the only capability available
- Coordinates cleanly with other skills
- Clearly defines its scope and boundaries
- Handles cases where multiple skills might apply

### Portability

Skills work identically across:
- [[Claude.ai]]
- [[Claude Code]]
- [[Claude API]]

A skill created once works across all surfaces without modification, provided the environment supports any required dependencies.

---

## YAML Frontmatter

The frontmatter is the critical component determining whether Claude loads a skill. It appears in Claude's system prompt and must be carefully structured.

### Minimal Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

### Field Specifications

#### name (required)
- Must be in kebab-case
- No spaces, capitals, or special characters
- Should match the folder name
- Cannot contain "claude" or "anthropic" (reserved terms)

#### description (required)
Must include both:
- **What the skill does**: Clear statement of functionality
- **When to use it**: Trigger conditions and example phrases users might say

Additional requirements:
- Under 1,024 characters
- No XML angle brackets (`<` or `>`)
- Include specific tasks and file types when relevant
- Provide example trigger phrases users would naturally use

#### license (optional)
- Used for open-source skills
- Common values: `MIT`, `Apache-2.0`

#### compatibility (optional)
- 1-500 characters
- Indicates environment requirements
- Examples: required system packages, network access needs, product compatibility

#### metadata (optional)
- Custom key-value pairs for skill information
- Suggested fields: `author`, `version`, `mcp-server`, `category`, `tags`
- Example:
  ```yaml
  metadata:
    author: ProjectHub
    version: 1.0.0
    mcp-server: projecthub
    category: productivity
  ```

### Security Restrictions

**Forbidden in frontmatter:**
- XML angle brackets (`<` or `>`)
- Skills named with "claude" or "anthropic" prefix

These restrictions exist because frontmatter appears in Claude's system prompt, making malicious content a potential injection vector.

---

## Writing Effective Skills

### Description Field Best Practices

The description is the first level of progressive disclosure. It must provide just enough information for Claude to know when the skill should be used without loading all content into context.

**Structure:** `[What it does] + [When to use it] + [Key capabilities]`

**Good Examples:**
- "Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'."
- "Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions 'sprint', 'Linear tasks', 'project planning', or asks to 'create tickets'."

**Poor Examples:**
- "Helps with projects." (too vague)
- "Creates sophisticated multi-page documentation systems." (missing trigger conditions)
- "Implements the Project entity model with hierarchical relationships." (too technical, no user triggers)

### Main Instructions Structure

After the frontmatter, organize instructions in Markdown using this recommended structure:

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

### Step 2: [Next Step]
...

## Examples

### Example 1: [common scenario]
**User says:** "Set up a new marketing campaign"

**Actions:**
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters

**Result:** Campaign created with confirmation link

## Troubleshooting

### Error: [Common error message]
**Cause:** Why it happens
**Solution:** How to fix

```

### Instruction Best Practices

**Be Specific and Actionable**
- Provide exact commands or code to run
- Explain expected outputs
- Include common failure modes and solutions

**Include Error Handling**
- Document common error messages
- Explain why errors occur
- Provide step-by-step solutions

**Reference Bundled Resources Clearly**
- Link to documentation in `references/`
- Explain what information to consult before proceeding
- Provide context for when to use external resources

**Use Progressive Disclosure**
- Keep SKILL.md focused on core instructions
- Move detailed documentation to `references/`
- Link to additional resources rather than inlining them

---

## Common Skill Use Cases

### Category 1: Document & Asset Creation

**Purpose:** Creating consistent, high-quality output including documents, presentations, applications, designs, and code.

**Real Example:** Frontend Design skill - "Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications."

**Key Techniques:**
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities (no external tools required)

### Category 2: Workflow Automation

**Purpose:** Multi-step processes that benefit from consistent methodology, including coordination across multiple [[Model Context Protocol|MCP]] servers.

**Real Example:** Skill Creator skill - "Interactive guide for creating new skills. Walks the user through use case definition, frontmatter generation, instruction writing, and validation."

**Key Techniques:**
- Step-by-step workflow with validation gates
-