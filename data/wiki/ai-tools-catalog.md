---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-26T05:15:55.531427
raw_file_updated: 2026-04-26T05:15:55.531427
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-26T05:15:55.531427
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and platforms designed to support [[artificial-intelligence|AI]] development, deployment, and operations. This catalog organizes over 300+ tools across ten functional categories, enabling developers and organizations to identify the right solutions for their specific AI implementation needs.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[Model Context Protocol]] | 19 | LLM-to-data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | Code writing and development |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and automation |

---

## 1. Agent Memory & Context

### Purpose
Systems for long-term persistence, state management, and semantic recall for [[intelligent agents]].

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### When to Use
- Agents need to "remember" user preferences across sessions
- Building systems that maintain [[context]] about codebases over time
- Implementing persistent user profiles or interaction history
- Semantic recall of previous conversations or decisions

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Large Language Models]], [[Semantic Search]]

---

## 2. Agent Orchestration & Frameworks

### Purpose
Logic engines that manage multi-step planning and multi-agent collaboration for complex workflows.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### When to Use
- Complex workflows requiring multiple specialized agents
- Implementing [[multi-agent systems]] with interdependent tasks
- Building no-code or low-code agent applications
- Coordinating parallel and sequential agent operations
- Creating visual workflow builders for AI applications

### Related Concepts
[[Intelligent Agents]], [[Workflow Automation]], [[Large Language Models]], [[Multi-Agent Systems]]

---

## 3. Model Context Protocol & Data Tools

### Purpose
Standardized protocols for connecting [[Large Language Models|LLMs]] to external data sources and local machine tools.

### Key Tools
Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### When to Use
- Bridging the gap between models and local file systems
- Connecting LLMs to specific databases or APIs
- Standardizing tool integration across multiple models
- Building extensible [[AI systems]] with pluggable data sources
- Integrating with third-party services via standardized protocols

### Related Concepts
[[Large Language Models]], [[API Integration]], [[Data Management]], [[Model Context Protocol]]

---

## 4. RAG & Document Processing

### Purpose
Ingestion pipelines that transform unstructured documents (PDFs, videos, websites) into searchable vector representations for [[Retrieval-Augmented Generation|RAG]] systems.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### When to Use
- Building "Chat with your Docs" features
- Processing large document repositories for semantic search
- Extracting structured data from unstructured sources
- Creating searchable knowledge bases from PDFs or websites
- Video content analysis and indexing

### Related Concepts
[[Retrieval-Augmented Generation]], [[Vector Databases]], [[Semantic Search]], [[Document Processing]], [[Large Language Models]]

---

## 5. Computer Use & Browser Automation

### Purpose
Tools enabling agents to interact with user interfaces, click buttons, navigate websites, and perform tasks like human operators.

### Key Tools
Vercel Labs Agent Browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### When to Use
- Automated web research and data gathering
- "Human-in-the-loop" UI task automation
- Web scraping with intelligent agent navigation
- Testing web applications with AI agents
- Automating repetitive browser-based workflows

### Related Concepts
[[Intelligent Agents]], [[Browser Automation]], [[Web Scraping]], [[UI Automation]], [[Robotic Process Automation]]

---

## 6. Evaluation, Security & Ops

### Purpose
Testing, monitoring, and securing [[Large Language Model|LLM]] outputs to prevent [[hallucinations]], data leaks, and ensure production reliability.

### Key Tools
Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### When to Use
- Production deployment of AI systems
- Monitoring model performance and drift
- Security testing and red-teaming
- Evaluating output quality and accuracy
- Compliance and audit trail requirements
- Detecting and preventing hallucinations

### Related Concepts
[[AI Safety]], [[Model Evaluation]], [[LLM Monitoring]], [[Security]], [[Quality Assurance]], [[Hallucination Detection]]

---

## 7. Developer Tools & IDEs

### Purpose
[[AI]]-augmented development environments accelerating code writing, repository management, and the development lifecycle.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

### When to Use
- Daily development workflows
- Code generation and completion
- Repository exploration and understanding
- Pair programming with AI assistance
- Learning new codebases quickly

### Related Concepts
[[Code Generation]], [[Developer Tools]], [[IDE]], [[GitHub Copilot]], [[Software Development]]

---

## 8. Voice & Vision Models