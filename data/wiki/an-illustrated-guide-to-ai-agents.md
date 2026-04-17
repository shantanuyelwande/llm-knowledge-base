---
title: An illustrated guide to AI Agents
source_file: I am sharing _An illustrated guide to AI Agents.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T21:14:24.757698
raw_file_updated: 2026-04-05T21:14:24.757698
version: 1
sources:
  - file: I am sharing _An illustrated guide to AI Agents.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T21:14:24.757698
tags: ["AI Agents", "Autonomous Systems", "Large Language Models", "AI Architecture", "Agentic AI"]
related_topics: []
backlinked_by: []

---
# AI Agents: The Illustrated Guide

## Summary

AI Agents are autonomous systems that can reason, think, plan, determine relevant sources, extract information, take actions, and self-correct when needed. Unlike traditional [[Large Language Models]] (LLMs) that only generate text based on training data, or [[Retrieval-Augmented Generation]] (RAG) systems that enhance LLMs with external information, AI agents actively orchestrate workflows, make decisions, and coordinate multiple tools to accomplish complex tasks without constant human intervention.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Defining AI Agents](#defining-ai-agents)
3. [AI Agents vs Related Technologies](#ai-agents-vs-related-technologies)
4. [Building Blocks of AI Agents](#building-blocks-of-ai-agents)
5. [Agentic AI Design Patterns](#agentic-ai-design-patterns)
6. [Levels of Agentic AI Systems](#levels-of-agentic-ai-systems)
7. [Practical Applications](#practical-applications)
8. [See Also](#see-also)

---

## Introduction

The emergence of AI agents represents a significant evolution in artificial intelligence capabilities. While traditional LLMs excel at generating text based on learned patterns, they remain fundamentally passive—they respond to queries but don't independently seek information or execute complex workflows. AI agents bridge this gap by combining reasoning capabilities with autonomous action, making them suitable for real-world applications that demand proactive problem-solving.

---

## Defining AI Agents

### What is an AI Agent?

An **AI Agent** is an autonomous system capable of:

- **Reasoning**: Analyzing problems and determining appropriate solutions
- **Planning**: Breaking down complex tasks into manageable steps
- **Information Retrieval**: Identifying and accessing relevant data sources
- **Tool Usage**: Leveraging external systems, APIs, and specialized functions
- **Action**: Executing tasks independently
- **Self-Correction**: Identifying and fixing errors in its own outputs

### Example: Research Report Generation

Consider generating a comprehensive report on AI research trends:

**Traditional LLM Approach** (Manual, iterative):
1. Ask for a summary of recent papers
2. Review response and identify missing sources
3. Request a list of papers with citations
4. Find outdated sources and refine query
5. Repeat until satisfactory results obtained

**AI Agent Approach** (Autonomous):
- **Research Agent**: Autonomously searches arXiv, Semantic Scholar, and Google Scholar
- **Filtering Agent**: Identifies most relevant papers by citation count, publication date, and keywords
- **Summarization Agent**: Extracts key insights and condenses into readable format
- **Formatting Agent**: Structures final report with professional layout

The agent completes the entire workflow without human intervention at each step, self-refining outputs to ensure comprehensiveness and accuracy.

---

## AI Agents vs Related Technologies

### Conceptual Comparison

The relationship between these three technologies can be understood through an analogy:

- **[[Large Language Model|LLM]]** = The brain
- **[[Retrieval-Augmented Generation|RAG]]** = Fresh information feeding the brain
- **AI Agent** = The decision-maker that plans and acts using the brain and tools

### Large Language Model (LLM)

An LLM (such as GPT-4) is trained on massive volumes of text data and can:
- Reason and generate responses
- Summarize information
- Answer questions based on training knowledge

**Limitations**: Static knowledge; cannot access real-time web data, call APIs, or fetch new information independently.

### Retrieval-Augmented Generation (RAG)

RAG enhances an LLM by:
- Retrieving external documents from vector databases, search engines, or knowledge bases
- Feeding retrieved documents as context before generation
- Updating LLM awareness without retraining

**Advantage**: Provides current, relevant information while maintaining LLM reasoning capabilities.

### AI Agent

An agent adds **autonomy** to the equation by:
- Deciding which steps to take
- Determining when to call tools
- Choosing whether to search the web, summarize, or store information
- Orchestrating complex workflows
- Functioning as an autonomous assistant

---

## Building Blocks of AI Agents

Effective AI agents require six essential architectural components:

### 1) Role-Playing

Assigning a specific, well-defined role significantly improves agent performance.

**Principle**: A generic AI assistant may provide vague answers, but defining it as a "Senior Contract Lawyer" produces legally precise, contextually appropriate responses.

**Why it works**: Role assignment shapes the agent's reasoning process and information retrieval strategy. More specific roles yield sharper, more relevant outputs.

### 2) Focus/Tasks

Focus is critical for reducing [[Hallucination|hallucinations]] and improving accuracy.

**Principle**: Overloading an agent with too many tasks or excessive data reduces performance rather than improving it.

**Example**: A marketing agent should focus exclusively on messaging, tone, and audience—not pricing or market analysis.

**Best Practice**: Use multiple specialized agents, each with narrow, specific focus areas rather than attempting to create one omniscient agent.

### 3) Tools

Agents become more capable when equipped with appropriate tools, but quantity doesn't guarantee quality.

**Principle**: More tools ≠ better results. Tools must be strategically selected.

#### Tool Categories

For an AI research agent, beneficial tools include:
- Web search tool for retrieving recent publications
- Summarization model for condensing long papers
- Citation manager for proper reference formatting

Unnecessary tools (speech-to-text, code execution) can confuse the agent and reduce efficiency.

#### 3.1) Custom Tools

While LLM-powered agents excel at reasoning and generation, they lack direct access to:
- Real-time information
- External systems
- Specialized computations

Custom tools enable agents to:
- Search the web for real-time data
- Retrieve structured information from APIs and databases
- Execute code for calculations and data transformations
- Analyze images, PDFs, and documents beyond text

**Implementation Example**: Building a real-time currency conversion tool in [[CrewAI]]

Instead of allowing an LLM to guess exchange rates, a custom tool fetches live rates from an external API (e.g., exchangerate-api.com), providing accurate, current information.

**Tool Structure**:
```
1. Define input fields using Pydantic for validation
2. Create tool class inheriting from BaseTool
3. Implement _run method containing tool logic
4. Handle errors for failed requests or invalid inputs
5. Assign tool to agent for direct invocation
```

#### 3.2) Custom Tools via Model Context Protocol (MCP)

[[Model Context Protocol|MCP]] enables tools to be exposed as reusable services across multiple agents and workflows.

**Advantages over embedded tools**:
- Reusability across multiple crews and flows
- Centralized tool management
- Simplified agent configuration
- Remote tool access via standardized interface

**MCP Implementation Pattern**:

1. **Server Setup**: Create lightweight server exposing tool via `@mcp.tool()` decorator
2. **Tool Logic**: Implement function taking inputs and returning results
3. **Server Startup**: Run MCP server (typically on localhost:8081/sse)
4. **Client Connection**: Use `MCPServerAdapter` in CrewAI agents
5. **Tool Invocation**: Agents call remote tool as if locally defined

**Benefit**: Enables tool sharing across different agent systems and deployment environments.

### 4) Cooperation

Multi-agent systems achieve superior results through collaboration and feedback exchange.

**Principle**: Rather than one agent handling everything, specialized agents split tasks and improve each other's outputs.

**Example: AI-Powered Financial Analysis**
- Agent 1: Gathers market data
- Agent 2: Assesses risk factors
- Agent 3: Builds investment strategy
- Agent 4: Writes comprehensive report

**Best Practice**: Design workflows enabling agents to exchange insights and collaboratively refine responses.

### 5) Guardrails

Guardrails are essential constraints preventing agents from going off-track.

**Without guardrails, agents may**:
- Hallucinate or generate false information
- Loop endlessly without reaching conclusions
- Make poor decisions or invalid tool calls

**Useful guardrail implementations**:
- **Tool usage limits**: Prevent overuse of APIs or irrelevant queries
- **Validation checkpoints**: Ensure outputs meet predefined criteria before proceeding
- **Fallback mechanisms**: Enable human intervention or alternative agent handling if primary agent fails

**Example**: A legal assistant agent requires guardrails to avoid citing outdated laws or making false claims.

### 6) Memory

Memory is perhaps the most critical component for practical AI agents.

**Without memory**: Agents start fresh each interaction, losing all context and learning from previous exchanges.

**With memory