---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-09T06:14:26.771288
raw_file_updated: 2026-06-09T06:14:26.771288
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-09T06:14:26.771288
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive directory of software tools and frameworks designed to support the development, deployment, and operation of artificial intelligence systems. This catalog organizes over 300+ tools across 10 functional categories, enabling developers and organizations to build sophisticated AI applications with specialized components for memory management, agent orchestration, data processing, security, and infrastructure.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

### Description
Systems for long-term persistence, state management, and semantic recall for [[AI agents]]. These tools enable AI systems to maintain context across multiple sessions and interactions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Maintaining user preferences across conversation sessions
- Preserving [[codebase context]] for development agents
- Building persistent state for long-running AI applications
- Implementing semantic memory retrieval systems

### Related Concepts
[[Agent Orchestration & Frameworks]], [[RAG & Document Processing]], [[LLM Context Management]]

---

## 2. Agent Orchestration & Frameworks

### Description
Logic engines that manage multi-step planning and multi-agent collaboration. These frameworks provide the foundational architecture for coordinating complex AI workflows where multiple specialized agents work together.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Orchestrating multi-agent systems for complex problem-solving
- Building no-code/low-code AI workflow platforms
- Creating [[agentic workflows]] with dependency management
- Implementing tool-use chains and reasoning loops

### Related Concepts
[[AI Agents]], [[Workflow Automation]], [[Multi-Agent Systems]], [[LLM Frameworks]]

---

## 3. MCP (Model Context Protocol) & Data Tools

### Description
Standardized protocols and tools for connecting [[Large Language Models]] to external data sources and local machine tools. The [[Model Context Protocol]] (MCP) provides a unified interface for [[LLM integration]] with diverse data systems.

### Key Tools
Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging [[LLM]] capabilities with local file systems
- Integrating specialized databases with AI systems
- Creating standardized tool interfaces for model access
- Connecting 3D modeling, data generation, and custom tools

### Related Concepts
[[Model Context Protocol]], [[Tool Use]], [[Data Integration]], [[API Integration]]

---

## 4. RAG & Document Processing

### Description
Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable vector representations. [[Retrieval-Augmented Generation]] (RAG) tools enable AI systems to reference external knowledge bases accurately.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral OCR, GroundX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" applications
- Processing complex document formats (PDFs, tables, images)
- Creating searchable knowledge bases from unstructured content
- Implementing semantic search across video content
- Evaluating RAG system performance

### Related Concepts
[[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Processing]], [[Semantic Search]], [[Embeddings]]

---

## 5. Computer Use & Browser Automation

### Description
Tools enabling [[AI agents]] to interact with graphical user interfaces, click buttons, navigate websites, and perform tasks like humans. These tools bridge the gap between AI systems and web-based workflows.

### Key Tools
Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automating web research and data gathering
- Implementing "human-in-the-loop" UI task automation
- Building web scraping agents with visual understanding
- Creating robotic process automation (RPA) systems
- Testing web applications through automated interaction

### Related Concepts
[[Browser Automation]], [[Computer Vision]], [[UI Automation]], [[Web Scraping]], [[Robotic Process Automation]]

---

## 6. Evaluation, Security & Ops

### Description
Tools for testing, monitoring, and securing [[LLM]] outputs in production environments. These systems prevent [[hallucinations]], detect security vulnerabilities, and ensure reliability and safety.

### Key Tools
Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Use Cases
- Implementing [[LLM evaluation]] frameworks
- Monitoring model outputs for hallucinations and bias
- Conducting security testing and red-teaming
- Tracking [[LLM observability]] metrics
- Ensuring compliance and safety in production
- Benchmarking model performance

### Related Concepts
[[LLM Evaluation]], [[Model Monitoring]], [[AI Safety]], [[Hallucination Detection]], [[Red Teaming]], [[Observability]]

---

## 7. Developer Tools & IDEs

### Description
AI-augmented integrated development environments and tools that accelerate code writing, repository navigation, and software development workflows through [[AI-assisted coding]].

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Ta