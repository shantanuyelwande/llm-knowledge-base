---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:52:28.959810
raw_file_updated: 2026-04-24T18:52:28.959810
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:52:28.959810
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support the development, deployment, and operation of artificial intelligence systems. This catalog organizes over 300+ tools across ten functional categories, ranging from [[agent memory]] systems to voice and vision models. It serves as a reference guide for developers, AI engineers, and organizations building production-grade AI applications.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP (Model Context Protocol)]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and security |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Categories

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- Maintaining [[codebase context]] for long-running development tasks
- Building persistent [[conversational AI]] systems
- Managing state in multi-turn interactions

**Key Concept:** [[Memory Management]] in AI systems enables continuity and personalization without retraining.

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Use Cases:**
- Complex workflows requiring multiple specialized agents
- Multi-agent collaboration and communication
- Workflow automation and orchestration
- Building [[agentic systems]] with specialized capabilities

**Key Concept:** [[Agent Orchestration]] distributes complex tasks across specialized agents for improved modularity and scalability.

---

### 3. MCP (Model Context Protocol) & Data Tools

**Purpose:** Standardized protocols for connecting [[Large Language Models|LLMs]] to external data and local machine tools.

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging the gap between models and local file systems
- Connecting LLMs to specific databases
- Standardizing tool integration across platforms
- Enabling consistent [[tool use]] patterns

**Key Concept:** [[Model Context Protocol]] provides a standardized interface for LLMs to access external tools and data sources.

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation]].

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Use Cases:**
- Building "Chat with your Docs" features
- Processing multi-format documents (PDFs, videos, websites)
- Creating [[semantic search]] capabilities
- Implementing [[vector databases]] for efficient retrieval

**Key Concept:** [[RAG]] systems augment LLM responses with retrieved contextual information, improving accuracy and relevance.

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing agents to interact with UIs, click buttons, and navigate the web like a human.

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Use Cases:**
- Automated web research and data extraction
- "Human-in-the-loop" UI task automation
- Web scraping and content aggregation
- Testing and validation workflows

**Key Concept:** [[Computer Vision]] combined with [[browser automation]] enables agents to navigate and interact with web interfaces autonomously.

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, leaks, and ensure reliability.

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Use Cases:**
- Production-grade safety and reliability assurance
- [[Red teaming]] and adversarial testing
- Monitoring and observability for deployed models
- Evaluating model performance across benchmarks
- Preventing [[hallucinations]] and data leaks

**Key Concept:** [[LLM Evaluation]] frameworks provide systematic approaches to measure model quality, safety, and alignment.

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented environments for faster code writing, completion, and repository management.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Use Cases:**
- Accelerating daily development workflows
- Intelligent code completion and generation
- Repository understanding and navigation
- Documentation generation and management
- AI-assisted debugging and refactoring

**Key Concept:** [[AI-Assisted Development]] tools integrate [[code generation]] capabilities directly into developer workflows.

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Key Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs, Murfai,