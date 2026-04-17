---
title: Harness engineering_ leveraging Codex in an agent-first world _ OpenAI
source_file: Harness engineering_ leveraging Codex in an agent-first world _ OpenAI.pdf
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-05T21:13:15.329916
raw_file_updated: 2026-04-05T21:13:15.329916
version: 1
sources:
  - file: Harness engineering_ leveraging Codex in an agent-first world _ OpenAI.pdf
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-05T21:13:15.329916
tags: ["AI-Assisted Development", "Code Generation", "Software Engineering", "AI Agents", "Development Methodology"]
related_topics: []
backlinked_by: []

---
# Harness Engineering: Leveraging Codex in an Agent-First World

## Summary

**Harness engineering** is an approach to software development where [[AI agents]] (specifically [[Codex]]) take primary responsibility for code generation and implementation, while human engineers focus on designing systems, specifying intent, and building feedback loops. This methodology was demonstrated through a five-month experiment at OpenAI where a complete software product was built with zero manually-written code, achieving approximately 10x faster development velocity.

---

## Overview

Harness engineering represents a fundamental shift in how software teams operate when [[AI coding assistants]] become the primary implementers. Rather than humans writing code directly, engineers create the conditions—tools, documentation, guardrails, and feedback systems—that enable [[AI agents]] to work reliably and coherently.

This approach was validated through a real-world case study where a team of three engineers (later growing to seven) shipped a production software product with:
- Approximately 1 million lines of code
- ~1,500 merged pull requests
- Average throughput of 3.5 PRs per engineer per day
- Real internal and external users
- Development time estimated at 1/10th of traditional approaches

---

## Core Philosophy

### Humans Steer, Agents Execute

The fundamental principle of harness engineering inverts traditional software development roles:

- **Humans** define requirements, design environments, specify intent, and validate outcomes
- **Agents** implement features, write tests, fix bugs, and maintain code
- **No manually-written code** becomes a core constraint that forces the team to build proper scaffolding

This constraint proved essential because it prevented shortcuts and forced investment in systems that scale with agent capability rather than human effort.

---

## Key Principles

### 1. Agent Legibility as Primary Goal

The entire codebase is optimized first for [[AI agent]] comprehension, not human readability.

**Implications:**
- Repository-local, versioned artifacts are the system of record
- Knowledge that exists only in external tools (Google Docs, Slack, email) is inaccessible to agents
- Code structure must be fully inspectable and reasonable from the repository itself
- "Boring" technologies with stable APIs and good training data representation are preferred

### 2. Repository as System of Record

Rather than relying on external documentation or instructions, all knowledge is stored in a structured docs/ directory:

```
docs/
├── design-docs/
│   ├── index.md
│   ├── core-beliefs.md
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
├── product-specs/
├── references/
├── DESIGN.md
├── FRONTEND.md
├── PLANS.md
├── PRODUCT_SENSE.md
└── QUALITY_SCORE.md
```

**AGENTS.md** serves as a table of contents (~100 lines) rather than an exhaustive manual. This prevents:
- Context crowding that obscures task and code
- Pattern-matching instead of intentional navigation
- Documentation rot and staleness
- Inability to verify completeness

### 3. Increasing Application Legibility

As code throughput increased, human QA became the bottleneck. The solution was making application state directly observable to agents:

**UI Legibility:**
- Applications bootable per git worktree for isolated testing
- Chrome DevTools Protocol integration for agent runtime
- Skills for DOM snapshots, screenshots, and navigation
- Agents can reproduce bugs and validate fixes directly

**Observability Legibility:**
- Logs, metrics, and traces exposed via local observability stack
- Ephemeral per-worktree instances that tear down automatically
- LogQL and PromQL query capabilities for agents
- Enables prompts like "ensure service startup completes in under 800ms"

### 4. Strict Architectural Boundaries

A rigid architectural model keeps agent-generated code coherent without micromanagement:

**Layered Architecture:**
Each business domain follows fixed layers with strictly validated dependency directions:
- Types → Config → Repo → Service → Runtime → UI
- Cross-cutting concerns (auth, connectors, telemetry, feature flags) enter through explicit Providers interface
- Dependency violations are mechanically enforced

**Benefits:**
- Agents operate effectively within clear constraints
- Speed without architectural decay
- Constraints apply everywhere automatically
- Allows autonomy within boundaries

### 5. Enforcing Invariants, Not Implementations

The team specifies *what* must be true but not *how* to achieve it:

- Require data validation at boundaries (not prescriptive on specific library)
- Enforce structured logging (not specific format)
- Require naming conventions (not specific naming scheme)
- Enforce file size limits and reliability requirements

Custom linters inject remediation instructions into agent context, making rules educational rather than just restrictive.

---

## Operational Patterns

### Minimal Blocking Merge Gates

Traditional engineering practices become counterproductive at agent throughput scales:

- Short-lived pull requests
- Test flakes addressed with follow-up runs rather than blocking indefinitely
- Corrections are cheap; waiting is expensive
- This inversion of traditional caution is justified when agent throughput exceeds human attention capacity

### Increasing Levels of Autonomy

The system progressively encoded more of the development loop:

**Single-Prompt End-to-End Feature Delivery:**
Given a task description, Codex can now:
1. Validate current codebase state
2. Reproduce reported bugs
3. Record video demonstrations
4. Implement fixes
5. Validate via application driving
6. Open pull requests
7. Respond to feedback
8. Detect and remediate build failures
9. Merge changes (escalating only when judgment required)

This depends heavily on repository structure and tooling and may not generalize without similar investment.

### Entropy and Garbage Collection

Agents naturally replicate existing patterns, leading to drift and technical debt accumulation:

**Golden Principles:**
Opinionated, mechanical rules encoded directly into the codebase:
- Prefer shared utility packages over hand-rolled helpers
- Validate data boundaries; don't probe "YOLO-style"
- Maintain centralized invariants

**Continuous Cleanup:**
- Background Codex tasks scan for deviations on regular cadence
- Update quality grades and open targeted refactoring PRs
- Most reviews complete in under a minute and auto-merge
- Functions like garbage collection—better to pay down debt continuously than in painful bursts

---

## Redefining the Engineer's Role

### From Code Writer to System Designer

Traditional engineering work shifted to:

**System Scaffolding:**
- Breaking down goals into building blocks (design, code, review, test)
- Prompting agents to construct blocks
- Using them to unlock complex tasks

**Capability Building:**
- When tasks fail, identify missing capabilities
- Make capabilities legible and enforceable for agents
- Always have Codex implement the fix

**Interaction Model:**
- Engineers describe tasks through prompts
- Agents open pull requests
- Codex reviews its own changes locally
- Agents request additional agent reviews
- Iterate until all reviewers satisfied
- Humans may review but aren't required to

### Context Management

**Progressive Disclosure:**
- Start agents with small, stable entry points
- Teach where to look next rather than overwhelming upfront
- Mechanical enforcement through linters and CI jobs
- Doc-gardening agents scan for stale documentation and open fix-up PRs

---

## Outcomes and Metrics

### Development Velocity

- **Throughput:** 3.5 PRs per engineer per day (average)
- **Throughput growth:** Increased as team grew from 3 to 7 engineers
- **Time savings:** ~1/10th the time vs. manual development
- **Code volume:** ~1 million lines in 5 months
- **Merge rate:** ~1,500 PRs merged

### Quality and Reliability

- Real internal daily users and external alpha testers
- Product ships, deploys, breaks, and gets fixed
- Entire lifecycle (application logic, tests, CI, documentation, observability, tooling) agent-generated
- Demonstrated maintainability through continuous operation

---

## Technical Infrastructure

### Development Tools Integration

Agents use standard development tools directly:
- `gh` (GitHub CLI) for PR management
- Local scripts for repository operations
- Repository-embedded skills
- Context gathering without human copy-paste

### Automation and Validation

- Custom linters for architectural enforcement
- Structural tests for dependency validation
- Mechanical verification of knowledge base
- CI jobs for documentation freshness and cross-linking
- Recurring cleanup and refactoring processes

---

## Lessons and Open Questions

### What We Know

1. **Discipline shifts to scaffolding:** Building software still demands discipline, but it manifests in tooling