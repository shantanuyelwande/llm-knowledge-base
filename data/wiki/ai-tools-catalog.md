---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-06T05:33:18.355080
raw_file_updated: 2026-05-06T05:33:18.355080
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-06T05:33:18.355080
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system organizing modern artificial intelligence tools and frameworks into ten functional categories. This catalog serves as a reference guide for developers, engineers, and organizations selecting appropriate tools for building AI-powered applications, from simple chatbots to complex multi-agent systems.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term state and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step workflows and collaboration |
| [[Model Context Protocol & Data Tools]] | 19 | LLM-to-external-system integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model hosting and optimization |
| [[Miscellaneous & General Tools]] | 36 | Utilities and automation |

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

### Purpose

Systems designed for long-term persistence, state management, and semantic recall for [[AI Agents]]. These tools enable agents to maintain context across multiple sessions and interactions.

### When to Use

- Agents that need to "remember" user preferences across sessions
- Applications requiring access to codebase context over time
- Systems where conversation history must inform future interactions
- [[Chatbot]] applications requiring personalization

### Key Concepts

- **Long-term persistence:** Storing agent state beyond single conversations
- **Semantic recall:** Retrieving contextually relevant information from memory
- **State management:** Tracking agent configuration and user preferences

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Purpose

Logic engines that manage [[multi-step planning]] and [[multi-agent collaboration]]. These frameworks orchestrate complex workflows where multiple AI agents work together to solve problems.

### When to Use

- Complex workflows requiring multiple sequential steps
- Applications where a single "brain" is insufficient
- Systems requiring inter-agent communication and coordination
- [[Workflow automation]] scenarios with conditional logic

### Key Concepts

- **Multi-agent systems:** Multiple AI agents working toward common goals
- **Planning engines:** Logic for determining action sequences
- **Collaboration protocols:** Mechanisms for agents to share information and coordinate

---

## 3. Model Context Protocol & Data Tools

**Tool Count:** 19 tools

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Purpose

Implements standardized protocols for connecting [[Large Language Models|LLMs]] to external data sources and local machine tools. The [[Model Context Protocol]] (MCP) provides a unified interface for tool integration.

### When to Use

- Bridging the gap between models and local file systems
- Connecting LLMs to specific databases or APIs
- Building [[Tool-use capabilities]] for AI agents
- Standardizing tool integration across platforms

### Key Concepts

- **Model Context Protocol:** Standardized interface for LLM-tool communication
- **Tool binding:** Connecting external systems to AI models
- **Data integration:** Providing models access to real-time information

---

## 4. RAG & Document Processing

**Tool Count:** 24 tools

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Purpose

Ingestion pipelines that convert unstructured data (PDFs, videos, websites) into searchable vector representations. These tools enable [[Retrieval-Augmented Generation]] (RAG) systems.

### When to Use

- Building "Chat with your Docs" features
- Creating searchable knowledge bases from documents
- Processing multi-format content (text, images, video)
- Implementing [[Semantic Search]] capabilities

### Key Concepts

- **Document parsing:** Extracting structured data from unstructured sources
- **Vectorization:** Converting text to embeddings for semantic search
- **Vector databases:** Storage and retrieval of embeddings
- **RAG pipeline:** Combining retrieval with generation for accurate responses

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Key Tools:** Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Purpose

Enables [[AI Agents]] to interact with user interfaces, click buttons, fill forms, and navigate the web like a human. These tools provide programmatic control over browser and desktop environments.

### When to Use

- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- Testing and quality assurance workflows
- Web scraping and content extraction
- Repetitive form-filling and data entry

### Key Concepts

- **UI automation:** Programmatic interaction with graphical interfaces
- **Browser control:** Remote operation of web browsers
- **Screen understanding:** Computer vision for identifying UI elements
- **Action sequencing:** Planning multi-step interactions

---

## 6. Evaluation, Security & Ops

**Tool Count:** 28 tools

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Purpose

Testing, monitoring, and securing [[Large Language Model|LLM]] outputs to prevent [[Hallucination|hallucinations]], data leaks, and unsafe behavior. These tools are essential for [[Production AI]] systems.

### When to Use

- Production-grade AI deployments
- Compliance and regulatory requirements
- Red-teaming and adversarial testing
- Performance monitoring and optimization
- Safety and alignment verification

### Key Concepts

- **Evaluation metrics:** Measuring model performance (BLEU, ROUGE, etc.)
- **Red teaming:** Adversarial testing to find vulnerabilities
- **Guardrails:**