---
title: The-Complete-Guide-to-Building-Skill-for-Claude_copy
source_file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:21:46.442023
raw_file_updated: 2026-04-05T20:21:46.442023
version: 1
sources:
  - file: The-Complete-Guide-to-Building-Skill-for-Claude_copy.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:21:46.442023
tags: []
related_topics: []
backlinked_by: []
---
# Agent Skills for Claude

## Summary

Agent Skills are structured instruction sets packaged as folders that teach Claude to handle specific tasks and workflows consistently. They represent one of the most powerful customization methods for Claude, enabling users to teach the model once and benefit across all conversations. Skills work across [[Claude.ai]], [[Claude Code]], and the [[Claude API]], making them portable across platforms.

## Overview

A **skill** is a folder containing standardized files that provide Claude with domain-specific knowledge, best practices, and workflow instructions. Rather than re-explaining preferences and processes in every conversation, skills embed this expertise directly into Claude's behavior, enabling reliable, repeatable task execution.

Skills are particularly valuable for:
- Creating consistent, high-quality output (documents, designs, code)
- Automating multi-step workflows
- Enhancing [[Model Context Protocol|MCP]] integrations with workflow guidance
- Standardizing processes across teams and organizations

## Core Concepts

### What Skills Contain

A skill folder has the following structure:

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

The **SKILL.md** file is the only required component and must be named exactly as specified (case-sensitive). It contains [[YAML]] frontmatter followed by Markdown instructions.

### Progressive Disclosure Architecture

Skills use a three-level information system to minimize token usage while maintaining specialized expertise:

1. **First Level (YAML Frontmatter)** - Always loaded in Claude's system prompt. Provides just enough information for Claude to recognize when the skill should be used without loading its full content.

2. **Second Level (SKILL.md Body)** - Loaded when Claude determines the skill is relevant to the current task. Contains complete instructions and detailed guidance.

3. **Third Level (Linked Files)** - Additional documentation, scripts, and assets that Claude can navigate and discover only as needed.

### Core Design Principles

#### Composability
Skills are designed to work together. Multiple skills can load simultaneously, and each skill should function well alongside others without assuming it's the only available capability.

#### Portability
Skills work identically across all Claude surfaces—[[Claude.ai]], [[Claude Code]], and the [[Claude API]]—without modification, provided the environment supports any required dependencies.

#### Progressive Disclosure
The three-level system ensures that only necessary information is loaded into context at any given time, optimizing token usage while maintaining access to specialized knowledge.

## Skill Categories

Anthropic has identified three primary skill use case categories:

### Category 1: Document and Asset Creation

Used for creating consistent, high-quality output including documents, presentations, applications, designs, and code.

**Characteristics:**
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalization
- Uses Claude's built-in capabilities (no external tools required)

**Examples:** Frontend design skills, document creation skills ([[DOCX]], [[PPTX]], [[XLSX]])

### Category 2: Workflow Automation

Used for multi-step processes that benefit from consistent methodology, including coordination across multiple [[MCP]] servers.

**Characteristics:**
- Step-by-step workflows with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Examples:** Project setup skills, sprint planning skills, skill-creator skill

### Category 3: MCP Enhancement

Used to provide workflow guidance that enhances tool access from an [[MCP]] server.

**Characteristics:**
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

**Examples:** Code review skills, service integration skills

## Planning and Design

### Defining Use Cases

Before writing any code, identify 2-3 concrete use cases the skill should enable. A well-defined use case includes:

- **Trigger**: What the user says or does
- **Steps**: The specific actions required
- **Result**: What success looks like

### Success Criteria

Effective skills should meet both quantitative and qualitative benchmarks:

**Quantitative Metrics:**
- Skill triggers on 90% of relevant queries
- Completes workflow in expected number of tool calls
- Zero failed API calls per workflow

**Qualitative Metrics:**
- Users don't need to prompt Claude about next steps
- Workflows complete without user correction
- Consistent results across sessions

## Technical Requirements

### File Structure and Naming

**Critical Rules:**
- SKILL.md must be named exactly as specified (case-sensitive)
- Skill folder names must use kebab-case: `notion-project-setup` ✓
- No spaces, underscores, or capitals in folder names
- Do not include README.md inside the skill folder (all documentation goes in SKILL.md or references/)

### YAML Frontmatter

The frontmatter is how Claude decides whether to load a skill. Minimal required format:

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Required Fields:**
- **name**: kebab-case only, must match folder name
- **description**: Must include both what the skill does and when to use it; under 1024 characters; no XML tags

**Optional Fields:**
- **license**: For open-source skills (e.g., MIT, Apache-2.0)
- **compatibility**: Environment requirements (1-500 characters)
- **metadata**: Custom key-value pairs (author, version, mcp-server)

**Security Restrictions:**
- Forbidden: XML angle brackets (< >)
- Forbidden: "claude" or "anthropic" in skill name (reserved)

### Writing Effective Descriptions

The description field implements the first level of progressive disclosure. It should contain:

1. **What it does** - Clear statement of functionality
2. **When to use it** - Specific trigger phrases users might say
3. **Key capabilities** - Relevant file types or features

**Good Example:**
> "Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for 'design specs', 'component documentation', or 'design-to-code handoff'."

**Bad Example:**
> "Helps with projects." (too vague, missing triggers)

## Testing and Iteration

### Testing Levels

Skills can be tested at varying levels of rigor:

- **Manual Testing** - Run queries in Claude.ai and observe behavior
- **Scripted Testing** - Automate test cases in Claude Code
- **Programmatic Testing** - Build evaluation suites via the [[Skills API]]

### Recommended Testing Approach

#### 1. Triggering Tests
Verify the skill loads at appropriate times:
- ✓ Triggers on obvious tasks
- ✓ Triggers on paraphrased requests  
- ✗ Doesn't trigger on unrelated topics

#### 2. Functional Tests
Verify correct outputs:
- Valid outputs generated
- API calls succeed
- Error handling works
- Edge cases covered

#### 3. Performance Comparison
Compare results with and without the skill:
- Reduction in back-and-forth messages
- Decrease in API call failures
- Token consumption improvement

### Iteration Based on Feedback

**Undertriggering** (skill doesn't load when it should):
- Add more detail and nuance to the description
- Include additional keywords, especially technical terms

**Overtriggering** (skill loads for irrelevant queries):
- Add negative triggers to the description
- Be more specific about scope

**Execution Issues** (inconsistent results, API failures):
- Improve instructions clarity
- Add error handling
- Include troubleshooting guidance

## Distribution and Sharing

### Current Distribution Models

**Individual Users:**
1. Download the skill folder
2. Zip the folder (if needed)
3. Upload via Claude.ai Settings > Capabilities > Skills
4. Or place in Claude Code skills directory

**Organization-Level:**
- Admins can deploy skills workspace-wide
- Automatic updates
- Centralized management

### Recommended Distribution Approach

1. **Host on GitHub**
   - Public repository for open-source skills
   - Clear README with installation instructions
   - Example usage and screenshots

2. **Document in MCP Repository**
   - Link to skill from MCP documentation
   - Explain value of using both together
   - Provide quick-start guide

3. **Create Installation Guide**
   - Step-by-step download instructions
   - Integration steps for Claude.ai or Claude Code
   - Testing