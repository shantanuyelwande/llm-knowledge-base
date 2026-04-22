---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-22T04:50:26.983933
raw_file_updated: 2026-04-22T04:50:26.983933
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-22T04:50:26.983933
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system organizing modern artificial intelligence development tools into ten distinct categories. This catalog serves as a reference guide for developers, engineers, and organizations building AI-powered applications, covering everything from foundational [[agent memory]] systems to production-grade [[inference]] infrastructure.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and state management |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol (MCP)]] | 19 | External data and tool integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code generation and repository management |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and auxiliary functions |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

### Purpose
Systems designed to provide [[artificial intelligence|AI agents]] with long-term persistence, state management, and semantic recall capabilities. These tools enable agents to maintain context across multiple sessions and interactions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### When to Use
- Agents need to "remember" user preferences across sessions
- Maintaining [[codebase context]] for development agents
- Building personalized AI experiences with historical context
- Semantic recall of relevant information from past interactions

### Related Concepts
- [[Agent State Management]]
- [[Semantic Search]]
- [[User Preference Learning]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

### Purpose
Logic engines that manage multi-step planning and coordinate collaboration between multiple [[AI agents]]. These frameworks provide the foundational architecture for complex, distributed AI systems.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### When to Use
- Complex workflows requiring multiple specialized agents
- Multi-agent collaboration and communication
- Hierarchical task planning and execution
- Distributed reasoning across different domains

### Related Concepts
- [[Multi-Agent Systems]]
- [[Workflow Automation]]
- [[Agentic AI]]

---

## 3. Model Context Protocol (MCP) & Data Tools

**Tool Count:** 19 tools

### Purpose
Standardized protocols and tools that connect [[large language models|LLMs]] to external data sources, local machine tools, and specialized resources. These tools bridge the gap between model capabilities and real-world data access.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### When to Use
- Connecting models to local file systems
- Accessing specialized databases and APIs
- Integrating 3D modeling tools (Blender)
- Standardized tool integration across platforms

### Related Concepts
- [[Model Context Protocol]]
- [[Tool Integration]]
- [[API Integration]]
- [[Data Access Patterns]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

### Purpose
Ingestion and processing pipelines that convert unstructured documents—PDFs, videos, websites, and images—into searchable vector representations. These tools enable [[retrieval-augmented generation (RAG)]] applications.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### When to Use
- Building "Chat with your Docs" features
- Processing large document collections
- Video content analysis and indexing
- OCR and structured data extraction
- Creating searchable knowledge bases

### Related Concepts
- [[Retrieval-Augmented Generation (RAG)]]
- [[Vector Databases]]
- [[Document Parsing]]
- [[Semantic Search]]
- [[Embedding Models]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

### Purpose
Tools that enable [[AI agents]] to interact with user interfaces, click buttons, navigate websites, and perform human-like actions on computers. These create the bridge between AI reasoning and UI interaction.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### When to Use
- Automated web research and scraping
- "Human-in-the-loop" UI task automation
- Testing web applications
- Autonomous web navigation
- Accessibility automation

### Related Concepts
- [[Browser Automation]]
- [[Web Scraping]]
- [[UI Interaction]]
- [[Computer Vision]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

### Purpose
Comprehensive testing, monitoring, and security infrastructure for [[LLM]] outputs. These tools prevent hallucinations, detect leaks, and ensure production-grade reliability and safety.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### When to Use
- Production deployment of AI systems
- Monitoring [[LLM]] performance and safety
- Red-teaming and adversarial testing
- Quality assurance and benchmarking
- Compliance and security auditing

### Related Concepts
- [[LLM Safety]]
- [[Model Evaluation]]
- [[Hallucination Detection]]
- [[AI Security]]
- [[Observability]]
- [[Benchmarking]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

### Purpose
AI-augmented integrated development environments and tools that accelerate code writing, repository management, and software development workflows through intelligent assistance.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copil