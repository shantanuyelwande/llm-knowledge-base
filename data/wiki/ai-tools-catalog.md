---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-07-01T06:39:14.985496
raw_file_updated: 2026-07-01T06:39:14.985496
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-07-01T06:39:14.985496
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and frameworks designed to support artificial intelligence development, deployment, and operations. This catalog organizes over 300+ AI tools into ten functional categories, each addressing specific aspects of the AI development lifecycle—from agent memory management to production monitoring and evaluation.

## Quick Summary

| Category | Tool Count | Primary Purpose |
|----------|-----------|-----------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data connection |
| [[RAG & Document Processing]] | 24 | Document ingestion and vector search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and specialized tools |

---

## 1. Agent Memory & Context

### Purpose
Systems for long-term persistence, state management, and semantic recall for agents.

### Key Tools
Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search.

### Use Cases
- Enabling agents to "remember" user preferences across sessions
- Maintaining [[Codebase Context|codebase context]] for extended interactions
- Preserving conversational history for multi-turn dialogues
- Semantic recall of relevant information from past interactions

### Related Concepts
[[Agent Orchestration & Frameworks]], [[RAG & Document Processing]]

---

## 2. Agent Orchestration & Frameworks

### Purpose
Logic engines that manage multi-step planning and multi-agent collaboration.

### Key Tools
Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet.

### Use Cases
- Complex workflows requiring multiple AI agents
- Multi-step planning and task decomposition
- Coordinating different specialized agents
- Building no-code/low-code AI automation workflows

### Related Concepts
[[Agent Memory & Context]], [[Evaluation, Security & Ops]], [[Developer Tools & IDEs]]

---

## 3. MCP (Model Context Protocol) & Data Tools

### Purpose
Standardized protocols for connecting [[Large Language Models|LLMs]] to external data and local machine tools.

### Key Tools
Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse.

### Use Cases
- Bridging the gap between models and local file systems
- Connecting to specific databases and APIs
- Standardizing tool integration across platforms
- Enabling seamless data pipeline connections

### Related Concepts
[[RAG & Document Processing]], [[Computer Use & Browser Automation]], [[Serving, Inference & Fine-tuning]]

---

## 4. RAG & Document Processing

### Purpose
Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors for [[Retrieval-Augmented Generation|retrieval-augmented generation (RAG)]].

### Key Tools
Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara.

### Use Cases
- Building "Chat with your Docs" features
- Processing unstructured document data
- Creating searchable knowledge bases
- Video and multimedia ingestion
- Optical character recognition (OCR) workflows

### Related Concepts
[[Agent Memory & Context]], [[MCP & Data Tools]], [[Evaluation, Security & Ops]]

---

## 5. Computer Use & Browser Automation

### Purpose
Allowing agents to interact with user interfaces, click buttons, and navigate the web autonomously like a human operator.

### Key Tools
Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic).

### Use Cases
- Automated web research and data collection
- "Human-in-the-loop" UI task automation
- End-to-end web application testing
- Robotic process automation (RPA)
- Screen understanding and navigation

### Related Concepts
[[Agent Orchestration & Frameworks]], [[MCP & Data Tools]], [[Evaluation, Security & Ops]]

---

## 6. Evaluation, Security & Ops

### Purpose
Testing, monitoring, and securing [[Large Language Models|LLM]] outputs to prevent hallucinations, security breaches, and ensure reliability in production environments.

### Key Tools
Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa.

### Use Cases
- Production-grade safety assurance
- Hallucination detection and prevention
- Red-teaming and adversarial testing
- Monitoring model performance in production
- Compliance and audit logging
- Benchmark evaluation against standard datasets

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Serving, Inference & Fine-tuning]], [[Developer Tools & IDEs]]

---

## 7. Developer Tools & IDEs

### Purpose
AI-augmented development environments that accelerate code writing, repository management, and software engineering workflows.

### Key Tools
Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net.

### Use Cases
- Daily development cycle acceleration
- Code generation and completion
- Repository understanding and navigation
- Collaborative AI-assisted coding
- Canvas-based code visualization
- Documentation generation

### Related Concepts
[[Agent Orchestration & Frameworks]], [[Evaluation, Security & Ops]], [[Serving, Inference & Fine-tuning]]

---

## 8. Voice & Vision Models

### Purpose
Multi-modal tools for generating and processing audio, images, and video content with AI capabilities.

### Key Tools
Veo2 (video), Landing