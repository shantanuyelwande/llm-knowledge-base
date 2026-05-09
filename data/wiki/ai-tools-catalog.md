---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-09T05:25:26.476023
raw_file_updated: 2026-05-09T05:25:26.476023
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-09T05:25:26.476023
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ tools across 10 primary categories, enabling developers, researchers, and AI engineers to identify the right solutions for specific use cases in agent development, data processing, model serving, and deployment.

## Quick Summary

| Category | Tool Count | Primary Use |
|----------|-----------|------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP (Model Context Protocol)]] | 19 | Protocol standardization and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code generation and development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Categories

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Qodo aware, Repo Prompt, Claude context semantic search

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- Maintaining [[codebase context]] for code-aware AI systems
- Building persistent [[conversational AI]] with historical context
- Semantic recall systems for complex information retrieval

**Key Concepts:** [[State Management]], [[Semantic Search]], [[Context Window]], [[Agent Persistence]]

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Use Cases:**
- Complex workflows where multiple agents collaborate
- Multi-step [[reasoning]] and planning pipelines
- [[Workflow automation]] requiring conditional logic
- Distributed [[agent systems]] with task coordination

**Key Concepts:** [[Agent Architecture]], [[Multi-Agent Systems]], [[Workflow Orchestration]], [[Task Planning]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data and local machine tools.

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox, Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging the gap between LLMs and local file systems
- Connecting models to specific databases
- Standardized [[tool integration]] across platforms
- Real-time data access for AI applications

**Key Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[API Standardization]], [[Data Connectivity]]

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation]].

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai, LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Use Cases:**
- Building "Chat with your Docs" features
- Processing unstructured data from multiple sources
- Creating searchable knowledge bases
- [[Document understanding]] and extraction
- Video and multimedia content indexing

**Key Concepts:** [[Vector Databases]], [[Document Parsing]], [[Semantic Search]], [[Embedding Models]], [[RAG Systems]]

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing agents to interact with user interfaces, click buttons, and navigate the web like humans.

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use, Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Use Cases:**
- Automated web research and data collection
- "Human-in-the-loop" [[UI automation]] tasks
- Web scraping with AI understanding
- Testing and quality assurance automation
- [[Autonomous browsing]] for information gathering

**Key Concepts:** [[Browser Automation]], [[UI Interaction]], [[Web Scraping]], [[Computer Vision]], [[Agent Actions]]

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, leaks, and ensure reliability.

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Use Cases:**
- Production-grade safety and reliability assurance
- [[Hallucination detection]] and mitigation
- [[Red teaming]] and adversarial testing
- Monitoring [[LLM performance]] in production
- Compliance and security validation
- [[Benchmark evaluation]] across standard datasets

**Key Concepts:** [[Model Evaluation]], [[Safety & Security]], [[Monitoring & Observability]], [[Benchmarking]], [[Quality Assurance]]

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented environments for faster code writing, repository management, and development workflows.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Use Cases:**
- Accelerating daily development cycles
- [[Code generation]] and completion
- Repository understanding and navigation
- Git workflow automation
- Collaborative coding with AI assistance
- [[Debugging]] and code analysis

**Key Concepts:** [[AI-Assisted Development]], [[Code Generation]], [[IDE Integration]], [[Developer Experience]]

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video content.

**Key Tools:** Veo2, Landing AI, Superwhisper, Cartesia ai, Nari-labs, Murfai, Play ai, Parakeet, Assembly ai, Eleven labs, FastR