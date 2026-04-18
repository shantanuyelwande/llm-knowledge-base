---
title: I am sharing _Claude Agents SDK_ with you
source_file: I am sharing _Claude Agents SDK_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:24:19.465053
raw_file_updated: 2026-04-17T20:24:19.465053
version: 1
sources:
  - file: I am sharing _Claude Agents SDK_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:24:19.465053
tags: []
related_topics: []
backlinked_by: []
---
# Claude Agent SDK

## Summary

The **Claude Agent SDK** is a comprehensive toolkit developed by [[Anthropic]] for building autonomous agents powered by Claude. Originally designed as the Claude Code SDK to support coding tasks, it has evolved into a general-purpose framework for creating agents that can perform diverse workflows including finance management, personal assistance, customer support, and research. The SDK enables agents to interact with computer systems through tools like file access, bash commands, code generation, and external API integrations via the [[Model Context Protocol]].

## Overview

The Claude Agent SDK represents Anthropic's approach to building practical, effective agents by giving Claude the same tools that programmers use daily. Rather than limiting agent capabilities to specific domains, the SDK provides a flexible foundation for creating agents that can handle complex, multi-step tasks across various industries and applications.

### Design Philosophy

The core design principle behind the Claude Agent SDK is that **Claude needs access to a computer**. By providing Claude with:

- File system access
- Terminal/bash command execution
- File creation and editing capabilities
- Code execution environments

The SDK enables Claude to work like a human would—finding information, taking actions, verifying results, and iterating until tasks are complete.

## Key Capabilities

### Agent Types

The Claude Agent SDK can power diverse agent implementations:

- **[[Finance Agents]]**: Understand portfolios, evaluate investments, and perform financial calculations through external APIs
- **Personal Assistant Agents**: Manage calendars, book travel, schedule appointments, and prepare briefings
- **Customer Support Agents**: Handle ambiguous user requests, collect data, connect to external systems, and escalate to humans when needed
- **Deep Research Agents**: Conduct comprehensive research across document collections, synthesize information, and generate detailed reports
- **And more**: The SDK provides primitives for automating virtually any digital workflow

## The Agent Loop

The Claude Agent SDK implements a proven feedback cycle that structures how agents operate:

```
Gather Context → Take Action → Verify Work → Repeat
```

This loop provides a mental model for designing effective agents and determining what capabilities they should have.

### Gather Context

Agents need to fetch and update their own context dynamically rather than relying solely on initial prompts.

#### Agentic Search and File System

The file system serves as a repository of information that agents can search and retrieve. When encountering large files (logs, user uploads), agents use bash scripts like `grep` and `tail` to intelligently load relevant portions into context. The folder and file structure becomes a form of [[context engineering]].

**Example**: An email agent might store previous conversations in a `Conversations` folder, allowing it to search and retrieve relevant historical context when needed.

#### Semantic Search

An alternative to agentic search that involves:

- Chunking relevant content
- Embedding chunks as vectors
- Querying vectors for conceptual matches

**Note**: Semantic search is typically faster but less accurate, less transparent, and harder to maintain. Best practice is to start with agentic search and add semantic search only if performance demands it.

#### Subagents

The SDK supports [[subagents]] for two primary purposes:

1. **Parallelization**: Spin up multiple subagents to work on different tasks simultaneously
2. **Context Management**: Each subagent maintains its own isolated context window, returning only relevant information rather than full context

This approach is ideal for tasks requiring agents to sift through large amounts of information where most won't be useful.

**Example**: An email agent could spawn multiple search subagents in parallel, each running different queries against email history and returning only relevant excerpts.

#### Compaction

For long-running agents, the SDK's compaction feature automatically summarizes previous messages as the context limit approaches, preventing context overflow. This feature is built on Claude Code's compact slash command.

### Take Action

Once context is gathered, agents need flexible mechanisms to execute tasks.

#### Tools

Tools are the primary building blocks of agent execution. They should represent the main actions an agent will take, and should be designed with context efficiency in mind. Tools are prominently featured in Claude's context window, making them the primary actions Claude considers.

**Best Practice**: Define tools as the agent's primary, most frequent actions.

**Example**: An email agent might define tools like `fetchInbox` or `searchEmails`.

#### Bash and Scripts

Bash provides a general-purpose mechanism for agents to perform flexible work using a computer. Agents can write and execute shell scripts to accomplish complex tasks.

**Example**: An email agent could write code to download PDF attachments, convert them to text, and search across them.

#### Code Generation

Code generation is a powerful capability because code is:

- Precise and unambiguous
- Composable and reusable
- Ideal for complex operations that require reliability

The Claude Agent SDK excels at code generation, enabling agents to create Python scripts, spreadsheets, presentations, and other structured outputs.

**Example**: An email agent could generate code to create rules for processing inbound emails.

#### Model Context Protocol (MCP)

The [[Model Context Protocol]] provides standardized integrations to external services, handling authentication and API calls automatically. This allows agents to connect to tools like:

- Slack
- GitHub
- Google Drive
- Asana
- And growing ecosystem of integrations

**Benefit**: Agents can use pre-built integrations without custom code or OAuth management.

**Example**: An email agent could search Slack messages or check Asana tasks using MCP servers.

### Verify Work

Agents that can evaluate and improve their own output are fundamentally more reliable. They catch mistakes before they compound, self-correct when drifting, and improve through iteration.

#### Rules-Based Feedback

Provide clearly defined rules for expected outputs and explain which rules failed and why. Code linting is an excellent form of rules-based feedback because it provides multiple layers of validation.

**Example**: An email agent could verify that email addresses are valid and check whether the user has previously contacted that address.

#### Visual Feedback

For visual tasks (UI generation, testing, formatting), provide visual feedback through screenshots or renders. Agents can verify:

- **Layout**: Are elements positioned correctly? Is spacing appropriate?
- **Styling**: Do colors, fonts, and formatting appear as intended?
- **Content Hierarchy**: Is information presented correctly with proper emphasis?
- **Responsiveness**: Does the output look broken or cramped?

Tools like [[Playwright]] can automate visual feedback loops within agent workflows.

#### LLM as Judge

Use another language model to evaluate agent output based on fuzzy rules. While not the most robust method and having latency tradeoffs, this can boost performance when needed.

**Example**: A separate subagent could judge the tone of drafted emails against the user's previous messaging style.

## Testing and Improvement

After iterating through the agent loop, test and evaluate agent performance by examining outputs, especially failures. Key evaluation questions:

- **Misunderstanding tasks**: Is the agent missing key information? Can you restructure search APIs to make relevant information easier to find?
- **Repeated failures**: Can you add formal rules in tool calls to identify and fix the failure?
- **Error correction**: Can you provide more useful or creative tools to approach problems differently?
- **Performance variation**: Build representative test sets for programmatic evaluations based on actual usage patterns.

## Getting Started

The Claude Agent SDK is available for developers to use immediately. The framework provides:

- Clear patterns for building autonomous agents
- Flexible tools for context gathering, action, and verification
- Integration with external services through MCP
- Automatic context management for long-running agents

Developers already using the SDK should migrate to the latest version by following the official migration guide.

## Related Concepts

- [[Claude Code]] - The agentic coding solution that inspired the SDK
- [[Model Context Protocol]] - Standardized integrations for external services
- [[Anthropic]] - The company behind Claude and the SDK
- [[Context Engineering]] - Structuring information for optimal agent performance
- [[Subagents]] - Parallel and context-isolated agent instances
- [[Code Generation]] - Precise, reusable agent outputs

## Metadata

**Source**: Engineering at Anthropic - "Building agents with the Claude Agent SDK"

**Author**: Thariq Shihipar (with Molly Vorweck, Suzanne Wang, Alex Isken, Cat Wu, Keir Bradwell, Alexander Bricken, and Ashwin Bhat)

**Published**: 2025

**Tags**: `#agents` `#claude` `#sdk` `#anthropic` `#ai-development` `#automation` `#llm`

**Related Topics**: 
- [[Agentic AI]]
- [[Large Language Models]]
- [[API Integration]]
- [[Software Development Tools]]
- [[Automation Workflows]]