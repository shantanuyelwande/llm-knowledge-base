---
title: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892
source_file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
source_url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-09T05:28:40.100844
raw_file_updated: 2026-05-09T05:28:40.100844
version: 1
sources:
  - file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-09T05:28:40.100844
tags: []
related_topics: []
backlinked_by: []
---
# GitHub Agentic Workflows Security Architecture

## Summary

GitHub Agentic Workflows are AI-powered automation systems that run within [[GitHub Actions]] with built-in security controls. The architecture implements a defense-in-depth approach with three distinct layers: substrate (container isolation), configuration (declarative policies), and planning (staged execution). Key security principles include zero-secret agent access, staged and vetted writes, comprehensive logging, and prompt injection prevention through network isolation and API proxying.

---

## Overview

[[GitHub Agentic Workflows]] represent a new paradigm for automation that combines the power of [[AI agents]] with the safety requirements of production CI/CD environments. Unlike traditional deterministic automation, agents are non-deterministic systems that must consume untrusted inputs, reason over repository state, and make autonomous decisions at runtime.

The fundamental challenge is enabling agents to operate at scale while maintaining predictable, secure behavior. GitHub addressed this by treating agent execution as an extension of the CI/CD model rather than as a separate runtime, with security baked into the architecture from the ground up.

## Threat Model

### Core Properties

The threat model for agentic workflows is shaped by two critical properties:

1. **Autonomous Reasoning**: Agents' ability to reason over repository state and act autonomously makes them valuable but also means they cannot be trusted by default, especially when processing untrusted inputs.

2. **Permissive Execution Environment**: [[GitHub Actions]] provide a highly permissive execution environment where all components share a single trust domain. While this is beneficial for deterministic automation, it creates a large blast radius when combined with untrusted agents.

### Threat Assumptions

Under this model, the system assumes an agent will:
- Attempt to read and write state it shouldn't access
- Try to communicate over unintended channels
- Abuse legitimate channels to perform unwanted actions
- Respond to [[prompt injection]] attacks embedded in untrusted inputs

By default, GitHub Agentic Workflows run in strict security mode with this threat model in mind.

## Security Principles

Four core security principles guide the design of GitHub Agentic Workflows:

### 1. Defense in Depth

A layered security architecture with distinct trust boundaries and security properties at each level. Failures at higher layers are contained by lower layers through explicit constraints.

### 2. Don't Trust Agents with Secrets

Agents have zero access to sensitive credentials, authentication tokens, and API keys. This prevents credential exfiltration through prompt injection attacks.

### 3. Stage and Vet All Writes

All write operations are buffered, analyzed, and validated before being applied to the repository. Workflow authors specify which operations are permitted and in what quantities.

### 4. Log Everything

Comprehensive logging at every trust boundary enables forensic analysis, policy validation, and detection of anomalous behavior.

## Layered Security Architecture

The security architecture consists of three distinct layers, each enforcing specific security properties:

```
┌─────────────────────────────────────────────────────┐
│ Planning Layer                                      │
│ • Safe Outputs MCP (GitHub write operations)       │
│ • Call filtering (call availability, volume)       │
│ • Output sanitization (secret removal, moderation) │
├─────────────────────────────────────────────────────┤
│ Configuration Layer                                 │
│ • Compiler (GH AW extension)                       │
│ • Firewall policies (allowlist)                    │
│ • MCP config (Docker image, auth token)            │
├─────────────────────────────────────────────────────┤
│ Substrate Layer                                     │
│ • Action runner VM (OS, hypervisor)                │
│ • Docker containers (Docker daemon, network)       │
│ • Trusted containers (firewall, MCP gateway, API)  │
└─────────────────────────────────────────────────────┘
```

### Substrate Layer

The foundation rests on a [[GitHub Actions]] runner virtual machine and several trusted containers that limit resource access. This layer provides:

- **Isolation**: Components are isolated from each other through container boundaries
- **Mediation**: Privileged operations and system calls are mediated through trusted components
- **Kernel-Enforced Boundaries**: Communication between components is controlled at the kernel level

These protections hold even if untrusted user-level code is compromised and executes arbitrary code within its container.

### Configuration Layer

The configuration layer includes declarative artifacts and toolchains that instantiate secure system structure and connectivity. It dictates:

- Which components are loaded
- How components are connected
- What communication channels are permitted
- What privileges are assigned to each component

Externally minted tokens (agent API keys, GitHub access tokens) are critical inputs that bound components' external effects. Configuration controls which tokens are loaded into which containers.

### Planning Layer

The planning layer creates a staged workflow with explicit data exchanges between stages. It does not dictate which components exist or how they communicate (that's the configuration layer), but rather which components are active over time and what data flows between them.

The **Safe Outputs subsystem** is the primary instance of secure planning, handling all write operations from agents.

## Zero-Secret Agent Architecture

### The Problem

In traditional [[GitHub Actions]], all components share a single trust domain on the runner VM. Sensitive material like authentication tokens and API keys reside in environment variables and configuration files visible to all processes.

This is dangerous because agents are susceptible to [[prompt injection]]: attackers can craft malicious inputs (web pages, repository issues, pull requests) that trick agents into leaking sensitive information.

A compromised agent with access to shell tools can:
- Read configuration files and SSH keys
- Access Linux `/proc` state and workflow logs
- Discover and exfiltrate credentials
- Encode secrets in public-facing GitHub objects

### Isolation Strategy

Agents are isolated in a dedicated container with tightly controlled egress:

**Network Isolation**
- Firewalled internet access through a dedicated firewall component
- Private network between agent and firewall
- Limited external connectivity

**MCP Access Control**
- [[Model Context Protocol]] (MCP) servers run in a separate trusted container
- MCP gateway has exclusive access to MCP authentication material
- Agent communicates with MCP servers through the gateway

**API Token Protection**
- LLM authentication tokens are never exposed to the agent container
- Tokens are stored in an isolated API proxy
- Agent routes all model traffic through the proxy using authenticated channels

### Volume Mounts and chroot Jail

To balance security with utility, agents need access to compilers, interpreters, and repository state without exposing sensitive system files.

The solution uses:

1. **Read-only host filesystem mount**: The entire VM host filesystem is mounted read-only at `/host`
2. **Overlay tmpfs layers**: Selected paths are overlaid with empty `tmpfs` layers to provide writable space
3. **chroot jail**: The agent runs in a `chroot` jail rooted at `/host`

This approach keeps the host-side setup intact while constraining the agent's writable and discoverable surface to exactly what it needs.

## Staged Execution and Safe Outputs

### Workflow Decomposition

The agentic workflows compiler decomposes workflows into explicit stages. For each stage, it defines:

- Active components and their permissions (read vs. write)
- Data artifacts emitted by that stage
- Admissible downstream consumers of those artifacts

### Safe Outputs Pipeline

While an agent executes, it can:
- **Read**: GitHub state through the GitHub MCP server
- **Write**: Only through the Safe Outputs MCP server (buffered)

Once the agent exits, buffered write operations pass through a suite of deterministic analyses:

**1. Operation Filtering**
- Workflow authors specify which write operations are allowed
- Supported operations include: creating issues, comments, pull requests
- Unauthorized operations are rejected

**2. Volume Limiting**
- Authors specify maximum quantities for each operation type
- Example: agent can create at most 3 pull requests per run
- Prevents spam and resource exhaustion

**3. Content Sanitization**
- Analyzes update content to remove unwanted patterns
- Removes URLs and other specified patterns
- Detects and removes accidentally exposed secrets

**4. Content Moderation**
- Applies moderation policies to generated content
- Prevents objectionable or off-topic content

Only artifacts that pass the entire Safe Outputs pipeline are applied to the repository, ensuring each stage's side effects are explicit and vetted.

## Comprehensive Logging and Observability

Even with zero secrets and vetted writes, agents can transform repository data and invoke tools in unintended ways. Comprehensive observability is essential for post-incident analysis and anomaly detection.

### Logging Points

Logging occurs at each trust boundary:

**Firewall Layer**
- Network and destination-level activity
- Records all external communication attempts

**API Proxy**
- Model request/response metadata
- Authenticated request