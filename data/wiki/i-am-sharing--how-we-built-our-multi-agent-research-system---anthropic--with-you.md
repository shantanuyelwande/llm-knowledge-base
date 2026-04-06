---
title: I am sharing _How we built our multi-agent research system _ Anthropic_ with you
source_file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T20:19:37.649601
raw_file_updated: 2026-04-05T20:19:37.649601
version: 1
sources:
  - file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T20:19:37.649601
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Research System at Anthropic

## Summary

Anthropic's multi-agent research system is an advanced [[AI architecture]] that leverages multiple [[Claude]] agents working in parallel to conduct comprehensive research on complex topics. The system uses an [[orchestrator-worker pattern]] where a lead agent coordinates specialized subagents that simultaneously explore different aspects of a query. This approach significantly outperforms single-agent systems, with internal evaluations showing 90.2% improvement over single-agent Claude Opus 4 on research tasks.

---

## Overview

The multi-agent research system represents a significant advancement in how [[Large Language Models]] (LLMs) approach open-ended research problems. Rather than following a predetermined linear path, the system dynamically adapts its research strategy based on emerging findings, mirroring how human researchers conduct investigations.

### Key Capabilities

- **Web search integration** across multiple sources simultaneously
- **Google Workspace integration** for accessing organizational documents
- **Custom integrations** through [[MCP servers]] (Model Context Protocol)
- **Parallel information gathering** from numerous complex tools
- **Automatic citation generation** with source attribution

---

## Architecture and Design

### System Architecture

The research system employs an [[orchestrator-worker pattern]] consisting of:

- **Lead Researcher Agent**: Analyzes user queries, develops research strategies, and spawns specialized subagents
- **Subagents**: Operate in parallel, each with specific research objectives and tool access
- **Citation Agent**: Post-processes findings to identify and attribute sources

### Process Flow

1. User submits a research query
2. Lead agent analyzes the query and develops a research plan
3. Plan is saved to [[Memory]] to persist context across token limits
4. Lead agent spawns multiple subagents with specific research tasks
5. Subagents independently perform parallel searches and analysis
6. Each subagent returns findings to the lead agent
7. Lead agent synthesizes results and determines if additional research is needed
8. Citation agent processes documents to attribute claims to sources
9. Final research results with citations are returned to user

### Comparison to Traditional Approaches

Unlike traditional [[Retrieval Augmented Generation]] (RAG) systems that use static retrieval, the multi-agent research system employs **dynamic, multi-step search** that:

- Iteratively finds relevant information
- Adapts to new findings in real-time
- Analyzes intermediate results to refine queries
- Formulates high-quality answers through continuous refinement

---

## Performance and Benefits

### Performance Metrics

Internal evaluations demonstrate significant advantages:

- **90.2% improvement** over single-agent Claude Opus 4 on research evaluation tasks
- **80% of performance variance** explained by token usage alone
- **15× more tokens** used compared to standard chat interactions
- **4× more tokens** used compared to single-agent systems
- **Up to 90% reduction** in research time through parallelization

### Ideal Use Cases

Multi-agent systems excel at:

- **Breadth-first queries** requiring exploration of multiple independent directions
- **Information-intensive tasks** exceeding single context window limits
- **Complex tool interfacing** with numerous specialized resources
- **High-value tasks** justifying increased token consumption
- **Parallel research** on distinct but related topics

### Limitations

The system is less suitable for:

- Tasks requiring all agents to share identical context
- Domains with extensive agent-to-agent dependencies
- Most coding tasks with limited parallelizable components
- Tasks where coordination overhead exceeds performance gains
- Low-value queries where token costs outweigh benefits

---

## Prompt Engineering and Agent Behavior

### Core Principles

#### 1. Develop Accurate Mental Models

Effective prompt engineering requires understanding agent behavior through:

- Building simulations using the exact prompts and tools
- Observing agents step-by-step to identify failure modes
- Recognizing patterns like excessive verbosity or incorrect tool selection
- Iterating based on direct observation of agent behavior

#### 2. Teach Orchestration and Delegation

The lead agent must decompose queries into clear subtasks with:

- Specific objectives for each subagent
- Defined output formats
- Guidance on appropriate tools and sources
- Clear task boundaries to prevent duplication
- Explicit division of labor to avoid redundant searches

#### 3. Scale Effort to Query Complexity

Embedded scaling rules guide resource allocation:

- **Simple fact-finding**: 1 agent with 3-10 tool calls
- **Direct comparisons**: 2-4 subagents with 10-15 calls each
- **Complex research**: 10+ subagents with clearly divided responsibilities

#### 4. Prioritize Tool Design and Selection

Agent-tool interfaces are critical to system performance:

- Examine all available tools before selection
- Match tool usage to user intent precisely
- Provide clear, distinct tool descriptions
- Use specialized tools over generic alternatives
- Implement explicit heuristics for tool selection
- Avoid SEO-optimized content farms in favor of authoritative sources

#### 5. Enable Self-Improvement

[[Claude]] models can serve as prompt engineers:

- Diagnose failure modes and suggest improvements
- Test tools dozens of times to discover nuances
- Rewrite tool descriptions to optimize usability
- Achieved 40% reduction in task completion time through improved tool ergonomics

#### 6. Search Strategy: Wide to Narrow

Mirror expert human research methodology:

- Begin with short, broad queries to explore the landscape
- Evaluate available information
- Progressively narrow focus based on findings
- Avoid overly specific queries that return few results

#### 7. Guide Thinking Processes

[[Extended Thinking Mode]] provides controllable reasoning:

- Lead agents use thinking to plan approaches
- Assess which tools fit each task
- Determine query complexity and subagent count
- Define each subagent's role
- Subagents use interleaved thinking to evaluate results and identify gaps
- Improved instruction-following, reasoning, and efficiency

#### 8. Enable Parallel Tool Calling

Parallelization dramatically improves performance:

- Lead agent spawns 3-5 subagents in parallel rather than sequentially
- Subagents use 3+ tools in parallel
- Achieved up to 90% reduction in research time
- Enables coverage of more information sources

---

## Evaluation Methods

### Small-Scale Testing

Effective evaluation begins immediately with small samples:

- Start with ~20 test queries representing real usage patterns
- Large effect sizes in early development enable detection with minimal test cases
- Avoid delaying evaluation until large-scale test suites are available
- Rapid feedback loops identify impactful changes

### LLM-as-Judge Evaluation

Automated evaluation at scale using LLM judges:

- Evaluate outputs against defined rubric criteria:
  - **Factual accuracy**: Do claims match sources?
  - **Citation accuracy**: Do cited sources match claims?
  - **Completeness**: Are all requested aspects covered?
  - **Source quality**: Are primary sources preferred over secondary sources?
  - **Tool efficiency**: Were appropriate tools used a reasonable number of times?
- Single LLM call with unified prompt outputting 0.0-1.0 scores
- Most consistent approach aligned with human judgments
- Scales to hundreds of outputs

### Human Evaluation

Manual testing identifies gaps in automated evaluation:

- Catches edge cases and hallucinations on unusual queries
- Identifies system failures and subtle biases
- Discovered preference for SEO-optimized content over authoritative sources
- Essential complement to automated evaluation
- Remains necessary even with comprehensive automated evals

### Emergent Behavior Monitoring

Multi-agent systems exhibit unpredictable interactions:

- Small changes to lead agent affect subagent behavior unpredictably
- Requires understanding interaction patterns, not just individual behavior
- Best prompts provide collaboration frameworks rather than strict instructions
- Define division of labor, problem-solving approaches, and effort budgets
- Requires careful observation and tight feedback loops

---

## Production Reliability and Engineering Challenges

### State Management and Error Handling

Agents operate as stateful systems across extended periods:

- Agents maintain state across many tool calls
- Errors compound without effective mitigation
- System must support resumption from failure points rather than full restarts
- Agents adapt gracefully when tools fail
- Combine AI adaptability with deterministic safeguards like retry logic and checkpoints

### Debugging and Observability

Non-deterministic agent behavior requires new debugging approaches:

- Agents make dynamic decisions that vary between runs
- Full production tracing enables diagnosis of failures
- Monitor agent decision patterns and interaction structures
- High-level observability without accessing individual conversation contents
- Maintains user privacy while enabling root cause analysis

### Deployment Strategies

Stateful agent systems require careful deployment coordination:

- Agents may be anywhere in their process during updates
- [[Rainbow deployments]] gradually shift traffic between versions
- Keep both old and new versions running simultaneously
- Prevent code changes from breaking existing agents
- Avoid disruption to