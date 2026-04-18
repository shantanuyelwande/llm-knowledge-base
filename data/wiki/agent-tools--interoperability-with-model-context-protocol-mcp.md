---
title: Agent Tools & Interoperability with Model Context Protocol (MCP)
source_file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:51:42.817763
raw_file_updated: 2026-04-17T20:51:42.817763
version: 1
sources:
  - file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:51:42.817763
tags: []
related_topics: []
backlinked_by: []
---
# Agent Tools & Interoperability with Model Context Protocol (MCP)

## Summary

This article explores the integration of external tools with [[AI agents]] and [[foundation models]] through the [[Model Context Protocol]] (MCP), an open standard introduced by Anthropic in 2024. It covers tool design best practices, MCP's architectural components, and the security challenges enterprises face when implementing MCP in production environments.

## Introduction

[[Foundation models]] and [[large language models]] (LLMs) are fundamentally limited to pattern prediction based on their training data. Without access to external functions, they cannot perceive new information about the world, interact with external systems, or take actions to influence their environment. **Tools** extend these capabilities by acting as an AI system's "eyes" and "hands," enabling [[AI agents]] to accomplish tasks beyond pure content generation.

With the emergence of [[agentic AI]], tools have become essential infrastructure. However, connecting external tools to foundation models presents significant technical and security challenges. The [[Model Context Protocol]] (MCP) was introduced as a standardized solution to streamline tool integration and address these challenges.

## Tools and Tool Calling

### What is a Tool?

In modern AI systems, a **tool** is a function or program that an [[LLM]]-based application can use to accomplish tasks outside the model's native capabilities. Tools broadly serve two purposes:

- **Information Retrieval**: Tools allow models to fetch data from various sources, including structured databases and unstructured documents
- **Action/Execution**: Tools enable models to perform real-world operations, such as sending emails, executing code, or controlling physical devices

### Example: Weather Agent

A practical example illustrates the necessity of tools. When asked "What's the weather in my location?", a foundation model cannot answer correctly because:
- The model lacks access to current weather data
- The model doesn't know the user's location
- The model's mathematical capabilities for unit conversion are limited

A weather tool solves this by fetching real-time data and performing the necessary calculations.

### Types of Tools

#### Function Tools

[[Function tools]] are external functions defined by developers that models can call as needed. The tool definition provides details about how the model should use the tool, typically extracted from code documentation (such as Python docstrings in frameworks like [[Google ADK]]).

**Key characteristics:**
- Clear name describing the function
- Parameter definitions with types and descriptions
- Natural language description of purpose

#### Built-in Tools

Some foundation models offer pre-configured tools where the definition is provided implicitly by the model service. Examples include:

- [[Google Gemini]] built-in tools:
  - Grounding with Google Search
  - Code Execution
  - URL Context
  - Computer Use

Built-in tools are invisible to developers; the model service handles tool definitions separately.

#### Agent Tools

An [[AI agent]] can be invoked as a tool itself, allowing a primary agent to maintain control over interactions while delegating specific tasks to sub-agents. This prevents full handoffs of user conversations and enables better control over input and output processing.

**Benefits:**
- Maintains primary agent control
- Allows remote agents to be available as tools via protocols like [[A2A (Agent-to-Agent Protocol)]]
- Enables hierarchical agent architectures

### Tool Categories and Design Considerations

| Tool Category | Use Case | Design Tips |
|---|---|---|
| Structured Data Retrieval | Querying databases, spreadsheets | Define clear schemas, optimize for efficient querying |
| Unstructured Data Retrieval | Searching documents, web pages, knowledge bases | Implement robust search algorithms, consider context window limitations |
| Built-in Templates | Generating content from predefined templates | Ensure template parameters are well-defined |
| Google Connectors | Interacting with Google Workspace apps | Leverage Google APIs, handle rate limits |
| Third-Party Connectors | Integrating external services | Document API specifications, manage API keys securely |

## Best Practices for Tool Design

### Documentation is Critical

Tool documentation directly influences how models use tools. Essential elements include:

- **Clear Names**: Use descriptive, specific names like `create_critical_bug_in_jira_with_priority` rather than `update_jira`
- **Parameter Descriptions**: Document all inputs with required types and usage
- **Short Parameter Lists**: Keep parameters concise to avoid model confusion
- **Detailed Descriptions**: Explain purpose, inputs, outputs, and any special considerations
- **Targeted Examples**: Provide examples addressing ambiguities and edge cases
- **Default Values**: Document default values clearly for model reference

### Describe Actions, Not Implementations

Tool instructions should explain **what** the model needs to do, not **how** to do it:

- ✓ "Create a bug to describe the issue"
- ✗ "Use the create_bug tool"

This approach:
- Eliminates conflicts between instructions and tool documentation
- Prevents model confusion from duplicated instructions
- Allows autonomous tool selection by the model

### Publish Tasks, Not API Calls

Tools should encapsulate user-facing tasks, not mirror complex internal APIs. While APIs are designed for human developers with full knowledge of parameters, agent tools must be usable dynamically by models deciding at runtime which parameters to provide.

### Make Tools Granular

Follow single-responsibility principles:
- Define clear, well-documented purposes for each tool
- Avoid multi-tools that encapsulate long workflows
- Make it easier for models to determine when tools are needed

### Design for Concise Output

Large responses can:
- Swamp the [[context window]], increasing cost and latency
- Impact subsequent requests stored in conversation history
- Degrade reasoning quality

**Solutions:**
- Return references rather than full data (e.g., table names instead of large query results)
- Use external storage systems like database tables or artifact services

### Use Validation Effectively

Implement schema validation for inputs and outputs:
- Provides additional documentation for models
- Enables runtime validation of tool operation
- Helps identify and correct misuse

**Error Messages as Documentation:**
Tool error messages provide opportunities to guide models on addressing failures. Instead of simple error codes, return instructive messages like: "No product data found for product ID XXX. Ask the customer to confirm the product name, and look up the product ID by name."

## Understanding the Model Context Protocol

### The N × M Integration Problem

Integrating LLMs with external tools traditionally required custom, one-off connectors for each tool-application pairing. This creates an "N × M" integration problem: the number of necessary connections grows exponentially with each new model (N) or tool (M) added to the ecosystem.

[[Model Context Protocol]] was introduced in November 2024 by [[Anthropic]] as an open standard to replace fragmented custom integrations with a unified, plug-and-play protocol. MCP aims to serve as a universal interface between AI applications and external tools and data sources, enabling a more modular, scalable, and efficient ecosystem.

### Core Architectural Components

MCP implements a [[client-server model]] inspired by the [[Language Server Protocol]] (LSP):

#### MCP Host

The application responsible for:
- Creating and managing individual MCP clients
- Managing user experience
- Orchestrating tool usage
- Enforcing security policies and content guardrails

May be a standalone application or a sub-component of larger systems like [[multi-agent systems]].

#### MCP Client

A software component embedded within the Host that:
- Maintains connections with MCP servers
- Issues commands and receives responses
- Manages communication session lifecycle

#### MCP Server

A program providing capabilities to AI applications, often functioning as an adapter or proxy for external tools, data sources, or APIs. Responsibilities include:
- Advertising available tools (tool discovery)
- Receiving and executing commands
- Formatting and returning results
- Implementing security, scalability, and governance in enterprise contexts

### Communication Layer

#### Base Protocol: JSON-RPC 2.0

MCP uses [[JSON-RPC 2.0]] as its base message format, providing lightweight, text-based, language-agnostic communication.

#### Message Types

- **Requests**: RPC calls expecting responses
- **Results**: Successful outcomes of requests
- **Errors**: Failed requests with code and description
- **Notifications**: One-way messages requiring no response

#### Transport Mechanisms

MCP supports two transport protocols:

**stdio (Standard Input/Output)**
- Used for fast, direct local communication
- MCP server runs as a subprocess of the Host application
- Suitable for tools accessing local resources like user filesystems

**Streamable HTTP**
- Recommended for remote client-server communication
- Supports SSE streaming responses
- Allows stateless servers without requiring SSE
- Can be implemented in plain HTTP servers

### Key Primitives

MCP defines several key entity types to enhance LLM-based applications:

#### Server-Side Capabilities

**Tools** (99% support)
- Standardized way for servers to describe available functions
- Examples: `read_file`, `get_weather`, `execute_sql`, `create