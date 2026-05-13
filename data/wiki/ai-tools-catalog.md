---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-13T05:53:01.175837
raw_file_updated: 2026-05-13T05:53:01.175837
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-13T05:53:01.175837
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive collection of software solutions and frameworks designed to build, deploy, and manage artificial intelligence applications. This catalog organizes over 300 tools across ten functional categories, enabling developers and organizations to construct sophisticated AI systems from specialized components.

## Summary

This catalog represents the modern AI development ecosystem, spanning from low-level inference engines to high-level orchestration frameworks. The tools enable practitioners to implement complete AI workflows: from managing agent memory and context, through data processing and retrieval, to monitoring and evaluation in production environments.

---

## Categories

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for agents.

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Context Mode, Qodo Aware, Repo Prompt, Claude Context Semantic Search

**Use Cases:** 
- Agents that need to "remember" user preferences across sessions
- Maintaining [[codebase context]] for code-generation tools
- Building personalized AI assistants with long-term learning

**Related Concepts:** [[Agent Orchestration]], [[State Management]], [[Semantic Search]]

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** AutoGen, CrewAI, LangChain/LangGraph, Smolagents, DSPy, OpenAI Agent SDK, CopilotKit, PySpur, Agno, Camel-AI, Julep-AI, Flock AI, Langflow, Flowise, Gumloop, n8n, Rivet

**Use Cases:**
- Complex workflows where multiple agents collaborate
- Multi-step planning and task decomposition
- Building autonomous systems with hierarchical control

**Related Concepts:** [[Multi-Agent Systems]], [[Workflow Automation]], [[AI Planning]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Purpose:** Standardized protocols for connecting LLMs to external data and local machine tools.

**Key Tools:** Google MCP Toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, OpenTools, MCP Studio, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging the gap between models and local file systems
- Integrating with specific databases and APIs
- Standardizing tool access across different LLM providers

**Related Concepts:** [[Model Context Protocol]], [[API Integration]], [[Tool Use]]

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that turn messy PDFs, videos, and websites into searchable vectors.

**Key Tools:** LangExtract, LlamaParse, LiteParse, Docling (IBM), RAGFlow, ragi.ai, LlamaExtract, LLamaIndex, Mistral OCR, GroudX, Unstructured, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Use Cases:**
- Building "Chat with your Docs" features
- Processing unstructured data at scale
- Creating searchable knowledge bases from diverse sources

**Related Concepts:** [[Retrieval-Augmented Generation]], [[Vector Databases]], [[Document Understanding]]

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing agents to interact with UIs, click buttons, and navigate the web like a human.

**Key Tools:** Vercel Labs Agent Browser, Claude Dev-Browser, WebRover, BrowserBase, Stagehand, Playwright, Google Mariner, Browser Use, Omniparser (Microsoft), Agentdesk, Computer Use (Anthropic)

**Use Cases:**
- Automated web research and data collection
- Human-in-the-loop UI task automation
- Building agents that can navigate complex web applications

**Related Concepts:** [[UI Automation]], [[Web Scraping]], [[Agent Perception]]

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing LLM outputs to prevent hallucinations and leaks.

**Key Tools:** DeepEval, Guardrails AI, LlamaGuard, Opik, LangSmith, Langfuse, AgentOps, Arize, Weights and Biases, Helicone, LM Evaluation Harness, EvalVerse, LiveBench, BigBench, SuperGLUE, TruthfulQA

**Use Cases:**
- Production-grade safety and reliability testing
- Monitoring model performance and drift
- Red-teaming and adversarial evaluation
- Compliance and hallucination detection

**Related Concepts:** [[LLM Evaluation]], [[AI Safety]], [[Observability]], [[Model Monitoring]]

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented environments for faster code writing and repository management.

**Key Tools:** Cursor, Windsurf, Warp.dev, Graphite, Codium, GitHub Copilot, LM Studio, Tabnine, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode

**Use Cases:**
- Accelerating daily development cycles
- Intelligent code completion and generation
- Repository understanding and navigation
- Pair programming with AI assistants

**Related Concepts:** [[AI-Assisted Development]], [[Code Generation]], [[Developer Experience]]

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Key Tools:** Veo2, Landing AI, Superwhisper, Cartesia AI, Murfai, Play AI, Parakeet, Assembly AI, Eleven Labs, FastRTC, Freepik, Gradio, Streamlit, Gamma.app, Mistral OCR

**Use Cases:**
- Building voice assistants and conversational interfaces
- Visual analysis and object detection
- Multi-modal content generation
- Accessibility features through audio/visual processing

**Related Concepts:** [[Multimodal AI]], [[Speech Recognition]], [[Computer Vision]], [[Audio Synthesis]]

---

### 9. Serving, Inference & Fine-tuning

**Purpose:** Backend infrastructure to host models and fine-tune them on your own data.

**Key Tools:** vLLM, Ollama, LM Studio, LlamaCPP, Unsloth, LlamaFactory, Fireworks AI, Lorax, LitServe, FAST API, SGLang, OUMI

**Use Cases:**
- Moving from prompts to hosted, scalable APIs
- Fine-tuning models on proprietary data
- Optimizing inference performance and cost
- Running models locally or on custom hardware

**Related Concepts:** [[Model Serving]], [[Fine-tuning]], [[Inference Optimization]], [[Model Deployment]]

---

### 10. Miscellaneous & General

**Purpose:** Workflow automation, synthetic data, prompt engineering utilities, and cross-cutting tools.

**Key Tools:** Kestra, Fabric, Instructor, Prompt Boost, Repo Prompt, Leverage.ai, Pixeltable, Instructlab, Meta Synthetic Data Kit, Tiktokenizer, Postman, Vellum, Tableau, Data Formulator

**Use Cases:**
- Prompt engineering and optimization
- Synthetic data generation for training
- Workflow orchestration and automation
- Token counting and cost estimation
- Data visualization and exploration

**Related Concepts:** [[Prompt Engineering]], [[Synthetic Data]], [[Workflow Automation]], [[Data Processing]]

---

## Key Concepts

### Essential Patterns

- **[[Agent-Based Systems]]** - Autonomous entities that perceive, plan, and act
- **[[Retrieval-Augmented Generation (RAG)]]** - Combining retrieval with generation for grounded responses
- **[[Multi-Agent Collaboration]]** - Coordinating multiple specialized agents
- **[[Observability and Monitoring]]** - Tracking AI system behavior in production
- **[[Safety and Alignment]]** - Ensuring AI systems behave as intended

### Technical Foundations

- [[Vector Databases]] - Storing and querying high-dimensional embeddings
- [[Model Context Protocol]] - Standard interface for tool integration
- [[Fine-tuning]] - Adapting pre-trained models to specific domains
- [[Inference Optimization]] - Improving speed and cost of model execution
- [[Evaluation Metrics]] - Measuring AI