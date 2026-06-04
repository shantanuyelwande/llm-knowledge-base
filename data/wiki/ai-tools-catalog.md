---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-04T06:47:02.097620
raw_file_updated: 2026-06-04T06:47:02.097620
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-04T06:47:02.097620
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive classification system organizing over 250 artificial intelligence tools and frameworks into ten functional categories. This catalog serves as a reference guide for developers, engineers, and organizations selecting appropriate solutions for specific AI implementation challenges, from [[Agent Memory & Context]] to [[Voice & Vision Models]].

---

## Table of Contents

1. [[Agent Memory & Context]]
2. [[Agent Orchestration & Frameworks]]
3. [[Model Context Protocol (MCP) & Data Tools]]
4. [[RAG & Document Processing]]
5. [[Computer Use & Browser Automation]]
6. [[Evaluation, Security & Ops]]
7. [[Developer Tools & IDEs]]
8. [[Voice & Vision Models]]
9. [[Serving, Inference & Fine-tuning]]
10. [[Miscellaneous & General AI Tools]]

---

## 1. Agent Memory & Context

### Overview
Systems designed for long-term persistence, state management, and semantic recall in AI agents.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Context Mode, Context7, Skillscreator, Skills.sh, Skills Patterns (Google), Qodo Aware, Repo Prompt, Claude Context Semantic Search

### Use Cases
- Maintaining user preferences across multiple sessions
- Preserving codebase context for [[code generation]] tasks
- Building stateful [[AI agents]] that learn from interactions
- Implementing semantic recall for complex domain knowledge

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Evaluation, Security & Ops]]

---

## 2. Agent Orchestration & Frameworks

### Overview
Logic engines that manage multi-step planning and coordinate collaboration between multiple agents. These frameworks form the backbone of complex AI workflows.

### Key Tools
Goose AI, Autoagent Harness, Hermes, Ralph Orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic Agents, DSpy, OpenAI Agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph Builder, Rivet

### Use Cases
- Orchestrating multi-step workflows requiring sequential decision-making
- Enabling multi-agent systems to collaborate on complex problems
- Building autonomous workflows that require planning and reasoning
- Creating no-code/low-code AI application builders

### Related Concepts
[[Agent Memory & Context]], [[Developer Tools & IDEs]], [[Evaluation, Security & Ops]]

---

## 3. Model Context Protocol (MCP) & Data Tools

### Overview
Standardized protocols and tools for connecting [[Large Language Models]] to external data sources and local machine tools. MCP enables seamless integration between AI models and diverse data ecosystems.

### Key Tools
Google MCP Toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

### Use Cases
- Bridging [[Large Language Models]] and local file systems
- Connecting models to specialized databases and data warehouses
- Enabling real-time data access for [[AI agents]]
- Standardizing tool integration across multiple AI platforms

### Related Concepts
[[RAG & Document Processing]], [[Serving, Inference & Fine-tuning]]

---

## 4. RAG & Document Processing

### Overview
Retrieval-Augmented Generation (RAG) systems and ingestion pipelines that transform unstructured data (PDFs, videos, websites) into searchable, vectorized formats for [[Large Language Models]].

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Ragflow, ragi.ai (video), LlamaExtract, Vectorize, LlamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag Eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

### Use Cases
- Building "Chat with Your Documents" features
- Processing multi-modal content (text, images, video)
- Creating semantic search capabilities over proprietary documents
- Implementing context-aware [[AI agents]] with document access
- Evaluating RAG pipeline quality and relevance

### Related Concepts
[[Model Context Protocol (MCP) & Data Tools]], [[Voice & Vision Models]], [[Evaluation, Security & Ops]]

---

## 5. Computer Use & Browser Automation

### Overview
Tools enabling [[AI agents]] to interact with user interfaces, execute clicks, navigate websites, and perform automated tasks that require visual understanding and UI manipulation.

### Key Tools
Vercel Labs Agent Browser, Claude Dev-Browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy Web Agent, Vibetest, Browser Use (Smooth/OpenAI/Open), Proxy Lite, Omniparser (Microsoft), Agentdesk, Simular, Computer Use (Anthropic)

### Use Cases
- Automating web research and data gathering
- Performing repetitive UI-based tasks without human intervention
- Building "human-in-the-loop" systems with agent assistance
- Testing web applications through automated interaction
- Enabling agents to navigate complex web applications

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Voice & Vision Models]], [[Developer Tools & IDEs]]

---

## 6. Evaluation, Security & Ops

### Overview
Comprehensive suite of tools for testing, monitoring, securing, and operationalizing [[Large Language Models]] in production environments. These tools prevent hallucinations, detect security vulnerabilities, and ensure reliability.

### Key Tools
Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red Teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation Harness, EvalVerse, Livebench, BLEU, ROUGE, BigBench, SuperGLUE, TruthfulQA

### Use Cases
- Red-teaming [[AI agents]] to identify security vulnerabilities
- Monitoring model outputs for hallucinations and factual errors
- Evaluating model performance against standardized benchmarks
- Tracking and logging agent behavior in production
- Implementing guardrails to prevent harmful outputs
- Measuring model reliability and safety metrics

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Serving, Inference & Fine-tuning]], [[Developer Tools & IDEs]]

---

## 7. Developer Tools & IDEs

### Overview
AI-augmented development environments that accelerate [[code generation]], repository management, and the daily development workflow through intelligent assistance.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment Code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

### Use Cases
- Accelerating code writing with intelligent suggestions
- Generating boilerplate and repetitive code patterns
- Analyzing and refactoring existing codebases
- Creating interactive development canvases
- Integrating AI assistance into version control workflows
- Building AI-native development environments

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Evaluation, Security & Ops]], [[Serving, Inference & Fine-tuning]]

---

## 8. Voice & Vision Models

### Overview
Multi-modal tools for generating, processing, and analyzing