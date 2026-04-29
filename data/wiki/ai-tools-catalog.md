---
title: ai-tools-catalog
source_file: ai-tools-catalog.md
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-29T05:30:42.303815
raw_file_updated: 2026-04-29T05:30:42.303815
version: 1
sources:
  - file: ai-tools-catalog.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-29T05:30:42.303815
tags: []
related_topics: []
backlinked_by: []
---
# AI Tools Catalog

## Overview

The **AI Tools Catalog** is a comprehensive taxonomy of software tools and frameworks designed to support the development, deployment, and management of artificial intelligence systems. This catalog organizes over 300+ tools across ten primary categories, each addressing specific challenges in the AI development lifecycle—from agent memory and orchestration to evaluation and deployment.

## Quick Summary

| Category | Tool Count | Primary Use Case |
|----------|-----------|------------------|
| [[Agent Memory & Context]] | 18 | Long-term persistence and semantic recall |
| [[Agent Orchestration & Frameworks]] | 32 | Multi-step planning and collaboration |
| [[MCP & Data Tools]] | 19 | Protocol standardization and data bridging |
| [[RAG & Document Processing]] | 24 | Document ingestion and semantic search |
| [[Computer Use & Browser Automation]] | 20 | UI interaction and web automation |
| [[Evaluation, Security & Ops]] | 28 | Testing, monitoring, and safety |
| [[Developer Tools & IDEs]] | 22 | AI-augmented development environments |
| [[Voice & Vision Models]] | 21 | Multi-modal processing |
| [[Serving, Inference & Fine-tuning]] | 17 | Model deployment and optimization |
| [[Miscellaneous & General]] | 36 | Utilities and workflow automation |

---

## Category Details

### Agent Memory & Context

**Tools:** Mem0, Claude-mem, Byterover, Lang-mem, Letta/Mem-GPT, Zep, Cognee, Rowboat, Acontext, Context hub, Superpowers, Context mode, Context7 Skillscreator, Skills.sh, Skills patterns google, Qodo aware, Repo Prompt, Claude context semantic search

**Purpose:** Systems for long-term persistence, state management, and semantic recall for [[AI agents]].

**Use Cases:**
- Preserving user preferences across sessions
- Maintaining codebase context for development agents
- Building persistent memory layers for conversational systems

**Key Concept:** These tools solve the problem of [[context window limitations]] by enabling agents to selectively retrieve and maintain relevant information over extended interactions.

---

### Agent Orchestration & Frameworks

**Tools:** Goose AI, Autoagent harness, Hermes, Ralph orchestrator, OpenCode, PentaAGI, rtk-ai, Smolagents, AutoGen, CrewAI, Langchain/Langgraph, Atomic agents, DSpy, OpenAI agent sdk, Copilotkit, Autoagent, Firebase.studio, Agentsdk, PySpur, Agno, Manus AI, Camel-AI, Owl, Anus (Manus alt), Julep-ai, Flock ai, Langflow, Flowise, Gumloop, n8n, Langraph builder, Rivet

**Purpose:** Logic engines that manage [[multi-step planning]] and [[multi-agent collaboration]].

**Use Cases:**
- Orchestrating complex workflows requiring multiple specialized agents
- Implementing [[agentic reasoning]] loops
- Building no-code/low-code agent applications
- Managing agent communication and task delegation

**Key Concept:** These frameworks provide the computational infrastructure for [[agent-based systems]] where individual components coordinate to solve complex problems.

---

### MCP & Data Tools

**Tools:** Google mcp toolbox, KitOps MCP, mcp.so, Smithery, MCP CLI, Pixeltable, SDV data generator, Blender MCP 3D, OpenTools, MCP Studio, mcp.getflow.dev, Gen AI Toolbox (Google), Magic mcp, Cline mcp, Composio, Zapier, Airweave, LangChain Payman, Dataverse

**Purpose:** Standardized protocols for connecting [[Large Language Models]] to external data and local machine tools via the [[Model Context Protocol]] (MCP).

**Use Cases:**
- Bridging models and local file systems
- Connecting to specialized databases
- Enabling tool use and function calling
- Creating standardized interfaces for [[LLM integrations]]

**Key Concept:** MCP provides a vendor-agnostic standard for extending model capabilities beyond their training data, similar to how APIs extended web applications.

---

### RAG & Document Processing

**Tools:** Langextraxt, Llamaparse, Liteparse, Docling (IBM), Rag flow, ragi.ai (video), LlamaExtract, Vectorize, LLamaIndex, Mistral ocr, GroudX, Smoldocling, Vectorize, Openrag eval, SiteRAG, Unstructured, Qmd cli, Qmd bm25, Milvus db, QDrant, pgVector, Elastic search, ChromaDB, Colivara

**Purpose:** [[Retrieval-Augmented Generation]] (RAG) ingestion pipelines that convert unstructured documents into searchable [[vector embeddings]].

**Use Cases:**
- Building "Chat with your Docs" applications
- Processing PDFs, videos, and websites
- Creating semantic search over proprietary documents
- Implementing knowledge base retrieval systems

**Key Concept:** RAG enables models to access external knowledge without retraining, combining [[information retrieval]] with [[generative AI]].

---

### Computer Use & Browser Automation

**Tools:** Vercel labs agent browser, Claude dev-browser, Fellou ai, WebRover, BrowserBase, Browsertools v1.2, Stagehand, Playwright, Convergence AI, Google mariner, Proxy web agent, vibetest, Browser use (Smooth/OpenAI/Open), Proxy lite, Omniparser (Microsoft), Agentdesk, Simular, Computer use (Anthropic)

**Purpose:** Tools enabling [[AI agents]] to interact with user interfaces, click buttons, navigate the web, and perform tasks like humans.

**Use Cases:**
- Automated web research and data gathering
- Robotic process automation (RPA)
- Testing and quality assurance
- Human-in-the-loop UI task automation

**Key Concept:** [[Computer vision]] combined with [[agentic control]] enables agents to operate in environments designed for human users.

---

### Evaluation, Security & Ops

**Tools:** Deepteam, Parlant, Plano ai, DeepEval, PentaAGI, DeepTeam LLM Red teaming, Debug-gym, Guardrails AI, LlamaGaurd, Opik, LangSmith, OpenTelemetry, Langfuse, LiteEval, LangWatch, AgentOps, Arize, Weights and Biases, Helicone, Maxim, LM Evaluation harness, EvalVerse, Livebench, Bleu, Rogue, Bigbench, Superglue, Truthfulqa

**Purpose:** Testing, monitoring, and securing [[LLM]] outputs to prevent [[hallucinations]], data leaks, and other safety issues.

**Use Cases:**
- Evaluating model quality and reliability
- Monitoring production AI systems
- Red-teaming and adversarial testing
- Compliance and safety verification
- Debugging agent behavior

**Key Concept:** [[AI safety]] and [[responsible AI]] require continuous evaluation and monitoring, not just pre-deployment testing.

---

### Developer Tools & IDEs

**Tools:** Warp.dev, Graphite, Diamond, Deepwiki, Talktogithub, Cursor, Windsurf, Trae, CodeLLM, Augment code, Codium, Qodo, Github Copilot, LM Studio, Tabnine, Traycer ai, OpenAI Canvas, Canvas in gemini, Project idx, Lightning AI, RooCode, Chaoscoder.net

**Purpose:** AI-augmented development environments that accelerate code writing, repository management, and software engineering workflows.

**Use Cases:**
- Accelerating daily development cycles
- Code completion and generation
- Repository navigation and understanding
- Collaborative development
- AI-assisted debugging

**Key Concept:** [[AI-assisted development]] tools integrate [[code generation]] capabilities directly into developer workflows.

---

### Voice & Vision Models

**Tools:** Veo2 (video), Landing AI (object detection), Superwhisper, Cartesia ai, Nari-labs, Murfai, Play ai, Parakeet, Assembly ai, Eleven labs, FastRTC, Orpheus tts, Llmvox, Zonos, Freepik, Gradio, Streamlit, Gamma.app, cursorful (Cap), Mistral ocr, Landing AI tuning

**Purpose