---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-16T16:56:24.075556
raw_file_updated: 2026-04-16T16:56:24.075556
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-16T16:56:24.075556
tags: ["AI Tools", "Machine Learning", "Developer Resources", "Catalog", "Framework Reference"]
related_topics: []
backlinked_by: []

---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for artificial intelligence development tools and platforms. It organizes over 300+ AI/ML tools across 10 primary functional categories, designed to help developers, engineers, and organizations identify the right solutions for their specific use cases.

This catalog serves as a reference guide for building [[AI applications]], from initial development through production deployment, covering memory systems, orchestration frameworks, data processing, and operational infrastructure.

## Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code generation and development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## Categories

### 1. Agent Memory & Context

**Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Description:** Systems designed for long-term persistence, state management, and semantic recall capabilities within [[AI agents]]. These tools enable agents to maintain context across multiple sessions and interactions.

**Primary Use Cases:**
- Remembering user preferences across conversations
- Maintaining codebase context for code-aware agents
- Building persistent knowledge bases for agent systems
- Implementing semantic search over historical interactions

**When to Use:** Select these tools when your [[AI agent]] needs to retain and recall information beyond a single conversation, or when you require sophisticated context management for multi-session interactions.

---

### 2. Agent Orchestration & Frameworks

**Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Description:** Logic engines that coordinate multi-step planning, task decomposition, and multi-agent collaboration. These frameworks provide the orchestration layer for complex [[AI workflows]].

**Primary Use Cases:**
- Coordinating multiple specialized agents
- Breaking down complex tasks into subtasks
- Managing dependencies between workflow steps
- Building no-code or low-code agent applications
- Implementing [[agent communication]] patterns

**When to Use:** Deploy these frameworks when your application requires sophisticated workflow management or when a single [[LLM]] cannot handle the complete problem scope. Essential for [[multi-agent systems]].

---

### 3. MCP (Model Context Protocol) & Data Tools

**Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Description:** Standardized protocols and tools for connecting [[language models]] to external data sources, local machine tools, and third-party services. These implement the [[Model Context Protocol]] specification.

**Primary Use Cases:**
- Connecting models to local file systems
- Integrating with specialized databases
- Accessing third-party APIs and services
- Enabling tool use and function calling
- Creating standardized tool interfaces

**When to Use:** Implement [[MCP]] when you need to bridge the gap between your [[LLM]] and external systems in a standardized, maintainable way.

---

### 4. RAG & Document Processing

**Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Description:** End-to-end ingestion pipelines that transform unstructured documents (PDFs, videos, websites, images) into searchable vector embeddings. These tools implement [[Retrieval-Augmented Generation]] (RAG) patterns.

**Primary Use Cases:**
- Building "Chat with your Docs" applications
- Creating searchable document repositories
- Processing multi-modal content (text, images, video)
- Implementing semantic search over document collections
- Creating knowledge bases from enterprise documents

**When to Use:** Essential for any application requiring the model to reference external documents or proprietary knowledge bases. Core component of [[RAG systems]].

---

### 5. Computer Use & Browser Automation

**Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Description:** Tools enabling [[AI agents]] to interact with graphical user interfaces, click buttons, fill forms, and navigate the web autonomously. These implement [[computer vision]] and [[UI automation]] capabilities.

**Primary Use Cases:**
- Automated web research and data collection
- Cross-website form filling and submission
- Testing web applications
- Implementing human-in-the-loop UI tasks
- Building autonomous web scraping agents

**When to Use:** Deploy when your application requires agents to interact with systems not providing programmatic APIs, or when you need human-like web interaction capabilities.

---

### 6. Evaluation, Security & Ops

**Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Description:** Comprehensive platforms for testing, monitoring, securing, and evaluating [[LLM]] outputs in production. These tools prevent [[hallucinations]], detect security vulnerabilities, and ensure reliability.

**Primary Use Cases:**
- Implementing [[prompt injection]] detection
- Monitoring model performance in production
- Conducting [[red teaming]] exercises
- Measuring [[hallucination]] rates
- Tracking model behavior changes over time
- Implementing [[guardrails]] for safe outputs

**When to Use:** Essential for any production-grade [[AI application]]. These tools are critical for maintaining safety, reliability, and compliance standards.

---

### 7. Developer Tools & IDEs

**Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx,