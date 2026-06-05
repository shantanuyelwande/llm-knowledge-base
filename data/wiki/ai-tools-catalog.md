---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-05T06:28:22.517902
raw_file_updated: 2026-06-05T06:28:22.517902
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-05T06:28:22.517902
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software solutions and frameworks designed to support artificial intelligence development, deployment, and operations. This catalog organizes over 300+ tools across ten functional categories, enabling developers and organizations to build, evaluate, and scale AI systems effectively.

## Quick Reference

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol-based data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal generation and processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## Categories

### 1. Agent Memory & Context

**Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[Intelligent Agents|agents]].

**Use Cases:**
- Maintaining user preferences across multiple sessions
- Storing and retrieving codebase context for code-aware agents
- Building contextual awareness into [[Large Language Models|LLM]]-based applications
- Implementing episodic and semantic memory for autonomous agents

**Key Concepts:** [[Memory Systems]], [[State Management]], [[Semantic Search]], [[Agent Architecture]]

---

### 2. Agent Orchestration & Frameworks

**Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Use Cases:**
- Orchestrating complex workflows requiring multiple decision points
- Coordinating multiple [[Intelligent Agents]] working toward shared objectives
- Building agentic systems with planning and reasoning capabilities
- Creating visual workflows for non-technical users

**Key Concepts:** [[Agent Frameworks]], [[Workflow Orchestration]], [[Multi-Agent Systems]], [[Task Planning]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Count:** 19 tools

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data sources and local machine tools.

**Use Cases:**
- Bridging LLMs with local file systems and databases
- Creating standardized interfaces for tool access
- Integrating third-party APIs and services
- Enabling structured data access for AI applications

**Key Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[Data Access]], [[API Standards]]

---

### 4. RAG & Document Processing

**Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable vector representations.

**Use Cases:**
- Building "Chat with your Docs" features
- Processing multi-format documents at scale
- Creating searchable knowledge bases
- Implementing semantic search over custom data
- Video content understanding and retrieval

**Key Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Parsing]], [[Semantic Search]], [[Embedding Models]]

---

### 5. Computer Use & Browser Automation

**Count:** 20 tools

**Key Tools:** Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Tools enabling agents to interact with user interfaces, click buttons, and navigate the web autonomously.

**Use Cases:**
- Automated web research and data collection
- Testing and quality assurance automation
- Human-in-the-loop UI task automation
- Web scraping and content extraction
- Cross-platform UI interaction

**Key Concepts:** [[Browser Automation]], [[UI Interaction]], [[Web Agents]], [[RPA]], [[Computer Vision]]

---

### 6. Evaluation, Security & Ops

**Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**Purpose:** Testing, monitoring, and securing [[Large Language Models|LLM]] outputs to prevent hallucinations, biases, and information leaks.

**Use Cases:**
- Evaluating model performance across benchmarks
- Monitoring production AI systems
- Red teaming and adversarial testing
- Detecting and preventing hallucinations
- Compliance and safety verification
- Cost and latency optimization

**Key Concepts:** [[LLM Evaluation]], [[Model Monitoring]], [[Security Testing]], [[Observability]], [[Benchmarking]], [[Hallucination Detection]]

---

### 7. Developer Tools & IDEs

**Count:** 22 tools

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments and IDEs that accelerate code writing and repository management.

**Use Cases:**
- Real-time code generation and completion
- Intelligent code review and refactoring
- Repository-aware development assistance
- Multi-modal code interaction (text and visual)
- Git workflow automation

**Key Concepts:** [[AI-Assisted Development]], [[Code Generation]], [[IDE Integration]], [[Developer Experience]], [[Repository Understanding]]

---