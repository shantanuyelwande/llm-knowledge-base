---
title: The-Complete-Guide-to-Building-Skill-for-Claude_copy
source_file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:16:45.832189
raw_file_updated: 2026-04-17T20:16:45.832189
version: 1
sources:
  - file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:16:45.832189
tags: []
related_topics: []
backlinked_by: []
---
# Agent Skills for Claude

## Summary

Agent Skills are structured knowledge packages that teach Claude how to handle specific tasks and workflows consistently. A skill is a folder containing a `SKILL.md` file with YAML frontmatter and optional supporting files (scripts, references, assets). Skills enable users to customize Claude's behavior for repeatable workflows without re-explaining preferences and domain expertise in every conversation.

## Overview

A **skill** is a portable, reusable instruction set designed to teach [[Claude]] how to execute specific tasks or multi-step workflows. Rather than requiring users to provide the same guidance repeatedly, skills embed best practices, domain expertise, and procedural knowledge into a format that Claude can recognize and apply automatically.

### Core Purpose

Skills address a fundamental challenge in AI assistance: consistency. Without skills, users must:
- Re-explain their preferences in every conversation
- Specify the same workflows repeatedly
- Provide context that Claude should already understand
- Accept inconsistent results based on how requests are phrased

With skills, these elements are packaged once and benefit every interaction.

### Who Should Use Skills

- **Developers** building custom Claude workflows
- **Power users** who work with repeatable processes
- **Teams** standardizing Claude usage across their organization
- **MCP server creators** enhancing tool access with workflow guidance

## Technical Structure

### File Organization

A skill follows a standardized folder structure:

```
your-skill-name/
├── SKILL.md              # Required: main skill file
├── scripts/              # Optional: executable code
│   ├── process_data.py
│   └── validate.sh
├── references/           # Optional: documentation
│   ├── api-guide.md
│   └── examples/
└── assets/              # Optional: templates, fonts, icons
    └── report-template.md
```

### Critical Naming Rules

- **Folder name**: Must use kebab-case (e.g., `notion-project-setup`)
  - ✅ Correct: `my-skill-name`
  - ❌ Wrong: `My-Skill-Name`, `my_skill_name`, `MySkillName`

- **Main file**: Must be exactly `SKILL.md` (case-sensitive)
  - ✅ Correct: `SKILL.md`
  - ❌ Wrong: `SKILL.MD`, `skill.md`, `Skill.md`

- **No README.md**: Documentation goes in `SKILL.md` or `references/` folder only

### YAML Frontmatter

The frontmatter is the most critical component—it determines whether Claude loads your skill. It uses a three-field structure:

```yaml
---
name: skill-name-in-kebab-case
description: What it does. Use when user asks to [specific phrases].
---
```

#### Required Fields

**name** (required)
- Must be kebab-case
- No spaces, capitals, or special characters
- Should match the folder name

**description** (required)
- Must include BOTH what the skill does AND when to use it
- Maximum 1024 characters
- Must include specific trigger phrases users would actually say
- Mention file types if relevant (e.g., "for PDF documents")
- Cannot contain XML angle brackets (`<` or `>`)

#### Optional Fields

**license**
- Use for open-source skills
- Examples: `MIT`, `Apache-2.0`

**compatibility**
- 1-500 characters describing environment requirements
- Indicates intended product, required system packages, network access needs

**metadata**
- Custom key-value pairs
- Suggested: `author`, `version`, `mcp-server`
- Example:
  ```yaml
  metadata:
    author: ProjectHub
    version: 1.0.0
    mcp-server: projecthub
  ```

#### Security Restrictions

Forbidden in frontmatter:
- XML angle brackets (`<` and `>`)
- Names containing "claude" or "anthropic" (reserved)

These restrictions prevent malicious instruction injection into Claude's system prompt.

## Core Design Principles

### Progressive Disclosure

Skills use a three-level information system to minimize token usage while maintaining specialized expertise:

1. **First level (YAML frontmatter)**: Always loaded in Claude's system prompt. Provides just enough information for Claude to know when the skill should be used without loading all of it into context.

2. **Second level (SKILL.md body)**: Loaded when Claude determines the skill is relevant to the current task. Contains full instructions and guidance.

3. **Third level (Linked files)**: Additional files bundled within the skill directory that Claude can navigate and discover only as needed.

### Composability

Claude can load multiple skills simultaneously. Skills should be designed to work well alongside other capabilities rather than assuming they are the only available tool.

### Portability

Skills work identically across [[Claude.ai]], Claude Code, and the [[Claude API]]. Once created, a skill functions across all surfaces without modification (provided the environment supports any required dependencies).

## Writing Effective Skills

### The Description Field

The description is the critical entry point for skill triggering. It must communicate:

1. **What it does** - Clear value proposition
2. **When to use it** - Trigger conditions and example phrases
3. **Key capabilities** - File types, services, or domains involved

#### Good Description Examples

```
Analyzes Figma design files and generates developer handoff documentation. 
Use when user uploads .fig files, asks for "design specs", "component documentation", 
or "design-to-code handoff".
```

```
Manages Linear project workflows including sprint planning, task creation, and 
status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", 
or asks to "create tickets".
```

#### Poor Description Examples

- Too vague: `"Helps with projects."`
- Missing triggers: `"Creates sophisticated multi-page documentation systems."`
- Too technical: `"Implements the Project entity model with hierarchical relationships."`

### Main Instructions

After the frontmatter, write the actual instructions in Markdown. Recommended structure:

```markdown
# Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

## Examples

### Example 1: [Common Scenario]
User says: "Set up a new marketing campaign"

Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters

Result: Campaign created with confirmation link

## Troubleshooting

### Error: [Common Error Message]
**Cause**: Why it happens

**Solution**: How to fix
```

### Best Practices for Instructions

**Be Specific and Actionable**
- ✅ Good: `Run python scripts/validate.py --input {filename} to check data format. If validation fails, common issues include: Missing required fields (add them to the CSV), Invalid date formats (use YYYY-MM-DD)`
- ❌ Bad: `Validate the data before proceeding.`

**Include Error Handling**
- Explicitly document common errors
- Provide clear troubleshooting steps
- Reference MCP connection issues if applicable

**Reference Bundled Resources**
- Link to `references/` files clearly
- Use progressive disclosure to keep SKILL.md focused
- Move detailed documentation to separate files

**Use Progressive Disclosure**
- Keep SKILL.md focused on core instructions
- Move detailed documentation to `references/`
- Link clearly to additional resources

## Skill Use Case Categories

### Category 1: Document & Asset Creation

**Purpose**: Creating consistent, high-quality output including documents, presentations, apps, designs, and code.

**Example**: Frontend design skill for creating production-grade web interfaces

**Key Techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities (no external tools required)

### Category 2: Workflow Automation

**Purpose**: Multi-step processes that benefit from consistent methodology, including coordination across multiple [[MCP]] servers.

**Example**: Skill-creator skill for interactive guide to creating new skills

**Key Techniques**:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

**Purpose**: Workflow guidance to enhance the tool access an [[MCP]] server provides.

**Example**: Sentry code review skill that analyzes and fixes bugs in GitHub Pull Requests

**Key Techniques**:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

## Skills and MCP