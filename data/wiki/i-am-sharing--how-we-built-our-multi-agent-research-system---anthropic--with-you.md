---
title: I am sharing _How we built our multi-agent research system _ Anthropic_ with you
source_file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:13:50.719867
raw_file_updated: 2026-04-17T20:13:50.719867
version: 1
sources:
  - file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:13:50.719867
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Research System at Anthropic

## Summary

Anthropic's Research feature implements a sophisticated [[multi-agent system]] that uses multiple [[Claude]] language models working in parallel to conduct complex research tasks more effectively than single-agent approaches. The system employs an orchestrator-worker architecture where a lead agent coordinates specialized subagents to explore different aspects of research queries simultaneously. This approach achieved 90.2% performance improvement over single-agent systems on internal evaluations, though it requires careful [[prompt engineering]], robust [[evaluation methodology]], and significant production engineering to maintain reliability at scale.

## Overview

[[Claude]] now includes Research capabilities that enable it to search across the web, [[Google Workspace]], and various integrations to accomplish complex research tasks. The development of this multi-agent system from prototype to production revealed critical lessons about [[system architecture]], [[tool design]], and [[prompt engineering]] that are applicable to building other multi-agent systems.

A multi-agent system consists of multiple [[AI agents]] (language models autonomously using tools in loops) working together toward common objectives. The Research feature's key innovation is its ability to handle open-ended problems that are difficult to predict in advance, making it particularly well-suited for research tasks that require dynamic adaptation and exploration.

## Benefits of Multi-Agent Architecture

### Handling Unpredictability

Research work involves inherently unpredictable problems where fixed paths cannot be predetermined. The dynamic, path-dependent nature of research requires systems that can:

- Continuously update approaches based on discoveries
- Follow leads that emerge during investigation
- Pivot or explore tangential connections as needed
- Operate autonomously for many turns

Traditional linear, one-shot [[pipeline|pipelines]] cannot handle these requirements, making [[AI agents]] with iterative decision-making capabilities essential.

### Information Compression Through Parallelization

The essence of search is compression—distilling insights from vast information sources. Multi-agent systems facilitate compression by:

- Operating multiple agents in parallel with separate context windows
- Exploring different aspects of questions simultaneously
- Condensing the most important information tokens for the lead agent
- Providing separation of concerns through distinct tools, prompts, and exploration trajectories
- Reducing path dependency and enabling thorough independent investigations

### Scaling Intelligence

Once intelligence reaches a threshold, multi-agent systems become vital for scaling performance. While individual humans have become more intelligent over millennia, human societies have become exponentially more capable through collective intelligence and coordination. Similarly, even generally-intelligent [[AI agents]] face limits when operating as individuals; groups of agents accomplish far more.

### Performance Metrics

Internal evaluations demonstrated significant performance improvements:

- **Multi-agent system with [[Claude Opus 4]] lead agent and [[Claude Sonnet 4]] subagents outperformed single-agent Claude Opus 4 by 90.2%** on internal research evaluations
- Example: When identifying all board members of Information Technology S&P 500 companies, the multi-agent system succeeded through task decomposition while the single agent failed with sequential searches

### Token Efficiency Analysis

Analysis of the BrowseComp evaluation revealed that three factors explain 95% of performance variance:

1. **Token usage**: 80% of variance explained by total tokens consumed
2. **Tool calls**: Number of tool invocations
3. **Model choice**: Selection of [[Claude]] model versions

This validates the architecture that distributes work across agents with separate context windows, effectively scaling token usage for complex tasks. Notably, upgrading to [[Claude Sonnet 4]] provided larger performance gains than doubling the token budget on earlier models, demonstrating the importance of model efficiency.

### Economic Considerations

While multi-agent systems deliver superior results, they have significant costs:

- Agents typically use approximately **4× more tokens than chat interactions**
- Multi-agent systems use approximately **15× more tokens than standard chats**
- Economic viability requires tasks where the value justifies increased token consumption

### Limitations and Constraints

Multi-agent systems are not universally applicable. They work poorly for:

- Domains requiring all agents to share identical context
- Tasks involving many dependencies between agents
- Most [[coding]] tasks with fewer parallelizable components
- Situations requiring real-time agent coordination and delegation

Multi-agent systems excel at valuable tasks involving heavy parallelization, information exceeding single context windows, and interfacing with numerous complex tools.

## System Architecture

### Orchestrator-Worker Pattern

The Research system uses a multi-agent architecture based on the orchestrator-worker pattern:

- **Lead Agent (Orchestrator)**: Analyzes queries, develops research strategy, and spawns specialized subagents
- **Subagents (Workers)**: Operate in parallel, exploring different aspects of the research question simultaneously

### Workflow Process

```
User Query
    ↓
Lead Agent Analysis & Planning
    ↓
Subagent Creation (Parallel)
    ↓
Iterative Search & Evaluation
    ↓
Result Synthesis & Quality Assessment
    ↓
Citation Processing
    ↓
Final Output to User
```

### Key Process Steps

1. **Lead Agent Planning**: When a user submits a query, the LeadResearcher agent:
   - Analyzes the query
   - Develops a comprehensive strategy
   - Saves the plan to [[Memory]] to persist context (important when context window exceeds 200,000 tokens)
   - Spawns specialized Subagents with specific research tasks

2. **Parallel Subagent Execution**: Each Subagent independently:
   - Performs web searches using available tools
   - Evaluates tool results using interleaved thinking
   - Returns findings to the LeadResearcher
   - Operates with its own context window and exploration trajectory

3. **Iterative Synthesis**: The LeadResearcher:
   - Synthesizes results from multiple subagents
   - Assesses whether additional research is needed
   - Creates additional subagents or refines strategy as necessary

4. **Citation Processing**: Once sufficient information is gathered:
   - The system passes findings to a CitationAgent
   - Citations are identified and properly attributed to sources
   - All claims are verified against their sources

5. **Result Delivery**: Final research results with complete citations are returned to the user

### Distinction from Traditional Approaches

Unlike traditional [[Retrieval Augmented Generation (RAG)]] systems that use static retrieval, the multi-agent architecture employs:

- **Dynamic search** that adapts to new findings
- **Multi-step processes** that analyze results and formulate high-quality answers
- **Iterative refinement** based on intermediate discoveries
- **Flexible tool usage** rather than predetermined retrieval paths

## Prompt Engineering Principles

Effective multi-agent systems rely heavily on prompt engineering, as each agent is steered by its prompt instructions. The following principles proved effective:

### 1. Think Like Your Agents

Understanding agent behavior is essential for effective iteration:

- Build simulations using the exact prompts and tools from production systems
- Watch agents work step-by-step to identify failure modes
- Develop accurate mental models of agent behavior
- Recognize obvious improvement opportunities through direct observation

Common failure modes revealed through simulation:

- Agents continuing research when sufficient results already obtained
- Overly verbose search queries reducing result relevance
- Incorrect tool selection for tasks

### 2. Teach the Orchestrator How to Delegate

The lead agent must decompose queries into clear subtasks with detailed descriptions:

- **Objective**: Clear goal for each subagent
- **Output format**: Specific structure for returned results
- **Tool guidance**: Explicit direction on which tools and sources to use
- **Task boundaries**: Clear limits on scope and effort

**Problem**: Early versions with simple instructions like "research the semiconductor shortage" led to:
- Subagent work duplication
- Information gaps
- Misinterpreted tasks
- Ineffective division of labor (e.g., one subagent exploring 2021 automotive chip crisis while two others duplicated 2025 supply chain investigations)

**Solution**: Detailed task descriptions prevent duplication and ensure comprehensive coverage.

### 3. Scale Effort to Query Complexity

Agents struggle to judge appropriate effort levels. Embedding scaling rules in prompts helps:

- **Simple fact-finding**: 1 agent with 3-10 tool calls
- **Direct comparisons**: 2-4 subagents with 10-15 calls each
- **Complex research**: 10+ subagents with clearly divided responsibilities

Explicit guidelines prevent overinvestment in simple queries, a common early failure mode.

### 4. Tool Design and Selection Are Critical

Agent-tool interfaces are as critical as [[human-computer interfaces]]:

- **Right tool selection is often strictly necessary**: Searching the web for context existing only in Slack dooms the agent from the start
- **Tool description quality matters**: Poor descriptions send agents down completely wrong paths
- **Explicit heuristics help agents choose correctly**:
  - Examine all available tools first
  - Match tool usage to user intent
  - Search the web for broad external exploration
  - Prefer specialized tools over generic ones