---
title: I am sharing _Claude Agents SDK_ with you
source_file: I am sharing _Claude Agents SDK_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:03:06.776878
raw_file_updated: 2026-04-24T19:03:06.776878
version: 1
sources:
  - file: I am sharing _Claude Agents SDK_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:03:06.776878
tags: []
related_topics: []
backlinked_by: []
---
# Claude Agent SDK

## Summary

The **Claude Agent SDK** is a collection of developer tools created by [[Anthropic]] for building autonomous agents powered by [[Claude]] (an AI model). Originally developed as the Claude Code SDK to support internal productivity, it has evolved into a general-purpose framework for creating agents that can perform diverse tasks beyond coding—including research, customer support, finance management, and personal assistance. The SDK provides developers with tools to implement an agent loop pattern: gathering context, taking action, and verifying work iteratively.

## Overview

The Claude Agent SDK represents [[Anthropic]]'s vision for empowering Claude with computer-like capabilities to perform complex, autonomous tasks. Rather than being limited to text generation, the SDK enables Claude to access files, execute commands, write code, and integrate with external services—effectively giving the AI model the same tools that human professionals use daily.

### Origins and Evolution

The SDK evolved from [[Claude Code]], an agentic coding solution originally built to enhance developer productivity at Anthropic. Over time, the team discovered that Claude Code's underlying architecture could power far more than just coding tasks. Applications expanded to include:

- Deep research and document analysis
- Video creation and media generation
- Note-taking and information management
- Various non-coding digital workflows

This broader applicability led to the renaming of Claude Code SDK to Claude Agent SDK to reflect its expanded purpose.

## Core Design Principles

The fundamental design philosophy centers on giving Claude access to the same tools that humans use:

- **File system access** for reading and writing files
- **Terminal/bash commands** for executing system operations
- **Code execution** for running and testing code
- **Iterative capabilities** for self-correction and improvement

By providing these capabilities, Claude can approach problems like a human professional would, gathering information, taking action, and refining its work based on feedback.

## Use Cases and Applications

The Claude Agent SDK enables developers to build specialized agents for various domains:

### Finance Agents
Agents that understand investment portfolios, evaluate investment opportunities, and perform financial calculations by accessing external APIs and analyzing data.

### Personal Assistant Agents
Agents capable of booking travel, managing calendars, scheduling appointments, preparing briefs, and coordinating across multiple applications and data sources.

### Customer Support Agents
Agents designed to handle complex customer service requests with high ambiguity, collect relevant user data, connect to external systems, and escalate to humans when necessary.

### Deep Research Agents
Agents that conduct comprehensive research across large document collections by searching file systems, analyzing multiple sources, cross-referencing data, and generating detailed reports.

## The Agent Loop Architecture

The core operational model of agents built with the Claude Agent SDK follows a three-phase feedback loop:

```
Gather Context → Take Action → Verify Work → [Repeat]
```

### Phase 1: Gather Context

Agents need more than just initial instructions; they must actively fetch and update their own contextual information.

#### Agentic Search and File System
The file system serves as a structured repository of information that agents can access. When encountering large files (logs, user uploads), agents use bash commands like `grep` and `tail` to selectively load relevant portions into their context. This approach turns folder and file structure into a form of [[context engineering]].

*Example:* An email agent might store previous conversations in a "Conversations" folder, allowing it to search and retrieve relevant historical context when needed.

#### Semantic Search
An alternative approach using vector embeddings and chunked content. While potentially faster than agentic search, semantic search is generally:
- Less accurate
- More difficult to maintain
- Less transparent

**Best practice:** Start with agentic search; add semantic search only if performance improvements are needed.

#### Subagents
The SDK supports [[subagents]] by default, enabling two key capabilities:

1. **Parallelization:** Multiple subagents can work on different tasks simultaneously
2. **Context management:** Each subagent maintains isolated context windows and returns only relevant information to the orchestrator

This is particularly valuable for tasks requiring analysis of large information volumes where most content will be irrelevant.

*Example:* An email agent could spawn multiple search subagents in parallel, each querying different aspects of email history, with each returning only relevant excerpts rather than full threads.

#### Compaction
For long-running agents, the SDK includes automatic context management through the **compact** feature, which summarizes previous messages as the context limit approaches. This prevents context exhaustion during extended operations.

### Phase 2: Take Action

Once context is gathered, agents need flexible mechanisms for executing tasks.

#### Tools
Tools are the primary building blocks for agent execution. They should represent the main actions the agent will consider when solving problems. Effective tool design maximizes context efficiency by:
- Making tools prominent in the model's context window
- Focusing on primary, frequent actions
- Avoiding redundant or overlapping capabilities

*Example:* An email agent might define tools like `fetchInbox` and `searchEmails` as primary actions.

#### Bash and Scripts
Bash commands provide flexible, general-purpose execution capabilities. Agents can write and execute shell scripts to perform system-level operations, manipulate files, and chain multiple commands.

*Example:* An email agent could write code to download PDF attachments, convert them to text, and search across the content.

#### Code Generation
The SDK excels at code generation because code provides:
- **Precision:** Exact specification of operations
- **Composability:** Reusable code components
- **Reliability:** Consistent execution of complex operations

Code generation is particularly powerful for tasks that benefit from formal expression and can be reused across multiple agent invocations.

*Example:* [[Claude]] generates Python scripts to create Excel spreadsheets, PowerPoint presentations, and Word documents with consistent formatting and complex functionality.

#### Model Context Protocol (MCP)
[[MCP (Model Context Protocol)]] provides standardized integrations to external services, handling authentication and API calls automatically. This enables agents to connect to services like:
- Slack
- GitHub
- Google Drive
- Asana

Without requiring custom integration code or OAuth management.

*Example:* An email agent can call `search_slack_messages` or `get_asana_tasks` through MCP servers without implementing authentication logic.

### Phase 3: Verify Work

Agents that can evaluate and improve their own output are fundamentally more reliable. They catch mistakes early, self-correct when drifting from objectives, and improve through iteration.

#### Rules-Based Feedback
The most effective verification approach: define clear rules for output, then provide specific feedback on which rules failed and why.

**Code linting** is an excellent example—generating TypeScript and linting it provides multiple feedback layers compared to raw JavaScript generation.

*Example:* For email generation, rules might verify:
- Email address validity
- Previous communication history with recipient
- Proper formatting and tone

#### Visual Feedback
For visual tasks (UI generation, email formatting, document layout), screenshot-based feedback helps agents verify:
- **Layout:** Correct element positioning and spacing
- **Styling:** Accurate colors, fonts, and formatting
- **Content hierarchy:** Proper information ordering and emphasis
- **Responsiveness:** Appropriate display across viewport sizes

Tools like [[Playwright]] (available via MCP) can automate visual feedback loops, capturing screenshots and testing interactive elements within the agent workflow.

#### LLM as Judge
An alternative approach using another language model to evaluate agent output based on fuzzy rules. While generally less robust and carrying latency tradeoffs, this method can provide performance improvements for certain applications.

*Example:* A separate subagent could judge the tone of draft emails against previous messages to ensure consistency.

## Testing and Improvement Strategies

After multiple agent loop iterations, systematic testing and evaluation ensures agents are well-equipped for their tasks. Key evaluation questions:

1. **Misunderstanding tasks?** The agent may lack key information. Can you restructure search APIs to make needed information more discoverable?

2. **Repeated failures?** Can you add formal rules in tool calls to identify and prevent the failure?

3. **Error recovery issues?** Can you provide more useful or creative tools for alternative problem-solving approaches?

4. **Performance variability?** Build representative test sets for programmatic evaluations based on actual customer usage patterns.

The best improvement path comes from analyzing failures: understanding what tools or information the agent needs to succeed.

## Getting Started

### Prerequisites
- Understanding of agent design patterns
- Familiarity with Claude's capabilities
- Development environment setup

### Initial Steps
1. Define your agent's primary workflow
2. Design the context gathering strategy (file system structure, search approach)
3. Identify and implement necessary tools
4. Plan verification and feedback mechanisms
5. Test iteratively with representative use cases

### Migration
Developers already using the SDK should migrate to the latest version following Anthropic's official migration guide.

## Key Concepts and Related Topics

- [[Claude]] - The underlying AI model powering the SDK
- [[Anthropic]] - The organization developing the SDK
- [[Claude Code]] - The predecessor system focused on coding
- [[Model Context Protocol]] - Standard for external service integration
- [[Subagents]] -