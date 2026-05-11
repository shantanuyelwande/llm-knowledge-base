---
title: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892
source_file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
source_url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-11T06:05:45.878247
raw_file_updated: 2026-05-11T06:05:45.878247
version: 1
sources:
  - file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-11T06:05:45.878247
tags: []
related_topics: []
backlinked_by: []
---
# GitHub Agentic Workflows Security Architecture

## Summary

**GitHub Agentic Workflows** are [[AI agent|AI-powered automations]] built on top of [[GitHub Actions]] that enable autonomous software engineering tasks while maintaining strict security controls. The security architecture is built on four core principles: defense in depth, zero-secret agents, staged and vetted writes, and comprehensive logging. This multi-layered approach isolates untrusted agent execution from sensitive resources through substrate, configuration, and planning layers.

## Overview

[[GitHub Agentic Workflows]] represent a new class of automation that goes beyond traditional [[CI/CD]] pipelines by introducing autonomous agents capable of reasoning over repository state and making runtime decisions. While this autonomy provides significant productivity benefits—such as automated documentation fixes, unit test generation, and code refactoring—it introduces unique security challenges that require novel architectural approaches.

The fundamental challenge is that agents are non-deterministic and must consume untrusted inputs, making them fundamentally different from traditional deterministic automation. Unlike conventional [[GitHub Actions]] that execute predetermined scripts, agents must be treated with suspicion and constrained through multiple security layers.

## Threat Model

The security architecture of GitHub Agentic Workflows is grounded in a comprehensive threat model that acknowledges two critical properties:

### Agent Non-Determinism and Autonomy

Agents cannot be trusted by default because they:
- Reason over repository state autonomously
- Make runtime decisions based on untrusted inputs
- Are susceptible to [[prompt injection]] attacks
- May attempt to exploit legitimate tools for unintended purposes

### Permissive Execution Environment

[[GitHub Actions]] provide a highly permissive execution environment where:
- All components share a single trust domain
- Broad access and composability are features for deterministic workflows
- A single compromise can create a large blast radius
- Sensitive material like [[authentication tokens]] and [[API keys]] are visible to all processes

Under this threat model, the default assumption is that agents will attempt to:
- Read and write unauthorized state
- Communicate over unintended channels
- Abuse legitimate channels for malicious purposes
- Exfiltrate sensitive information

## Core Security Principles

GitHub Agentic Workflows are guided by four foundational security principles:

### 1. Defense in Depth

The architecture employs a layered defense strategy with three distinct layers, each enforcing separate security properties:

#### Substrate Layer
- Runs on [[GitHub Actions]] runner [[virtual machines]]
- Uses [[Docker containers]] for component isolation
- Enforces kernel-level communication boundaries
- Provides OS and hypervisor-level protections
- Protects against arbitrary code execution within container boundaries

#### Configuration Layer
- Defines which components are loaded and how they connect
- Controls which communication channels are permitted
- Assigns privileges to components
- Manages authentication tokens and [[API keys]]
- Determines which tokens are loaded into which containers

#### Planning Layer
- Creates staged workflows with explicit data exchanges
- Implements the safe outputs subsystem
- Controls which components are active over time
- Stages agent decisions for vetting before execution

### 2. Don't Trust Agents with Secrets

Agents have zero access to sensitive credentials by design. This principle addresses the critical vulnerability of [[prompt injection]] attacks that could otherwise trick agents into leaking credentials.

#### Isolation Mechanisms

**Dedicated Container with Controlled Egress**
- Agents run in isolated containers with tightly restricted network access
- Private networks separate agents from external systems
- Firewalled internet access prevents arbitrary network communication

**MCP Gateway Separation**
- The [[Model Context Protocol]] (MCP) gateway runs in a separate trusted container
- MCP servers are launched and managed by the gateway
- Only the gateway has access to MCP authentication material
- Agents communicate with MCP through a trusted intermediary

**API Proxy for LLM Authentication**
- [[Language model]] authentication tokens are stored in isolated API proxies
- Agents route model traffic through the proxy rather than directly
- Prevents agents from accessing or exfiltrating authentication credentials

**Chroot Jail with Volume Mounts**
- Host file system is mounted read-only at `/host`
- Selected paths are overlaid with empty `tmpfs` layers
- Agents run in `chroot` jails with constrained writable surfaces
- Provides access to necessary development tools without exposing sensitive files

### 3. Stage and Vet All Writes

Even without access to secrets, compromised agents could cause harm through:
- Spam attacks (creating numerous issues or pull requests)
- Content injection (adding malicious URLs or objectionable content)
- Repository manipulation (corrupting state or structure)

#### Safe Outputs Analysis

The compiler decomposes workflows into explicit stages with defined:
- Active components and their permissions (read vs. write)
- Data artifacts emitted by each stage
- Admissible downstream consumers of artifacts

#### Write Operation Filtering

The safe outputs subsystem processes all agent writes through:

1. **Operation Filtering** - Specifies which write operations are allowed (e.g., creating issues, comments, or pull requests)
2. **Volume Limiting** - Restricts the number of operations (e.g., maximum three pull requests per run)
3. **Content Sanitization** - Removes unwanted patterns such as malicious URLs
4. **Secret Removal** - Strips any accidentally included credentials
5. **Moderation Analysis** - Detects and removes objectionable content

Only artifacts that pass the entire pipeline can be executed, ensuring explicit and vetted side effects.

### 4. Log Everything

Comprehensive logging provides visibility and forensic capability across all trust boundaries.

#### Logging Locations

- **Firewall Layer** - Records network and destination-level activity
- **API Proxy** - Captures model request/response metadata and authenticated requests
- **MCP Gateway** - Logs tool invocations and MCP server interactions
- **Agent Container** - Audits sensitive actions like environment variable accesses
- **MCP Servers** - Records all server operations and state changes

#### Forensic and Security Benefits

- End-to-end reconstruction of agent execution paths
- Policy validation and compliance verification
- Rapid detection of anomalous agent behavior
- Foundation for future [[information flow control]]

## Architecture Layers

### Substrate Layer

The substrate layer provides the foundational isolation and resource constraints:

- **Runner VM** - GitHub Actions runner virtual machine with OS and hypervisor protections
- **Docker Daemon** - Container runtime for component isolation
- **Trusted Containers** - Specialized containers for firewall, MCP gateway, and API proxy
- **Kernel Enforcement** - System-level call mediation and boundary enforcement

### Configuration Layer

The configuration layer defines the structure and connectivity of the system:

- **Compiler** - Transforms GitHub Agentic Workflows extensions into GitHub Actions
- **Firewall Policies** - Allowlists for network communication
- **MCP Configuration** - Specifies Docker images, authentication tokens, and server configuration
- **Token Management** - Controls credential distribution to components

### Planning Layer

The planning layer orchestrates execution and ensures safe outcomes:

- **Safe Outputs MCP** - Manages GitHub write operations with constraints
- **Call Filtering** - Controls tool availability and invocation volume
- **Output Sanitization** - Removes secrets and applies content moderation
- **Execution Staging** - Sequences operations for review and approval

## Related Technologies and Concepts

### [[GitHub Actions]]
The underlying platform on which Agentic Workflows execute, providing the runner infrastructure and workflow orchestration.

### [[Model Context Protocol]] (MCP)
The protocol enabling agents to interact with external tools and data sources in a controlled manner through the MCP gateway.

### [[Prompt Injection]]
A key threat that the architecture defends against by isolating agents and controlling their access to sensitive resources.

### [[GitHub Copilot]]
The AI code assistant that powers many agentic workflows, with extensions for autonomous operation.

### [[DevSecOps]]
The broader security philosophy that GitHub Agentic Workflows embodies by integrating security throughout the automation lifecycle.

## Future Developments

The GitHub Agentic Workflows team is planning additional security enhancements:

- **Information Flow Controls** - Policies enforcing restrictions based on repository visibility and object authorship
- **Lockdown Mode** - Already supported through GitHub MCP server configuration with enhanced restrictions in development
- **Role-Based Access Control** - MCP server policies based on the role of repository object authors
- **Enhanced Monitoring** - Additional observability and anomaly detection capabilities

## Getting Involved

The GitHub community is invited to:
- Share feedback in [Community Discussions](https://github.com/orgs/community/discussions/186451)
- Join the #agentic-workflows channel in the [GitHub Next Discord](https://gh.io/next-discord)
- Participate in security reviews and threat modeling discussions
- Report security concerns through proper channels

---

## Metadata

**Authors:** 
- Landon Cox, Senior Principal Researcher, Microsoft Research