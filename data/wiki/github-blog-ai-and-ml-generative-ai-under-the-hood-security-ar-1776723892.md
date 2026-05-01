---
title: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892
source_file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
source_url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:48:23.350582
raw_file_updated: 2026-05-01T05:48:23.350582
version: 1
sources:
  - file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:48:23.350582
tags: []
related_topics: []
backlinked_by: []
---
# GitHub Agentic Workflows Security Architecture

## Summary

GitHub Agentic Workflows implement a multi-layered security architecture designed to safely execute autonomous [[AI agents]] within [[GitHub Actions]]. The system employs defense-in-depth principles, isolates agents from secrets, stages and vets all write operations, and maintains comprehensive logging for forensic analysis. This architecture addresses the unique security challenges posed by non-deterministic agents operating in [[CI/CD]] environments.

---

## Overview

[[GitHub Agentic Workflows]] are autonomous systems that can perform repository tasks such as documentation fixes, unit test generation, and code refactoring. While offering significant productivity benefits, agents present novel security challenges: they must consume untrusted inputs, reason over repository state, and make runtime decisions without deterministic guarantees.

The core security challenge emerges from combining two factors:

1. **Agent autonomy**: Agents reason over repository state and act independently, making them inherently untrustworthy by default
2. **Permissive execution environment**: [[GitHub Actions]] provides a shared trust domain where all components have broad access to resources, creating a large blast radius if an agent malfunctions

GitHub addresses these challenges through a security architecture built on four foundational principles: [[#Defend in Depth|defend in depth]], [[#Don't Trust Agents with Secrets|don't trust agents with secrets]], [[#Stage and Vet All Writes|stage and vet all writes]], and [[#Log Everything|log everything]].

---

## Threat Model

### Assumptions

GitHub Agentic Workflows operate under the assumption that agents will attempt to:

- Read and write state beyond their intended scope
- Communicate over unintended channels
- Abuse legitimate channels to perform unwanted actions
- Extract sensitive information through [[prompt injection]] attacks

This threat model is shaped by two key properties:

**Non-determinism**: Unlike traditional [[CI/CD]] automation, agents cannot be fully predicted or controlled by configuration alone. Their behavior emerges from reasoning over input data and repository context.

**Untrusted Input Exposure**: Agents must process external inputs such as web pages, [[GitHub]] issues, and pull requests that may contain adversarial content designed to manipulate agent behavior.

### Security Mode

By default, Agentic Workflows run in strict security mode, treating agents as untrusted components regardless of their source or configuration.

---

## Defend in Depth

GitHub Agentic Workflows employ a three-layer security architecture, where each layer enforces distinct security properties and limits the impact of failures in layers above it.

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│  PLANNING LAYER                                 │
│  • Safe Outputs MCP                             │
│  • Call Filtering                               │
│  • Output Sanitization                          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  CONFIGURATION LAYER                            │
│  • Compiler (GH AW Extension)                   │
│  • Firewall Policies                            │
│  • MCP Configuration                            │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  SUBSTRATE LAYER                                │
│  • Action Runner VM                             │
│  • Docker Containers                            │
│  • Trusted Containers                           │
└─────────────────────────────────────────────────┘
```

### Substrate Layer

The substrate layer provides the foundational security guarantees through:

- **Isolation**: Separation of agent containers from other system components
- **Mediation**: Privileged operations and system calls are intercepted and controlled
- **Kernel-enforced boundaries**: Communication channels are restricted at the operating system level

These protections persist even if an untrusted user-level component is compromised and executes arbitrary code within its container isolation boundary.

Key substrate components include:

- **Action Runner VM**: The underlying [[GitHub Actions]] runner virtual machine
- **Docker Containers**: Container-based isolation for agent execution
- **Trusted Containers**: Special containers including firewall, [[MCP]] gateway, and [[API]] proxy

### Configuration Layer

The configuration layer controls the structure and connectivity of the system through:

- **Declarative Artifacts**: YAML and configuration files that define system structure
- **Compiler**: The GitHub Agentic Workflows extension that translates high-level definitions into secure configurations
- **Firewall Policies**: Allowlist-based rules controlling network access
- **MCP Configuration**: Specification of which [[Model Context Protocol]] servers load and how they authenticate

Critically, the configuration layer controls the distribution of sensitive material:

- Agent API keys
- [[GitHub]] access tokens ([[PAT|Personal Access Tokens]])
- MCP server authentication credentials

### Planning Layer

The planning layer manages temporal execution flow and data exchanges. While the configuration layer defines which components exist and how they connect, the planning layer determines:

- Which components are active at each execution stage
- What data flows between stages
- Which outputs are allowed to leave the system

The primary mechanism is the **Safe Outputs subsystem** (see [[#Stage and Vet All Writes|Stage and Vet All Writes]]).

---

## Don't Trust Agents with Secrets

### The Secret Exposure Problem

In traditional [[GitHub Actions]], all components share a single trust domain on the runner [[VM]]. This means sensitive material resides in environment variables and configuration files visible to all processes, creating a critical vulnerability when combined with untrusted agents.

Agents are particularly vulnerable to [[prompt injection]] attacks, where malicious inputs trick agents into leaking sensitive information. An injected agent with shell access can:

- Read configuration files and SSH keys
- Access Linux `/proc` filesystem state
- Extract credentials from workflow logs
- Upload secrets to external services
- Encode credentials in public [[GitHub]] objects (issues, pull requests, comments)

### Zero-Secret Architecture

GitHub implements a "zero-secret agents" approach through multiple complementary mechanisms:

#### Container Isolation

Agents execute in a dedicated container with tightly controlled egress:

- **Firewalled internet access**: Network access restricted to allowlisted destinations
- **MCP access through trusted gateway**: All [[Model Context Protocol]] communication mediated by separate trusted container
- **LLM API calls through proxy**: Model requests routed through authenticated proxy rather than exposing tokens directly

#### Private Network Enforcement

Agentic workflows create a private network between the agent container and firewall, preventing direct external communication.

#### Credential Isolation

Authentication tokens are never exposed to the agent container:

- **MCP Gateway**: Runs in separate trusted container, launches MCP servers, maintains exclusive access to MCP authentication material
- **API Proxy**: Holds [[LLM]] authentication tokens, routes model traffic from agent through authenticated proxy

#### File System Constraints

Rather than duplicating action provisioning logic or expanding the in-container environment, GitHub uses:

- **Read-only host mount**: Entire VM host filesystem mounted read-only at `/host`
- **Tmpfs overlays**: Selected paths overlaid with empty temporary filesystems
- **Chroot jail**: Agent executes in chroot jail rooted at `/host`, constraining writable and discoverable surface

This approach preserves the host-side setup while limiting agent access to necessary resources for legitimate work.

---

## Stage and Vet All Writes

### Write Operation Risks

Even without access to secrets, compromised or prompt-injected agents can cause harm through write operations:

- Spam repositories with pointless issues and pull requests
- Add objectionable URLs and malicious content to repository objects
- Overwhelm maintainers with noise and false information
- Pollute repository state with garbage data

### Safe Outputs Architecture

The compiler decomposes workflows into explicit stages, with each stage defining:

- **Active components and permissions**: Which components are active and their read/write access levels
- **Emitted artifacts**: Data produced by the stage
- **Admissible consumers**: Which downstream stages can consume which artifacts

### Safe Outputs Pipeline

During agent execution:

1. Agent reads [[GitHub]] state through read-only GitHub MCP server
2. Agent stages updates through Safe Outputs MCP server (write-buffered)
3. Agent exits
4. Safe Outputs analyses process buffered write operations

### Safe Outputs Analysis

The Safe Outputs pipeline applies three deterministic analyses to all staged operations:

#### Operation Filtering

Workflow authors specify which write operations are permitted:

- Creating issues
- Creating comments
- Creating pull requests
- Other specific GitHub operations

Unauthorized operation types are rejected before execution.

#### Volume Limiting

Safe Outputs restricts the number of updates allowed per run:

- Maximum pull requests per run
- Maximum issues per run
- Maximum comments per run
- Other rate limits

This prevents spam attacks and resource exhaust