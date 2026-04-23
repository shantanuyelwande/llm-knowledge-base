---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-23T04:54:53.405075
raw_file_updated: 2026-04-23T04:54:53.405075
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-23T04:54:53.405075
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system for modern artificial intelligence development tools and platforms. It organizes over 300+ software solutions across 10 primary categories, enabling developers, data scientists, and AI engineers to identify and select appropriate tools for specific tasks in the AI development lifecycle.

## Table of Contents

1. [[Agent Memory & Context]]
2. [[Agent Orchestration & Frameworks]]
3. [[Model Context Protocol]]
4. [[Retrieval Augmented Generation]]
5. [[Computer Use & Browser Automation]]
6. [[Evaluation, Security & Operations]]
7. [[Developer Tools & IDEs]]
8. [[Voice & Vision Models]]
9. [[Model Serving & Inference]]
10. [[AI Utilities & Miscellaneous Tools]]

---

## 1. Agent Memory & Context

### Overview
Systems designed for long-term persistence, state management, and semantic recall in [[AI Agents]]. These tools enable intelligent systems to maintain context and "remember" information across multiple sessions.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

### Use Cases
- Persistent user preference tracking across sessions
- Codebase context retention for development agents
- Long-term conversation history management
- Semantic knowledge recall for multi-turn interactions

### Related Concepts
- [[Agent Orchestration & Frameworks]]
- [[Retrieval Augmented Generation]]

---

## 2. Agent Orchestration & Frameworks

### Overview
Logic engines that manage multi-step planning and coordinate collaboration between multiple [[AI Agents]]. These frameworks provide the foundational architecture for complex, multi-agent workflows.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

### Use Cases
- Complex multi-step workflows requiring orchestration
- Multi-agent collaboration systems
- Workflow automation and task decomposition
- Agentic reasoning and planning pipelines

### Related Concepts
- [[Agent Memory & Context]]
- [[Model Context Protocol]]
- [[Evaluation, Security & Operations]]

---

## 3. Model Context Protocol

### Overview
Standardized protocols and tools for connecting [[Large Language Models]] to external data sources and local machine tools. The Model Context Protocol (MCP) enables seamless integration between AI models and external systems.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging LLMs and local file systems
- Database connectivity for AI systems
- Integration with specialized tools and APIs
- Real-time data access for model context

### Related Concepts
- [[Agent Orchestration & Frameworks]]
- [[Retrieval Augmented Generation]]
- [[Computer Use & Browser Automation]]

---

## 4. Retrieval Augmented Generation

### Overview
Ingestion and processing pipelines that transform unstructured data (PDFs, videos, websites) into searchable vector representations. [[RAG]] systems enable models to reference external knowledge sources accurately.

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

### Use Cases
- "Chat with your Docs" applications
- Document-based question answering
- Multi-format data ingestion (PDF, video, web)
- Vector database management
- Semantic search implementations

### Related Concepts
- [[Model Context Protocol]]
- [[Agent Memory & Context]]
- [[Large Language Models]]

---

## 5. Computer Use & Browser Automation

### Overview
Tools enabling [[AI Agents]] to interact with user interfaces, execute clicks, navigate web content, and perform tasks autonomously like a human user. These systems bridge the gap between AI and graphical interfaces.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

### Use Cases
- Automated web research and information gathering
- Human-in-the-loop UI task automation
- Web scraping and data extraction
- Cross-platform application testing
- Autonomous web navigation and interaction

### Related Concepts
- [[Agent Orchestration & Frameworks]]
- [[Model Context Protocol]]
- [[Evaluation, Security & Operations]]

---

## 6. Evaluation, Security & Operations

### Overview
Comprehensive testing, monitoring, and security frameworks for [[Large Language Models]] in production environments. These tools ensure reliability, safety, and prevent hallucinations and data leaks.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

### Use Cases
- LLM output validation and safety testing
- Red-teaming and adversarial evaluation
- Production monitoring and observability
- Hallucination detection and mitigation
- Benchmark evaluation and performance tracking
- Security and compliance verification

### Related Concepts
- [[Agent Orchestration & Frameworks]]
- [[Model Serving & Inference]]
- [[Large Language Models]]

---

## 7. Developer Tools & IDEs

### Overview
AI-augmented development environments that enhance code writing speed, repository management, and software engineering workflows. These tools integrate [[Large Language Models]] directly into the development process.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

### Use Cases
- Accelerated code generation and completion
- Repository understanding and navigation
- AI-assisted code review and refactoring
- Documentation generation
- Context-aware development assistance

### Related Concepts
- [[Large Language Models]]
- [[Model Serving & Inference]]
- [[Agent Memory & Context]]

---

## 8. Voice & Vision Models

### Overview
Multi-modal [[Machine Learning]] tools for generating, processing, and analyzing audio, images, and video content. These systems enable voice assistants, visual analysis, and cross-modal AI applications.

### Key Tools
Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs, Murfai, Play ai, Parakeet, Assembly ai, Eleven labs, FastRTC