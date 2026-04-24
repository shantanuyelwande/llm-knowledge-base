---
title: Agent Tools & Interoperability with Model Context Protocol (MCP)
source_file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:50:40.095071
raw_file_updated: 2026-04-24T18:50:40.095071
version: 1
sources:
  - file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:50:40.095071
tags: []
related_topics: []
backlinked_by: []
---
# Agent Tools & Interoperability with Model Context Protocol

## Summary

This article explores the role of agent tools in AI systems and the [[Model Context Protocol]] (MCP), an open standard designed to address the "N x M" integration problem. It covers tool design best practices, MCP's architecture and capabilities, and critical security considerations for enterprise deployment.

---

## Introduction

[[Foundation models]], even the most advanced, are fundamentally pattern prediction engines without access to external functions. While they excel at diverse tasks—from legal analysis to code generation—they cannot independently access new data, interact with external systems, or take actions to influence their environment.

Modern [[foundation models]] now support the ability to call external functions, or **tools**, which serve as the agent's "eyes" and "hands." With the rise of [[Agentic AI]], tools become increasingly critical, enabling AI agents to accomplish specific goals through external actions. However, connecting external tools to foundation models presents significant technical and security challenges.

The [[Model Context Protocol]] (MCP), introduced in 2024 by Anthropic, aims to standardize tool integration and address these challenges through a unified, plug-and-play protocol.

---

## Tools and Tool Calling

### What Is a Tool?

In modern AI systems, a **tool** is a function or program that an [[LLM]]-based application uses to accomplish tasks outside the model's native capabilities. Tools fall into two primary categories:

- **Knowledge retrieval**: Fetch data from structured and unstructured sources (databases, documents, web services)
- **Action execution**: Perform real-world operations such as sending emails, posting messages, executing code, or controlling physical devices

#### Example Use Case

A weather agent tool might call an API to retrieve the forecast for a user's location and convert temperatures to their preferred units. The model cannot accomplish this alone because:
1. It lacks real-time weather data
2. It doesn't know the user's location
3. Mathematical unit conversions are error-prone for LLMs

### Types of Tools

#### Function Tools

All models supporting [[function calling]] allow developers to define external functions that the model can invoke as needed. Tool definitions provide the model with:
- Clear name
- Parameter descriptions
- Natural language description of purpose and usage

In frameworks like Google ADK, tool definitions are extracted from Python docstrings in the tool code.

#### Built-in Tools

Some foundation models offer pre-integrated tools with implicit definitions managed by the model service. Examples include:
- Google Gemini's [[Grounding with Google Search]]
- [[Code Execution]]
- [[URL Context]]
- [[Computer Use]]

These tools are provided to the model without requiring developer configuration.

#### Agent Tools

Agents themselves can be invoked as tools, preventing full handoff of user conversations while allowing the primary agent to maintain control. This is accomplished in frameworks like ADK through the `AgentTool` class, and can even be extended to remote agents via the [[Agent2Agent Protocol]].

### Tool Categories & Design Considerations

| Category | Use Case | Key Design Tips |
|----------|----------|-----------------|
| Structured Data Retrieval | Querying databases, spreadsheets | Define clear schemas; optimize for efficient querying |
| Unstructured Data Retrieval | Searching documents, knowledge bases | Implement robust search; consider context window limits |
| Built-in Templates | Generating content from templates | Ensure parameters well-defined; clear template guidance |
| Google Connectors | Interacting with Google Workspace apps | Leverage APIs; handle authentication and rate limits |
| Third-Party Connectors | Integrating external services | Document API specifications; manage credentials securely |

---

## Best Practices for Tool Design

### Documentation Is Critical

Tool documentation is passed to the model as part of the request context, directly influencing how the model uses the tool.

**Recommended practices:**
- **Clear names**: Use descriptive, specific names (e.g., `create_critical_bug_in_jira_with_priority` rather than `update_jira`)
- **Parameter descriptions**: Clearly describe all inputs and outputs, including types and usage
- **Simplified parameter lists**: Keep parameter lists short with clear names to avoid model confusion
- **Detailed descriptions**: Provide clear explanations of purpose, parameters, and usage without technical jargon
- **Targeted examples**: Include examples to clarify ambiguities and demonstrate handling of edge cases
- **Default values**: Document default values clearly so models can use them correctly

### Describe Actions, Not Implementations

Instructions should describe what the model needs to accomplish, not how to accomplish it.

**Best practices:**
- Say "create a bug to describe the issue" rather than "use the `create_bug` tool"
- Avoid duplicating tool instructions in system prompts
- Describe objectives while allowing autonomous tool selection
- Document tool interactions and side effects

### Publish Tasks, Not API Calls

Tools should encapsulate user-facing tasks, not serve as thin wrappers over complex APIs. Enterprise APIs often have tens or hundreds of parameters; agents need tools representing specific, well-defined actions.

### Make Tools Granular

Follow standard coding best practices by keeping each tool focused on a single responsibility:
- Define clear, well-documented purposes
- Avoid multi-tools that encapsulate long workflows
- Document side effects and data returns clearly

### Design for Concise Output

Poorly designed tools can return excessive data, adversely affecting performance and cost:
- Avoid large responses (tables, files, images)
- Use external systems for data storage
- Return references to data rather than the data itself

### Use Validation Effectively

Leverage schema validation for tool inputs and outputs:
- Serve as documentation for the model
- Provide runtime validation of tool operation
- Include descriptive error messages that guide the model on remediation

---

## Understanding the Model Context Protocol

### The "N x M" Integration Problem

Integrating an LLM with an external tool traditionally requires custom-built, one-off connectors for each pairing. This creates an exponential explosion in development effort as the number of models (N) and tools (M) increases—the "N x M" integration problem.

MCP addresses this by providing a unified, plug-and-play protocol that serves as a universal interface between AI applications and external tools and data sources, enabling:
- Reduced development costs
- Faster time to market
- A reusable, shareable ecosystem of tools
- Decoupling of AI agents from tool implementation details

### Core Architectural Components

MCP implements a client-server model inspired by the [[Language Server Protocol]] (LSP), with three core components:

#### MCP Host

The application responsible for:
- Creating and managing individual MCP clients
- Managing user experience
- Orchestrating tool usage
- Enforcing security policies and content guardrails

May be a standalone application or sub-component of larger systems like multi-agent systems.

#### MCP Client

A software component embedded in the Host that:
- Maintains connections with MCP Servers
- Issues commands and receives responses
- Manages session lifecycle

#### MCP Server

A program providing capabilities (tools, resources, prompts) for AI applications. Often functions as an adapter or proxy for external tools, APIs, or data sources. Responsibilities include:
- Tool discovery and advertisement
- Command execution
- Result formatting and return
- Enterprise-level security, scalability, and governance (in enterprise contexts)

### Communication Layer: JSON-RPC, Transports, and Message Types

#### Base Protocol

MCP uses [[JSON-RPC]] 2.0 as its base message format, providing a lightweight, text-based, language-agnostic structure.

#### Message Types

- **Requests**: RPC calls expecting responses
- **Results**: Successful outcome messages
- **Errors**: Failure messages with code and description
- **Notifications**: One-way messages not requiring response

#### Transport Mechanisms

MCP supports two transport protocols:

- **stdio (Standard Input/Output)**: Fast, direct communication for local environments where the MCP server runs as a subprocess; used for local resource access
- **Streamable HTTP**: Recommended for remote client-server communication; supports SSE streaming while allowing stateless servers

### Key Primitives

MCP defines several key entity types that enhance LLM interactions with external systems:

**Server-side capabilities:**
- [[Tools]]
- [[Resources]]
- [[Prompts]]

**Client-side capabilities:**
- [[Sampling]]
- [[Elicitation]]
- [[Roots]]

Currently, only Tools are broadly supported (99% of tracked clients), while Resources and Prompts are supported by approximately one-third, and client-side capabilities have significantly lower adoption.

#### Tools

The standardized way for a server to describe available functions. Tool definitions must include:

- **name**: Unique identifier
- **title** (optional): Human-readable display name
- **description**: Functionality description for humans and LLMs
- **inputSchema**: JSON schema defining expected parameters
- **outputSchema** (optional): JSON schema defining output structure
- **annotations** (optional): Properties describing tool behavior

**Annotation