---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:53:30.927699
raw_file_updated: 2026-04-17T20:53:30.927699
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:53:30.927699
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ AI/ML tools across 10 distinct categories, each serving specific functions in the AI development lifecycle—from agent memory management to production inference serving.

This catalog serves as a reference guide for developers, AI engineers, and organizations building intelligent systems, helping them identify the right tools for their specific use cases.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and security |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal generation and processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and cross-cutting tools |

---

## Detailed Categories

### 1. Agent Memory & Context

**Tool Count:** 18

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for agents.

**Use Cases:**
- Enabling agents to "remember" user preferences across sessions
- Maintaining codebase context in development workflows
- Building persistent conversational experiences
- Semantic recall of historical interactions

**Key Concepts:** [[Agent Memory]], [[State Management]], [[Semantic Search]], [[Conversational AI]]

---

### 2. Agent Orchestration & Frameworks

**Tool Count:** 32

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Use Cases:**
- Complex workflows requiring multiple processing steps
- Multi-agent systems where coordination is essential
- Task decomposition and delegation
- Workflow automation and orchestration

**Key Concepts:** [[Multi-Agent Systems]], [[Workflow Orchestration]], [[Task Planning]], [[Agent Coordination]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Tool Count:** 19

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting LLMs to external data sources and local machine tools.

**Use Cases:**
- Bridging models and local file systems
- Integrating with specific databases
- Standardized tool integration
- Cross-platform data access

**Key Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[Data Access]], [[LLM Grounding]]

---

### 4. RAG & Document Processing

**Tool Count:** 24

**Key Tools:** Langextract, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vector representations.

**Use Cases:**
- Building "Chat with your Docs" features
- Document knowledge base creation
- Multi-format document processing
- Vector database population

**Key Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Parsing]], [[Semantic Search]]

---

### 5. Computer Use & Browser Automation

**Tool Count:** 20

**Key Tools:** Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Enabling agents to interact with user interfaces, click buttons, and navigate the web autonomously like a human.

**Use Cases:**
- Automated web research and data gathering
- Human-in-the-loop UI task automation
- Web scraping and monitoring
- Cross-platform UI interaction

**Key Concepts:** [[Computer Vision]], [[UI Automation]], [[Web Scraping]], [[Agent Behavior]]

---

### 6. Evaluation, Security & Ops

**Tool Count:** 28

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**Purpose:** Testing, monitoring, and securing LLM outputs to prevent hallucinations, data leaks, and ensure reliability.

**Use Cases:**
- Production-grade safety assurance
- Hallucination detection and prevention
- Model performance benchmarking
- Security and compliance monitoring
- Red teaming and adversarial testing

**Key Concepts:** [[LLM Safety]], [[Evaluation Metrics]], [[Monitoring & Observability]], [[Security & Compliance]]

---

### 7. Developer Tools & IDEs

**Tool Count:** 22

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments that accelerate code writing and repository management.

**Use Cases:**
- Daily development workflow enhancement
- Code generation and completion
- Repository understanding and navigation
- Real-time code suggestions
- Documentation generation

**Key Concepts:** [[AI-Assisted Development]], [[Code Generation]], [[Developer Experience]], [[IDE Integration]]

---

### 8. Voice & Vision Models

**Tool Count:** 21

**Key Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia AI, Nari-labs, Murf AI, Play AI, Parakeet, Assembly AI, Eleven Labs, FastRTC, Orpheus TTS, LLMVox, Zonos, Freepik, Grad