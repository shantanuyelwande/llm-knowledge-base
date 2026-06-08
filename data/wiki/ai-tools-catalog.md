---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-08T06:48:47.178877
raw_file_updated: 2026-06-08T06:48:47.178877
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-08T06:48:47.178877
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support [[artificial-intelligence|AI]] development, deployment, and operations. This catalog organizes over 300+ tools across 10 functional categories, from [[agent-memory|memory systems]] to [[model-inference|inference engines]], providing developers and organizations with a structured reference for building production-grade AI applications.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol|MCP & Data Tools]] | 19 | LLM-to-external-system connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Model Serving & Inference]] | 17 | Deployment and fine-tuning infrastructure |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Purpose

Systems for long-term persistence, state management, and semantic recall for [[AI-agents|agents]]. These tools enable [[language-models|language models]] and autonomous agents to maintain context across multiple sessions and interactions.

### Use Cases

- Agents that need to "remember" user preferences across sessions
- Maintaining codebase context for code-aware AI assistants
- Building conversational systems with persistent user profiles
- Semantic recall of relevant information from large knowledge bases

### Key Concepts

- **Long-term Memory:** Persistent storage of agent interactions and learned patterns
- **State Management:** Tracking agent status and context between invocations
- **Semantic Search:** Finding relevant historical information through meaning-based retrieval

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Purpose

Logic engines that manage [[multi-agent-systems|multi-agent]] planning, execution, and collaboration. These frameworks provide the orchestration layer for complex, multi-step [[AI-workflows|workflows]].

### Use Cases

- Complex workflows where single-agent solutions are insufficient
- Multi-agent collaboration on specialized subtasks
- Dynamic planning and task decomposition
- Hierarchical control structures for autonomous systems

### Key Concepts

- **Task Decomposition:** Breaking complex problems into manageable sub-tasks
- **Agent Collaboration:** Coordinating multiple specialized agents
- **Workflow Orchestration:** Managing execution flow and dependencies

---

## 3. Model Context Protocol & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Purpose

Standardized protocols and integrations for connecting [[language-models|LLMs]] to external data sources, APIs, and local machine tools. The [[Model Context Protocol|MCP]] enables seamless data exchange between models and their operating environment.

### Use Cases

- Bridging the gap between models and local file systems
- Connecting to specialized databases and data sources
- Integrating with third-party APIs and services
- Enabling agents to access real-time information

### Key Concepts

- **Model Context Protocol (MCP):** Open standard for LLM-to-tool communication
- **Tool Integration:** Connecting external services and data sources
- **API Abstraction:** Standardized interfaces for diverse data sources

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Purpose

Ingestion pipelines and vector databases that transform unstructured documents (PDFs, videos, websites) into searchable, semantically meaningful [[vector-embeddings|vector representations]]. Core infrastructure for [[Retrieval-Augmented Generation|RAG]] systems.

### Use Cases

- Building "Chat with Your Docs" features
- Creating searchable knowledge bases from diverse document types
- Extracting structured data from unstructured sources
- Enabling semantic search across document collections

### Key Concepts

- **[[Document Parsing]]:** Converting PDFs and complex formats to processable text
- **[[Vector Embeddings]]:** Transforming text into semantic vector representations
- **[[Vector Databases]]:** Storing and querying high-dimensional vectors efficiently
- **[[Retrieval-Augmented Generation|RAG]]:** Combining retrieval and generation for grounded responses

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Purpose

Tooling that enables [[AI-agents|agents]] to interact with user interfaces, click buttons, navigate websites, and perform tasks like humans. Bridges the gap between AI models and graphical interfaces.

### Use Cases

- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Testing and quality assurance automation
- Web scraping and information extraction
- End-to-end workflow automation

### Key Concepts

- **[[UI Automation]]:** Programmatic interaction with graphical interfaces
- **[[Browser Control]]:** Remote control of web browsers
- **[[Vision-Language Models]]:** Using visual understanding to navigate UIs
- **[[Computer Vision]]:** Screen parsing and element detection

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Purpose

Comprehensive testing, monitoring, and security infrastructure for [[language-models|LLM]]