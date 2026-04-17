---
title: Claude Agents SDK
source_file: I am sharing _Claude Agents SDK_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:29:37.295765
raw_file_updated: 2026-04-05T20:29:37.295765
version: 1
sources:
  - file: I am sharing _Claude Agents SDK_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:29:37.295765
tags: ["AI Development", "Agent Framework", "Claude API", "Autonomous Systems", "Developer Tools"]
related_topics: []
backlinked_by: []

---
# Claude Agent SDK

## Summary

The **Claude Agent SDK** is a comprehensive toolkit developed by [[Anthropic]] for building autonomous agents powered by [[Claude]]. Originally created as the Claude Code SDK to support internal development workflows, it has evolved into a general-purpose framework for creating agents that can perform diverse tasks including research, customer support, finance management, and personal assistance. The SDK enables agents to interact with computer systems through tools like file access, bash commands, and external API integrations via the [[Model Context Protocol]].

## Overview

The Claude Agent SDK represents a fundamental shift in how developers can build autonomous systems. Rather than limiting Claude to text-based interactions, the SDK provides Claude with computer access—the same tools that programmers use daily—enabling it to write code, edit files, run commands, and iterate on solutions autonomously.

### Core Philosophy

The key design principle is that **Claude needs the same tools that programmers use every day**. By giving Claude access to a user's computer via terminal commands, the agent can:

- Find and navigate appropriate files in a codebase
- Write and edit files
- Lint and debug code
- Execute commands iteratively until tasks succeed
- Perform non-coding digital work

This principle extends beyond coding: with tools to run bash commands, edit files, search documents, and access external services, Claude can effectively become a general-purpose computer-using agent.

## Agent Use Cases

The SDK enables developers to build specialized agents for various domains:

### Finance Agents
Understand user portfolios and investment goals by accessing external APIs, storing financial data, and running calculations to evaluate investment opportunities.

### Personal Assistant Agents
Manage calendars, book travel, schedule appointments, and create briefs by connecting to internal data sources and maintaining context across multiple applications.

### Customer Support Agents
Handle complex, ambiguous user requests by collecting and reviewing customer data, connecting to external systems, messaging users, and escalating to humans when necessary.

### Deep Research Agents
Conduct comprehensive research across large document collections by searching file systems, analyzing multiple sources, cross-referencing data, and generating detailed reports.

### Additional Applications
The SDK's flexibility supports countless other workflows requiring automation and intelligent decision-making.

## The Agent Loop: Core Architecture

Effective agents operate in a specific feedback loop that forms the foundation of the SDK's design:

```
Gather Context → Take Action → Verify Work → Repeat
```

This loop ensures agents can autonomously improve their outputs and handle complex, multi-step tasks.

### Phase 1: Gather Context

Agents must do more than respond to prompts—they need to fetch and update their own context dynamically.

#### Agentic Search and File System
The file system serves as a structured knowledge base. When Claude encounters large files like logs or user uploads, it decides how to load them using bash scripts such as `grep` and `tail`. The folder and file structure becomes a form of [[context engineering]].

**Example:** An email agent might store previous conversations in a "Conversations" folder, allowing it to search and retrieve relevant message history when needed.

#### Semantic Search
Semantic search uses vector embeddings to find conceptually similar information. While faster than agentic search, it is:
- Less accurate
- More difficult to maintain
- Less transparent

**Recommendation:** Start with agentic search and add semantic search only if you need faster results or greater variations.

#### Subagents
The SDK supports subagents natively, which provide two key benefits:

1. **Parallelization:** Multiple subagents can work on different tasks simultaneously
2. **Context Management:** Subagents use isolated context windows and return only relevant information to the orchestrator

**Example:** An email agent could spawn multiple search subagents in parallel, each querying different aspects of email history and returning only relevant excerpts rather than full threads.

#### Compaction
For long-running agents, the SDK's compaction feature automatically summarizes previous messages as the context limit approaches, preventing context exhaustion. This feature builds on Claude Code's compact slash command.

### Phase 2: Take Action

Once an agent has gathered context, it needs flexible mechanisms for executing tasks.

#### Tools
Tools are the primary building blocks of agent execution. Because tools are prominently displayed in Claude's context window, they become the primary actions the model considers when solving tasks. Tool design should maximize context efficiency.

**Best Practice:** Define tools as primary, frequent actions you want the agent to take (e.g., "fetchInbox" or "searchEmails" for an email agent).

#### Bash & Scripts
Bash provides general-purpose computing capabilities, allowing agents to perform flexible work on a computer system.

**Example:** An email agent could write bash commands to download PDF attachments, convert them to text, and search across their content.

#### Code Generation
The SDK excels at code generation because code is:
- Precise and unambiguous
- Composable and reusable
- Ideal for complex, reliable operations

**Example:** Claude.AI's file creation feature uses code generation—Claude writes Python scripts to create Excel spreadsheets, PowerPoint presentations, and Word documents with consistent formatting.

For email agents, code generation could create rules for handling inbound emails automatically.

#### Model Context Protocol (MCP)

The [[Model Context Protocol]] provides standardized integrations to external services, automatically handling authentication and API calls. This eliminates the need for custom integration code or OAuth management.

**Available Integrations:**
- Slack (search messages, understand team context)
- GitHub (access repositories and issues)
- Google Drive (file access and management)
- Asana (task tracking and assignment)
- Playwright (automated visual testing)

**Benefit:** As the MCP ecosystem grows, developers can quickly add new capabilities without writing custom integration code.

### Phase 3: Verify Work

Agents that can check and improve their own output are fundamentally more reliable. They catch mistakes before they compound, self-correct when drifting, and improve through iteration.

#### Rules-Based Feedback
Provide clearly defined rules for outputs, then report which rules failed and why.

**Example:** Code linting provides multiple layers of feedback. For email generation, rules might validate:
- Email address format correctness
- Whether the recipient has been contacted before

**Best Practice:** More in-depth feedback is better. Generating TypeScript and linting it provides more feedback layers than generating pure JavaScript.

#### Visual Feedback
For visual tasks like UI generation or HTML email creation, screenshots and renders provide concrete feedback.

**Verification Checklist:**
- **Layout:** Are elements positioned correctly? Is spacing appropriate?
- **Styling:** Do colors, fonts, and formatting appear as intended?
- **Content Hierarchy:** Is information presented in the right order with proper emphasis?
- **Responsiveness:** Does the design appear broken or cramped on different viewports?

**Automation:** MCP servers like Playwright can automate visual feedback loops by capturing screenshots, testing different viewport sizes, and validating interactive elements.

#### LLM as Judge
A separate language model can evaluate agent output based on fuzzy rules. While not the most robust method and carrying latency tradeoffs, this approach can improve performance in applications where any boost justifies the cost.

**Example:** A separate subagent could judge the tone of email drafts to ensure they align with the user's previous communication style.

## Testing and Improvement

After iterating through the agent loop, systematic testing ensures agents are well-equipped for their tasks. Key evaluation questions include:

- **Missing Information:** If the agent misunderstands tasks, can you restructure search APIs to make required information easier to find?
- **Repeated Failures:** Can you add formal rules in tool calls to identify and fix the failure pattern?
- **Limited Problem-Solving:** Can you provide more useful or creative tools for alternative approaches?
- **Performance Variability:** Should you build a representative test set for programmatic evaluations (evals) based on actual customer usage?

## Getting Started

### Prerequisites
- Understanding of the [[agent loop]] framework
- Familiarity with Claude's capabilities
- Basic knowledge of API integration

### Next Steps
1. Access the Claude Agent SDK documentation
2. Review best practices for tool design
3. Build a prototype agent using the gather-action-verify loop
4. Test and iterate based on agent performance

For developers already using the SDK, Anthropic provides migration guides to adopt the latest version.

## Related Concepts

- [[Claude]] - The language model powering the SDK
- [[Claude Code]] - The original agentic coding solution
- [[Model Context Protocol]] - Standardized external service integration
- [[Context Engineering]] - Structuring information for optimal model performance
- [[Agent Loop]] - The core feedback mechanism for autonomous agents
- [[Semantic Search]] - Vector-based information retrieval
- [[Code Generation]] - Using code as precise agent output

## Metadata

**Source:** Engineering at Anthropic - "Building agents with the Claude Agent SDK"

**Author:** Thariq Shihipar (with notes and editing from Molly Vorweck, Suzanne Wang, Alex Isken, Cat Wu, Keir Bradwell, Alexander Bricken, and Ashwin Bhat)

**Organization:**