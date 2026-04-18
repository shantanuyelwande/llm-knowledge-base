---
title: AI Agents guidebook
source_file: AI Agents guidebook.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:23:10.660179
raw_file_updated: 2026-04-17T20:23:10.660179
version: 1
sources:
  - file: AI Agents guidebook.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:23:10.660179
tags: []
related_topics: []
backlinked_by: []
---
# AI Agents Guidebook

## Summary

A comprehensive guide to understanding and building [[AI Agents]] - autonomous systems that can reason, plan, and take action independently. This resource covers the fundamental concepts, building blocks, design patterns, and practical implementations of agentic AI systems, with detailed code examples and 12 real-world projects.

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
3. [Building Blocks](#building-blocks)
4. [Design Patterns](#design-patterns)
5. [Levels of Agency](#levels-of-agency)
6. [Practical Projects](#practical-projects)
7. [Related Resources](#related-resources)

---

## Introduction

### What is an AI Agent?

An **AI Agent** is an autonomous system that can reason, think, plan, identify relevant sources, extract information, take actions, and self-correct when something goes wrong. Unlike static [[Large Language Models]] (LLMs), agents actively orchestrate workflows and make independent decisions.

#### Key Distinction: The Research Example

**Traditional LLM Approach:**
- Ask for a summary of recent papers
- Review and realize sources are needed
- Request citations
- Discover outdated sources
- Refine query iteratively
- Multiple manual interventions required

**AI Agent Approach:**
- Research Agent autonomously searches academic databases
- Filtering Agent identifies most relevant papers
- Summarization Agent extracts key insights
- Formatting Agent structures the final report
- Entire process completes without human intervention

### Agent vs LLM vs RAG

The relationship between these three concepts can be understood through an analogy:

| Component | Role | Capabilities |
|-----------|------|--------------|
| **LLM** | The brain | Reasoning and generation based on training data |
| **[[RAG]]** | Information feeder | Retrieves external documents and provides context |
| **Agent** | Decision-maker | Plans, acts, orchestrates workflows using brain and tools |

#### Large Language Model (LLM)

- Trained on massive text datasets
- Can reason, generate, and summarize
- Limited to knowledge from training data
- Static and cannot access real-time information
- Cannot independently call APIs or fetch new facts

#### Retrieval-Augmented Generation (RAG)

- Enhances LLMs with external knowledge
- Retrieves documents from [[Vector Database|vector databases]] and search engines
- Feeds retrieved information as context before generation
- Enables awareness of updated, relevant information
- Does not require model retraining

#### Agent

- Adds autonomous decision-making to the mix
- Determines which steps to take independently
- Decides when to call tools, search the web, summarize, or store information
- Orchestrates complete workflows like a real assistant
- Combines LLM capabilities with tool use and planning

---

## Building Blocks

AI agents require six essential building blocks to be reliable, intelligent, and effective in real-world applications:

### 1. Role-Playing

**Purpose:** Shape the agent's reasoning and output quality through explicit role assignment.

**Key Principle:** Specific roles produce sharper, more relevant outputs than generic assistants.

**Example:**
- Generic assistant: Vague, general responses
- "Senior Contract Lawyer" role: Precise legal language and context-aware analysis

**Best Practice:** Define clear, specific roles that align with the task domain.

### 2. Focus/Tasks

**Purpose:** Reduce [[Hallucination|hallucinations]] and improve accuracy through task specialization.

**Key Principle:** Overloading agents with multiple tasks causes confusion and poor results.

**Guidelines:**
- Assign narrow, specific focus areas
- Avoid multi-domain tasks in a single agent
- Example: Marketing agent focuses on messaging and tone, not pricing or market analysis
- Use multiple specialized agents instead of one generalist

**Best Practice:** "Specialized agents perform better - every time."

### 3. Tools

**Purpose:** Enable agents to access real-time information and execute specialized computations.

**Key Principle:** More tools ≠ better results. Select only relevant, necessary tools.

**Appropriate Tools Example (AI Research Agent):**
- Web search tool for recent publications
- Summarization model for condensing papers
- Citation manager for formatting references
- ❌ Avoid: Speech-to-text, unrelated code execution

#### 3.1 Custom Tools

Custom tools extend agent capabilities beyond built-in functions by:
- Searching the web for real-time data
- Retrieving structured information from [[API|APIs]] and [[Database|databases]]
- Executing code for calculations and transformations
- Analyzing images, PDFs, and documents

**Example Implementation: Currency Converter Tool**

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class CurrencyInput(BaseModel):
    amount: float = Field(description="Amount to convert")
    source_currency: str = Field(description="Source currency code")
    target_currency: str = Field(description="Target currency code")

class CurrencyConverterTool(BaseTool):
    name: str = "currency_converter"
    description: str = "Convert currency using live exchange rates"
    args_schema: type[BaseModel] = CurrencyInput
    
    def _run(self, amount: float, source_currency: str, target_currency: str) -> str:
        # Fetch live exchange rates from API
        # Handle errors and return conversion result
        pass
```

#### 3.2 Custom Tools via MCP

**Model Context Protocol (MCP)** allows tools to be exposed as reusable services across multiple agents through a lightweight server architecture.

**Advantages:**
- Decouple tools from specific agent implementations
- Share tools across multiple crews and workflows
- Simplify tool management and updates
- Enable tool discovery and versioning

**Architecture:**
1. Define tool logic with `@mcp.tool()` decorator
2. Start MCP server (e.g., `http://localhost:8081/sse`)
3. Connect agents using `MCPServerAdapter`
4. Agents call remote tools transparently

**Use Case:** Centralized currency conversion service accessible to any agent across the organization.

### 4. Cooperation

**Purpose:** Enable multi-agent collaboration for improved results.

**Key Principle:** Specialized agents working together produce smarter, more accurate outcomes than single agents.

**Example: Financial Analysis System**
- Data Gathering Agent → Collects market data
- Risk Assessment Agent → Evaluates risk factors
- Strategy Agent → Develops investment strategy
- Report Writer Agent → Generates comprehensive report

**Best Practice:** Design workflows where agents exchange insights and refine responses collaboratively.

### 5. Guardrails

**Purpose:** Maintain agent reliability and prevent uncontrolled behavior.

**Key Principle:** Without constraints, agents can hallucinate, loop endlessly, or make poor decisions.

**Essential Guardrails:**
- **Tool Usage Limits:** Prevent API overuse or irrelevant queries
- **Validation Checkpoints:** Ensure outputs meet predefined criteria
- **Fallback Mechanisms:** Allow human intervention or alternative agents when tasks fail
- **Output Constraints:** Enforce format, length, and content restrictions

**Example:** Legal assistant guardrails prevent outdated law citations and false claims.

### 6. Memory

**Purpose:** Enable agents to learn from interactions and maintain context over time.

**Key Principle:** Without memory, agents start fresh each interaction, losing all context.

**Memory Types:**

| Type | Scope | Use Case |
|------|-------|----------|
| **Short-term Memory** | Current execution only | Recalling recent conversation history |
| **Long-term Memory** | Persists across sessions | Remembering user preferences over time |
| **Entity Memory** | Stores key subjects | Tracking customer details in CRM systems |

**Example:** AI tutoring system uses memory to recall past lessons, tailor feedback, and avoid repetition.

---

## Design Patterns

Five primary design patterns enable sophisticated agentic behaviors through self-evaluation, planning, and collaboration:

### 1. Reflection Pattern

**Mechanism:** Agent reviews its own output to identify mistakes and iterate.

**Process:**
1. Generate initial response
2. Self-evaluate for errors or gaps
3. Refine and regenerate
4. Repeat until satisfactory

**Benefit:** Improves output quality through self-correction.

### 2. Tool Use Pattern

**Mechanism:** Agent leverages external tools to gather information beyond training data.

**Capabilities:**
- Query [[Vector Database|vector databases]]
- Execute Python scripts
- Invoke [[API|APIs]]
- Access external systems

**Benefit:** Overcomes LLM limitations regarding real-time information and specialized computations.

### 3. ReAct (Reason and Act) Pattern

**Mechanism:** Combines reflection and tool use