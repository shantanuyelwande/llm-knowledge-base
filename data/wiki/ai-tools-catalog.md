---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-07T05:36:02.319886
raw_file_updated: 2026-05-07T05:36:02.319886
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-07T05:36:02.319886
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software platforms and libraries designed to support the development, deployment, and management of artificial intelligence applications. This catalog organizes over 300+ tools across ten distinct categories, each addressing specific challenges in the AI development lifecycle—from agent memory management to production-grade monitoring and security.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and multi-agent workflows |
| [[Model Context Protocol & Data Tools]] | 19 | LLM-to-data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Operations]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and cross-cutting concerns |

---

## 1. Agent Memory & Context

**Tool Count:** 18

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for [[long-term persistence]], [[state management]], and [[semantic recall]] for [[AI agents]].

**When to Use:** 
- Agents need to "remember" user preferences across sessions
- Building context-aware systems that reference previous interactions
- Maintaining codebase context for code-generating agents
- Implementing semantic search over agent interaction history

**Key Concepts:**
- [[Persistent Memory]] - Storing and retrieving agent state over time
- [[Semantic Recall]] - Finding relevant past interactions using meaning rather than exact matching
- [[Session Management]] - Maintaining agent state across conversation boundaries

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage [[multi-step planning]] and [[multi-agent collaboration]].

**When to Use:**
- Complex workflows where a single "brain" is insufficient
- Building systems where multiple agents must coordinate
- Implementing sequential decision-making processes
- Creating visual workflow builders for non-technical users

**Key Concepts:**
- [[Multi-Agent Systems]] - Coordinating multiple independent agents
- [[Workflow Orchestration]] - Managing task sequences and dependencies
- [[Agent Planning]] - Strategic reasoning about multi-step problem solving
- [[Low-Code Automation]] - Visual tools for workflow definition (n8n, Langflow, Flowise)

---

## 3. Model Context Protocol & Data Tools

**Tool Count:** 19

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[LLMs]] to [[external data sources]] and [[local machine tools]].

**When to Use:**
- Bridging the gap between AI models and local file systems
- Integrating with specific databases or APIs
- Standardizing tool access across different [[LLM]] providers
- Building extensible AI applications with plugin architectures

**Key Concepts:**
- [[Model Context Protocol]] - Standardized interface for LLM-to-tool communication
- [[Tool Integration]] - Connecting external services and data sources
- [[Data Connectivity]] - Providing LLMs access to real-time information
- [[Plugin Architecture]] - Extensible systems for adding new capabilities

---

## 4. RAG & Document Processing

**Tool Count:** 24

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Purpose:** [[Ingestion pipelines]] that transform messy PDFs, videos, and websites into searchable [[vector embeddings]].

**When to Use:**
- Building "Chat with your Docs" features
- Creating knowledge bases from unstructured documents
- Implementing semantic search over large document collections
- Processing video content for retrieval-augmented generation

**Key Concepts:**
- [[Retrieval-Augmented Generation (RAG)]] - Combining document retrieval with generation
- [[Document Parsing]] - Converting PDFs and web content into structured text
- [[Vector Embeddings]] - Representing documents as numerical vectors for semantic search
- [[Vector Databases]] - Storing and querying embeddings (QDrant, Milvus, ChromaDB, pgVector)
- [[Semantic Search]] - Finding relevant documents by meaning rather than keywords

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Enabling [[AI agents]] to interact with [[user interfaces]], click buttons, and navigate the web like a human.

**When to Use:**
- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Testing web applications at scale
- Building agents that can operate existing web applications without APIs

**Key Concepts:**
- [[UI Automation]] - Programmatic interaction with graphical interfaces
- [[Web Scraping]] - Extracting data from websites
- [[Browser Control]] - Remote operation of web browsers
- [[Visual Understanding]] - Interpreting page layouts and identifying clickable elements
- [[Human-Like Interaction]] - Mimicking natural user behavior patterns

---

## 6. Evaluation, Security & Operations

**Tool Count:** 28

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent [[hallucinations]] and [[data leaks]].

**When to Use:**
- Production-grade AI systems requiring safety guarantees
- Continuous monitoring of model performance in production
- Red-teaming and adversarial testing of