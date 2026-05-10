---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-10T05:41:16.508355
raw_file_updated: 2026-05-10T05:41:16.508355
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-10T05:41:16.508355
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of modern artificial intelligence and machine learning tools organized by functional category. This catalog encompasses over 300 tools spanning from [[Agent Memory & Context]] systems to [[Computer Use & Browser Automation]] platforms, designed to help developers, researchers, and organizations select appropriate tools for their AI implementation needs.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Persistent state and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP (Model Context Protocol) & Data Tools]] | 19 | Protocol standardization and data connection |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

### Description
Systems designed for long-term persistence, state management, and semantic recall for [[AI Agents]]. These tools enable intelligent systems to maintain context across sessions and interactions, crucial for building persistent and stateful applications.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Agents remembering user preferences across multiple conversations
- Maintaining codebase context and repository understanding
- Building [[Conversational AI]] systems with persistent memory
- Semantic recall of relevant historical information

### Related Concepts
- [[State Management]]
- [[Semantic Search]]
- [[Conversational Context]]

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

### Description
Logic engines and frameworks that manage multi-step planning and multi-agent collaboration. These platforms provide the foundational architecture for coordinating complex AI workflows where single-model solutions are insufficient.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex workflows requiring multiple specialized agents
- Multi-step reasoning and planning tasks
- Coordination of heterogeneous AI systems
- Building [[Agentic Workflows]] with conditional logic
- Enterprise automation pipelines

### Related Concepts
- [[AI Agents]]
- [[Workflow Automation]]
- [[Multi-Agent Systems]]
- [[LangChain]]

---

## 3. MCP (Model Context Protocol) & Data Tools

**Tool Count:** 19 tools

### Description
Standardized protocols and tools for connecting large language models to external data sources and local machine tools. [[MCP (Model Context Protocol)]] provides a unified interface for bridging the gap between AI models and diverse data ecosystems.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Connecting [[Language Models]] to local file systems
- Integrating with specialized databases and data sources
- Standardizing tool interfaces across different platforms
- Building extensible AI systems with pluggable data sources
- 3D modeling and specialized domain tools integration

### Related Concepts
- [[Model Context Protocol]]
- [[Data Integration]]
- [[Tool Use]]
- [[API Integration]]

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

### Description
Ingestion pipelines and retrieval systems that transform unstructured documents—PDFs, videos, and websites—into searchable vector embeddings. [[Retrieval-Augmented Generation (RAG)]] systems enable AI applications to ground responses in specific documents and knowledge bases.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Document parsing and extraction from PDFs and images
- Creating searchable knowledge bases
- Video content indexing and retrieval
- Implementing [[Semantic Search]] over large document collections

### Related Concepts
- [[Retrieval-Augmented Generation (RAG)]]
- [[Vector Databases]]
- [[Semantic Search]]
- [[Document Parsing]]
- [[Embeddings]]

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

### Description
Tools that enable agents to interact with user interfaces, click buttons, navigate websites, and perform actions like humans. These systems bridge the gap between AI reasoning and real-world digital interactions.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and information gathering
- Robotic process automation (RPA) for web applications
- Testing and quality assurance automation
- Building "human-in-the-loop" UI task assistants
- E-commerce and data extraction workflows

### Related Concepts
- [[Browser Automation]]
- [[Robotic Process Automation (RPA)]]
- [[Web Scraping]]
- [[UI Automation]]

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

### Description
Comprehensive testing, monitoring, and security frameworks for production-grade AI systems. These tools prevent hallucinations, detect data leaks, evaluate model performance, and ensure reliable, safe AI deployments.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Testing AI outputs for accuracy and hallucinations
- Monitoring production AI systems in real-time
- Red-teaming and adversarial evaluation
- Compliance and safety verification
- Performance benchmarking and comparison
- Detecting data leaks and security vulnerabilities

### Related Concepts
- [[AI Safety]]
- [[Model Evaluation]]
- [[Monitoring & Observability]]
- [[Red Teaming]]
- [[Hallucination Detection]]