---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-30T05:34:33.269121
raw_file_updated: 2026-04-30T05:34:33.269121
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-30T05:34:33.269121
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ AI tools across 10 functional categories, helping developers and organizations select appropriate solutions for their specific use cases. This catalog reflects the rapidly expanding ecosystem of [[AI Development Tools]] and represents the current state of AI infrastructure and tooling as of 2024.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and specialized solutions |

---

## 1. Agent Memory & Context

### Purpose
Systems for long-term persistence, state management, and semantic recall for [[Intelligent Agents]].

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Agents that need to "remember" user preferences across sessions
- Codebase context persistence for development agents
- Long-term conversational memory for chatbots
- Semantic recall of historical interactions

### Key Concepts
- [[Agent State Management]]
- [[Semantic Memory]]
- [[Persistent Context]]

---

## 2. Agent Orchestration & Frameworks

### Purpose
Logic engines that manage multi-step planning and multi-agent collaboration. These frameworks serve as the "brain" coordinating complex AI workflows.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple sequential steps
- Multi-agent systems with specialized roles
- Conditional logic and branching workflows
- Integration of multiple [[Large Language Models]]
- Visual workflow builders for non-technical users

### Key Concepts
- [[Agent Planning]]
- [[Multi-Agent Systems]]
- [[Workflow Orchestration]]
- [[Agent Frameworks]]

---

## 3. MCP (Model Context Protocol) & Data Tools

### Purpose
Standardized protocols for connecting [[Large Language Models]] to external data sources and local machine tools, enabling seamless integration between AI models and external systems.

### Key Tools
Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging the gap between models and local file systems
- Connecting to specific databases
- Standardized tool integration
- Cross-platform data access
- 3D model processing and manipulation

### Key Concepts
- [[Model Context Protocol]]
- [[Tool Integration]]
- [[Data Access Patterns]]

---

## 4. RAG & Document Processing

### Purpose
Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable vectors, enabling [[Retrieval-Augmented Generation]] systems.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Document ingestion and parsing
- Video content indexing and retrieval
- Website scraping and vectorization
- Multi-format document handling
- Semantic search over large document collections

### Key Concepts
- [[Retrieval-Augmented Generation]]
- [[Vector Databases]]
- [[Document Parsing]]
- [[Semantic Search]]

---

## 5. Computer Use & Browser Automation

### Purpose
Tools allowing agents to interact with user interfaces, click buttons, and navigate the web autonomously, simulating human-like browser behavior.

### Key Tools
Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and information gathering
- Human-in-the-loop UI task automation
- End-to-end web application testing
- Automated form filling and data entry
- Web scraping with intelligent navigation
- Cross-platform UI interaction

### Key Concepts
- [[Browser Automation]]
- [[UI Automation]]
- [[Web Agents]]
- [[Computer Vision for UI]]

---

## 6. Evaluation, Security & Ops

### Purpose
Comprehensive testing, monitoring, and security solutions to prevent [[Hallucinations]], data leaks, and ensure production-grade reliability of [[Large Language Models]].

### Key Tools
Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Use Cases
- Quality assurance and evaluation of model outputs
- Red-teaming and adversarial testing
- Production monitoring and observability
- Preventing hallucinations and misinformation
- Security vulnerability detection
- Performance benchmarking
- Cost optimization and latency monitoring

### Key Concepts
- [[LLM Evaluation]]
- [[Model Safety]]
- [[Observability & Monitoring]]
- [[Red Teaming]]
- [[Guardrails]]

---

## 7. Developer Tools & IDEs

### Purpose
AI-augmented development environments designed to accelerate code writing, repository management, and software development workflows.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, TalkToGithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

### Use Cases
- Real-time code completion and suggestion
- Automated code review and refactoring
- Repository navigation and understanding
- Natural language to code generation