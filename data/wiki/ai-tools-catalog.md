---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-27T05:30:47.828587
raw_file_updated: 2026-04-27T05:30:47.828587
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-27T05:30:47.828587
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support the development, deployment, and operation of [[Artificial Intelligence]] systems. This catalog organizes over 300+ tools across ten functional categories, enabling developers and organizations to build intelligent applications with specialized components for [[Agent Architecture|agent-based systems]], [[Machine Learning Operations]], and [[Large Language Models]].

## Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol]] | 19 | LLM connectivity to external systems |
| [[Retrieval-Augmented Generation]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Operations]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Model Serving & Inference]] | 17 | Deployment and fine-tuning infrastructure |
| [[Miscellaneous & General Utilities]] | 36 | Workflow automation and utilities |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Context Mode, Context7, Skillscreator, Skills.sh, Qodo Aware, Repo Prompt, Claude Context Semantic Search

### Purpose

Systems that enable [[Intelligent Agents|intelligent agents]] to maintain [[State Management|state]] and [[Context Window|context]] across multiple sessions. These tools provide mechanisms for long-term persistence, semantic recall, and user preference tracking.

### Use Cases

- Agents that need to "remember" user preferences across sessions
- Maintaining [[Codebase Context|codebase context]] in development workflows
- Building personalized AI assistants with continuous learning
- [[Knowledge Persistence|Knowledge persistence]] in multi-turn conversations

### Key Concepts

- [[Semantic Memory]]
- [[Session Management]]
- [[Vector Embeddings]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent Harness, Hermes, Ralph Orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic Agents, DSpy, OpenAI Agent SDK, Copilotkit, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph Builder, Rivet

### Purpose

Logic engines and frameworks that manage [[Multi-Agent Systems|multi-agent collaboration]], [[Planning|planning]], and complex workflow execution. These platforms provide the orchestration layer for coordinating multiple [[AI Agents|AI agents]] or reasoning steps.

### Use Cases

- Complex workflows requiring multiple specialized agents
- Multi-step reasoning and task decomposition
- Coordinating different [[Language Models]] for different subtasks
- Building [[Autonomous Systems|autonomous systems]] with multiple decision points

### Key Concepts

- [[Agent Architecture]]
- [[Workflow Orchestration]]
- [[Task Decomposition]]
- [[Multi-Agent Communication]]

---

## 3. Model Context Protocol & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google MCP Toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Purpose

Implements the [[Model Context Protocol]] (MCP), a standardized interface for connecting [[Large Language Models]] to external data sources, APIs, and local machine tools. These tools bridge the gap between LLM capabilities and real-world data systems.

### Use Cases

- Connecting LLMs to proprietary databases
- Accessing local file systems and tools
- Integrating with third-party APIs and services
- Building [[Tool Use|tool-using agents]] with standardized interfaces

### Key Concepts

- [[Model Context Protocol]]
- [[API Integration]]
- [[Data Connectivity]]
- [[Tool Abstraction]]

---

## 4. Retrieval-Augmented Generation & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag Flow, ragi.ai, LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag Eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Purpose

Ingestion pipelines and [[Vector Database|vector databases]] that transform unstructured documents (PDFs, websites, videos) into searchable, semantically-indexed formats. These tools enable [[Retrieval-Augmented Generation|RAG]] systems that augment [[Language Models]] with external knowledge.

### Use Cases

- Building "Chat with Your Docs" features
- Processing large document collections
- Creating searchable knowledge bases
- Implementing [[Semantic Search]] capabilities
- Handling multi-modal document types

### Key Concepts

- [[Document Parsing]]
- [[Vector Embeddings]]
- [[Semantic Search]]
- [[Vector Databases]]
- [[Retrieval-Augmented Generation]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel Labs Agent Browser, Claude Dev-Browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy Web Agent, Vibetest, Browser Use (Smooth/OpenAI/Open), Proxy Lite, Omniparser (Microsoft), Agentdesk, Simular, Computer Use (Anthropic)

### Purpose

Tools that enable [[Intelligent Agents|agents]] to interact with graphical user interfaces, navigate websites, and perform actions like clicking buttons and filling forms. These enable agents to operate in environments designed for humans.

### Use Cases

- Automated web research and information gathering
- End-to-end workflow automation across web applications
- "Human-in-the-loop" UI task automation
- Testing and quality assurance automation
- Accessibility and assistive technology applications

### Key Concepts

- [[UI Automation]]
- [[Browser Automation]]
- [[Agent Perception]]
- [[Computer Vision]]

---

## 6. Evaluation, Security & Operations

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation Harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Purpose

Comprehensive testing, monitoring, and security frameworks for [[Large Language Models]] in production. These tools assess model quality, prevent [[Hallucination|hallucinations]], detect security vulnerabilities, and provide [[Observability|observability]] for deployed systems.

### Use Cases

- Evaluating model performance before production deployment
- Monitoring LLM behavior in real-time
- [[Red Teaming|Red teaming]] and adversarial testing
- Ensuring [[AI Safety|AI safety]] and [[Alignment|alignment]]
- Detecting data leaks and security vulnerabilities
- [[MLOps|MLOps]] and model lifecycle management