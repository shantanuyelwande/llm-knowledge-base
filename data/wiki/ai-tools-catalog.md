---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-05T05:18:20.998990
raw_file_updated: 2026-05-05T05:18:20.998990
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-05T05:18:20.998990
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system organizing modern artificial intelligence development tools and frameworks into ten distinct categories. This catalog serves as a reference guide for developers, engineers, and AI practitioners selecting appropriate tools for specific use cases in [[machine learning]] and [[AI application development]].

The catalog encompasses over 280 specialized tools spanning from [[agent architecture]] to [[model serving]], reflecting the diverse ecosystem of contemporary AI development platforms.

---

## Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code generation and repository management |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

**Use Cases:**
- Maintaining user preferences across multiple sessions
- Preserving [[codebase context]] for code-aware agents
- Implementing [[semantic memory]] for intelligent recall
- Building persistent agent knowledge bases

**Key Concepts:** [[Agent persistence]], [[State management]], [[Semantic search]], [[Context windows]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Use Cases:**
- Orchestrating complex [[multi-agent workflows]]
- Implementing [[agent communication protocols]]
- Building [[agentic reasoning]] systems
- Managing [[workflow automation]] at scale

**Key Concepts:** [[Agent frameworks]], [[Workflow orchestration]], [[Multi-agent systems]], [[Planning algorithms]]

---

## 3. MCP & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data sources and local machine tools.

**Use Cases:**
- Bridging [[LLMs]] with local file systems
- Connecting models to specific databases
- Implementing standardized [[tool use protocols]]
- Enabling [[API integration]] for agents

**Key Concepts:** [[Model Context Protocol]], [[Tool integration]], [[Data connectivity]], [[API abstraction]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval Augmented Generation]].

**Use Cases:**
- Building "Chat with your Docs" features
- Processing unstructured documents
- Creating [[vector databases]]
- Implementing [[semantic search]] over documents
- Video and multimedia ingestion

**Key Concepts:** [[RAG systems]], [[Vector embeddings]], [[Document parsing]], [[Vector databases]], [[OCR technology]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Enabling [[AI agents]] to interact with user interfaces, click buttons, and navigate the web like humans.

**Use Cases:**
- Automated [[web research]]
- [[Human-in-the-loop]] UI task automation
- Web scraping and data collection
- Cross-website process automation
- Accessibility testing

**Key Concepts:** [[Browser automation]], [[UI interaction]], [[Computer vision]], [[Web agents]], [[RPA (Robotic Process Automation)]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent [[hallucinations]], leaks, and ensure reliability.

**Use Cases:**
- [[LLM evaluation]] and benchmarking
- Production monitoring and observability
- [[Red teaming]] and security testing
- [[Hallucination detection]] and prevention
- Performance metrics tracking
- Compliance and safety validation

**Key Concepts:** [[LLM safety]], [[Evaluation metrics]], [[Observability]], [[Security testing]], [[Production monitoring]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments for faster code writing and repository management.

**Use Cases:**
- Accelerating [[code generation]]
- Intelligent code completion
- Repository-aware development
- [[AI-assisted debugging]]
- Interactive code canvases
- Documentation generation

**Key Concepts:** [[Code generation]], [[IDE integration]], [[Developer productivity]], [[Repository management]]

---

## 8. Voice & Vision Models

**Tool Count:** 