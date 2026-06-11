---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-11T06:55:07.126467
raw_file_updated: 2026-06-11T06:55:07.126467
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-11T06:55:07.126467
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for artificial intelligence development tools and frameworks. It organizes over 300+ tools across 10 functional categories, providing developers and AI engineers with a structured reference for selecting appropriate solutions based on their specific use cases and project requirements.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol-based LLM connections |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented coding environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Category Breakdown

### 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** These systems enable [[AI Agents|agents]] to maintain long-term persistence, manage state, and perform semantic recall across sessions.

**Use Cases:**
- Storing and retrieving user preferences across conversations
- Maintaining codebase context for extended development sessions
- Building agents with persistent memory of past interactions
- Semantic search over accumulated agent knowledge

**Related Concepts:** [[State Management]], [[Semantic Search]], [[Context Windows]]

---

### 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and coordinate collaboration between multiple [[AI Agents|agents]].

**Use Cases:**
- Complex workflows requiring sequential decision-making
- Multi-agent systems where agents must communicate and collaborate
- Hierarchical task decomposition and execution
- Conditional logic and branching workflows

**Related Concepts:** [[Multi-Agent Systems]], [[Workflow Automation]], [[Task Planning]]

---

### 3. MCP & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Implements standardized [[Model Context Protocol]] (MCP) to connect [[Large Language Models|LLMs]] with external data sources and local machine tools.

**Use Cases:**
- Bridging models with local file systems
- Connecting to specialized databases
- Enabling real-time data access for agents
- Standardizing tool integration across platforms

**Related Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[API Connections]]

---

### 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai, LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform unstructured documents (PDFs, videos, websites) into searchable vector embeddings for [[Retrieval-Augmented Generation]] (RAG) systems.

**Use Cases:**
- Building "Chat with your Docs" applications
- Processing multi-format documents at scale
- Creating searchable knowledge bases
- Extracting structured data from unstructured sources

**Related Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Parsing]], [[Semantic Search]]

---

### 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Enables [[AI Agents|agents]] to interact with user interfaces, click buttons, fill forms, and navigate the web autonomously.

**Use Cases:**
- Automated web research and data gathering
- Human-in-the-loop UI task automation
- End-to-end web application testing
- Screenshot analysis and UI understanding

**Related Concepts:** [[Browser Automation]], [[UI Interaction]], [[Robotic Process Automation]]

---

### 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**Purpose:** Testing, monitoring, and securing [[Large Language Models|LLM]] outputs to prevent [[Hallucinations|hallucinations]], data leaks, and ensure safety and reliability.

**Use Cases:**
- Production-grade LLM safety verification
- Red teaming and adversarial testing
- Monitoring model performance in production
- Compliance and audit logging
- Detecting and preventing data exfiltration

**Related Concepts:** [[LLM Safety]], [[Model Evaluation]], [[Monitoring & Observability]], [[Red Teaming]]

---

### 7. Developer Tools & IDEs

**Tool Count:** 22 tools

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, TalkToGithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments that accelerate code writing, provide intelligent code completion, and enhance repository management.

**Use Cases:**
- Daily development workflows
- Intelligent code generation and suggestions
- Repository navigation and understanding
- Natural language code queries
- Real-time code review assistance

**Related Concepts:** [[Code Generation]], [[IDE Integration]], [[Developer Experience]]

---

### 8. Voice & Vision Models

**Tool Count:** 21 tools

**Key Tools:** Veo2 (video), Landing AI (object detection