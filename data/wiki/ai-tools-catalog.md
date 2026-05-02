---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:14:53.864218
raw_file_updated: 2026-05-02T05:14:53.864218
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:14:53.864218
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive reference guide organizing artificial intelligence development and deployment tools into ten functional categories. This catalog encompasses over 280 tools designed to support the full lifecycle of AI agent development, from memory management and orchestration to evaluation and production deployment.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

### Description

Systems for long-term persistence, state management, and semantic recall for [[AI agents]]. These tools enable agents to maintain context and user preferences across multiple sessions and interactions.

### Key Tools

Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases

- Remembering user preferences across sessions
- Maintaining [[codebase context]] for development agents
- Building conversational history for [[chatbots]]
- Semantic recall of previous interactions

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

### Description

Logic engines that manage [[multi-step planning]], [[multi-agent collaboration]], and complex workflow coordination. These frameworks serve as the "brains" orchestrating multiple agents working together.

### Key Tools

Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alternative), Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases

- Complex workflows requiring multiple specialized agents
- Autonomous task decomposition and execution
- Multi-agent communication and coordination
- [[Workflow automation]] at scale

---

## 3. MCP & Data Tools

**Tool Count:** 19 tools

### Description

Standardized protocols for connecting [[Large Language Models|LLMs]] to external data sources and local machine tools. The [[Model Context Protocol]] (MCP) enables seamless integration between models and external systems.

### Key Tools

Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases

- Bridging models and local file systems
- Accessing specific databases and APIs
- Integrating custom tools with LLMs
- Standardized tool connectivity

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

### Description

Ingestion pipelines that convert unstructured documents into searchable [[vector databases]]. [[Retrieval-Augmented Generation]] (RAG) systems enable agents to access and reason over external documents.

### Key Tools

Langextract, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroundX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Use Cases

- Building "Chat with your Docs" features
- Processing PDFs, videos, and websites
- Creating searchable knowledge bases
- [[Document understanding]] and extraction

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

### Description

Tools enabling [[AI agents]] to interact with user interfaces, click buttons, fill forms, and navigate the web like a human operator. These tools bridge the gap between digital systems and agent capabilities.

### Key Tools

Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases

- Automated web research and scraping
- Human-in-the-loop UI task automation
- Testing and quality assurance
- Web-based workflow automation

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

### Description

Comprehensive testing, monitoring, and security infrastructure for production-grade [[LLM applications]]. These tools prevent [[hallucinations]], detect security vulnerabilities, and ensure reliability.

### Key Tools

Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Use Cases

- [[LLM evaluation]] and benchmarking
- Security and adversarial testing
- Monitoring production agents
- Compliance and safety verification
- Performance tracking and optimization

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

### Description

AI-augmented development environments that accelerate code writing, repository management, and software development. These tools integrate [[AI assistance]] directly into the developer workflow.

### Key Tools

Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

### Use Cases

- Accelerating daily development cycles
- Code generation and completion
- Repository understanding and navigation
- Automated code review and refactoring

---

## 8. Voice & Vision Models

**Tool Count:** 21 tools

### Description

[[Multi-modal]] tools for generating and processing audio, images, and video content. These models enable rich sensory interfaces for AI applications.

### Key Tools

Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia AI, Nari-labs, Murfai, Play AI, Parakeet, Assembly AI, Eleven Labs, FastRTC, Orpheus TTS, LLMVox, Zonos, Freepik, Gradio, Streamlit, Gamma.app, Cursorful (Cap), Mistral OCR, Landing AI tuning

### Use Cases

- Building [[voice assistants