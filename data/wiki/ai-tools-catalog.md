---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:29:05.082604
raw_file_updated: 2026-06-07T06:29:05.082604
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:29:05.082604
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for artificial intelligence development tools and platforms. It organizes over 300+ tools across ten primary categories, enabling developers and organizations to identify the right solutions for specific AI implementation challenges. This catalog serves as a reference guide for building AI agents, processing data, deploying models, and managing AI operations at scale.

## Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol (MCP) & Data Tools]] | 19 | LLM-to-data bridging |
| [[RAG & Document Processing]] | 24 | Document ingestion and search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and security |
| [[Developer Tools & IDEs]] | 22 | Code augmentation and repositories |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

### Description
Systems for long-term persistence, state management, and semantic recall for agents. These tools enable AI agents to maintain context and "remember" information across multiple sessions and interactions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Preserving user preferences across sessions
- Maintaining codebase context for code generation
- Building persistent conversational agents
- Semantic memory retrieval for complex workflows

### Related Concepts
[[Agent Orchestration & Frameworks]], [[RAG & Document Processing]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

### Description
Logic engines that manage multi-step planning and multi-agent collaboration. These frameworks provide the structural foundation for orchestrating complex AI workflows where multiple agents or reasoning steps are required.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple reasoning steps
- Multi-agent collaboration and communication
- Autonomous task execution and planning
- Workflow automation with conditional logic

### Related Concepts
[[Agent Memory & Context]], [[Model Context Protocol (MCP) & Data Tools]], [[Evaluation, Security & Ops]]

---

## 3. Model Context Protocol (MCP) & Data Tools

**Tool Count:** 19 tools

### Description
Standardized protocols for connecting large language models to external data sources and local machine tools. [[Model Context Protocol]] enables seamless integration between AI models and the broader software ecosystem.

### Key Tools
Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging models and local file systems
- Connecting to specific databases and APIs
- Standardized tool integration
- Real-time data access for AI agents

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Computer Use & Browser Automation]], [[Serving, Inference & Fine-tuning]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

### Description
Ingestion pipelines that transform unstructured documents (PDFs, videos, websites) into searchable, vector-embedded formats. [[Retrieval-Augmented Generation (RAG)]] systems enable AI applications to access and leverage external knowledge bases effectively.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Processing and indexing large document collections
- Multi-modal document understanding (text, images, video)
- Semantic search across knowledge bases

### Related Concepts
[[Agent Memory & Context]], [[Model Context Protocol (MCP) & Data Tools]], [[Voice & Vision Models]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

### Description
Tools enabling AI agents to interact with user interfaces, click buttons, fill forms, and navigate the web autonomously. These platforms simulate human-like behavior for automated web tasks and research.

### Key Tools
Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and data collection
- Human-in-the-loop UI task automation
- Web scraping with intelligent navigation
- Form filling and multi-step web interactions

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Model Context Protocol (MCP) & Data Tools]], [[Evaluation, Security & Ops]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

### Description
Comprehensive testing, monitoring, and security infrastructure for production AI systems. These tools prevent hallucinations, detect data leaks, monitor performance, and ensure reliability at scale.

### Key Tools
Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Use Cases
- Production-grade safety and reliability testing
- Hallucination detection and mitigation
- Performance monitoring and observability
- Security auditing and red teaming
- Compliance and governance tracking

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Developer Tools & IDEs]], [[Serving, Inference & Fine-tuning]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

### Description
AI-augmented development environments that accelerate code writing, repository management, and software development workflows. These tools integrate AI capabilities directly into the developer experience.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode,