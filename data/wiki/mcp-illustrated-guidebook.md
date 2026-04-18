---
title: MCP illustrated guidebook
source_file: MCP illustrated guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:52:07.541469
raw_file_updated: 2026-04-17T20:52:07.541469
version: 1
sources:
  - file: MCP illustrated guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:52:07.541469
tags: []
related_topics: []
backlinked_by: []
---
# Model Context Protocol (MCP) Illustrated Guidebook

## Overview

The **Model Context Protocol (MCP) Illustrated Guidebook** is a comprehensive 2025 edition resource created by Avi Chawla and Akshay Pachar from Daily Dose of Data Science. This guidebook provides both theoretical foundations and practical implementations for understanding and building with MCP, a standardized interface that enables [[AI Models]] to seamlessly interact with external tools, resources, and environments.

## Quick Summary

| Aspect | Details |
|--------|---------|
| **Reading Time** | ~3 hours (customizable based on expertise assessment) |
| **Edition** | 2025 |
| **Authors** | Avi Chawla & Akshay Pachar |
| **Source** | Daily Dose of Data Science |
| **Assessment Tool** | https://bit.ly/mcp-assessment |

---

## Table of Contents

### Section 1: Model Context Protocol Fundamentals

#### 1.1 What is MCP?

[[Model Context Protocol]] (MCP) is a standardized interface and framework that allows [[Artificial Intelligence]] models to seamlessly interact with external tools, resources, and environments. The protocol functions as a universal connector for AI systems, analogous to how USB-C standardizes connections between electronic devices.

**Core Concept**: MCP acts as a translator between AI agents and external capabilities. Rather than requiring an AI system to learn how to communicate with each individual tool or data source, MCP provides a single standardized language that all parties understand.

#### 1.2 Why Was MCP Created?

##### The Problem: M×N Integration Complexity

Before MCP, connecting [[AI Applications]] to external tools and data sources created a significant architectural challenge known as the **M×N integration problem**:

- If you have **M** different AI applications and **N** different tools or data sources
- You would need up to **M × N** custom integration modules
- Each AI would require unique code to connect to each external service
- This created "spaghetti-like interconnections" that did not scale

**Real-world impact**:
- Developers were "reinventing the wheel" with each new integration
- Tool providers had to support multiple incompatible [[APIs]]
- Integration maintenance became exponentially complex

##### The Solution: Standardized Interface

MCP reduces the integration problem from **M × N** to **M + N** implementations:

- Each of the **M** AI applications implements the [[MCP Client]] side once
- Each of the **N** tools implements an [[MCP Server]] once
- All parties "speak the same language" through MCP
- New pairings require no custom code—they already understand each other

#### 1.3 MCP Architecture Overview

MCP follows a client-server architecture with three main roles:

##### Host

The **Host** is the user-facing [[AI Application]] where the AI model lives and interacts with users.

**Examples**:
- Chat applications (OpenAI's ChatGPT, Anthropic's Claude Desktop)
- AI-enhanced IDEs (Cursor)
- Custom applications (Chainlit)

**Responsibilities**:
- Initiates connections to available [[MCP Server|MCP Servers]]
- Captures user input
- Maintains conversation history
- Displays model responses

##### Client

The **MCP Client** is a component within the Host that handles low-level communication with an [[MCP Server]].

**Role**: Acts as an adapter or messenger between the Host and Server
- The Host decides what to do
- The Client knows how to speak MCP to carry out those instructions

##### Server

The **MCP Server** is an external program or service that provides capabilities (tools, data, etc.) to the application.

**Characteristics**:
- Can run locally on the same machine or remotely on cloud services
- Advertises available capabilities in a standard format
- Executes requests from clients
- Returns results in standardized format

#### 1.4 Tools, Resources, and Prompts

MCP defines three core types of capabilities that servers can expose:

##### Tools

**Definition**: Executable actions or functions that [[AI Models]] can invoke, often with side effects or external [[API]] calls.

**Key characteristics**:
- Triggered by the AI model's choice (the [[Language Model]] decides when to use them)
- Can perform computations or external operations
- Return structured data
- May require user permission before execution

**Example implementation**:
```python
@mcp.tool()
def get_weather(location: str) -> dict:
    """Get current weather for a location"""
    return {
        "temperature": 72,
        "conditions": "Sunny",
        "location": location
    }
```

**Safety consideration**: Often requires user approval ("Allow AI to use 'get_weather' tool? Yes/No") to prevent abuse.

##### Resources

**Definition**: Read-only data sources that [[AI Models]] can query for information without side effects.

**Key characteristics**:
- Provide information retrieval without modification capability
- Usually accessed under host application control (not spontaneously by the model)
- Identified by URIs or names
- Application-regulated for privacy and permissions

**Examples**:
- Local file contents
- Knowledge base snippets
- Database query results (read-only)
- Configuration information
- ArXiv papers database

**Safety advantage**: Since resources are read-only, they present fewer security risks than tools, though privacy concerns remain.

##### Prompts

**Definition**: Predefined prompt templates or conversation flows that guide [[AI Model]] behavior.

**Characteristics**:
- Represent best practices or predefine strategies for AI use
- Can be updated on the server without changing client applications
- Usually user-controlled or developer-controlled
- Often fetched at the beginning of interactions or when users choose specific modes

**Use cases**:
- Code review templates
- Brainstorming guides
- Step-by-step problem solver templates
- Domain-specific system roles
- Multi-turn diagnostic workflows

---

## Section 2: Practical MCP Projects

This section contains 11 hands-on projects demonstrating real-world MCP implementations:

### Project #1: 100% Local MCP Client

**Objective**: Build an [[MCP Client]] component entirely locally without cloud dependencies.

**Tech Stack**:
- [[LlamaIndex]] for building MCP-powered agents
- [[Ollama]] for locally serving Deepseek-R1
- LightningAI for development and hosting

**Workflow**:
1. User submits a query
2. Agent connects to MCP server to discover tools
3. Agent invokes appropriate tool and retrieves context
4. Agent returns context-aware response

**Key Implementation Steps**:
1. Build an SQLite MCP Server with tools (add data, fetch data)
2. Set up local [[Language Model]] via Ollama
3. Define agent system prompt
4. Create agent with tool access
5. Manage agent interactions with memory context
6. Initialize MCP client and integrate tools
7. Run agent interactions

**Reference**: https://www.dailydoseofds.com/p/building-a-100-local-mcp-client/

### Project #2: MCP-powered Agentic RAG

**Objective**: Create an [[Retrieval-Augmented Generation]] system with intelligent tool selection.

**Tech Stack**:
- [[Bright Data]] for web scraping at scale
- [[Qdrant]] as vector database
- [[Cursor]] as MCP client

**Workflow**:
1. User inputs query through MCP client
2. Client contacts MCP server to select relevant tool
3. Tool output returned to client
4. Client generates response

**Capabilities**:
- Vector database search for ML-related queries
- Web search fallback for general queries
- Agentic behavior (tool selection based on query type)

**Reference**: https://www.dailydoseofds.com/p/mcp-powered-agentic-rag/

### Project #3: MCP-powered Financial Analyst

**Objective**: Build an AI agent for stock market analysis and visualization.

**Tech Stack**:
- [[CrewAI]] for multi-agent orchestration
- [[Ollama]] for local DeepSeek-R1
- [[Cursor]] as MCP host

**Agent Roles**:
- **Query Parser Agent**: Extracts structured output from natural language
- **Code Writer Agent**: Generates Python code for stock visualization
- **Code Executor Agent**: Reviews and executes code in sandbox

**Workflow**:
1. User submits query
2. MCP agent initiates financial analyst crew
3. Crew conducts research and creates executable script
4. Agent runs script to generate analysis plot

**MCP Tools Exposed**:
- `save_code`: Saves generated code locally
- `run_code_and_show_plot