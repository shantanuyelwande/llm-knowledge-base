---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-06T05:58:33.726192
raw_file_updated: 2026-06-06T05:58:33.726192
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-06T05:58:33.726192
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software solutions, frameworks, and services designed to support the development, deployment, and management of [[Artificial Intelligence|AI]] and [[Large Language Models|LLM]] applications. This catalog organizes over 300+ tools across ten specialized categories, enabling developers and organizations to identify the right infrastructure for their specific use cases.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP (Model Context Protocol)]] | 19 | Protocol standards and data integration |
| [[RAG & Document Processing]] | 24 | Knowledge ingestion and vectorization |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web navigation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## 1. Agent Memory & Context

### Description
Systems and frameworks for enabling [[Intelligent Agents|agents]] to maintain long-term persistence, manage state, and perform semantic recall across multiple sessions. These tools address the critical challenge of giving AI agents "memory" similar to human context awareness.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Personalizing agent behavior based on accumulated user preferences
- Maintaining codebase context across development sessions
- Enabling agents to reference historical interactions and decisions
- Building contextual understanding for complex, multi-turn conversations

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Intelligent Agents]], [[Context Management]]

---

## 2. Agent Orchestration & Frameworks

### Description
Logic engines and orchestration platforms that manage complex, multi-step planning and enable collaboration between multiple [[Intelligent Agents|agents]]. These frameworks provide the backbone for building sophisticated AI systems where a single model isn't sufficient to handle the complexity.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Coordinating multiple specialized agents for complex workflows
- Implementing hierarchical decision-making systems
- Managing task dependencies and state transitions
- Building no-code or low-code agent systems
- Creating workflow automation pipelines

### Related Concepts
[[Intelligent Agents]], [[Multi-Agent Systems]], [[Workflow Automation]], [[LLM Frameworks]]

---

## 3. MCP (Model Context Protocol) & Data Tools

### Description
Standardized protocol implementations and tools that establish secure, standardized connections between [[Large Language Models|LLMs]] and external data sources, local machine tools, and specialized services. [[MCP (Model Context Protocol)|MCP]] acts as a universal interface layer enabling models to access resources beyond their training data.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging the gap between model capabilities and local file systems
- Integrating specialized databases and data warehouses
- Connecting to third-party APIs and services
- Enabling real-time data access for agents
- Standardizing tool integrations across different platforms

### Related Concepts
[[Model Context Protocol]], [[API Integration]], [[Data Integration]], [[Tool Use]]

---

## 4. RAG & Document Processing

### Description
Retrieval-Augmented Generation ([[RAG]]) pipelines and document processing tools that transform unstructured data (PDFs, videos, websites, documents) into searchable, vectorized knowledge bases. These systems enable [[Large Language Models|LLMs]] to access and reason over custom knowledge sources.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- Building "Chat with your Docs" features
- Creating searchable knowledge bases from internal documents
- Improving model accuracy with domain-specific information
- Processing and indexing video content for retrieval
- Implementing semantic search across large document collections

### Related Concepts
[[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Processing]], [[Semantic Search]], [[Knowledge Bases]]

---

## 5. Computer Use & Browser Automation

### Description
Tools and frameworks that enable [[Intelligent Agents|agents]] to interact with graphical user interfaces, execute browser-based tasks, and navigate web applications as a human would. This capability bridges the gap between model reasoning and real-world digital interaction.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and data collection
- Executing complex web-based workflows without human intervention
- Testing web applications at scale
- Implementing "human-in-the-loop" UI task automation
- Building agents that interact with legacy systems

### Related Concepts
[[Browser Automation]], [[Intelligent Agents]], [[UI Automation]], [[Web Scraping]]

---

## 6. Evaluation, Security & Ops

### Description
Comprehensive suite of tools for testing, monitoring, securing, and operationalizing [[Large Language Models|LLM]] applications. These solutions address critical concerns including hallucination prevention, output validation, performance monitoring, and security compliance in production environments.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- Red-teaming and adversarial testing of models
- Monitoring model performance and drift in production
- Evaluating output quality against custom metrics
- Detecting and preventing [[Hallucinations|hallucinations]]
- Ensuring compliance and security standards
- Tracking and debugging agent behavior

### Related Concepts
[[LLM Evaluation]], [[Model Monitoring]], [[AI Safety]], [[Quality Assurance]], [[Production Deployment]]

---

## 7. Developer Tools & IDEs

### Description
AI-augmented integrated development environments and code