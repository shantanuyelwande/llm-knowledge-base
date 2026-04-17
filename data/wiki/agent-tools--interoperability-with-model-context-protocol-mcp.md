---
title: Agent Tools & Interoperability with Model Context Protocol (MCP)
source_file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:18:39.725702
raw_file_updated: 2026-04-05T20:18:39.725702
version: 1
sources:
  - file: Agent Tools & Interoperability with Model Context Protocol (MCP).pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:18:39.725702
tags: ["AI Agents", "Model Context Protocol", "Tool Integration", "Enterprise Security", "Foundation Models"]
related_topics: []
backlinked_by: []

---
# Agent Tools & Interoperability with Model Context Protocol (MCP)

## Summary

**Agent Tools & Interoperability with MCP** is a comprehensive technical guide addressing how [[AI agents]] interact with external systems through standardized tools and the [[Model Context Protocol]] (MCP). The document examines tool design best practices, MCP architecture, and enterprise security considerations for agentic AI systems.

---

## Introduction

Without access to external functions, even advanced [[foundation models]] are limited to pattern prediction based on training data. They cannot access new information, interact with external systems, or take actions to influence their environment. **Tools** serve as the essential bridge between AI systems and the external world, acting as an agent's "eyes" and "hands."

The rise of [[Agentic AI]] has made tools increasingly critical to enterprise applications. However, connecting tools to foundation models presents significant technical and security challenges. The [[Model Context Protocol]] was introduced in 2024 as an open standard to streamline tool integration and address these challenges systematically.

---

## Understanding Tools and Tool Calling

### What Are Tools?

In modern AI systems, a **tool** is a function or program that an [[LLM]]-based application can use to accomplish tasks outside the model's native capabilities. Tools fall into two primary categories:

- **Knowledge tools**: Retrieve data from structured and unstructured sources (databases, APIs, web services)
- **Action tools**: Perform real-world operations on behalf of users (sending emails, executing code, controlling devices)

#### Example Use Case

A weather agent tool illustrates these concepts: to answer "What's the weather in my location?", the model needs:
- Current location data (external knowledge)
- Weather forecast information (external data retrieval)
- Unit conversion capabilities (external computation)

### Types of Tools

#### Function Tools

Custom functions defined by developers that models can call as needed. The tool definition provides basic details including:
- Clear, descriptive name
- Parameter specifications
- Natural language description of purpose

Function tools are passed to the model as part of the request context, often extracted from code documentation (e.g., Python docstrings).

#### Built-in Tools

Pre-defined tools offered implicitly by foundation model providers. Examples include:
- [[Gemini API]] features: Grounding with Google Search, Code Execution, URL Context, Computer Use
- Tools where definitions are provided to the model behind the scenes

#### Agent Tools

Agents themselves can be invoked as tools through frameworks like [[Google ADK]]. This allows:
- Primary agents to maintain control over interactions
- Sub-agent inputs and outputs to be processed by parent agents
- Remote agents to be made available as tools via [[A2A protocol]] (Agent2Agent Protocol)

### Tool Categories and Design

| Tool Use Case | Key Design Tips |
|---|---|
| Structured Data Retrieval | Define clear schemas, optimize for efficient querying, handle data types gracefully |
| Unstructured Data Retrieval | Implement robust search algorithms, consider context window limitations |
| Built-in Templates | Ensure template parameters are well-defined, provide clear guidance on selection |
| Google Connectors | Leverage Google APIs, ensure proper authentication, handle rate limits |
| Third-Party Connectors | Document API specifications, manage API keys securely, implement error handling |

---

## Best Practices for Tool Design

### Documentation is Critical

Tool documentation—including name, description, and attributes—is passed to the model as request context. Quality documentation directly influences model performance.

**Best practices:**
- Use clear, descriptive names (e.g., `create_critical_bug_in_jira_with_priority` rather than `update_jira`)
- Describe all input and output parameters with required types and usage
- Keep parameter lists short with clear names
- Provide detailed descriptions avoiding technical jargon
- Include targeted examples addressing ambiguities
- Provide documented default values

### Describe Actions, Not Implementations

Model instructions should describe what needs to be accomplished, not how to accomplish it using specific tools.

**Principles:**
- Explain what the model needs to do, not which tool to use
- Avoid duplicating tool documentation in system instructions
- Don't dictate specific sequences of tool calls
- Document tool interactions and side effects clearly

### Publish Tasks, Not API Calls

Tools should encapsulate user-facing tasks, not simply wrap existing APIs. Complex enterprise APIs may have dozens of parameters; tools should expose only what agents need at runtime.

### Make Tools Granular

Follow standard coding best practices by keeping functions concise and focused:
- Define clear, single responsibilities
- Avoid multi-tools that encapsulate long workflows
- Make tools easier to document and maintain
- Enable consistent agent decision-making about when to use tools

### Design for Concise Output

Poorly designed tools can return large volumes of data, adversely affecting performance and cost:
- Avoid returning large data tables or files directly to the LLM
- Use external storage systems (databases, artifact services)
- Return references to data rather than the data itself
- Store results in temporary locations for subsequent tool retrieval

### Use Validation Effectively

Schema validation for inputs and outputs serves dual purposes:
- **Documentation**: Clarifies tool capabilities and usage for LLMs
- **Runtime checking**: Validates correct tool operation

**Error messages are opportunities**: Tool error messages should guide LLMs on addressing specific errors, not just report failure codes.

---

## Understanding the Model Context Protocol

### The N×M Integration Problem

Integrating an [[LLM]] with an external tool traditionally requires custom, one-off connectors for each tool-application pairing. This creates exponential development effort—the "N×M" problem—where necessary custom connections grow with each new model (N) or tool (M).

### MCP Solution

Introduced by Anthropic in November 2024, [[Model Context Protocol]] (MCP) is an open standard providing:
- Unified, plug-and-play protocol for AI applications and external tools
- Standardized communication layer decoupling agents from tool implementation details
- Foundation for modular, scalable, and efficient ecosystems

### Core Architectural Components

MCP implements a client-server model inspired by the [[Language Server Protocol]] (LSP):

#### MCP Host
The application responsible for:
- Creating and managing MCP clients
- Managing user experience
- Orchestrating tool usage
- Enforcing security policies and content guardrails

#### MCP Client
A software component embedded in the Host that:
- Maintains server connections
- Issues commands and receives responses
- Manages communication session lifecycle

#### MCP Server
A program providing capabilities to AI applications, typically functioning as an adapter or proxy for external tools, data sources, or APIs. Responsibilities include:
- Tool discovery and advertising
- Receiving and executing commands
- Formatting and returning results
- Enterprise security, scalability, and governance (in enterprise contexts)

### Communication Layer

#### Base Protocol: JSON-RPC 2.0
MCP uses JSON-RPC 2.0 for lightweight, text-based, language-agnostic communication.

#### Message Types
- **Requests**: RPC calls expecting responses
- **Results**: Successful outcomes of requests
- **Errors**: Failed requests with codes and descriptions
- **Notifications**: One-way messages requiring no response

#### Transport Protocols

**stdio (Standard Input/Output)**
- Fast, direct communication in local environments
- Used when tools access local resources like user filesystems
- MCP server runs as subprocess of Host application

**Streamable HTTP**
- Recommended for remote client-server communication
- Supports SSE streaming responses
- Allows stateless servers and plain HTTP implementation

### Key Primitives

MCP defines several key concepts enhancing LLM-based application capabilities:

#### Server-Side Capabilities

**Tools** (99% client support)
- Standardized way for servers to describe available functions
- Examples: `read_file`, `get_weather`, `execute_sql`, `create_ticket`
- Servers publish lists with descriptions and parameter schemas

**Resources** (34% client support)
- Contextual data for Host applications
- Examples: file contents, database records, schemas, images, configuration data
- Security risk: arbitrary external content in LLM context requires validation

**Prompts** (32% client support)
- Reusable prompt examples or templates
- Intended for client-LLM interaction
- Security concern: third-party instruction injection into execution path
- Current recommendation: Use rarely until stronger security model develops

#### Client-Side Capabilities

**Sampling** (10% client support)
- Allows MCP servers to request LLM completions from client
- Reverses typical control flow, enabling tools to leverage Host's AI model
- Benefits: Client controls LLM providers, costs, content guardrails
- Risks: Opens avenue for prompt injection
- Best practice: Implement human-in-the-loop approval

**Elicitation** (4% client support)
- Allows servers to request additional user information from client
- Provides formal mechanism for server-user interaction via client UI