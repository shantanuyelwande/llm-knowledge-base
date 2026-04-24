---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T04:58:21.919375
raw_file_updated: 2026-04-24T04:58:21.919375
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T04:58:21.919375
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support [[artificial-intelligence]] development, deployment, and management. This catalog organizes over 300+ tools across 10 functional categories, providing developers and AI practitioners with a structured reference for building, orchestrating, and operating intelligent systems.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web navigation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented coding environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Purpose

Systems designed for long-term persistence, state management, and semantic recall for [[AI agents]]. These tools enable agents to maintain contextual information across multiple sessions and interactions.

### When to Use

- Agents need to "remember" user preferences across sessions
- Maintaining codebase context for code-generation tasks
- Building persistent user profiles for personalized interactions
- Semantic recall of historical information for decision-making

### Key Concepts

- [[Persistent State Management]]
- [[Semantic Memory]]
- [[Agent Context]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Purpose

Logic engines that manage multi-step planning, task decomposition, and multi-agent collaboration. These frameworks provide the orchestration layer for complex AI workflows.

### When to Use

- Complex workflows requiring multiple reasoning steps
- Multi-agent systems where coordination is essential
- Building production-grade AI applications
- Implementing hierarchical task planning

### Key Concepts

- [[Multi-Agent Systems]]
- [[Workflow Orchestration]]
- [[Task Decomposition]]
- [[Agent Planning]]

---

## 3. MCP (Model Context Protocol) & Data Tools

**Tool Count:** 19

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Purpose

Standardized protocols for connecting [[large language models]] to external data sources, local machine tools, and specialized services. The [[Model Context Protocol]] (MCP) enables seamless integration between AI systems and external resources.

### When to Use

- Bridging the gap between models and local file systems
- Accessing specialized databases and data sources
- Integrating with third-party APIs and services
- Enabling real-time data access for AI agents

### Key Concepts

- [[Model Context Protocol]]
- [[Tool Integration]]
- [[Data Connectivity]]
- [[API Integration]]

---

## 4. RAG & Document Processing

**Tool Count:** 24

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Purpose

Ingestion pipelines that transform unstructured data (PDFs, videos, websites, images) into searchable vector embeddings. These tools are essential for [[Retrieval-Augmented Generation]] (RAG) systems.

### When to Use

- Building "Chat with Your Documents" features
- Creating searchable knowledge bases
- Processing multi-format documents at scale
- Implementing semantic search over custom data
- Video and image content analysis

### Key Concepts

- [[Retrieval-Augmented Generation]]
- [[Vector Embeddings]]
- [[Document Ingestion]]
- [[Semantic Search]]
- [[Vector Databases]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20

**Key Tools:** Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Purpose

Tools enabling [[AI agents]] to interact with graphical user interfaces, click buttons, fill forms, and navigate the web autonomously. These systems bridge the gap between AI capabilities and human-oriented interfaces.

### When to Use

- Automated web research and information gathering
- Robotic process automation (RPA) tasks
- Testing web applications
- Human-in-the-loop UI automation
- Autonomous web navigation and interaction

### Key Concepts

- [[Computer Vision]]
- [[UI Automation]]
- [[Web Scraping]]
- [[Robotic Process Automation]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Purpose

Testing, monitoring, evaluation, and security frameworks for [[large language models]] and AI systems. These tools prevent [[hallucinations]], detect security vulnerabilities, and ensure production reliability.

### When to Use

- Production-grade AI deployment
- Red-teaming and adversarial testing
- Continuous monitoring of model outputs
- Compliance and safety verification
- Performance benchmarking

### Key Concepts

- [[Model Evaluation]]
- [[Hallucination Detection]]
- [[AI Safety]]
- [[Monitoring & Observability]]
- [[Red Teaming]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project Idx, Lightning AI, RooCode, Chaoscoder.net