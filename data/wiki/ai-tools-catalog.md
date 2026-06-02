---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-02T06:46:30.210074
raw_file_updated: 2026-06-02T06:46:30.210074
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-02T06:46:30.210074
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and frameworks designed to build, deploy, and manage [[artificial intelligence]] applications. This catalog organizes over 300+ tools across ten functional categories, providing developers and AI engineers with a structured reference for selecting appropriate technologies based on project requirements.

## Summary

Modern [[AI]] development requires specialized tools across multiple domains—from [[agent]] memory and orchestration to [[retrieval-augmented generation]] (RAG), browser automation, and production monitoring. This catalog serves as a master reference for understanding the AI development stack, helping teams identify the right tools for specific use cases in building [[large language model]] (LLM) applications.

---

## 1. Agent Memory & Context

**Tool Count:** 18 tools

**Primary Tools:** Mem0, Claude-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context Hub, Superpowers, Repo Prompt, Claude Context Semantic Search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[agents]].

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- Maintaining [[context]] of codebases for code-focused agents
- Building persistent user profiles and interaction histories
- Semantic recall of past conversations and decisions

**Key Concept:** These tools solve the stateless nature of traditional [[LLM]] APIs by providing memory layers that agents can query and update.

---

## 2. Agent Orchestration & Frameworks

**Tool Count:** 32 tools

**Primary Tools:** AutoGen, CrewAI, LangChain/LangGraph, Smolagents, Atomic Agents, DSPy, OpenAI Agent SDK, CopilotKit, PySpur, Agno, Camel-AI, Julep-ai, Langflow, Flowise, n8n, Rivet

**Purpose:** Logic engines that manage multi-step planning and multi-[[agent]] collaboration.

**Use Cases:**
- Complex workflows requiring sequential task execution
- Multi-agent systems where specialized agents collaborate
- Workflow automation with decision trees and branching logic
- Building autonomous systems with planning capabilities

**Key Concept:** [[Agent orchestration]] frameworks provide the "control flow" for AI systems, enabling agents to coordinate, hand off tasks, and work toward complex objectives. These are foundational to building production [[agentic systems]].

---

## 3. Model Context Protocol & Data Tools

**Tool Count:** 19 tools

**Primary Tools:** Google MCP Toolbox, KitOps MCP, Smithery, MCP CLI, Pixeltable, SDV Data Generator, Blender MCP 3D, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[LLMs]] to external data and local machine tools.

**Use Cases:**
- Integrating [[LLMs]] with local file systems
- Connecting models to specialized databases
- Enabling tool use through standardized interfaces
- Building extensible AI applications with pluggable data sources

**Key Concept:** The [[Model Context Protocol]] (MCP) provides a standardized way for [[language models]] to access external tools and data, similar to how APIs work but optimized for AI use cases.

---

## 4. Retrieval-Augmented Generation & Document Processing

**Tool Count:** 24 tools

**Primary Tools:** LangExtract, Llamaparse, Docling (IBM), Rag Flow, LlamaIndex, Unstructured, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Purpose:** Ingestion pipelines that convert messy PDFs, videos, and websites into searchable vectors for [[retrieval-augmented generation]].

**Use Cases:**
- Building "Chat with your Docs" features
- Processing unstructured documents at scale
- Creating searchable [[vector databases]] from diverse content
- Implementing [[semantic search]] over document collections

**Key Concept:** [[RAG]] systems bridge the gap between static [[knowledge bases]] and [[LLMs]], allowing models to reference specific documents without retraining. Document processing tools handle the critical first step of preparing raw content.

---

## 5. Computer Use & Browser Automation

**Tool Count:** 20 tools

**Primary Tools:** Claude Dev-Browser, WebRover, BrowserBase, Stagehand, Playwright, Google Mariner, Browser Use, Omniparser (Microsoft), Agentdesk, Computer Use (Anthropic)

**Purpose:** Tools allowing agents to interact with user interfaces, click buttons, and navigate the web like a human.

**Use Cases:**
- Automated web research and data gathering
- "Human-in-the-loop" UI task automation
- Web scraping with intelligent interaction
- Testing and quality assurance automation
- Building virtual assistants that use web applications

**Key Concept:** [[Computer use]] represents a significant capability leap, enabling AI systems to operate existing web applications without custom integrations, though with careful [[evaluation]] for reliability and safety.

---

## 6. Evaluation, Security & Operations

**Tool Count:** 28 tools

**Primary Tools:** DeepEval, Guardrails AI, LlamaGuard, Opik, LangSmith, Langfuse, AgentOps, Arize, Weights and Biases, Helicone, EvalVerse, Livebench

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent hallucinations, security breaches, and reliability issues.

**Use Cases:**
- [[Hallucination]] detection and mitigation
- Automated [[evaluation]] of model outputs
- Production monitoring and observability
- [[Red teaming]] and adversarial testing
- Compliance and safety verification
- Performance benchmarking

**Key Concept:** Production-grade AI requires continuous [[evaluation]] and monitoring. These tools provide the instrumentation necessary to maintain safety, reliability, and performance standards in deployed systems.

---

## 7. Developer Tools & IDEs

**Tool Count:** 22 tools

**Primary Tools:** Cursor, Windsurf, Warp.dev, GitHub Copilot, Tabnine, LM Studio, Codium, OpenAI Canvas, Canvas in Gemini, Project IDX, RooCode

**Purpose:** AI-augmented development environments for faster code writing and repository management.

**Use Cases:**
- Code generation and completion
- Repository-aware code assistance
- AI-powered debugging and refactoring
- Natural language to code translation
- Documentation generation

**Key Concept:** [[AI-augmented IDEs]] represent the most direct application of [[LLMs]] to developer workflows, increasing productivity through intelligent code completion and generation.

---

## 8. Voice & Vision Models

**Tool Count:** 21 tools

**Primary Tools:** Veo2 (video), Landing AI, Superwhisper, Cartesia AI, Eleven Labs, Assembly AI, Parakeet, Mistral OCR, Freepik, Gradio, Streamlit

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Use Cases:**
- Building voice assistants and conversational interfaces
- Visual analysis and object detection
- [[OCR]] and document understanding
- Video generation and editing
- Audio transcription and synthesis
- Interactive UI prototyping

**Key Concept:** [[Multimodal models]] extend [[LLM]] capabilities beyond text, enabling richer interactions and more comprehensive data understanding.

---

## 9. Model Serving, Inference & Fine-tuning

**Tool Count:** 17 tools

**Primary Tools:** vLLM, Ollama, LLaMA.cpp, Unsloth, Fireworks AI, Litserve, FastAPI, LM Studio, LlamaCFactory, Transformer Lab

**Purpose:** Backend infrastructure to host models and fine-tune them on proprietary data.

**Use Cases:**
- Deploying models as scalable APIs
- Running models locally or on-premises
- Fine-tuning models on custom datasets
- Optimizing inference performance
- Cost-effective model hosting

**Key Concept:** Moving from prompt-based development to hosted, customized models enables better performance, privacy, and cost control for production applications.

---

## 10. Miscellaneous & General Utilities

**Tool Count:** 36 tools

**Primary Tools:** Fabric, Instructor, Kestra, Vellum, Luma, Promptimize, Repo Prompt, Leverage.ai, Meta Synthetic Data Kit, InstructLab

**Purpose:** Workflow automation, [[synthetic data]] generation, prompt engineering, and general development utilities.

**Use Cases:**
- Prompt optimization and engineering
- Synthetic data generation for training
- Workflow orchestration and automation