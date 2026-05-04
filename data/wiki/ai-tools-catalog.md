---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-04T05:38:57.921615
raw_file_updated: 2026-05-04T05:38:57.921615
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-04T05:38:57.921615
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The AI Tools Catalog is a comprehensive classification system for artificial intelligence development tools and platforms. It organizes over 300+ AI tools across ten major categories, enabling developers and organizations to identify appropriate solutions for specific use cases in [[AI development]], [[agent systems]], and [[machine learning operations]].

## Summary

This catalog serves as a reference guide for the modern AI development stack, covering everything from [[agent memory systems]] to [[model serving infrastructure]]. Each category addresses distinct challenges in building, deploying, and monitoring AI applications at scale.

---

## Categories

### 1. Agent Memory & Context

**Purpose:** Systems for long-term persistence, state management, and semantic recall for agents.

**Key Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7, Skillscreator, Skills.sh, Skills patterns (Google), Qodo aware, Repo Prompt, Claude context semantic search

**Use Cases:**
- Agents that need to "remember" user preferences across sessions
- [[Codebase context]] management and retrieval
- Long-term conversation history preservation
- Semantic recall of past interactions

**Related Concepts:** [[State management]], [[Semantic search]], [[Context windows]]

---

### 2. Agent Orchestration & Frameworks

**Purpose:** Logic engines that manage multi-step planning and multi-agent collaboration.

**Key Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent SDK, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Julep-ai, Flock AI, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Use Cases:**
- Complex workflows requiring multiple specialized agents
- Multi-step planning and task decomposition
- Inter-agent communication and coordination
- Workflow automation across diverse systems

**Related Concepts:** [[Multi-agent systems]], [[Workflow automation]], [[Task planning]]

---

### 3. MCP (Model Context Protocol) & Data Tools

**Purpose:** Standardized protocols for connecting LLMs to external data and local machine tools.

**Key Tools:** Google MCP toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic MCP, Cline MCP, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Use Cases:**
- Bridging models with local file systems
- Database connectivity and querying
- Integration with external APIs and services
- Tool standardization across platforms

**Related Concepts:** [[Model Context Protocol]], [[API integration]], [[Data connectivity]]

---

### 4. RAG & Document Processing

**Purpose:** Ingestion pipelines that transform messy PDFs, videos, and websites into searchable vectors.

**Key Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral OCR, GroudX, Smoldocling, Openrag eval, SiteRAG, Unstructured, Qmd CLI, Qmd BM25, Milvus DB, QDrant, pgVector, Elasticsearch, ChromaDB, Colivara

**Use Cases:**
- Building "Chat with your Docs" features
- Multi-format document ingestion
- Vector database management
- Semantic search over document collections
- Video and image content processing

**Related Concepts:** [[Retrieval-Augmented Generation]], [[Vector databases]], [[Document parsing]], [[Semantic search]]

---

### 5. Computer Use & Browser Automation

**Purpose:** Allowing agents to interact with UIs, click buttons, and navigate the web like a human.

**Key Tools:** Vercel Labs agent browser, Claude dev-browser, Fellou AI, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google Mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Use Cases:**
- Automated web research and data collection
- Human-in-the-loop UI task automation
- Cross-website workflow automation
- Accessibility testing and validation
- Web scraping and monitoring

**Related Concepts:** [[Browser automation]], [[UI automation]], [[Web scraping]], [[Computer vision]]

---

### 6. Evaluation, Security & Ops

**Purpose:** Testing, monitoring, and securing LLM outputs to prevent hallucinations and leaks.

**Key Tools:** Deepteam, Parlant, Plano AI, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGuard, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Use Cases:**
- Production-grade safety and reliability testing
- Hallucination detection and mitigation
- Model evaluation and benchmarking
- Monitoring and observability
- Red teaming and adversarial testing
- Compliance and security auditing

**Related Concepts:** [[Model evaluation]], [[LLM safety]], [[Observability]], [[Red teaming]], [[Hallucination detection]]

---

### 7. Developer Tools & IDEs

**Purpose:** AI-augmented environments for faster code writing and repository management.

**Key Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, GitHub Copilot, LM Studio, Tabnine, Traycer AI, OpenAI Canvas, Canvas in Gemini, Project IDX, Lightning AI, RooCode, Chaoscoder.net

**Use Cases:**
- Accelerating daily development cycles
- Code generation and completion
- Repository understanding and navigation
- Collaborative coding experiences
- Integrated development environments

**Related Concepts:** [[Code generation]], [[AI-assisted programming]], [[Developer experience]]

---

### 8. Voice & Vision Models

**Purpose:** Multi-modal tools for generating and processing audio, images, and video.

**Key Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia AI, Nari-labs, Murf AI, Play AI, Parakeet, Assembly AI, Eleven Labs, FastRTC, Orpheus TTS, LLMvox, Zonos, Freepik, Gradio, Streamlit, Gamma.app, Cursorful (Cap), Mistral OCR, Landing AI tuning

**Use Cases:**
- Building voice assistants and conversational interfaces
- Visual analysis and object detection
- Video generation and processing
- Speech-to-text and text-to-speech conversion
- Multi-modal content creation

**Related Concepts:** [[Multimodal AI]], [[Speech processing]], [[Computer vision]], [[Voice synthesis]]

---

### 9. Serving, Inference & Fine-tuning

**Purpose:** Backend infrastructure to host models and fine-tune them on proprietary data.

**Key Tools:** Lorax, vLLM, FAST API, Litserve, Fireworks AI, LitAPI, OpenLLM, Hostinger, Netlify, Ollama, LM Studio, LlamaCPP, Unsloth, Llamafactory, Transformer lab, SGLang, OUMI

**Use Cases:**
- Moving from prompts to hosted, scalable APIs
- Model fine-tuning on custom datasets
- On-premises and edge deployment
- Performance optimization and quantization