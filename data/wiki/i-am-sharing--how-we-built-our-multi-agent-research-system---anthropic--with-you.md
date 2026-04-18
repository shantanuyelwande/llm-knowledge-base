---
title: I am sharing _How we built our multi-agent research system _ Anthropic_ with you
source_file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-17T20:52:40.290035
raw_file_updated: 2026-04-17T20:52:40.290035
version: 1
sources:
  - file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-17T20:52:40.290035
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Research System Architecture

## Summary

Anthropic's Research feature demonstrates a sophisticated [[multi-agent system]] that uses multiple [[Claude]] agents working in parallel to explore complex topics more effectively than single-agent approaches. The system employs an orchestrator-worker pattern where a lead agent coordinates specialized subagents, achieving 90.2% performance improvement over single-agent systems on breadth-first research queries. This architecture required novel approaches to [[prompt engineering]], [[agent evaluation]], and production reliability to transition from prototype to reliable production system.

## Overview

The multi-agent research system represents a significant advancement in [[artificial intelligence]] application design. Rather than using traditional linear pipelines or static [[retrieval-augmented generation]] (RAG), the system dynamically coordinates multiple agents to search for information simultaneously across web sources, Google Workspace, and integrated tools.

### Key Innovation

The fundamental insight driving this architecture is that research tasks are inherently unpredictable and path-dependent. Unlike traditional software pipelines that follow predetermined steps, research requires continuous adaptation based on emerging discoveries. Multi-agent systems excel at this because they:

- Operate with separate [[context windows]], enabling parallel exploration of different aspects
- Provide separation of concerns through distinct tools and exploration trajectories
- Reduce path dependency through independent investigations
- Scale token usage across multiple agents to handle information exceeding single context window limits

## System Architecture

### Orchestrator-Worker Pattern

The Research system uses a hierarchical architecture where:

1. **Lead Agent (Orchestrator)**: Analyzes user queries, develops research strategy, and spawns specialized subagents
2. **Subagents (Workers)**: Execute specific research tasks in parallel, using [[search tools]] and evaluation mechanisms
3. **Citation Agent**: Post-processes findings to ensure proper source attribution

### Workflow Process

```
User Query
    ↓
Lead Agent Planning
    ↓
Parallel Subagent Creation
    ↓
Independent Information Gathering
    ↓
Result Synthesis & Decision Making
    ↓
Citation Processing
    ↓
Final Output
```

The lead agent saves its research plan to external memory to persist context when approaching token limits (200,000+ tokens). Each subagent independently performs web searches, evaluates results using [[interleaved thinking]], and returns findings to the orchestrator.

### Comparison to Traditional Approaches

Unlike static RAG systems that retrieve pre-identified chunks similar to input queries, this architecture:
- Dynamically finds relevant information
- Adapts to new findings iteratively
- Analyzes results to formulate high-quality answers
- Enables continuous refinement of search strategy

## Performance Characteristics

### Benchmarking Results

Internal evaluations demonstrate significant performance advantages:

- **Multi-agent vs. Single-agent**: Multi-agent system with [[Claude Opus 4]] lead agent and [[Claude Sonnet 4]] subagents outperformed single-agent Claude Opus 4 by **90.2%** on internal research evaluation
- **Example task**: Identifying all board members of Information Technology S&P 500 companies—multi-agent system succeeded through task decomposition while single-agent system failed with sequential searches
- **Token efficiency**: Token usage explains 80% of performance variance, with model choice and tool calls accounting for remaining 15%

### Token Economics

The system trades increased token consumption for improved performance:

- **Agents vs. chat**: ~4× more tokens than standard chat interactions
- **Multi-agent vs. chat**: ~15× more tokens than standard interactions
- **Economic requirement**: Tasks must justify increased token costs through sufficiently high value

### Optimal Use Cases

Multi-agent systems excel at:
- Valuable tasks with heavy parallelization potential
- Information exceeding single context window capacity
- Complex tool integration scenarios
- Breadth-first queries pursuing multiple independent directions

Multi-agent systems are less suitable for:
- Domains requiring shared context across all agents
- Tasks with heavy interdependencies between agents
- Most coding tasks (limited parallelization opportunities)
- Real-time agent coordination and delegation

## Prompt Engineering Principles

### Core Strategies

**1. Think Like Your Agents**
Develop accurate mental models of agent behavior by simulating execution with exact prompts and tools. Observing step-by-step execution reveals failure modes: agents continuing with sufficient results, using verbose queries, or selecting incorrect tools.

**2. Teach Orchestrator Delegation**
Lead agents must receive detailed task descriptions including:
- Specific objectives
- Output format requirements
- Tool and source guidance
- Clear task boundaries

Early attempts using simple instructions like "research the semiconductor shortage" resulted in vague interpretations and duplicated work across subagents.

**3. Scale Effort to Query Complexity**
Embed explicit scaling rules in prompts:
- Simple fact-finding: 1 agent, 3-10 tool calls
- Direct comparisons: 2-4 subagents, 10-15 calls each
- Complex research: 10+ subagents with clearly divided responsibilities

**4. Critical Tool Design and Selection**
Agent-tool interfaces are as critical as [[human-computer interaction]] (HCI) design:
- Examine all available tools before selection
- Match tool usage to user intent
- Prefer specialized tools over generic ones
- Provide explicit heuristics for tool selection
- Ensure distinct tool purposes with clear descriptions

Poor tool descriptions send agents down incorrect paths; a 40% decrease in task completion time resulted from improved tool descriptions.

**5. Enable Agent Self-Improvement**
[[Claude 4]] models can serve as prompt engineers:
- Diagnose failure modes from prompts
- Suggest improvements
- Tool-testing agents can rewrite descriptions to avoid failures
- Iterative testing reveals key nuances and bugs

**6. Start Wide, Then Narrow Down**
Mirror expert human research practices:
- Begin with short, broad queries
- Evaluate available information
- Progressively narrow focus
- Avoid overly specific queries that return few results

**7. Guide the Thinking Process**
[[Extended thinking mode]] serves as a controllable scratchpad:
- Lead agents use thinking to plan approaches and assess tool fit
- Determine query complexity and subagent count
- Define each subagent's role
- Subagents use interleaved thinking after tool results to evaluate quality and identify gaps
- Extended thinking improved instruction-following, reasoning, and efficiency

**8. Parallel Tool Calling**
Transform speed and performance through parallelization:
- Lead agent spins up 3-5 subagents in parallel rather than serially
- Subagents use 3+ tools in parallel
- Result: Up to 90% reduction in research time for complex queries

## Agent Evaluation Methods

### Unique Evaluation Challenges

Multi-agent systems present evaluation difficulties absent in traditional systems:
- Agents may take completely different valid paths to identical goals
- No single "correct" sequence of steps to validate
- Require flexible evaluation judging outcomes and process reasonableness
- Non-deterministic behavior even with identical starting conditions

### Evaluation Approaches

**Start Early with Small Samples**
- Begin with ~20 queries representing real usage patterns
- Early-stage changes often show dramatic impact (30% → 80% success)
- Small sample sizes sufficient to detect large effect sizes
- Don't delay evaluations waiting for large-scale test sets

**LLM-as-Judge Evaluation**
Scalable evaluation of free-form research outputs using LLM judges evaluating against rubric criteria:
- **Factual accuracy**: Claims match sources
- **Citation accuracy**: Cited sources match claims
- **Completeness**: All requested aspects covered
- **Source quality**: Primary sources preferred over secondary
- **Tool efficiency**: Appropriate tool usage and call count

Single LLM call with unified prompt outputting 0.0-1.0 scores and pass-fail grades proved most consistent with human judgments.

**Human Evaluation**
Manual testing catches automation-missed edge cases:
- Hallucinated answers on unusual queries
- System failures and subtle biases
- Source selection problems (e.g., SEO-optimized content farms over authoritative sources)
- Essential for production reliability despite automated evaluations

### Emergent Behavior Considerations

Multi-agent systems exhibit emergent behaviors arising without specific programming. Small changes to lead agent prompts unpredictably affect subagent behavior, requiring:
- Understanding interaction patterns beyond individual agent behavior
- Prompts as collaboration frameworks rather than strict instructions
- Clear division of labor definitions
- Solid heuristics and observability
- Tight feedback loops

## Production Reliability and Engineering

### State Management Challenges

Agents are inherently stateful, maintaining context across many tool calls:
- Minor system failures can cascade into catastrophic agent failures
- Errors compound across long-running processes
- Restarts are expensive and frustrating for users
- Solutions require durable execution and graceful error handling

**Mitigation strategies:**
- Resume execution from checkpoint rather than restart
- Leverage model intelligence for graceful error handling (inform agents of tool failures, enable adaptation)
- Combine AI adaptability