---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-25T04:39:56.717539
raw_file_updated: 2026-04-25T04:39:56.717539
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-25T04:39:56.717539
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software solutions and frameworks designed to support the development, deployment, and management of artificial intelligence systems. This catalog organizes over 300 tools across ten functional categories, each addressing specific aspects of the AI development lifecycle—from agent memory and orchestration to evaluation, security, and inference optimization.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol (MCP) & Data Tools]] | 19 | LLM integration with external data |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Operations]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General Tools]] | 36 | Workflow automation and utilities |

---

## 1. Agent Memory & Context

### Purpose
Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Enabling agents to "remember" user preferences across sessions
- Maintaining codebase context in long-running development tasks
- Building persistent state for conversational AI systems
- Semantic recall of historical interactions and patterns

### When to Use
Use when agents need continuous context awareness and must reference past interactions or accumulated knowledge without reprocessing original data.

---

## 2. Agent Orchestration & Frameworks

### Purpose
Logic engines that manage multi-step planning and multi-agent collaboration.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Coordinating multiple specialized agents on complex tasks
- Building agentic workflows with branching logic and feedback loops
- Creating no-code/low-code agent applications
- Implementing tool-use chains and reasoning loops

### When to Use
Complex workflows where a single "brain" isn't sufficient, requiring delegation, tool selection, and inter-agent communication.

---

## 3. Model Context Protocol (MCP) & Data Tools

### Purpose
Standardized protocols for connecting [[Large Language Models (LLMs)]] to external data sources and local machine tools.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging LLMs and local file systems
- Integrating with specialized databases and APIs
- Standardizing tool definitions across multiple AI platforms
- Creating composable data pipelines

### When to Use
When you need standardized, reliable integration between your model and external data sources or tools without custom middleware.

---

## 4. RAG & Document Processing

### Purpose
Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation (RAG)]].

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Converting unstructured documents into queryable embeddings
- Video and image content indexing
- Multi-format document ingestion (PDF, web, video, images)

### When to Use
When building knowledge-grounded AI systems that need to search and reference proprietary or domain-specific documents.

---

## 5. Computer Use & Browser Automation

### Purpose
Allowing [[AI agents]] to interact with user interfaces, click buttons, and navigate the web like a human.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and data extraction
- "Human-in-the-loop" UI task automation
- Testing web applications at scale
- Scraping and monitoring web content

### When to Use
When you need agents to perform tasks in environments designed for human interaction, or to automate complex web-based workflows.

---

## 6. Evaluation, Security & Operations

### Purpose
Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, security breaches, and reliability issues.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Red-teaming and adversarial testing
- Monitoring model drift and performance degradation
- Evaluating output quality with standardized benchmarks
- Implementing guardrails against harmful outputs
- Tracing and debugging agent behavior

### When to Use
Essential for production-grade AI systems to ensure safety, reliability, and compliance with organizational standards.

---

## 7. Developer Tools & IDEs

### Purpose
AI-augmented development environments for faster code writing and repository management.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

### Use Cases
- AI-assisted code generation and completion
- Intelligent code review and refactoring
- Repository understanding and navigation
- Real-time coding assistance
- Documentation generation

### When to Use
In your daily development cycle to accelerate coding, reduce boilerplate, and improve code quality.

---

## 8. Voice & Vision Models

### Purpose
Multi-modal tools for generating and processing audio, images, and video content.

### Key Tools
Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs,