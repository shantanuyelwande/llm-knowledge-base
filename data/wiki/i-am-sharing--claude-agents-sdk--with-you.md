---
title: I am sharing _Claude Agents SDK_ with you
source_file: I am sharing _Claude Agents SDK_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:03:05.758176
raw_file_updated: 2026-04-17T21:03:05.758176
version: 1
sources:
  - file: I am sharing _Claude Agents SDK_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:03:05.758176
tags: []
related_topics: []
backlinked_by: []
---
# Claude Agent SDK

## Summary

The **Claude Agent SDK** is a comprehensive toolkit developed by [[Anthropic]] for building autonomous agents powered by [[Claude]], Anthropic's large language model. Originally created as the Claude Code SDK to support developer productivity, it has evolved into a general-purpose framework for creating agents that can perform diverse tasks including research, data analysis, and workflow automation. The SDK enables developers to build agents that operate through a core feedback loop: gather context → take action → verify work → repeat.

---

## Overview

The Claude Agent SDK represents a significant evolution in agent-based AI development. Rather than limiting Claude's capabilities to a single domain, the SDK provides developers with a comprehensive set of tools and primitives to create agents for virtually any workflow automation task.

### Key Philosophy

The foundational design principle is simple yet powerful: **give Claude the same tools that programmers use every day**. This includes:

- File system access
- Command-line execution
- Code editing and creation
- Debugging capabilities
- Iterative problem-solving

By providing Claude with access to a computer environment, the SDK enables agents to operate with the same flexibility and capability as human workers.

---

## Core Agent Loop

All agents built with the Claude Agent SDK follow a structured feedback loop that ensures reliability and effectiveness:

### 1. Gather Context

Agents must actively retrieve and manage information from various sources:

#### Agentic Search and File System
The file system serves as a repository of contextual information. When encountering large files such as logs or user uploads, Claude uses [[bash]] scripts (like `grep` and `tail`) to intelligently load relevant portions into its context window. The folder and file structure effectively becomes a form of [[context engineering]].

**Example**: An email agent might organize previous conversations in a 'Conversations' folder, allowing it to search and retrieve relevant past interactions when needed.

#### Semantic Search
Semantic search offers faster performance than agentic search but with trade-offs in accuracy and transparency. It involves:

- Chunking relevant context
- Embedding chunks as vectors
- Querying vectors for conceptual matches

**Recommendation**: Start with agentic search and only add semantic search if performance requirements demand it.

#### Subagents
The SDK natively supports subagents for two primary purposes:

1. **Parallelization**: Multiple subagents can work on different tasks simultaneously
2. **Context Management**: Subagents maintain isolated context windows and return only relevant information to the orchestrator, preventing context bloat

**Example**: An email agent could spawn multiple search subagents in parallel, each querying different aspects of email history and returning only relevant excerpts.

#### Compaction
The **compaction feature** automatically summarizes previous messages as the context limit approaches, preventing context overflow during extended agent operations. This feature is built on Claude Code's compact functionality.

### 2. Take Action

Once context is gathered, agents require flexible mechanisms for executing tasks:

#### Tools
Tools are the primary building blocks of agent execution. They should be:

- Prominent in the context window
- Representative of primary, frequent actions
- Consciously designed for context efficiency

**Example**: An email agent might define tools like `fetchInbox` or `searchEmails` as its primary actions.

Tools are customizable and developers should focus on making them effective through proper design patterns.

#### Bash & Scripts
Bash provides general-purpose flexibility for agents to perform computer-based work. Claude can write and execute shell scripts to accomplish tasks that require system-level operations.

**Example**: An email agent could write code to download PDF attachments, convert them to text, and search across their contents.

#### Code Generation
The SDK excels at code generation, which offers several advantages:

- **Precision**: Code is unambiguous
- **Composability**: Code components can be reused
- **Reliability**: Complex operations can be expressed reliably

Code generation is particularly effective for tasks like creating formatted documents, performing calculations, and building interactive elements.

**Example**: Claude can write Python scripts to create Excel spreadsheets, PowerPoint presentations, and Word documents with consistent formatting and complex functionality.

#### Model Context Protocol (MCP)
The [[Model Context Protocol]] provides standardized integrations to external services, handling authentication and API calls automatically. This eliminates the need for custom integration code or OAuth management.

**Supported integrations include**:
- Slack
- GitHub
- Google Drive
- Asana
- And growing ecosystem of services

**Example**: An email agent could call `search_slack_messages` or `get_asana_tasks` without implementing custom authentication or API handling.

### 3. Verify Work

Agents that can evaluate and improve their own output are fundamentally more reliable. The SDK provides three effective verification approaches:

#### Defining Rules
Rules-based feedback is the most effective verification method. Provide clearly defined rules for outputs and explain which rules failed and why.

**Code linting** is an excellent example: generating TypeScript and linting it provides multiple layers of feedback compared to generating pure JavaScript.

**Example**: An email agent could verify that email addresses are valid (error if not) and check if the recipient has been contacted before (warning if not).

#### Visual Feedback
For visual tasks like UI generation or testing, screenshots and renders provide valuable verification data. Agents can evaluate:

- **Layout**: Correct element positioning and spacing
- **Styling**: Colors, fonts, and formatting accuracy
- **Content Hierarchy**: Proper information order and emphasis
- **Responsiveness**: Appearance across different viewport sizes

Tools like [[Playwright]] can automate this feedback loop by capturing screenshots, testing different viewport sizes, and validating interactive elements.

#### LLM as a Judge
A separate language model can evaluate agent output based on fuzzy rules. While less robust and carrying latency costs, this approach can provide performance improvements for certain applications.

**Example**: A subagent judge could evaluate the tone of email drafts to ensure they match the user's communication style.

---

## Use Cases

The Claude Agent SDK enables developers to build agents for diverse applications:

### Finance Agents
Agents that understand investment portfolios and financial goals, evaluate investment opportunities through external APIs, store financial data, and perform complex calculations.

### Personal Assistant Agents
Agents that manage travel bookings, calendar scheduling, appointment coordination, and brief preparation by connecting to internal data sources and maintaining context across applications.

### Customer Support Agents
Agents that handle complex customer service requests by collecting user data, connecting to external APIs, communicating with users, and escalating to humans when necessary.

### Deep Research Agents
Agents that conduct comprehensive research across large document collections by searching file systems, analyzing multiple sources, cross-referencing data, and generating detailed reports.

### Additional Applications
The SDK's flexibility enables agents for virtually any workflow automation task, from data analysis to content creation.

---

## Best Practices

### Agent Design

1. **Understand Task Requirements**: If your agent misunderstands tasks, it may lack key information. Consider restructuring search APIs to make information discovery easier.

2. **Address Repeated Failures**: If an agent fails repeatedly at a task, add formal rules in tool calls to identify and fix the failure.

3. **Expand Tool Capabilities**: If an agent cannot fix errors, provide more useful or creative tools for alternative approaches.

4. **Performance Testing**: When adding features, build representative test sets for programmatic evaluations based on actual customer usage patterns.

5. **Tool Design**: Tools should represent primary actions and be designed with context efficiency in mind. Avoid cluttering the context window with rarely-used tools.

6. **Context Management**: Actively manage context through search optimization, subagent delegation, and compaction to prevent context exhaustion during long-running operations.

---

## Getting Started

The Claude Agent SDK is available for immediate use. Developers can:

1. Access the [[Claude Developer Platform]] for documentation and resources
2. Implement the agent loop framework in their applications
3. Start with agentic search and basic tools, expanding capabilities as needed
4. Build and test agents with representative use cases
5. Migrate to the latest version if already using the SDK

---

## Evolution from Claude Code

The Claude Agent SDK evolved from **Claude Code**, an agentic coding solution originally built to support developer productivity at [[Anthropic]]. While Claude Code remains focused on coding tasks, the broader agent framework has proven effective for:

- Deep research and analysis
- Video creation and editing
- Note-taking and documentation
- Data manipulation and visualization
- And numerous other non-coding applications

This evolution led to the renaming of Claude Code SDK to Claude Agent SDK to reflect its broader capabilities.

---

## Related Technologies

- [[Claude]] - The underlying language model
- [[Model Context Protocol]] - Standard integration protocol for external services
- [[Anthropic]] - Developing organization
- [[Bash]] - Command-line tool for agent execution
- [[Code Generation]] - Core capability for agent task execution
- [[Context Management]] - Critical technique for long-running agents

---

## Metadata

**Source**: Engineering at Anthropic - "Building agents with the Claude Agent SDK"

**Tags**: `#AI-Agents` `#Claude` `#SDK` `#Anthropic` `#Agent-Framework` `