---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-19T04:54:29.790339
raw_file_updated: 2026-04-19T04:54:29.790339
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-19T04:54:29.790339
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and frameworks designed to support artificial intelligence development, deployment, and management. This catalog organizes over 300+ tools across 10 major categories, enabling developers and organizations to build production-grade AI systems with proper infrastructure for memory, orchestration, data handling, security, and monitoring.

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
| [[Voice & Vision Models]] | 21 | Multi-modal AI capabilities |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and deployment |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Purpose**: Systems for long-term persistence, state management, and semantic recall for agents.

**Key Tools**: Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**When to Use**: 
- Agents need to "remember" user preferences across sessions
- Maintaining [[codebase context]] for code-aware AI systems
- Building conversational systems with long-term user understanding
- Implementing semantic recall from large knowledge bases

**Related Concepts**: [[Vector embeddings]], [[Semantic search]], [[State management]]

---

## 2. Agent Orchestration & Frameworks

**Purpose**: Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools**: Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**When to Use**:
- Complex workflows where one "brain" isn't enough
- Coordinating multiple specialized agents
- Building [[agentic workflows]] with branching logic
- Implementing task decomposition and parallel execution
- Creating no-code or low-code AI applications

**Related Concepts**: [[Multi-agent systems]], [[Workflow automation]], [[Task planning]]

---

## 3. MCP (Model Context Protocol) & Data Tools

**Purpose**: Standardized protocols for connecting [[Large Language Models|LLMs]] to external data and local machine tools.

**Key Tools**: Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**When to Use**:
- Bridging the gap between models and local file systems
- Connecting to specific databases or APIs
- Standardizing tool integrations across multiple LLM providers
- Building extensible AI systems with pluggable data sources
- Enabling [[function calling]] at scale

**Related Concepts**: [[API integration]], [[Data sources]], [[Tool use]]

---

## 4. RAG & Document Processing

**Purpose**: Ingestion pipelines that turn messy PDFs, videos, and websites into searchable vectors.

**Key Tools**: Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**When to Use**:
- Building "Chat with your Docs" features
- Processing unstructured documents at scale
- Creating [[Retrieval-Augmented Generation|RAG]] systems
- Ingesting video, audio, and image content
- Building searchable knowledge bases
- Implementing [[semantic search]] over document collections

**Related Concepts**: [[Vector databases]], [[Document parsing]], [[Embeddings]], [[Information retrieval]]

---

## 5. Computer Use & Browser Automation

**Purpose**: Allowing agents to interact with UIs, click buttons, and navigate the web like a human.

**Key Tools**: Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**When to Use**:
- Automated web research and data extraction
- "Human-in-the-loop" UI task automation
- Testing web applications
- Building web scraping agents
- Automating repetitive browser-based workflows
- Implementing [[visual understanding]] for UI interaction

**Related Concepts**: [[Web automation]], [[UI interaction]], [[Screen understanding]]

---

## 6. Evaluation, Security & Ops

**Purpose**: Testing, monitoring, and securing LLM outputs to prevent hallucinations and leaks.

**Key Tools**: Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**When to Use**:
- Essential for production-grade AI systems
- Ensuring safety and preventing [[hallucinations]]
- Monitoring model performance in production
- [[Red teaming]] and adversarial testing
- Compliance and audit requirements
- Detecting and preventing data leaks
- Benchmarking model quality

**Related Concepts**: [[Model evaluation]], [[Safety guardrails]], [[Observability]], [[Quality metrics]]

---

## 7. Developer Tools & IDEs

**Purpose**: AI-augmented environments for faster code writing and repository management.

**Key Tools**: Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**When to Use**:
- Daily development cycles
- Accelerating code writing and refactoring
- Repository understanding and navigation
- Pair programming with AI assistants
- Learning and code exploration
- Automated code generation and completion

**Related Concepts**: [[Code generation]], [[Developer productivity]], [[Pair programming]]

---

## 8. Voice & Vision Models

**Purpose**: Multi-modal tools for generating and processing audio, images, and video.

**Key Tools**: Veo2 (video), Landing AI (object detection), Super