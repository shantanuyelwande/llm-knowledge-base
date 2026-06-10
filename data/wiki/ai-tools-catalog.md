---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-10T06:28:55.328284
raw_file_updated: 2026-06-10T06:28:55.328284
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-10T06:28:55.328284
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and frameworks. It organizes over 300+ AI-related tools across 10 functional categories, providing developers and organizations with guidance on selecting appropriate solutions for specific use cases.

## Summary

This catalog maps the expanding AI tooling ecosystem into distinct categories based on functionality:

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code generation and repository management |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and cross-cutting tools |

---

## Categories

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[Autonomous Agents|agents]].

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- Codebase context retention for code-focused agents
- Long-term conversation continuity
- Personalization without re-prompting

**Related Concepts:** [[State Management]], [[Vector Embeddings]], [[Semantic Search]]

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Use Cases:**
- Complex workflows requiring multiple specialized agents
- Multi-step reasoning and planning
- Agent-to-agent communication and coordination
- Workflow visualization and management

**Related Concepts:** [[Autonomous Agents]], [[Workflow Automation]], [[Multi-Agent Systems]], [[LLM Frameworks]]

---

### 3. MCP & Data Tools

**Purpose:** Standardized protocols for connecting [[Large Language Models|LLMs]] to external data and local machine tools.

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging models and local file systems
- Database connectivity and querying
- Tool integration standardization
- Real-time data access for agents

**Related Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[API Integration]], [[Data Connectors]]

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that turn messy PDFs, videos, and websites into searchable vectors.

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Use Cases:**
- "Chat with your Docs" features
- Enterprise document retrieval
- Video content analysis
- Website indexing and search
- Multi-format document processing

**Related Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Parsing]], [[Semantic Search]]

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing agents to interact with UIs, click buttons, and navigate the web like a human.

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Use Cases:**
- Automated web research
- Human-in-the-loop UI task completion
- RPA (Robotic Process Automation)
- Web scraping and monitoring
- Cross-browser testing automation

**Related Concepts:** [[Browser Automation]], [[Robotic Process Automation]], [[UI Automation]], [[Web Scraping]]

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing [[LLM|LLM]] outputs to prevent hallucinations and leaks.

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Use Cases:**
- Production-grade safety and reliability
- Red-teaming and adversarial testing
- Hallucination detection and mitigation
- Monitoring and observability
- Compliance and audit trails
- Model evaluation and benchmarking

**Related Concepts:** [[LLM Safety]], [[Model Evaluation]], [[Observability]], [[Red Teaming]], [[Prompt Injection]]

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented environments for faster code writing and repository management.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Use Cases:**
- Accelerated code generation during development
- Repository understanding and navigation
- Code review and refactoring
- Documentation generation
- IDE integration and extensions

**Related Concepts:** [[Code Generation]], [[IDE Integration]], [[AI-Assisted Development]], [[Git Integration]]

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Key Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs, Murfai, Play ai, Parakeet, Assembly ai, Eleven labs, FastRTC, Orpheus tts, Llmvox, Zonos, Freepik, Gradio, Streamlit,