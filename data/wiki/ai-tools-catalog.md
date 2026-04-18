---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-18T13:50:34.755393
raw_file_updated: 2026-04-18T13:50:34.755393
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-18T13:50:34.755393
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ AI/ML tools across 10 functional categories, enabling developers and organizations to identify the right solutions for specific use cases in agent development, data processing, model serving, and production deployment.

## Quick Summary

| Category | Tool Count | Primary Use |
|----------|-----------|-------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Category Details

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Context Mode, Context7, Skillscreator, Skills.sh, Skills Patterns (Google), Qodo Aware, Repo Prompt, Claude Context Semantic Search

**When to Use:** 
- Agents need to "remember" user preferences across sessions
- Maintaining [[codebase context]] over multiple interactions
- Building stateful conversational experiences
- Implementing [[semantic memory]] for complex domains

**Related Concepts:** [[State Management]], [[Semantic Search]], [[Conversation History]]

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, Autoagent Harness, Hermes, Ralph Orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic Agents, DSpy, OpenAI Agent SDK, Copilotkit, Autoagent, Firebase Studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph Builder, Rivet

**When to Use:**
- Complex workflows requiring multiple specialized agents
- Coordinating parallel task execution
- Building [[agentic AI systems]] with interdependent steps
- Implementing [[multi-agent collaboration]] patterns

**Related Concepts:** [[Workflow Automation]], [[Agent Coordination]], [[Task Planning]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data and local machine tools.

**Key Tools:** Google MCP Toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**When to Use:**
- Bridging [[LLMs]] with local file systems
- Connecting to specific databases or APIs
- Standardizing tool integration across platforms
- Building [[tool-augmented AI]] systems

**Related Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[API Abstraction]]

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation]].

**Key Tools:** Langextract, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag Eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**When to Use:**
- Building "Chat with your Docs" features
- Processing unstructured document collections
- Creating searchable knowledge bases
- Implementing [[semantic search]] over proprietary data

**Related Concepts:** [[Vector Databases]], [[Document Parsing]], [[Embedding Models]], [[Semantic Search]]

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing [[AI agents]] to interact with user interfaces, click buttons, and navigate the web like a human.

**Key Tools:** Vercel Labs Agent Browser, Claude Dev-Browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy Web Agent, VibeTest, Browser Use (Smooth/OpenAI/Open), Proxy Lite, Omniparser (Microsoft), Agentdesk, Simular, Computer Use (Anthropic)

**When to Use:**
- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Testing and QA automation
- Building web-based [[agent workflows]]

**Related Concepts:** [[RPA (Robotic Process Automation)]], [[Web Scraping]], [[UI Automation]]

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, data leaks, and ensure production reliability.

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red Teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation Harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**When to Use:**
- Production-grade AI systems requiring safety guarantees
- Monitoring [[LLM]] behavior and performance
- Red-teaming and adversarial testing
- Implementing [[guardrails]] and output validation
- Tracking metrics and observability

**Related Concepts:** [[LLM Safety]], [[Hallucination Prevention]], [[Observability]], [[Model Evaluation]]

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented development environments for faster code writing and repository management.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, TalkToGithub, Cursor, Windsurf, Trae, CodeLLM, Augment Code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**When to Use:**
- Accelerating daily development cycles
- Code generation and completion
- Repository understanding and navigation
- [[AI pair programming]]
- Documentation generation

**Related Concepts:** [[Code Generation]], [[IDE Integration]], [[Developer Productivity]]

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Key Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia AI, Nari-labs, Murfai, Play AI, Parakeet, Assembly AI, Eleven Labs, FastRTC, Orpheus TTS, LLMVox, Zonos, Freepik, Gradio,