---
title: Agentic_Ai_Problem_Set_Release_12
source_file: Agentic_Ai_Problem_Set_Release_12.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T21:06:51.962296
raw_file_updated: 2026-04-17T21:06:51.962296
version: 1
sources:
  - file: Agentic_Ai_Problem_Set_Release_12.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T21:06:51.962296
tags: []
related_topics: []
backlinked_by: []
---
# Agentic AI Problem Set Release 12

## Overview

The **Agentic AI Problem Set Release 12** is an educational resource developed by Prof. Tom Yeh in collaboration with Ofer Mendelevitch that presents 20 core concepts in [[Agentic AI]] through a problem-driven learning methodology. Created in 2025 and sponsored by AI by Hand, this problem set uses a structured approach where each concept is introduced through a real-world problem statement, followed by multiple-choice questions, and then detailed explanations with industry insights.

## Design Philosophy

The problem set follows four core principles:

1. **Problem-Driven** - Every concept begins with a concrete problem statement that motivated its development
2. **Think-First** - Students encounter multiple-choice questions before learning the answer, encouraging active problem-solving
3. **Solution-Oriented** - Each answer page reveals the correct term and explains how it addresses the stated problem
4. **Industry-Grounded** - Real-world perspectives from industry practitioners complement academic understanding

## The 20 Core Agentic AI Concepts

### Reasoning and Planning Concepts

#### [[LLM Agent]]
Uses a large language model's general reasoning ability to follow instructions and adapt to new tasks with flexibility rather than relying on brittle rules.

#### [[Reason-and-Act]] (ReAct)
Makes agents reason explicitly before taking actions, ensuring every action has a clear, visible chain of reasoning behind it.

#### [[Chain of Thought]]
Encourages agents to break problems into small, clear steps and think out loud, producing deeper, clearer, and more accurate answers by avoiding shallow reasoning.

#### [[Tree of Thought]]
Allows agents to explore multiple reasoning branches in parallel and compare them, leading to more reliable and creative solutions instead of following a single line of thinking.

#### [[Graph of Thought]]
Enables agents to link and reuse insights across multiple reasoning branches, supporting non-linear reasoning by connecting ideas rather than losing them.

#### [[Plan-and-Execute]]
Separates planning from execution by making agents outline a clear plan first, then follow it step by step to keep work organized and predictable.

### Action and Tool Concepts

#### [[Tool Use]]
Lets agents take real actions instead of just explaining steps by calling tools directly to perform tasks rather than handing everything back to the user.

#### [[Function Calling]]
Ensures tool calls are structured and machine-executable by requiring the model to follow a strict schema with correct arguments.

#### [[Delegation]]
Allows agents to hand off tasks to other tools or sub-agents to avoid bottlenecks and speed up work completion.

#### [[Orchestration]]
Coordinates tools, intermediate results, and execution steps across multiple operations, ensuring they stay synchronized and iterate until completion.

### Feedback and Improvement Concepts

#### [[Agent Loop]]
Adds continuous feedback so agents can observe outcomes and adjust actions, preventing agents from blindly moving forward without reflection.

#### [[Reflection]]
Allows agents to review their own work, spot errors, and correct themselves before trying again, preventing repetition of the same mistakes.

#### [[Critic]]
Provides preference signals to judge which outputs are better by evaluating outputs against goals, constraints, or quality criteria, enabling iterative improvement.

### Memory Concepts

#### [[Episodic Memory]]
Stores short-term events and recent actions that agents can look back on, preventing agents from forgetting what happened minutes ago or repeating mistakes.

#### [[Semantic Memory]]
Stores long-term knowledge and distilled lessons so expertise carries over across interactions, allowing agents to accumulate and reuse knowledge over time.

#### [[Context Selection]]
Chooses only relevant information for the prompt by deliberately selecting which pieces of retrieved text, memory, or prior interaction enter the context window, keeping prompts focused and compact.

### Data and Knowledge Concepts

#### [[RAG]] (Retrieval-Augmented Generation)
Grounds agent reasoning in external data by letting agents retrieve user documents and use them directly, ensuring answers are based on real information rather than just model knowledge.

#### [[Graph RAG]]
Reasons over relationships between retrieved documents by building a graph of connections (people, places, events), allowing agents to reason across entire networks rather than isolated chunks.

### Safety and Governance Concepts

#### [[Safety Guardrails]]
Enforces boundaries for safe, governed agent behavior by defining clear limits and rules so agents understand where they can and cannot go.

#### [[Model Control Protocol]] (MCP)
Standardizes secure, auditable access to tools and data by replacing ad-hoc integrations with one clear, permissioned protocol that all calls follow consistently.

## Industry Insights

The problem set includes perspectives from **Ofer Mendelevitch**, Head of Developer Relations at Vectara and author of *Hands-On RAG for Production*, highlighting key challenges in agentic AI:

> "Most agents today are simple tool loops — but making them production-grade is the real challenge"

> "45% of enterprises will struggle to operationalize agentic prototypes due to governance and infrastructure gaps."

> "The hard part of agents isn't the reasoning — it's everything around it: sessions, tools, state, safety, and scale."

> "Piecemeal Agentic AI solutions take months to implement — and twice as long to stabilize. Enterprises need an end-to-end Agent Operating System designed to avoid common AI pitfalls."

## Learning Methodology

Each of the 20 concepts follows a consistent structure:

1. **Problem Statement** - A specific challenge agents face
2. **Multiple Choice Question** - Four possible solutions to choose from
3. **Answer and Explanation** - The correct concept with detailed explanation of how it solves the problem
4. **Industry Context** - Real-world insights and practical implications (selected concepts)

## Key Themes

The problem set reveals several interconnected themes:

- **Autonomy with Structure** - Agents need reasoning flexibility combined with planning and execution frameworks
- **Feedback and Improvement** - Continuous loops, reflection, and critical evaluation are essential for agent reliability
- **Knowledge Integration** - Multiple forms of memory and data retrieval enable agents to leverage both internal and external knowledge
- **Governance at Scale** - Safety guardrails and standardized protocols become critical as agents move from prototypes to production
- **Coordination Complexity** - As agents become more capable, orchestration and delegation become essential to avoid bottlenecks

## Related Topics

- [[Agentic AI]] - The broader field of autonomous AI agents
- [[Large Language Models]] - The foundation for modern agents
- [[AI Safety]] - Ensuring safe agent behavior
- [[Knowledge Graphs]] - Supporting structured reasoning in agents
- [[AI Governance]] - Frameworks for managing agent behavior at scale

## Metadata

**Creator:** Prof. Tom Yeh  
**Collaborator:** Ofer Mendelevitch (Vectara)  
**Sponsor:** AI by Hand  
**Release:** 12  
**Year:** 2025  
**Concepts Covered:** 20 core agentic AI terms  
**Format:** Problem-driven learning with multiple-choice questions  

**Tags:** #agentic-ai #education #problem-set #llm-agents #ai-concepts #reasoning #tool-use #memory #safety #governance

**Related Resources:**
- Hands-On RAG for Production (O'Reilly) by Ofer Mendelevitch
- AI by Hand initiative
- Vectara documentation and resources