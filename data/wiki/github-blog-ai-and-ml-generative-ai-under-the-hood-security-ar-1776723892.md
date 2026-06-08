---
title: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892
source_file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
source_url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-08T06:48:19.103834
raw_file_updated: 2026-06-08T06:48:19.103834
version: 1
sources:
  - file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-08T06:48:19.103834
tags: []
related_topics: []
backlinked_by: []
---
# GitHub Agentic Workflows Security Architecture

## Summary

**GitHub Agentic Workflows** is a security-first automation system that enables [[AI agents]] to operate safely within [[GitHub Actions]] by implementing a layered defense architecture. The system addresses the unique security challenges posed by non-deterministic agents through isolation, constrained outputs, comprehensive logging, and a zero-secrets approach. Published by GitHub in March 2026, this architecture represents a significant advancement in securing autonomous software engineering agents.

---

## Overview

[[GitHub Agentic Workflows]] represent a new paradigm for [[automation]] in software development, enabling [[AI agents]] to autonomously handle repository tasks such as documentation updates, unit testing, and code refactoring. However, this power comes with significant security challenges. Unlike traditional deterministic automation, agents are non-deterministic systems that must consume untrusted inputs, reason over repository state, and make runtime decisions—making them inherently difficult to constrain.

GitHub's solution treats agent execution as an extension of the [[CI/CD]] model rather than a separate runtime, implementing security through architectural design rather than relying on agent behavior alone.

## Threat Model

### Core Assumptions

The threat model for Agentic Workflows is built on two fundamental properties:

1. **Agent Untrustworthiness**: Agents' ability to reason autonomously over repository state makes them valuable but also means they cannot be trusted by default, especially when exposed to untrusted inputs.

2. **Permissive Execution Environment**: [[GitHub Actions]] provide a highly permissive execution environment with a shared trust domain—a feature that enables composability and performance but creates large blast radius risks when combined with untrusted agents.

### Threat Assumptions

Under this model, GitHub assumes that agents will:
- Attempt to read and write unauthorized state
- Communicate over unintended channels
- Abuse legitimate channels to perform unwanted actions
- Fall victim to [[prompt injection]] attacks

By default, Agentic Workflows run in strict security mode with this threat model in mind.

## Security Principles

The architecture is guided by four core security principles:

### 1. Defense in Depth

Agentic Workflows provide a layered security architecture with distinct trust boundaries and security properties at each layer. This ensures that failures at one level are contained by protections at lower levels.

### 2. Don't Trust Agents with Secrets

Agents have zero access to sensitive credentials including authentication tokens, API keys, and other secrets. This prevents [[prompt injection]] attacks from being able to exfiltrate sensitive material.

### 3. Stage and Vet All Writes

All write operations from agents are explicitly staged, analyzed, and vetted before being committed to the repository. This prevents spam, injection attacks, and other unwanted side effects.

### 4. Log Everything

Comprehensive logging at every trust boundary enables post-incident forensic analysis, policy validation, and detection of anomalous behavior.

---

## Architecture Layers

The security architecture consists of three distinct layers, each enforcing specific security properties:

### Substrate Layer

The **substrate layer** provides the foundational infrastructure and runs on top of [[GitHub Actions]] runner virtual machines.

**Components:**
- Action runner VM (OS, hypervisor)
- Docker containers with isolated environments
- Trusted containers (firewall, MCP gateway, API proxy)

**Security Properties:**
- Component isolation through containerization
- Mediation of privileged operations and system calls
- Kernel-enforced communication boundaries
- Protection holds even if user-level components are compromised

### Configuration Layer

The **configuration layer** includes declarative artifacts and toolchains that instantiate a secure system structure.

**Components:**
- [[Compiler]] for Agentic Workflows extension
- Firewall policies with allowlisting
- [[MCP]] (Model Context Protocol) configuration
- Docker image specifications and authentication tokens

**Security Properties:**
- Dictates which components are loaded and active
- Controls component connectivity and communication channels
- Assigns privileges and manages external tokens
- Ensures tokens are loaded only into appropriate containers

### Planning Layer

The **planning layer** creates staged workflows with explicit data exchanges and manages runtime execution flow.

**Components:**
- Safe outputs subsystem
- Call filtering mechanisms
- Output sanitization tools

**Security Properties:**
- Creates staged workflow with explicit data exchanges
- Enforces which components are active over time
- Manages timing and sequencing of operations
- Implements content analysis and sanitization

---

## Zero-Secrets Architecture

### Challenge

Agents are susceptible to [[prompt injection]] attacks where malicious inputs (web pages, repository issues, etc.) can trick agents into leaking sensitive information. A compromised agent could:
- Read configuration files and SSH keys
- Access Linux `/proc` state and workflow logs
- Upload secrets to external websites
- Encode credentials in public repository objects

### Solution: Container Isolation

Agents execute in a dedicated container with tightly controlled egress:

1. **Firewalled Internet Access**: Private network between agent and firewall
2. **MCP Gateway Isolation**: [[MCP]] servers run in separate trusted container with exclusive access to authentication material
3. **API Proxy for LLM Tokens**: [[LLM]] authentication tokens stored in isolated API proxy rather than exposed to agent container

### File System Isolation

To balance security with utility (agents need access to compilers, interpreters, and repository state):

- Mount entire VM host filesystem read-only at `/host`
- Overlay selected paths with empty `tmpfs` layers
- Launch agent in `chroot` jail rooted at `/host`
- This constrains writable surface to only what agent needs for its job

### Architecture Diagram

```
[Codex Token] → [API Proxy] → [OpenAI Service]
                     ↓
[Agent Container] → [Firewall] → [MCP Gateway] → [GitHub MCP]
(chroot/host)       (Docker)     (Docker)         (GitHub PAT)
```

---

## Staged and Vetted Writes

### Workflow Compilation

The Agentic Workflows compiler decomposes workflows into explicit stages, defining for each stage:
- Active components and their permissions (read vs. write)
- Data artifacts emitted by that stage
- Admissible downstream consumers of those artifacts

### Safe Outputs Subsystem

While agents run, they can:
- Read GitHub state through the GitHub [[MCP]] server
- Only stage updates through the **safe outputs MCP server**

After agent execution, buffered write operations pass through a suite of deterministic analyses:

1. **Operation Filtering**: Workflow authors specify which GitHub write operations are allowed (issues, comments, pull requests, etc.)

2. **Volume Limiting**: Restrict number of updates allowed (e.g., maximum three pull requests per run)

3. **Content Sanitization**: 
   - Remove unwanted patterns (URLs, sensitive data)
   - Remove secrets from output
   - Apply content moderation

Only artifacts passing the entire safe outputs pipeline can proceed downstream, ensuring explicit and vetted side effects at each stage.

---

## Comprehensive Logging and Observability

### Logging Strategy

Agentic Workflows implement pervasive logging at each trust boundary to support forensic reconstruction and anomaly detection:

**Firewall Layer:**
- Network and destination-level activity recording
- Traffic pattern analysis

**API Proxy Layer:**
- Model request/response metadata
- Authenticated request capture

**MCP Gateway and Servers:**
- Tool invocation logging
- Service call tracking

**Agent Container:**
- Internal instrumentation for sensitive actions
- Environment variable access auditing

### Forensic Capabilities

Comprehensive logging enables:
- End-to-end execution path reconstruction
- Policy validation and compliance verification
- Rapid detection of anomalous agent behavior
- Post-incident analysis and root cause determination

### Foundation for Future Controls

Pervasive logging creates the foundation for information-flow controls. Every location where communication is observed is also a location where it can be mediated. Future enhancements include:
- Additional safety controls based on [[MCP]] server policies
- Visibility-based policies (public vs. private)
- Author role-based access controls

---

## Related Concepts

### [[AI Agents]]
Autonomous systems that can reason about code and repository state, requiring novel security approaches when integrated into CI/CD pipelines.

### [[GitHub Actions]]
The underlying automation platform on which Agentic Workflows run, providing the execution environment and trust model.

### [[Prompt Injection]]
A security vulnerability where malicious inputs trick AI agents into performing unintended actions or revealing sensitive information.

### [[Model Context Protocol]] (MCP)
The protocol enabling agents to interact with tools and services in a controlled manner through the MCP gateway.

### [[CI/CD]]
Continuous integration and continuous deployment systems that benefit from agentic automation while requiring security constraints.

### [[LLM]] (Large Language Model)
The underlying AI models powering agents, requiring isolated authentication and API access controls.

---

## Future Developments

GitHub is actively developing additional safety controls including