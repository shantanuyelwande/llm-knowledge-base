---
title: Agentic_Ai_Problem_Set_Release_12
source_file: Agentic_Ai_Problem_Set_Release_12.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T19:06:51.545836
raw_file_updated: 2026-04-24T19:06:51.545836
version: 1
sources:
  - file: Agentic_Ai_Problem_Set_Release_12.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T19:06:51.545836
tags: []
related_topics: []
backlinked_by: []
---
# Agentic AI Problem Set Release 12

## Overview

**Agentic AI Problem Set Release 12** is an educational resource developed by Prof. Tom Yeh in collaboration with Ofer Mendelevitch (Vectara) to teach the 20 key concepts of agentic AI that became prominent in 2025. The problem set follows a problem-driven, think-first pedagogical approach, where students encounter real-world challenges before learning the terminology and solutions.

## Design Philosophy

The problem set is structured around five core principles:

1. **Problem-Driven**: Each concept begins with a concrete problem statement that motivated its development
2. **Think-First**: Multiple-choice questions encourage active reasoning before revealing answers
3. **Solution-Oriented**: Clear explanations of how each concept addresses the identified problem
4. **Industry Perspectives**: Real-world insights from experienced practitioners complement academic theory
5. **Hands-On Learning**: Inspired by the "AI by Hand" philosophy emphasizing practical understanding

## The 20 Core Agentic AI Concepts

### Reasoning and Planning

#### [[LLM Agent]]
An agent that leverages a Large Language Model's general reasoning capabilities to follow instructions and adapt to new tasks with flexibility rather than brittle rules.

#### [[Reason-and-Act (ReAct)]]
A framework that requires agents to explicitly reason before taking action, ensuring every action has a clear, visible chain of reasoning behind it.

#### [[Chain of Thought]]
A technique that encourages step-by-step reasoning, breaking problems into small, clear steps rather than jumping straight to answers. This improves accuracy and allows agents to catch mistakes.

#### [[Tree of Thought]]
A method enabling agents to explore multiple reasoning branches in parallel and compare them, leading to more reliable and creative solutions rather than following a single line of thinking.

#### [[Graph of Thought]]
An advanced reasoning approach that links and reuses insights across multiple reasoning branches, supporting non-linear reasoning and allowing agents to connect insights that would otherwise remain isolated.

### Planning and Execution

#### [[Plan-and-Execute]]
A pattern that separates planning from execution, requiring agents to outline a clear plan before following it step-by-step, keeping work organized and predictable.

#### [[Orchestration]]
The coordination of tools, intermediate results, and execution steps to ensure agents maintain synchronization while executing complex tasks.

### Tool Interaction

#### [[Tool Use]]
The capability that allows agents to take real actions instead of merely explaining steps, enabling them to perform tasks directly rather than returning everything to the user.

#### [[Function Calling]]
A mechanism that ensures tool calls follow a strict schema with correct arguments, preventing situations where agents select the right tool but fail to emit valid, machine-executable calls.

#### [[Model Control Protocol (MCP)]]
A standardized protocol that provides secure, auditable, and consistent access to tools and data. MCP replaces ad-hoc integrations with a maintainable system where all calls follow the same safe pattern.

### Memory Systems

#### [[Episodic Memory]]
Short-term memory that stores recent events and actions, allowing agents to look back on what they were doing and avoid repeating mistakes within a session.

#### [[Semantic Memory]]
Long-term memory that stores facts, concepts, and distilled lessons, enabling agents to build persistent expertise that carries over across multiple interactions rather than starting from scratch each time.

### Information Retrieval and Reasoning

#### [[Retrieval-Augmented Generation (RAG)]]
A technique that grounds agent reasoning in external data by allowing agents to retrieve and incorporate user documents directly into their reasoning process, ensuring answers are grounded in real information rather than relying solely on model training data.

#### [[Context Selection]]
A mechanism for deliberately choosing which pieces of retrieved text, memory, or prior interaction should enter the prompt, keeping prompts focused and compact rather than loading entire documents or conversation histories.

#### [[Graph RAG]]
An enhancement to RAG that reasons over relationships between retrieved documents by building a graph of connections (people, places, events), allowing agents to reason across the whole network rather than treating documents as isolated chunks.

### Feedback and Improvement

#### [[Agent Loop]]
A continuous feedback mechanism that makes agents pause after each step, observe outcomes, and adjust subsequent actions, preventing blind forward movement without feedback.

#### [[Reflection]]
A capability that allows agents to review their own work, identify errors, and correct themselves before trying again, preventing repetition of the same mistakes.

#### [[Critic]]
A component that provides preference signals to evaluate which outputs are better, allowing agents to compare options, revise decisions, and iteratively improve behavior against goals and quality criteria.

### Coordination and Delegation

#### [[Delegation]]
A pattern that allows agents to hand off tasks to other tools or sub-agents, preventing bottlenecks and enabling faster, distributed work rather than having one overloaded agent handle everything.

### Safety and Governance

#### [[Safety Guardrails]]
Mechanisms that define clear boundaries and rules for agent behavior, ensuring agents understand where they can and cannot go, preventing wandering into unsafe or unwanted behavior.

## Industry Insights

The problem set includes several key insights from Ofer Mendelevitch, Head of Developer Relations at Vectara:

> "Most agents today are simple tool loops — but making them production-grade is the real challenge"

> "45% of enterprises will struggle to operationalize agentic prototypes due to governance and infrastructure gaps."

> "The hard part of agents isn't the reasoning — it's everything around it: sessions, tools, state, safety, and scale."

> "Piecemeal Agentic AI solutions take months to implement — and twice as long to stabilize. Enterprises need an end-to-end Agent Operating System designed to avoid common AI pitfalls."

## Pedagogical Approach

Each of the 20 problems follows a consistent structure:

1. **Problem Statement** (odd-numbered pages): A real-world challenge agents face
2. **Multiple Choice Question**: Four potential solutions to consider
3. **Answer and Explanation** (even-numbered pages): The correct concept with detailed explanation of how it solves the problem
4. **Industry Context** (selected entries): Practical insights from experienced practitioners

This structure encourages active learning and critical thinking rather than passive information absorption.

## About the Contributors

### Prof. Tom Yeh
Academic researcher and educator specializing in agentic AI systems and human-computer interaction.

### Ofer Mendelevitch
- Head of Developer Relations at Vectara
- Author of "Hands-On RAG for Production" (O'Reilly)
- Contributes real-world enterprise perspectives on agentic AI implementation

## Educational Value

This problem set serves multiple purposes:

- **Student Learning**: Provides structured introduction to core agentic AI concepts
- **Professional Development**: Helps practitioners understand modern AI agent architecture
- **Enterprise Context**: Addresses real challenges in operationalizing agentic systems
- **Hands-On Philosophy**: Emphasizes practical understanding over theoretical abstraction

## Related Topics

- [[Large Language Models (LLM)]]
- [[Artificial Intelligence Agents]]
- [[Prompt Engineering]]
- [[Knowledge Graphs]]
- [[AI Safety and Alignment]]
- [[Enterprise AI Systems]]

---

## Metadata

**Source**: Agentic_Ai_Problem_Set_Release_12.pdf

**Creators**: Prof. Tom Yeh, Ofer Mendelevitch

**Sponsor**: AI by Hand ✍

**Publication Year**: 2025

**Subject Area**: Agentic AI, Machine Learning, AI Systems

**Educational Level**: Intermediate to Advanced

**Tags**: `agentic-ai`, `problem-set`, `ai-concepts`, `llm-agents`, `ai-education`, `tool-use`, `reasoning`, `memory-systems`, `rag`, `safety-guardrails`

**Related Articles**: [[LLM Agent]], [[Tool Use]], [[RAG]], [[Safety in AI]], [[AI Agent Architecture]], [[Prompt Engineering Techniques]]