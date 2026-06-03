---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-03T06:57:28.013171
raw_file_updated: 2026-06-03T06:57:28.013171
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-03T06:57:28.013171
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools, frameworks, and platforms designed to support the development, deployment, and management of [[artificial-intelligence|AI]] and [[large-language-models|LLM]]-powered applications. This catalog organizes over 300+ tools across ten primary categories, each addressing specific needs in the AI development lifecycle.

## Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and agent collaboration |
| [[Model Context Protocol|MCP & Data Tools]] | 19 | Protocol standardization and data connectivity |
| [[Retrieval-Augmented Generation|RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and security |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal AI processing |
| [[Model Serving & Inference]] | 17 | Deployment and fine-tuning infrastructure |
| [[Miscellaneous & General Tools]] | 36 | Utilities and workflow automation |

---

## Category Breakdown

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for agents.

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Context Mode, Context7 Skillscreator, Skills.sh, Skills Patterns Google, Qodo Aware, Repo Prompt, Claude Context Semantic Search

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- Maintaining [[codebase]] context for code-aware [[AI agents]]
- Long-term user interaction history and preference tracking
- [[Semantic search]] capabilities for historical context retrieval

**When to Use:** Essential when building [[conversational-AI|conversational agents]] or [[code-generation]] tools that require continuity across multiple interactions.

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, AutoAgent Harness, Hermes, Ralph Orchestrator, OpenCode, PentaAGI, RTK-AI, Smolagents, [[AutoGen]], [[CrewAI]], [[LangChain]]/[[LangGraph]], Atomic Agents, DSPy, OpenAI Agent SDK, Copilotkit, AutoAgent, Firebase.studio, AgentSDK, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-AI, Flock AI, [[Langflow]], Flowise, Gumloop, [[n8n]], LangGraph Builder, Rivet

**Use Cases:**
- Complex workflows requiring multiple specialized agents
- [[Multi-agent systems]] for collaborative problem-solving
- Sequential task execution and dependency management
- Agent communication protocols and message routing

**When to Use:** When a single "brain" isn't sufficient and you need multiple specialized [[AI agents]] working together toward a common goal.

---

### 3. Model Context Protocol & Data Tools

**Purpose:** Standardized protocols for connecting [[large-language-models|LLMs]] to external data sources and local machine tools.

**Key Tools:** Google MCP Toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, [[Composio]], Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging the gap between models and local file systems
- Connecting to specialized databases and APIs
- Standardized tool integration across multiple LLMs
- Real-time data fetching and processing

**When to Use:** When you need reliable, standardized communication between your [[LLM]] and external systems or local resources.

---

### 4. Retrieval-Augmented Generation & Document Processing

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[retrieval-augmented-generation|RAG]] systems.

**Key Tools:** LangExtract, LlamaParse, LiteParse, Docling (IBM), RAG Flow, ragi.ai (video), LlamaExtract, Vectorize, [[LlamaIndex]], Mistral OCR, GroudX, SmolDocling, OpenRAG Eval, SiteRAG, Unstructured, QMD CLI, QMD BM25, [[Milvus]] DB, [[Qdrant]], pgVector, [[Elasticsearch]], [[ChromaDB]], Colivara

**Use Cases:**
- Building "Chat with Your Docs" features
- Processing multi-format documents (PDF, images, video)
- Creating searchable [[vector databases]] for semantic retrieval
- Evaluating RAG system performance

**When to Use:** Essential for applications requiring document-based knowledge retrieval and [[semantic search]] capabilities.

---

### 5. Computer Use & Browser Automation

**Purpose:** Tools allowing [[AI agents]] to interact with user interfaces, click buttons, and navigate the web like a human.

**Key Tools:** Vercel Labs Agent Browser, Claude Dev-Browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, [[Playwright]], Convergence AI, Google Mariner, Proxy Web Agent, VibeTest, Browser Use (Smooth/OpenAI/Open), Proxy Lite, Omniparser (Microsoft), AgentDesk, Simular, Computer Use (Anthropic)

**Use Cases:**
- Automated web research and information gathering
- "Human-in-the-loop" UI task automation
- Web scraping and data extraction
- Testing and quality assurance automation
- Cross-browser compatibility testing

**When to Use:** When you need agents to autonomously interact with web interfaces or perform UI-based tasks.

---

### 6. Evaluation, Security & Operations

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, data leaks, and ensure reliability.

**Key Tools:** Deepteam, Parlant, Plano AI, [[DeepEval]], PentaAGI, DeepTeam LLM Red Teaming, Debug-Gym, [[Guardrails AI]], LlamaGuard, [[Opik]], [[LangSmith]], [[OpenTelemetry]], [[Langfuse]], LiteEval, LangWatch, [[AgentOps]], Arize, Weights and Biases, Helicone, Maxim, LM Evaluation Harness, EvalVerse, LiveBench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

**Use Cases:**
- [[LLM evaluation]] and benchmarking
- [[Red teaming]] and adversarial testing
- Production monitoring and observability
- Hallucination detection and mitigation
- [[Data privacy]] and security compliance
- Performance tracking and analytics

**When to Use:** Critical for production-grade AI systems requiring safety, reliability, and compliance verification.

---

### 7. Developer Tools & IDEs

**Purpose:** [[AI]]-augmented development environments for faster code writing and repository management.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, TalkToGitHub, [[Cursor]], Windsurf, Trae, CodeLLM, Augment Code, Codium, Qodo, [[GitHub Copilot]], LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Use Cases:**
- AI-assisted code completion and generation
- Repository understanding and navigation
- Documentation generation
- Code refactoring and optimization
- Integrated development workflows

**When to Use:** In your daily development cycle to increase productivity and code quality.

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images