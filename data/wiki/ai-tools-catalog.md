---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-28T05:34:51.656322
raw_file_updated: 2026-04-28T05:34:51.656322
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-28T05:34:51.656322
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive reference guide organizing artificial intelligence development tools and platforms across ten major functional categories. This catalog serves as a resource for developers, engineers, and organizations building AI-powered applications, from simple chatbots to complex multi-agent systems.

The catalog encompasses over 300 tools spanning [[agent memory systems]], [[orchestration frameworks]], [[data processing]], [[security]], and [[infrastructure]], providing a structured approach to understanding the AI development ecosystem.

---

## Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term state persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and multi-agent coordination |
| [[Model Context Protocol (MCP)]] | 19 | LLM integration with external data and tools |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and LLM safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## 1. Agent Memory & Context

### Description
Systems designed for long-term persistence, state management, and semantic recall for [[AI agents]]. These tools enable agents to maintain context across multiple sessions and interactions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Remembering user preferences across sessions
- Maintaining [[codebase context]] for development agents
- Building persistent knowledge bases for virtual assistants
- Semantic recall of historical interactions

### Key Concepts
- [[State Management]]
- [[Semantic Search]]
- [[Persistent Memory]]

---

## 2. Agent Orchestration & Frameworks

### Description
Logic engines that manage multi-step planning and [[multi-agent collaboration]]. These frameworks provide the backbone for coordinating complex workflows where multiple AI agents or components work together.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple specialized agents
- Coordinating parallel and sequential task execution
- Building [[agentic workflows]] with branching logic
- Managing agent communication and handoffs

### Key Concepts
- [[Workflow Automation]]
- [[Multi-Agent Systems]]
- [[Task Planning]]
- [[Agent Communication]]

---

## 3. Model Context Protocol (MCP) & Data Tools

### Description
Standardized protocols for connecting [[large language models]] to external data sources and local machine tools. MCP establishes a unified interface for bridging models and their operating environment.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Connecting models to local file systems
- Accessing specific databases and data sources
- Integrating with external APIs and services
- Standardizing tool interfaces for model interaction

### Key Concepts
- [[Model Context Protocol]]
- [[Tool Integration]]
- [[Data Connectivity]]
- [[API Integration]]

---

## 4. RAG & Document Processing

### Description
Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable [[vector embeddings]]. These tools are essential for building [[retrieval-augmented generation]] systems and document-based AI applications.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Converting unstructured documents into searchable knowledge bases
- Processing video content for semantic understanding
- Creating domain-specific knowledge repositories

### Key Concepts
- [[Retrieval-Augmented Generation (RAG)]]
- [[Vector Databases]]
- [[Document Parsing]]
- [[Semantic Search]]
- [[Embeddings]]

---

## 5. Computer Use & Browser Automation

### Description
Tools enabling [[AI agents]] to interact with user interfaces, click buttons, and navigate the web autonomously. These systems allow agents to perform tasks that typically require human interaction.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Testing and quality assurance automation
- Web scraping and information extraction
- Automated form filling and data entry

### Key Concepts
- [[Browser Automation]]
- [[UI Automation]]
- [[Web Scraping]]
- [[Agent Autonomy]]

---

## 6. Evaluation, Security & Ops

### Description
Comprehensive testing, monitoring, and security tools for [[LLM applications]]. These platforms ensure that AI outputs are safe, reliable, and production-ready while preventing hallucinations and data leaks.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Detecting and preventing [[hallucinations]]
- Monitoring model performance in production
- [[Red teaming]] and adversarial testing
- Evaluating [[model quality]] and accuracy
- Ensuring data privacy and preventing leaks
- Compliance and audit logging

### Key Concepts
- [[LLM Evaluation]]
- [[Model Monitoring]]
- [[Security & Safety]]
- [[Red Teaming]]
- [[Hallucination Detection]]

---

## 7. Developer Tools & IDEs

### Description
AI-augmented development environments that accelerate code writing, repository management, and software development workflows. These tools integrate [[large language models]] directly into developer workflows.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github