---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-21T04:52:09.474856
raw_file_updated: 2026-04-21T04:52:09.474856
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-21T04:52:09.474856
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and frameworks designed to build, deploy, and manage artificial intelligence systems. This catalog organizes over 300+ tools across 10 functional categories, addressing the complete lifecycle of AI application development from agent memory management to production inference.

## Summary

Modern AI development requires specialized tools across multiple domains. This catalog categorizes essential AI infrastructure into functional groups, helping developers and engineers select appropriate tools for specific use cases. The catalog spans from low-level infrastructure (model serving, inference optimization) to high-level abstractions (agent orchestration, RAG pipelines), enabling both rapid prototyping and production-grade deployments.

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Purpose
Systems for long-term persistence, state management, and semantic recall for [[Artificial Intelligence Agents]].

### Use Cases
- Agents that need to "remember" user preferences across sessions
- Maintaining codebase context and historical interactions
- Building persistent [[Knowledge Bases]] for AI systems
- Semantic recall of relevant information from large memory stores

### Key Concepts
- [[State Management]]
- [[Semantic Search]]
- [[Agent Persistence]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Purpose
Logic engines that manage multi-step planning and multi-agent collaboration.

### Use Cases
- Complex workflows requiring orchestration of multiple [[Artificial Intelligence Agents]]
- Multi-step reasoning and planning tasks
- Collaborative agent systems
- Visual workflow builders for non-technical users
- Enterprise automation pipelines

### Key Concepts
- [[Agent Orchestration]]
- [[Workflow Automation]]
- [[Multi-Agent Systems]]
- [[Planning and Reasoning]]

---

## 3. MCP (Model Context Protocol) & Data Tools

**Tool Count:** 19 tools

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Purpose
Standardized protocols for connecting [[Large Language Models]] to external data and local machine tools.

### Use Cases
- Bridging the gap between models and local file systems
- Integration with specific databases
- Connecting to 3D tools and specialized software
- Standardized tool access across different AI platforms

### Key Concepts
- [[Model Context Protocol]]
- [[Tool Integration]]
- [[API Standardization]]
- [[Data Connectivity]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Purpose
Ingestion pipelines that convert messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation]].

### Use Cases
- Building "Chat with your Docs" features
- Processing unstructured documents at scale
- Video and image analysis
- OCR and document parsing
- [[Vector Database]] management
- Semantic search across document collections

### Key Concepts
- [[Retrieval-Augmented Generation]]
- [[Vector Embeddings]]
- [[Document Processing]]
- [[Vector Databases]]
- [[Semantic Search]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Purpose
Enabling agents to interact with user interfaces, click buttons, and navigate the web like humans.

### Use Cases
- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Web scraping and information extraction
- Cross-platform UI automation
- Accessibility testing and browser automation

### Key Concepts
- [[Browser Automation]]
- [[Web Agents]]
- [[UI Interaction]]
- [[Computer Vision]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Purpose
Testing, monitoring, and securing [[Large Language Model]] outputs to prevent hallucinations and information leaks.

### Use Cases
- Production monitoring and observability
- [[Red Teaming]] and adversarial testing
- Hallucination detection and mitigation
- Benchmark evaluation and performance tracking
- Security and compliance validation
- Cost and latency optimization

### Key Concepts
- [[LLM Evaluation]]
- [[Monitoring and Observability]]
- [[Security and Safety]]
- [[Benchmarking]]
- [[Red Teaming]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

### Purpose
AI-augmented development environments for faster code writing and repository management.

### Use Cases
- Accelerating daily development cycles
- Code generation and completion
- Repository understanding and navigation
- Integrated code analysis
- Collaborative development environments
- AI-assisted debugging and refactoring

### Key Concepts
- [[Code Generation]]
- [[Developer Experience]]
- [[IDE Integration]]
- [[Copilot Systems]]

---

## 8. Voice & Vision Models

**Tool Count:** 21 tools

### Key Tools
Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs, Murfai, Play ai, Parakeet, Assembly ai, Eleven labs, FastRTC, Orpheus tts, Llmvox, Zonos, Freepik, Gradio, Streamlit, Gamma.app, cursorful (Cap