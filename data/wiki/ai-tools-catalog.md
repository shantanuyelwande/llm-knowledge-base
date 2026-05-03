---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-03T05:34:42.149275
raw_file_updated: 2026-05-03T05:34:42.149275
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-03T05:34:42.149275
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to build, deploy, and manage artificial intelligence applications. This catalog organizes over 300+ tools across ten functional categories, each addressing specific challenges in the AI development lifecycle—from agent memory and orchestration to inference serving and evaluation.

This resource serves as a reference guide for developers, engineers, and AI practitioners selecting appropriate tools for their specific use cases.

## Quick Summary

| Category | Tool Count | Primary Use |
|----------|-----------|------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI Agents]].

**Use Cases:**
- Maintaining user preferences across sessions
- Preserving codebase context for code-aware agents
- Implementing episodic and semantic memory for conversational AI
- Building context-aware recommendation systems

**Key Concepts:** [[Memory Management]], [[State Persistence]], [[Semantic Search]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Use Cases:**
- Complex workflows requiring multiple specialized agents
- Distributed task execution and coordination
- Dynamic planning and reasoning across domains
- Building multi-step reasoning chains

**Key Concepts:** [[Agent Collaboration]], [[Workflow Orchestration]], [[Multi-Agent Systems]], [[Planning Algorithms]]

---

## 3. MCP & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data and local machine tools via the [[Model Context Protocol]].

**Use Cases:**
- Bridging models to local file systems
- Integrating with specialized databases
- Connecting to third-party APIs and services
- Enabling tool use and function calling

**Key Concepts:** [[Model Context Protocol]], [[Tool Integration]], [[Data Connectivity]], [[API Integration]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform unstructured documents (PDFs, videos, websites) into searchable vector representations.

**Use Cases:**
- Building "Chat with your Docs" applications
- Creating searchable knowledge bases
- Processing multimodal content (text, images, video)
- Implementing semantic search over proprietary documents

**Key Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Parsing]], [[Semantic Search]], [[Embeddings]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Tools enabling agents to interact with user interfaces, click buttons, and navigate the web autonomously.

**Use Cases:**
- Automated web research and information gathering
- Robotic process automation (RPA)
- Human-in-the-loop UI task completion
- Testing and quality assurance automation
- Web scraping and data extraction

**Key Concepts:** [[Browser Automation]], [[UI Interaction]], [[Robotic Process Automation]], [[Web Scraping]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent [[Hallucinations]], information leaks, and ensure reliability.

**Use Cases:**
- Evaluating model performance on custom benchmarks
- Monitoring production AI systems for drift and errors
- Red teaming and adversarial testing
- Implementing guardrails and safety constraints
- Tracking metrics and observability

**Key Concepts:** [[LLM Evaluation]], [[Model Monitoring]], [[Security Testing]], [[Red Teaming]], [[Observability]], [[Hallucination Detection]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments accelerating code writing, debugging, and repository management.

**Use Cases:**
- Accelerating daily development workflows
- Intelligent code completion and suggestion
- Automated code review and refactoring
- Repository understanding and navigation
- Test generation and debugging assistance

**Key Concepts:** [[Code Generation]], [[AI-Assisted Development]], [[IDE Integration]], [[Code Completion]]

---

## 8. Voice & Vision Models

**Tool Count:** 21 tools