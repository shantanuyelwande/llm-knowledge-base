---
title: I am sharing _How we built our multi-agent research system _ Anthropic_ with you
source_file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-24T18:51:37.472554
raw_file_updated: 2026-04-24T18:51:37.472554
version: 1
sources:
  - file: I am sharing _How we built our multi-agent research system _ Anthropic_ with you.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-24T18:51:37.472554
tags: []
related_topics: []
backlinked_by: []
---
# Multi-Agent Research System Architecture

## Summary

Anthropic's multi-agent research system represents a significant advancement in [[AI agent]] design, utilizing multiple coordinated [[Language Model|LLMs]] to conduct complex research tasks more effectively than single-agent approaches. The system employs an [[Orchestrator-Worker Pattern|orchestrator-worker architecture]] where a lead agent coordinates specialized [[Subagent|subagents]] operating in parallel, achieving a 90.2% performance improvement over single-agent systems on internal evaluations.

## Overview

The Research feature enables [[Claude (AI)|Claude]] to search across the web, [[Google Workspace]], and various integrations to accomplish complex research tasks. This multi-agent system evolved from prototype to production through careful engineering, revealing critical lessons about [[System Architecture|system architecture]], [[Tool Design|tool design]], and [[Prompt Engineering|prompt engineering]].

A multi-agent system consists of multiple [[Autonomous Agent|agents]] (LLMs autonomously using tools in a loop) working together. The key innovation lies in distributing work across agents with separate [[Context Window|context windows]], enabling parallel reasoning and increased capacity for complex problem-solving.

## Benefits of Multi-Agent Systems

### Handling Unpredictability

Research work involves open-ended problems where required steps cannot be predicted in advance. Unlike traditional [[Pipeline (Software)|pipelines]], multi-agent systems provide the flexibility to:

- Pivot or explore tangential connections as investigation unfolds
- Operate autonomously across many turns
- Make dynamic decisions based on intermediate findings
- Adapt approaches based on discoveries

### Information Compression

The essence of search is compression—distilling insights from vast information sources. [[Subagent|Subagents]] facilitate compression by:

- Operating in parallel with independent context windows
- Exploring different aspects simultaneously
- Condensing important findings before returning to lead agent
- Providing separation of concerns through distinct tools and prompts

### Scaling Performance

Once [[Intelligence|intelligence]] reaches a threshold, multi-agent systems become essential for scaling performance. Similar to how human societies became exponentially more capable through collective intelligence and coordination, AI agents can accomplish far more when working collectively than individually.

### Performance Metrics

Internal evaluations demonstrate significant advantages:

- **Performance Improvement**: Multi-agent system with [[Claude Opus 4]] as lead agent and [[Claude Sonnet 4]] subagents outperformed single-agent Claude Opus 4 by 90.2%
- **Token Efficiency**: Token usage explains 80% of performance variance in browsing tasks
- **Model Efficiency**: Upgrading to Claude Sonnet 4 provides larger performance gains than doubling token budget on Claude Sonnet 3.7

### Token Economy Trade-offs

The increased performance comes with significant resource costs:

- Agents typically use approximately 4× more tokens than chat interactions
- Multi-agent systems use approximately 15× more tokens than standard chats
- Economic viability requires tasks where value justifies increased token consumption
- Best suited for tasks with high parallelization potential and information exceeding single context windows

### Limitations

Multi-agent systems are not universally optimal. They perform poorly for:

- Domains requiring all agents to share identical context
- Tasks with many interdependencies between agents
- Most coding tasks with limited parallelizable components
- Situations requiring real-time coordination and delegation

## Architecture Overview

### Orchestrator-Worker Pattern

The system implements a clear hierarchical structure:

```
User Query
    ↓
Lead Agent (Analyzer & Coordinator)
    ↓
Specialized Subagents (Parallel Execution)
    ↓
Results Aggregation
    ↓
Citation Agent (Attribution)
    ↓
Final Output with Citations
```

### Workflow Process

1. **Query Analysis**: User submits query to lead agent
2. **Strategy Development**: Lead agent analyzes query and develops research strategy
3. **Subagent Spawning**: Lead agent creates specialized subagents for parallel exploration
4. **Information Gathering**: Subagents iteratively use search tools and evaluate results
5. **Synthesis**: Lead agent synthesizes findings and determines if additional research needed
6. **Citation Processing**: Citation agent identifies specific source locations for all claims
7. **Result Delivery**: Final research results with proper citations returned to user

### Contrast with Traditional Approaches

Unlike [[Retrieval Augmented Generation|RAG]] systems that use static retrieval of pre-selected chunks, this architecture employs:

- Multi-step dynamic search adapting to new findings
- Iterative information discovery
- Quality analysis and evaluation of results
- Adaptive formulation of high-quality answers

### Memory Management

The system addresses [[Context Window]] limitations through:

- **Memory Persistence**: Lead agent saves research plan to memory before context exceeds 200,000 tokens
- **Context Preservation**: Critical information retained despite truncation
- **State Recovery**: Ability to resume from checkpoints rather than restart entirely

## Prompt Engineering Principles

### 1. Think Like Your Agents

Effective prompt iteration requires understanding agent behavior:

- Build simulations using exact prompts and tools from production system
- Watch agents work step-by-step to identify failure modes
- Develop accurate mental models of agent decision-making
- Recognize that most impactful changes become obvious through observation

### 2. Teach the Orchestrator How to Delegate

Delegation quality directly impacts system performance:

- Each subagent requires clear objective and output format
- Provide guidance on appropriate tools and sources
- Establish clear task boundaries and divisions of labor
- Detailed task descriptions prevent duplication and gaps

**Common Problem**: Simple instructions like "research the semiconductor shortage" led to:
- Vague task interpretation
- Duplicate work across subagents
- Ineffective division of labor

### 3. Scale Effort to Query Complexity

Embed explicit scaling rules in prompts:

- **Simple Fact-Finding**: 1 agent with 3-10 tool calls
- **Direct Comparisons**: 2-4 subagents with 10-15 calls each
- **Complex Research**: 10+ subagents with clearly divided responsibilities

This prevents overinvestment in simple queries and optimizes resource allocation.

### 4. Tool Design and Selection

Agent-tool interfaces are as critical as [[Human-Computer Interface|human-computer interfaces]]:

- Examine all available tools before selection
- Match tool usage to user intent
- Use web search for broad external exploration
- Prefer specialized tools over generic alternatives
- Provide distinct purpose and clear descriptions for each tool

**Impact of Tool Design**: Flawed tool descriptions send agents down completely wrong paths. A tool-testing agent found that improved descriptions resulted in 40% decrease in task completion time for future agents.

### 5. Let Agents Improve Themselves

[[Claude (AI)|Claude]] models demonstrate capability for self-improvement:

- Diagnose failure modes in prompts and tools
- Suggest improvements based on observed failures
- Test tools dozens of times to identify nuances and bugs
- Rewrite tool descriptions to avoid common mistakes

### 6. Start Wide, Then Narrow Down

Mirror expert human research methodology:

- Explore landscape before drilling into specifics
- Counter tendency toward overly long, specific queries
- Start with short, broad queries
- Evaluate available information
- Progressively narrow focus based on findings

### 7. Guide the Thinking Process

[[Extended Thinking Mode|Extended thinking mode]] serves as controllable scratchpad:

- Lead agent uses thinking to plan approach
- Assess which tools fit the task
- Determine query complexity and subagent count
- Define each subagent's role
- Subagents use interleaved thinking after tool results to evaluate quality and identify gaps

**Observed Benefits**: Extended thinking improved instruction-following, reasoning, and efficiency.

### 8. Parallel Tool Calling

Parallelization transforms speed and performance:

- **Lead Agent Parallelization**: Spin up 3-5 subagents in parallel rather than serially
- **Subagent Parallelization**: Use 3+ tools in parallel
- **Performance Impact**: Cut research time by up to 90% for complex queries
- **Efficiency**: More work completed in minutes instead of hours with greater information coverage

### Strategy Summary

Rather than rigid rules, the prompting strategy focuses on instilling good heuristics:

- Decompose difficult questions into smaller tasks
- Carefully evaluate source quality
- Adjust search approaches based on new information
- Recognize when to focus on depth versus breadth
- Set explicit guardrails to prevent unintended side effects
- Maintain fast iteration loops with observability and test cases

## Evaluation Methodology

### Unique Challenges of Multi-Agent Evaluation

Traditional evaluations assume deterministic paths: given input X, follow path Y to produce output Z. Multi-agent systems violate this assumption:

- Identical starting points produce completely different valid paths
- Agents might use different tools to find the same answer
- Multiple search depths and sources can be equally valid
- Correct steps are often unknown in advance

### Small-