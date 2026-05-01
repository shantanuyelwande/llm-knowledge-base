---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:45:36.206895
raw_file_updated: 2026-05-01T05:45:36.206895
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:45:36.206895
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of 277+ software tools and platforms designed to support the development, deployment, and management of [[artificial intelligence]] systems. This catalog organizes tools across ten primary functional categories, from [[agent memory]] systems to [[inference]] infrastructure, providing developers and organizations with a structured reference for building production-grade AI applications.

## Summary

This catalog serves as a master reference for the AI development ecosystem, categorizing tools by their primary function and use case. Whether building [[multi-agent systems]], implementing [[retrieval-augmented generation]] (RAG), or deploying [[large language models]] at scale, this taxonomy helps practitioners identify the right tools for their specific needs.

---

## 1. Agent Memory & Context

**Category Focus:** Long-term persistence and semantic recall systems

**Tool Count:** 18 tools

**Key Tools:** Mem0, Claude-mem, Letta/Mem-GPT, Zep, Cognee, Repo Prompt, Claude context semantic search

### Description

Systems designed to enable [[agents]] to maintain state, remember user preferences, and recall contextual information across multiple sessions. These tools solve the fundamental problem of [[context window]] limitations in [[large language models]] by providing persistent storage layers and intelligent retrieval mechanisms.

### Primary Use Cases

- Maintaining user preference profiles across conversation sessions
- Storing and retrieving [[codebase]] context for code-generation agents
- Implementing [[semantic search]] over historical interactions
- Managing long-term [[knowledge graphs]] for agent reasoning

### Key Concepts

- [[Memory persistence]]
- [[State management]]
- [[Semantic recall]]
- [[Context retrieval]]

---

## 2. Agent Orchestration & Frameworks

**Category Focus:** Multi-agent coordination and workflow management

**Tool Count:** 32 tools

**Key Tools:** AutoGen, CrewAI, Langchain/Langgraph, DSpy, Smolagents, Camel-AI, n8n, Langflow, Flowise

### Description

Logic engines and frameworks that manage complex [[multi-agent systems]], enabling coordination between multiple specialized [[agents]], handling multi-step planning, and orchestrating [[workflows]] that require collaboration between different AI components. These platforms abstract away the complexity of agent communication and state management.

### Primary Use Cases

- Coordinating teams of specialized agents for complex tasks
- Managing sequential and parallel task execution
- Implementing hierarchical agent structures
- Building [[no-code]] and [[low-code]] AI applications
- Creating reusable [[agent patterns]]

### Key Concepts

- [[Multi-agent systems]]
- [[Workflow orchestration]]
- [[Agent communication]]
- [[Task planning]]
- [[Hierarchical reasoning]]

---

## 3. MCP (Model Context Protocol) & Data Tools

**Category Focus:** Standardized interfaces for data and tool integration

**Tool Count:** 19 tools

**Key Tools:** Google MCP Toolbox, KitOps MCP, Smithery, Composio, Zapier, Pixeltable, Airweave

### Description

Tools implementing the [[Model Context Protocol]] (MCP), a standardized specification for connecting [[large language models]] to external data sources, local machine tools, and APIs. These systems provide a unified interface layer that enables models to access real-time information and execute actions on external systems.

### Primary Use Cases

- Connecting models to local file systems and databases
- Integrating with third-party APIs and services
- Providing real-time data access to models
- Standardizing tool definitions across different AI platforms
- Building composable tool chains

### Key Concepts

- [[Model Context Protocol]]
- [[Tool integration]]
- [[API standardization]]
- [[Data source connectivity]]
- [[Composable systems]]

---

## 4. RAG & Document Processing

**Category Focus:** Data ingestion and vector-based retrieval

**Tool Count:** 24 tools

**Key Tools:** LlamaIndex, Llamaparse, Docling (IBM), Unstructured, Milvus, QDrant, ChromaDB, pgVector, Elasticsearch

### Description

Specialized tools for building [[retrieval-augmented generation]] (RAG) systems that transform unstructured documents—PDFs, websites, videos, and images—into searchable [[vector embeddings]]. These platforms handle document parsing, chunking, embedding, and vector storage, enabling "chat with your docs" functionality.

### Primary Use Cases

- Building document-based question-answering systems
- Creating searchable knowledge bases from enterprise documents
- Processing multi-modal content (PDFs, videos, websites)
- Implementing [[semantic search]] over large document collections
- Reducing [[hallucinations]] through grounded retrieval

### Key Concepts

- [[Retrieval-augmented generation]]
- [[Vector embeddings]]
- [[Document parsing]]
- [[Semantic search]]
- [[Vector databases]]
- [[Chunking strategies]]

---

## 5. Computer Use & Browser Automation

**Category Focus:** UI automation and web interaction

**Tool Count:** 20 tools

**Key Tools:** Claude Dev-Browser, Playwright, BrowserBase, Stagehand, Google Mariner, Omniparser (Microsoft), Computer Use (Anthropic)

### Description

Frameworks enabling [[agents]] to interact with graphical user interfaces, click buttons, navigate websites, and perform tasks that typically require human interaction. These tools bridge the gap between [[language models]] and the visual, interactive web, using techniques like [[visual parsing]] and [[UI element detection]].

### Primary Use Cases

- Automated web research and data scraping
- End-to-end workflow automation across web applications
- Testing and QA automation
- Building [[human-in-the-loop]] systems for complex tasks
- Enabling agents to use tools designed for human users

### Key Concepts

- [[Browser automation]]
- [[Visual parsing]]
- [[UI element detection]]
- [[Web scraping]]
- [[Human-in-the-loop systems]]

---

## 6. Evaluation, Security & Ops

**Category Focus:** Quality assurance, monitoring, and safety

**Tool Count:** 28 tools

**Key Tools:** DeepEval, Guardrails AI, LlamaGuard, LangSmith, Langfuse, AgentOps, Weights and Biases, Arize, OpenTelemetry

### Description

Essential tools for production deployment of AI systems, covering evaluation metrics, [[red teaming]], output validation, monitoring, and security. These platforms help detect [[hallucinations]], prevent data leaks, ensure compliance, and maintain system reliability in production environments.

### Primary Use Cases

- Evaluating [[model performance]] across multiple metrics
- Detecting and preventing [[hallucinations]] and false outputs
- Monitoring model behavior and performance in production
- Conducting [[red teaming]] and adversarial testing
- Implementing [[guardrails]] for safe model outputs
- Tracking and debugging agent behavior

### Key Concepts

- [[Model evaluation]]
- [[Hallucination detection]]
- [[Production monitoring]]
- [[Red teaming]]
- [[Guardrails]]
- [[Observability]]
- [[Compliance]]

---

## 7. Developer Tools & IDEs

**Category Focus:** AI-augmented development environments

**Tool Count:** 22 tools

**Key Tools:** Cursor, Windsurf, GitHub Copilot, VS Code extensions, LM Studio, Tabnine, Codium, RooCode

### Description

Integrated development environments (IDEs) and editor extensions augmented with [[AI capabilities]], enabling developers to write code faster, understand repositories, and leverage [[large language models]] directly in their workflow. These tools bridge the gap between development and AI assistance.

### Primary Use Cases

- Accelerating code writing with AI suggestions
- Understanding large codebases through AI analysis
- Generating tests and documentation
- Refactoring and code optimization
- Building AI-native applications
- Managing code repositories with AI assistance

### Key Concepts

- [[Code generation]]
- [[AI-augmented development]]
- [[Repository understanding]]
- [[Copilot systems]]
- [[IDE integration]]

---

## 8. Voice & Vision Models

**Category Focus:** Multi-modal AI processing

**Tool Count:** 21 tools

**Key Tools:** Eleven Labs, Assembly AI, Cartesia AI, Veo2, Landing AI, Superwhisper, FastRTC, Freepik

### Description

Tools for processing and generating audio, images, and video, extending AI capabilities beyond text. These platforms include [[speech recognition]], [[text-to-speech]], [[object detection]], [[image generation]], and [[video synthesis]], enabling creation of rich multi-modal applications.

### Primary Use Cases

- Building voice assistants and conversational interfaces
- Processing audio for transcription and analysis
- Implementing [[computer vision]] for object detection and analysis
- Generating synthetic images and videos
- Creating accessible interfaces through voice
- Building video analysis applications

###