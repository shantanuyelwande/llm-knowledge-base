---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-12T06:48:07.168669
raw_file_updated: 2026-06-12T06:48:07.168669
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-12T06:48:07.168669
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software solutions and frameworks designed to build, deploy, and manage artificial intelligence applications. This catalog organizes over 300+ tools across 10 functional categories, from [[Agent Memory & Context]] systems to specialized [[Voice & Vision Models]]. It serves as a reference guide for developers, AI engineers, and product teams selecting appropriate tools for their specific use cases.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol-based external data integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented coding environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## 1. Agent Memory & Context

### Description
Systems for long-term persistence, state management, and semantic recall for [[AI Agents]]. These tools enable agents to maintain context across multiple sessions and interactions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Preserving user preferences across sessions
- Maintaining [[Codebase Context]] for development agents
- Building persistent [[Conversational AI]] systems
- Semantic memory retrieval for complex workflows

### When to Use
Use when agents need to "remember" user preferences or codebase context across sessions. Critical for applications requiring continuity and personalization.

---

## 2. Agent Orchestration & Frameworks

### Description
Logic engines that manage multi-step planning and multi-agent collaboration. These frameworks provide the foundational architecture for coordinating complex AI workflows.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Key Concepts
- **Multi-Agent Systems**: Coordinating multiple [[AI Agents]] toward common goals
- **Workflow Orchestration**: Managing sequential and parallel task execution
- **Agent Planning**: Enabling agents to decompose complex problems
- **Collaboration Protocols**: Defining inter-agent communication patterns

### Use Cases
- Building complex multi-step workflows
- Coordinating specialized agents with different capabilities
- Creating autonomous systems that can adapt to changing conditions
- Implementing hierarchical task decomposition

### When to Use
Use for complex workflows where one "brain" isn't enough. Ideal when you need multiple specialized agents working together or sequential task pipelines requiring decision-making.

---

## 3. MCP & Data Tools

### Description
Standardized protocols for connecting [[Large Language Models]] to external data sources and local machine tools. The [[Model Context Protocol]] (MCP) provides a unified interface for tool integration.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Key Concepts
- **Model Context Protocol**: Standardized interface for LLM tool access
- **Data Integration**: Connecting models to structured and unstructured data
- **Local Machine Tools**: Enabling file system and application access
- **API Bridging**: Connecting to third-party services and databases

### Use Cases
- Integrating LLMs with local development environments
- Connecting models to specialized databases
- Automating workflows through third-party APIs
- Providing real-time data access to models

### When to Use
Use when bridging the gap between the model and your local file system or specific databases. Essential for applications requiring dynamic data access or system integration.

---

## 4. RAG & Document Processing

### Description
Ingestion pipelines that convert unstructured data (PDFs, videos, websites) into searchable vector representations. [[Retrieval-Augmented Generation]] (RAG) enables models to reference external knowledge bases.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Key Concepts
- **Document Parsing**: Extracting text from PDFs, images, and videos
- **Vectorization**: Converting text to embeddings for semantic search
- **Vector Databases**: Storing and retrieving semantic embeddings
- **Evaluation Metrics**: Assessing RAG system quality and relevance

### Use Cases
- Building "Chat with your Docs" features
- Creating searchable knowledge bases
- Implementing semantic document retrieval
- Processing multi-modal documents (text, images, video)

### When to Use
Use when you need to build applications that can search and reason over custom documents or data sources. Essential for knowledge-intensive applications.

---

## 5. Computer Use & Browser Automation

### Description
Tools enabling [[AI Agents]] to interact with user interfaces, click buttons, navigate websites, and perform actions like humans. Bridges the gap between [[Large Language Models]] and desktop/web applications.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Key Concepts
- **UI Automation**: Programmatic interaction with graphical interfaces
- **Web Navigation**: Autonomous browsing and information extraction
- **Visual Understanding**: Processing screenshots and visual layouts
- **Human-in-the-Loop**: Combining automation with human oversight

### Use Cases
- Automated web research and information gathering
- Testing web applications at scale
- Automating repetitive UI tasks
- Creating assistants that interact with legacy systems

### When to Use
Use for automated web research or "human-in-the-loop" UI tasks. Valuable when you need to interact with systems that don't expose APIs or when visual understanding is required.

---

## 6. Evaluation, Security & Ops

### Description
Testing, monitoring, and securing [[Large Language Model]] outputs to prevent [[Hallucinations]], data leaks, and ensure production reliability. Includes [[Red Teaming]] and continuous monitoring solutions.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU,