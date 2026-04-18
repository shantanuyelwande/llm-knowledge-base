---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:14:40.342470
raw_file_updated: 2026-04-17T20:14:40.342470
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:14:40.342470
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support the development, deployment, and operation of artificial intelligence systems. This catalog organizes over 300+ tools across ten functional categories, providing developers and organizations with a structured reference for building AI-powered applications.

## Summary

This catalog categorizes AI development tools into specialized domains:

| Category | Tool Count | Primary Use |
|----------|-----------|------------|
| [[Agent Memory & Context]] | 18 | Long-term state management for AI agents |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standards and data connectivity |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web navigation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18

### Description
Systems designed for long-term persistence, state management, and semantic recall for [[AI agents]]. These tools enable intelligent systems to maintain context and remember user preferences across multiple sessions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Maintaining user preferences across conversation sessions
- Persisting [[codebase context]] for development agents
- Building contextual memory for long-running [[AI applications]]
- Semantic recall of historical interactions

### Related Concepts
[[Agent Orchestration & Frameworks]], [[RAG & Document Processing]], [[LLM Memory Systems]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32

### Description
Logic engines that manage multi-step planning and multi-agent collaboration. These frameworks provide the orchestration layer for complex workflows where multiple AI agents or reasoning steps are required.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple reasoning steps
- Multi-agent collaboration and delegation
- Conditional logic and branching in AI pipelines
- Workflow automation and task decomposition

### Related Concepts
[[AI Agents]], [[Workflow Automation]], [[Multi-Agent Systems]], [[Agent Memory & Context]]

---

## 3. MCP & Data Tools

**Tool Count:** 19

### Description
Tools implementing the [[Model Context Protocol]] (MCP), a standardized protocol for connecting [[Large Language Models]] to external data sources and local machine tools. These tools bridge the gap between LLM capabilities and real-world data systems.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Connecting LLMs to local file systems
- Integrating with specific databases and APIs
- Standardized tool integration for AI agents
- Real-time data access for model inference

### Related Concepts
[[Model Context Protocol]], [[API Integration]], [[Data Connectivity]], [[Agent Orchestration & Frameworks]]

---

## 4. RAG & Document Processing

**Tool Count:** 24

### Description
Ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable, vector-encoded knowledge bases. These tools are essential for implementing [[Retrieval-Augmented Generation]] (RAG) systems.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" applications
- Creating searchable knowledge bases
- Processing multi-modal documents (text, images, video)
- Implementing semantic search over large document collections

### Related Concepts
[[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Processing]], [[Semantic Search]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20

### Description
Tools that enable [[AI agents]] to interact with graphical user interfaces, click buttons, navigate websites, and perform human-like web interactions. These tools extend agent capabilities into visual and interactive domains.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and information gathering
- Human-in-the-loop UI task automation
- Web scraping and data extraction
- Testing and validation of web applications

### Related Concepts
[[Web Automation]], [[AI Agents]], [[Vision Models]], [[UI Interaction]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28

### Description
Comprehensive testing, monitoring, and security tools designed to ensure [[LLM]] outputs are safe, reliable, and free from hallucinations or data leaks. Essential for production-grade AI systems.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Red teaming and adversarial testing
- Monitoring [[LLM]] performance in production
- Hallucination detection and prevention
- Safety and security validation
- Model evaluation benchmarking

### Related Concepts
[[AI Safety]], [[LLM Evaluation]], [[Monitoring & Observability]], [[Security]]

---

## 7. Developer Tools & IDEs

**Tool Count:** 22

### Description
AI-augmented development environments that accelerate code writing, repository management, and software development workflows. These tools integrate [[Large Language Models]] directly into the developer experience.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

### Use Cases