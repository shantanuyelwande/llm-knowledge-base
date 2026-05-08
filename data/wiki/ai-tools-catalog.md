---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-08T04:56:31.110750
raw_file_updated: 2026-05-08T04:56:31.110750
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-08T04:56:31.110750
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support the development, deployment, and management of artificial intelligence systems. This catalog organizes over 300 tools across ten functional categories, providing developers, researchers, and organizations with a structured reference for selecting appropriate tools based on their specific use cases and technical requirements.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and agent collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and specialized solutions |

---

## 1. Agent Memory & Context

### Purpose
Systems for long-term persistence, state management, and semantic recall for autonomous agents.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Agents that need to "remember" user preferences across sessions
- Maintaining codebase context and historical interactions
- Building persistent [[AI Agent|agent]] personalities
- Semantic search over conversation history

### Related Concepts
[[Agent Orchestration & Frameworks]], [[RAG & Document Processing]]

---

## 2. Agent Orchestration & Frameworks

### Purpose
Logic engines that manage multi-step planning, task decomposition, and multi-agent collaboration.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple specialized agents
- Orchestrating communication between distributed AI components
- Building no-code or low-code AI workflows
- Implementing hierarchical task planning

### Related Concepts
[[Agent Memory & Context]], [[MCP & Data Tools]], [[Evaluation, Security & Ops]]

---

## 3. MCP & Data Tools

### Purpose
Standardized protocols and tools for connecting [[Large Language Models|LLMs]] to external data sources and local machine resources.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging gaps between AI models and local file systems
- Connecting LLMs to specialized databases
- Integrating 3D modeling tools with AI workflows
- Creating standardized tool interfaces for [[AI Agent|agents]]

### Related Concepts
[[RAG & Document Processing]], [[Agent Orchestration & Frameworks]], [[Computer Use & Browser Automation]]

---

## 4. RAG & Document Processing

### Purpose
Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable vector embeddings for [[Retrieval-Augmented Generation|RAG]] systems.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Processing multi-modal documents (text, images, video)
- Creating searchable knowledge bases
- Implementing semantic search over proprietary data

### Related Concepts
[[Agent Memory & Context]], [[MCP & Data Tools]], [[Voice & Vision Models]]

---

## 5. Computer Use & Browser Automation

### Purpose
Tools enabling agents to interact with graphical user interfaces, click buttons, navigate websites, and perform human-like browsing tasks.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and information gathering
- Human-in-the-loop UI task automation
- Testing web applications through agent interaction
- Building web scraping workflows

### Related Concepts
[[Agent Orchestration & Frameworks]], [[MCP & Data Tools]], [[Evaluation, Security & Ops]]

---

## 6. Evaluation, Security & Ops

### Purpose
Testing, monitoring, and security frameworks to prevent [[Hallucination|hallucinations]], data leaks, and ensure production-grade reliability of AI systems.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Red-teaming AI systems to identify vulnerabilities
- Monitoring LLM outputs in production
- Evaluating model performance with standardized benchmarks
- Implementing safety guardrails and compliance checks
- Tracing and debugging agent behavior

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Developer Tools & IDEs]], [[Serving, Inference & Fine-tuning]]

---

## 7. Developer Tools & IDEs

### Purpose
AI-augmented integrated development environments and tools that accelerate code writing, repository management, and software development workflows.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

### Use Cases
- Accelerating daily development cycles
- Code generation and completion
- Repository understanding and navigation
- Interactive coding environments with AI assistance
- Collaborative development workflows

### Related Concepts
[[Agent Memory & Context]], [[Evaluation, Security & Ops]], [[Serving, Inference & Fine-tuning]]

---

## 8. Voice & Vision Models

### Purpose
Multi-modal tools for generating, processing, and analyzing audio, images, and video content.

### Key Tools
Veo2 (video), Landing AI (object detection), Super