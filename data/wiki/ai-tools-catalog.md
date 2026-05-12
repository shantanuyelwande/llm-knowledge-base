---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-12T05:42:14.351995
raw_file_updated: 2026-05-12T05:42:14.351995
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-12T05:42:14.351995
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for artificial intelligence development tools and platforms. It organizes over 300+ AI tools into 10 functional categories, enabling developers and organizations to identify the right solutions for specific use cases in building, deploying, and managing AI systems.

## Quick Summary

| Category | Tool Count | Primary Use |
|----------|-----------|-------------|
| [[Agent Memory & Context]] | 18 | Long-term state persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and multi-agent collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connection |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and LLM safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and customization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Category Details

### 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[Intelligent Agents|agents]]. These tools enable AI systems to maintain context across multiple sessions and interactions.

**Primary Use Cases:**
- Remembering user preferences across sessions
- Maintaining codebase context for code-generation agents
- Building persistent knowledge bases for specialized domains
- Implementing semantic search over historical interactions

**Related Concepts:** [[Agent Orchestration & Frameworks]], [[RAG & Document Processing]]

---

### 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and coordinate collaboration between multiple AI agents. These frameworks provide the orchestration layer for complex AI workflows.

**Primary Use Cases:**
- Complex workflows requiring multiple decision points
- Multi-agent systems where agents must coordinate tasks
- Hierarchical task decomposition and execution
- Real-time workflow monitoring and adjustment

**Related Concepts:** [[Agent Memory & Context]], [[Evaluation, Security & Ops]], [[MCP & Data Tools]]

---

### 3. MCP & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Tools implementing the [[Model Context Protocol|Model Context Protocol (MCP)]] - a standardized framework for connecting [[Language Models|language models]] to external data sources and local machine tools.

**Primary Use Cases:**
- Connecting LLMs to local file systems
- Bridging models and specialized databases
- Standardizing tool access across different AI platforms
- Enabling safe, controlled external integrations

**Related Concepts:** [[RAG & Document Processing]], [[Computer Use & Browser Automation]], [[Agent Orchestration & Frameworks]]

---

### 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into [[Vector Embeddings|vector embeddings]] for semantic search and retrieval. [[RAG|Retrieval-Augmented Generation (RAG)]] systems depend on these tools.

**Primary Use Cases:**
- Building "Chat with Your Docs" features
- Processing multi-format documents (PDF, HTML, video)
- Creating searchable knowledge bases
- Implementing semantic search over large document collections

**Related Concepts:** [[Agent Memory & Context]], [[MCP & Data Tools]], [[Evaluation, Security & Ops]]

---

### 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Tools enabling agents to interact with user interfaces, click buttons, navigate websites, and perform actions like humans. These are critical for [[Computer Vision|vision-based]] automation.

**Primary Use Cases:**
- Automated web research and information gathering
- End-to-end UI task automation
- Testing and quality assurance workflows
- Human-in-the-loop task completion

**Related Concepts:** [[Voice & Vision Models]], [[Agent Orchestration & Frameworks]], [[Evaluation, Security & Ops]]

---

### 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**Purpose:** Comprehensive testing, monitoring, and security infrastructure for [[Language Models|LLMs]]. These tools prevent [[Hallucination|hallucinations]], detect data leaks, and ensure production-grade reliability.

**Primary Use Cases:**
- Evaluating model quality and performance
- Red-teaming and adversarial testing
- Monitoring production LLM systems
- Ensuring compliance and data security
- Detecting and preventing hallucinations

**Related Concepts:** [[Agent Orchestration & Frameworks]], [[Serving, Inference & Fine-tuning]], [[Developer Tools & IDEs]]

---

### 7. Developer Tools & IDEs

**Tool Count:** 22 tools

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented integrated development environments (IDEs) and tools that accelerate code writing