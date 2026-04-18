---
title: AI Agents guidebook
source_file: AI Agents guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:01:56.454821
raw_file_updated: 2026-04-17T21:01:56.454821
version: 1
sources:
  - file: AI Agents guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:01:56.454821
tags: []
related_topics: []
backlinked_by: []
---
# AI Agents Guidebook

## Summary

The **AI Agents Guidebook** is a comprehensive resource for understanding and building autonomous AI systems. It covers the fundamental differences between [[Large Language Models]], [[Retrieval-Augmented Generation]], and AI agents, explores the six essential building blocks needed for effective agents, describes five major design patterns, and provides twelve practical, production-ready project implementations using modern frameworks like [[CrewAI]] and [[LlamaIndex]].

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Building Blocks](#building-blocks)
4. [Design Patterns](#design-patterns)
5. [Levels of Agency](#levels-of-agency)
6. [Practical Projects](#practical-projects)
7. [Implementation Resources](#implementation-resources)

---

## Introduction

An **AI Agent** is an autonomous system that can reason, think, plan, identify relevant sources, extract information, take actions, and correct itself when errors occur. Unlike traditional [[Large Language Models]] that operate statically on training data, AI agents actively interact with their environment through [[Tools]], [[Memory]], and decision-making capabilities.

### The Agent Advantage

Consider a research task: generating a comprehensive report on AI trends.

**Traditional LLM Approach:**
- Ask for a summary
- Review and realize you need sources
- Request citations
- Identify outdated information
- Refine queries iteratively
- Result: Multiple manual iterations required

**AI Agent Approach:**
- Research Agent autonomously searches academic databases
- Filtering Agent identifies relevant papers by citation count and date
- Summarization Agent extracts key insights
- Formatting Agent structures the final report
- Result: Comprehensive, up-to-date report without human intervention at each step

---

## Core Concepts

### AI Agents vs LLMs vs RAG

These three concepts form a hierarchy of increasing autonomy:

#### Large Language Model (LLM)
[[Large Language Models]] like GPT-4 are trained on massive text datasets and can reason, generate, and summarize content. However, they are **static**—limited to their training data and unable to access the web, call APIs, or fetch new information independently.

**Characteristics:**
- Knowledge frozen at training time
- No external data access
- Reasoning limited to learned patterns
- No autonomous action capability

#### Retrieval-Augmented Generation (RAG)
[[Retrieval-Augmented Generation]] enhances an LLM by retrieving external documents from vector databases or search engines and feeding them as context before generating responses. This allows the LLM to access updated, relevant information without retraining.

**Characteristics:**
- Access to external knowledge bases
- Context-aware responses
- No retraining required for new information
- Still requires human direction for queries

#### AI Agents
AI agents add **autonomy** to the equation. Rather than simply answering questions, agents decide what steps to take: Should they call a [[Tool]]? Search the web? Summarize information? Store data? Agents orchestrate entire workflows like a real assistant.

**Characteristics:**
- Autonomous decision-making
- Multi-step planning
- Tool integration and execution
- Self-correction and iteration
- Workflow orchestration

### Conceptual Framework

A useful analogy:
- **LLM** = The brain
- **RAG** = Feeding the brain with fresh information
- **Agent** = The decision-maker that plans and acts using the brain and tools

---

## Building Blocks

Effective AI agents require six essential components:

### 1. Role-Playing

Assigning a clear, specific role dramatically improves agent performance. A generic AI assistant may provide vague answers, but defining it as a "Senior Contract Lawyer" produces legally precise, contextually relevant responses.

**Why it matters:**
- Shapes reasoning processes
- Influences information retrieval
- Increases output specificity and relevance
- More specific roles = sharper results

**Example:**
```
Generic: "Tell me about contracts"
→ Vague, general response

Specific: "You are a senior contract lawyer specializing in tech startups"
→ Precise, legally sound, contextually appropriate response
```

### 2. Focus/Tasks

Agents perform best with narrow, specific focus. Overloading an agent with too many tasks or excessive data causes confusion, inconsistency, and poor results.

**Best Practice:** Use multiple specialized agents rather than one generalist agent.

**Example:**
- ❌ One marketing agent handling messaging, pricing, and market analysis
- ✅ Separate agents: one for messaging tone, one for pricing strategy, one for market analysis

**Principle:** Specialized agents outperform generalist agents consistently.

### 3. Tools

[[Tools]] enable agents to move beyond reasoning into action. However, more tools don't guarantee better results—only relevant tools matter.

#### Benefits of Tools
- Search the web for real-time data
- Retrieve structured information from APIs and databases
- Execute code for calculations and transformations
- Analyze images, PDFs, and documents
- Interact with external systems

#### Tool Selection
Choose tools that directly support the agent's role and tasks. An AI research agent benefits from:
- Web search tool (recent publications)
- Summarization model (long papers)
- Citation manager (proper formatting)

But adding speech-to-text or code execution would create confusion and reduce efficiency.

#### Custom Tools

While frameworks like [[CrewAI]] provide built-in tools, custom tools are often necessary for specialized tasks.

**Custom Tool Development Process:**

1. **Define Input/Output** using Pydantic schemas
2. **Implement Core Logic** in the `_run()` method
3. **Handle Errors** gracefully
4. **Integrate with Agent** by attaching the tool

**Example: Currency Converter Tool**

A real-time currency conversion tool demonstrates custom tool development:

```python
# Define input schema
class CurrencyInput(BaseModel):
    amount: float
    source_currency: str
    target_currency: str

# Inherit from BaseTool
class CurrencyConverterTool(BaseTool):
    def _run(self, amount, source, target):
        # Fetch live exchange rates from API
        # Handle errors
        # Return converted amount
```

#### Model Context Protocol (MCP) Tools

For tools needed across multiple agents and flows, the [[Model Context Protocol]] enables creating reusable, server-based tools.

**MCP Advantages:**
- Expose tools as remote services
- Share across multiple agents
- Decouple tool logic from agent implementation
- Enable tool discovery and composition

**MCP Implementation:**
1. Create `server.py` with `@mcp.tool()` decorated functions
2. Run MCP server (e.g., `localhost:8081/sse`)
3. Connect agents using `MCPServerAdapter`
4. Agents call remote tools transparently

### 4. Cooperation

Multi-agent systems excel when agents collaborate and exchange feedback. Rather than one agent handling everything, specialized agents split tasks and improve each other's outputs.

**Collaboration Example: Financial Analysis System**
- Agent 1: Gathers financial data
- Agent 2: Assesses risk factors
- Agent 3: Builds investment strategy
- Agent 4: Writes comprehensive report

**Best Practice:** Design workflows where agents exchange insights and iteratively refine responses together.

**Benefits:**
- More accurate analysis
- Reduced individual agent burden
- Better error detection
- Higher quality outputs

### 5. Guardrails

Guardrails are constraints that keep agents on track and maintain quality standards. Without guardrails, agents may hallucinate, loop endlessly, or make poor decisions.

**Types of Guardrails:**

| Guardrail Type | Purpose | Example |
|---|---|---|
| Tool Usage Limits | Prevent API overuse | Max 10 web searches per query |
| Validation Checkpoints | Ensure output quality | Verify citations before finalizing |
| Fallback Mechanisms | Handle failures gracefully | Human review if agent fails |
| Output Constraints | Maintain standards | Legal assistant avoids outdated laws |
| Token Limits | Control costs | Max 2000 tokens per response |

**Implementation:** Guardrails should be built into the agent's task definitions and execution logic.

### 6. Memory

[[Memory]] is critical for agents that interact over time. Without memory, agents start fresh with each interaction, losing all context from previous sessions.

#### Types of Memory

**Short-term Memory**
- Exists only during current execution
- Stores recent conversation history
- Enables coherent responses within a session
- Cleared after interaction ends

**Long-term Memory**
- Persists across multiple interactions
- Stores user preferences and historical context
- Enables personalized, consistent behavior
- Requires external storage (databases, vector stores)

**Entity Memory**
- Tracks information about