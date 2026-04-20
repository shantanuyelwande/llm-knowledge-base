---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-20T05:17:50.458539
raw_file_updated: 2026-04-20T05:17:50.458539
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-20T05:17:50.458539
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ tools across 10 primary categories, enabling developers and organizations to select appropriate solutions for specific AI implementation challenges. This catalog serves as a reference guide for building [[AI Agent|AI agents]], processing data, managing infrastructure, and deploying production-grade AI systems.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term state persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and agent collaboration |
| [[MCP (Model Context Protocol)]] | 19 | External data and tool integration |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and security |
| [[Developer Tools & IDEs]] | 22 | Code generation and repository management |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Categories

### 1. Agent Memory & Context

**Tool Count:** 18

**Key Tools:** Mem0, Claude-mem, Letta/Mem-GPT, Zep, Cognee, Repo Prompt, Claude context semantic search

**Description:**
Systems designed for long-term persistence, state management, and semantic recall in [[AI Agent|AI agents]]. These tools enable agents to maintain context across multiple sessions and retrieve relevant information efficiently.

**Primary Use Cases:**
- Remembering user preferences across conversations
- Maintaining codebase context for development agents
- Semantic recall of historical interactions
- Persistent state management for multi-session workflows

**When to Use:**
Choose these tools when your agents need to "remember" information beyond a single conversation or when you require sophisticated context management for complex workflows.

**Related Concepts:** [[Agent Orchestration & Frameworks]], [[RAG & Document Processing]]

---

### 2. Agent Orchestration & Frameworks

**Tool Count:** 32

**Key Tools:** AutoGen, CrewAI, Langchain/Langgraph, Smolagents, DSpy, OpenAI Agent SDK, Copilotkit, Camel-AI, n8n, Flowise

**Description:**
Logic engines that manage multi-step planning and coordinate collaboration between multiple agents. These frameworks provide the foundational architecture for complex AI workflows requiring orchestrated decision-making and task distribution.

**Primary Use Cases:**
- Multi-agent collaboration systems
- Complex workflow automation
- Sequential task planning and execution
- Conditional logic and branching workflows
- Agent communication and coordination

**When to Use:**
Deploy orchestration frameworks when a single "brain" is insufficient—when you need multiple agents working together, complex planning logic, or workflows that span multiple steps with dependencies.

**Related Concepts:** [[AI Agent]], [[Agent Memory & Context]], [[MCP (Model Context Protocol)]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Tool Count:** 19

**Key Tools:** Google MCP Toolbox, KitOps MCP, Smithery, Composio, Zapier, Pixeltable, Dataverse

**Description:**
Standardized protocols and tools for connecting [[Large Language Model|Large Language Models]] to external data sources and local machine capabilities. MCP establishes a unified interface between models and the tools they need to access.

**Primary Use Cases:**
- Connecting models to local file systems
- Database integration and querying
- API connectivity and service integration
- Standardized tool interface management
- Data pipeline orchestration

**When to Use:**
Use MCP tools when you need to bridge the gap between your model and external systems—whether that's your local file system, specific databases, or third-party APIs.

**Related Concepts:** [[RAG & Document Processing]], [[Agent Orchestration & Frameworks]], [[Serving, Inference & Fine-tuning]]

---

### 4. RAG & Document Processing

**Tool Count:** 24

**Key Tools:** LlamaIndex, Llamaparse, Docling (IBM), Unstructured, Milvus DB, QDrant, pgVector, ChromaDB, Elastic Search

**Description:**
Retrieval-Augmented Generation (RAG) ingestion pipelines that transform unstructured data—PDFs, videos, websites—into searchable vector representations. These tools enable semantic search and knowledge retrieval for AI systems.

**Primary Use Cases:**
- "Chat with your Docs" applications
- Document ingestion and preprocessing
- Vector database management
- Multi-modal document parsing (text, images, video)
- Semantic search implementation
- Knowledge base construction

**When to Use:**
Build with RAG tools when you need to enable AI systems to search and retrieve information from large document collections, creating context-aware responses based on your proprietary data.

**Related Concepts:** [[Agent Memory & Context]], [[MCP (Model Context Protocol)]], [[Large Language Model]]

---

### 5. Computer Use & Browser Automation

**Tool Count:** 20

**Key Tools:** Claude Dev-Browser, Playwright, BrowserBase, Stagehand, Google Mariner, Omniparser (Microsoft), Computer Use (Anthropic)

**Description:**
Tools that enable [[AI Agent|AI agents]] to interact with user interfaces, click buttons, navigate websites, and perform actions as a human would. These tools bridge the gap between AI systems and web-based applications.

**Primary Use Cases:**
- Automated web research and scraping
- Form filling and data entry automation
- Cross-website workflow automation
- UI-based testing and validation
- Human-in-the-loop task execution
- Visual element recognition and interaction

**When to Use:**
Deploy browser automation tools when you need agents to perform tasks that require UI interaction, visual navigation, or when existing APIs are unavailable. Ideal for "human-like" automation tasks.

**Related Concepts:** [[Agent Orchestration & Frameworks]], [[Evaluation, Security & Ops]]

---

### 6. Evaluation, Security & Ops

**Tool Count:** 28

**Key Tools:** DeepEval, Guardrails AI, LlamaGuard, LangSmith, Langfuse, AgentOps, Weights and Biases, OpenTelemetry, LM Evaluation Harness

**Description:**
Comprehensive testing, monitoring, and security frameworks for [[Large Language Model|LLM]] outputs and agent behavior. These tools ensure reliability, safety, and compliance in production AI systems.

**Primary Use Cases:**
- Hallucination detection and prevention
- Security testing and red-teaming
- Performance monitoring and observability
- Model evaluation and benchmarking
- Prompt injection prevention
- Data leak detection
- Compliance and audit logging

**When to Use:**
Essential for production-grade AI systems. Implement evaluation and security tools before deploying to users to ensure safety, reliability, and regulatory compliance.

**Related Concepts:** [[Agent Orchestration & Frameworks]], [[Serving, Inference & Fine-tuning]], [[Developer Tools & IDEs]]

---

### 7. Developer Tools & IDEs

**Tool Count:** 22

**Key Tools:** Cursor, Windsurf, Github Copilot, Warp.dev, LM Studio, Tabnine, Codium, Project IDX

**Description:**
AI-augmented integrated development environments and command-line tools that accelerate software development through intelligent code generation, completion, and repository management.

**Primary Use Cases:**
- Code generation and completion
- Repository navigation and understanding
- Refactoring suggestions
- Documentation generation
- Testing assistance
- Git workflow optimization

**When to Use:**
Integrate into your daily development cycle to increase productivity. These tools are particularly valuable for rapid prototyping, learning new codebases, and reducing boilerplate code writing.

**Related Concepts:** [[Serving, Inference & Fine-tuning]], [[Evaluation, Security & Ops]]

---

### 8. Voice & Vision Models

**Tool Count:** 21

**Key Tools:** Veo2 (video), Eleven Labs, Assembly AI, Superwhisper, Cartesia AI, Landing AI, Freepik, Mistral OCR

**Description:**
Multi-modal tools for generating and processing audio, images, and video content. These models enable voice assistants, visual analysis, and cross-modal AI applications.

**Primary Use Cases:**
- Text-to-speech and voice synthesis
- Speech-to-text transcription
- Image generation and editing
- Video generation and