---
title: Anthropic - Claude Skills Guide
source_file: Anthropic - Claude Skills Guide.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:27:19.498400
raw_file_updated: 2026-04-17T20:27:19.498400
version: 1
sources:
  - file: Anthropic - Claude Skills Guide.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:27:19.498400
tags: []
related_topics: []
backlinked_by: []
---
# Claude Skills Guide

## Summary

A comprehensive guide to building, testing, and distributing **Skills** for Claude—packaged sets of instructions that teach Claude to handle specific tasks and workflows. Skills enable customization without re-explaining preferences in every conversation, working across Claude.ai, Claude Code, and the API.

---

## Overview

A **skill** is a folder containing structured instructions that teaches [[Claude]] how to handle specific tasks or workflows. Rather than repeating explanations, preferences, and domain expertise in each conversation, skills allow users to teach Claude once and benefit from that knowledge consistently across multiple interactions.

Skills are most powerful for:
- Repeatable workflows (generating designs from specifications, conducting research with consistent methodology)
- Creating documents that follow organizational style guides
- Orchestrating multi-step processes
- Enhancing [[MCP]] (Model Context Protocol) integrations with workflow guidance

## Core Concepts

### What is a Skill?

A skill consists of:
- **SKILL.md** (required): Main instructions in Markdown with YAML frontmatter
- **scripts/** (optional): Executable code in Python, Bash, or other languages
- **references/** (optional): Documentation loaded as needed
- **assets/** (optional): Templates, fonts, icons used in output

### Fundamental Design Principles

#### Progressive Disclosure

Skills use a three-level information system to minimize token usage:

1. **YAML Frontmatter** (always loaded): Provides just enough information for Claude to know when to use the skill without loading full context
2. **SKILL.md Body** (conditionally loaded): Full instructions and guidance loaded when Claude determines the skill is relevant
3. **Linked Files** (on-demand): Additional documentation Claude can navigate only when needed

#### Composability

Skills work together seamlessly. Multiple skills can load simultaneously, and each skill should assume it's one capability among many rather than the only available tool.

#### Portability

Skills function identically across all Claude surfaces:
- Claude.ai
- [[Claude Code]]
- API

Create once, deploy everywhere (provided environment dependencies are met).

### Skills and MCP Integration

For developers building [[MCP]] servers, skills provide the knowledge layer on top of tool connectivity:

| Aspect | MCP | Skills |
|--------|-----|--------|
| Function | Connects Claude to services (Notion, Asana, Linear, etc.) | Teaches Claude how to use services effectively |
| Provides | Real-time data access and tool invocation | Workflows and best practices |
| Answers | "What can Claude do?" | "How should Claude do it?" |

Together, they enable users to accomplish complex tasks without figuring out every step independently.

---

## Planning and Design

### Starting with Use Cases

Before writing any code, identify 2-3 concrete use cases your skill should enable. A good use case definition includes:
- **Trigger**: What users say to activate the workflow
- **Steps**: Multi-step process required
- **Tools**: Built-in capabilities or MCP tools needed
- **Result**: Expected outcome

### Common Skill Use Case Categories

#### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output including documents, presentations, applications, designs, and code.

**Key techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- Uses Claude's built-in capabilities (no external tools required)

**Example**: Frontend design skill for creating production-grade interfaces

#### Category 2: Workflow Automation

**Used for**: Multi-step processes benefiting from consistent methodology, including coordination across multiple MCP servers.

**Key techniques**:
- Step-by-step workflows with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Example**: Skill-creator skill for interactive skill development

#### Category 3: MCP Enhancement

**Used for**: Workflow guidance to enhance tool access an MCP server provides.

**Key techniques**:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise specify
- Error handling for common MCP issues

**Example**: Sentry code review skill that analyzes bugs in GitHub PRs

### Defining Success Criteria

Success criteria establish how to measure skill effectiveness through both quantitative and qualitative metrics.

**Quantitative metrics**:
- Skill triggers on 90% of relevant queries
- Completes workflow in X tool calls
- Zero failed API calls per workflow

**Qualitative metrics**:
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

### Critical Rules

**SKILL.md naming**:
- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted

**Skill folder naming**:
- Use kebab-case: `notion-project-setup` ✅
- No spaces, underscores, or capitals

**No README.md inside skill folder**:
- All documentation goes in SKILL.md or references/
- When distributing via GitHub, include repo-level README for human users

### YAML Frontmatter

The YAML frontmatter is the most critical component—it determines whether Claude loads your skill.

**Minimal required format**:
```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Required fields**:

- **name**: kebab-case only, no spaces or capitals, should match folder name
- **description**: Must include BOTH what the skill does AND when to use it (trigger conditions), under 1024 characters, no XML tags, include specific tasks users might say

**Optional fields**:

- **license**: MIT, Apache-2.0, etc. for open-source skills
- **compatibility**: 1-500 characters indicating environment requirements
- **metadata**: Custom key-value pairs (author, version, mcp-server, etc.)

**Security restrictions**:
- Forbidden: XML angle brackets (`< >`)
- Forbidden: Skills named with "claude" or "anthropic" prefix (reserved)

### Writing Effective Descriptions

The description field implements the first level of progressive disclosure.

**Structure**: [What it does] + [When to use it] + [Key capabilities]

**Good examples**:
- "Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'."
- "Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions 'sprint', 'Linear tasks', 'project planning', or asks to 'create tickets'."

**Bad examples**:
- "Helps with projects." (too vague)
- "Creates sophisticated multi-page documentation systems." (missing triggers)

### Writing Main Instructions

**Recommended structure**:

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
\`\`\`bash
python scripts/fetch_data.py --project-id PROJECT_ID
\`\`\`

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
**Cause**: [Why it happens]
**Solution**: [How to fix]
```

**Best practices**:
- Be specific and actionable with concrete commands
- Include error handling and common issues
- Reference bundled resources clearly
- Use progressive disclosure—keep SKILL.md focused, move detailed docs to references/

---

## Testing and Iteration

Skills can be tested at varying levels of rigor depending on needs and visibility.

### Testing Approaches

1. **Manual testing in Claude.ai**: Run queries directly and observe behavior (fast iteration, no setup)
2. **Scripted testing in Claude Code**: Automate test cases for repeatable validation
3. **Programmatic testing via Skills API**: Build evaluation suites against defined test sets

**Pro tip**: Iterate on a single challenging task until Claude succeeds