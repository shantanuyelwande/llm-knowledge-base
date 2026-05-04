---
title: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892
source_file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
source_url: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-04T05:42:06.471299
raw_file_updated: 2026-05-04T05:42:06.471299
version: 1
sources:
  - file: github-blog-ai-and-ml-generative-ai-under-the-hood-security-ar-1776723892.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-04T05:42:06.471299
tags: []
related_topics: []
backlinked_by: []
---
# GitHub Agentic Workflows Security Architecture

## Summary

GitHub Agentic Workflows represent a secure approach to running [[AI agents]] in [[GitHub Actions]] environments. The architecture implements defense-in-depth security principles including agent isolation, zero-secret access, staged write operations, and comprehensive logging. By treating agent execution as an extension of the CI/CD model rather than a separate runtime, GitHub ensures that autonomous agents can safely automate repository tasks while maintaining strict security boundaries.

## Overview

[[GitHub Agentic Workflows]] enable teams to automate repository management tasks such as documentation fixes, unit test generation, and code refactoring through autonomous agents. However, the non-deterministic nature of agents—which must consume untrusted inputs, reason over repository state, and make runtime decisions—creates unique security challenges that traditional [[CI/CD]] automation does not face.

The security architecture of Agentic Workflows addresses these challenges through a layered approach that prevents agents from accessing secrets, ensures all write operations are vetted, and maintains comprehensive audit logs of all agent activities.

## Threat Model

### Key Assumptions

The threat model for Agentic Workflows is based on two critical properties:

1. **Agent Autonomy and Untrustworthiness**: Agents' ability to reason over repository state and act autonomously makes them valuable, but they cannot be trusted by default—especially when processing untrusted inputs such as web content or malicious [[GitHub issues]].

2. **Permissive Execution Environment**: [[GitHub Actions]] provide a highly permissive execution environment where components share a single trust domain. While this design enables broad access and good performance for deterministic automation, it creates a large blast radius when combined with untrusted agents.

### Threat Assumptions

Under this model, GitHub assumes that agents will attempt to:
- Read and write state they should not access
- Communicate over unintended channels
- Abuse legitimate channels to perform unwanted actions
- Leak sensitive information through [[prompt injection]] attacks

## Security Architecture

The security architecture consists of three distinct layers, each providing defense in depth against agent misbehavior:

### Substrate Layer

The **substrate layer** provides the foundational security infrastructure and runs on top of a [[GitHub Actions]] runner [[virtual machine]] (VM) with several trusted containers.

Key components include:
- **Isolation**: Separate containers for the agent, [[MCP]] gateway, and API proxy
- **Mediation**: Privileged operations and system calls are mediated through trusted components
- **Kernel-enforced Boundaries**: Communication boundaries are enforced at the operating system level

Even if an untrusted user-level component is compromised and executes arbitrary code, the kernel-enforced isolation prevents it from accessing resources outside its container boundary.

### Configuration Layer

The **configuration layer** includes declarative artifacts and toolchains that instantiate a secure system structure and manage component connectivity.

Responsibilities include:
- Determining which components are loaded and active
- Defining how components communicate
- Specifying which communication channels are permitted
- Controlling privilege assignment and token distribution

Critical inputs to this layer include externally minted tokens such as agent API keys and [[GitHub access tokens]], which bound components' external effects.

### Planning Layer

The **planning layer** creates staged workflows with explicit data exchanges between components and manages the active components over time.

Key functions include:
- **Safe Outputs Subsystem**: Buffers and vets all write operations before they are committed to the repository
- **Operation Filtering**: Restricts which GitHub operations (create issues, comments, pull requests) are allowed
- **Volume Limiting**: Enforces quotas on the number of operations allowed per workflow run
- **Content Sanitization**: Removes unwanted patterns such as API tokens and suspicious URLs

## Security Principles

### 1. Defend in Depth

The three-layer architecture ensures that failures at one level are contained by security properties at lower levels. Each layer makes distinct assumptions about the trustworthiness of components above it.

### 2. Don't Trust Agents with Secrets

Agents have **zero access to secrets** by default. This principle addresses the threat of [[prompt injection]], where attackers craft malicious inputs to trick agents into leaking sensitive information.

#### Secret Isolation Mechanisms

**Network Isolation**: Agents execute in a dedicated container with tightly controlled egress:
- Firewalled internet access through a private network
- [[MCP]] access through a trusted MCP gateway
- [[LLM]] API calls through an API proxy

**Credential Management**: 
- Agent authentication tokens and MCP server API keys are never exposed to the agent container
- [[LLM]] authentication tokens are placed in an isolated API proxy
- Agents route model traffic through the proxy rather than directly accessing credentials

**File System Constraints**:
- Agents run in a `chroot` jail with limited filesystem visibility
- The host filesystem is mounted read-only
- Writable paths are overlaid with empty `tmpfs` layers
- Selected host files and executables are exposed through container volume mounts

### 3. Stage and Vet All Writes

Even without access to secrets, compromised agents could cause harm by:
- Spamming repositories with pointless issues and pull requests
- Adding objectionable content to repository objects
- Performing unauthorized modifications

#### Safe Outputs Analysis

The **Safe Outputs MCP Server** implements a deterministic analysis pipeline:

1. **Operation Filtering**: Authors specify which write operations are allowed (e.g., create issues, add comments, create pull requests)
2. **Volume Limiting**: Enforces quotas on the number of operations per workflow run (e.g., maximum three pull requests)
3. **Content Moderation**: Analyzes update content to remove unwanted patterns
4. **Secret Removal**: Strips sensitive information from staged outputs

All write operations are buffered during agent execution and only committed after passing the complete Safe Outputs pipeline.

### 4. Log Everything

Comprehensive logging at each [[trust boundary]] enables:
- **Post-incident Analysis**: Complete reconstruction of execution paths
- **Policy Validation**: Verification that agents operated within constraints
- **Anomaly Detection**: Rapid identification of unexpected agent behavior

#### Logging Locations

- **Firewall Layer**: Network and destination-level activity
- **API Proxy**: Model request/response metadata and authenticated requests
- **MCP Gateway**: Tool invocations and MCP server interactions
- **Agent Container**: Internal instrumentation for sensitive actions like environment variable accesses

## Technical Implementation

### Container Architecture

The architecture uses multiple Docker containers with specific responsibilities:

- **Agent Container**: Runs the untrusted agent with restricted privileges
- **MCP Gateway Container**: Manages MCP servers and has exclusive access to MCP authentication material
- **API Proxy Container**: Routes LLM traffic and holds LLM authentication tokens
- **Firewall Container**: Enforces network policies and logs traffic

### Compilation Process

The Agentic Workflows compiler:
1. Decomposes workflows into explicit stages
2. Defines active components and permissions for each stage
3. Specifies data artifacts emitted by each stage
4. Identifies admissible downstream consumers of artifacts

### Execution Model

During execution:
1. Agents read GitHub state through the read-only GitHub MCP server
2. Agents stage updates through the Safe Outputs MCP server
3. All network traffic flows through the firewall
4. All LLM API calls route through the API proxy
5. Upon agent exit, Safe Outputs analyses process buffered updates
6. Only vetted updates are committed to the repository

## Future Enhancements

GitHub plans to introduce additional safety controls including:
- **Information-flow Controls**: Enforce policies across MCP servers based on visibility (public vs. private)
- **Role-based Access**: Restrict agent operations based on the repository object's author role
- **Lockdown Mode**: Enhanced restrictions on MCP server capabilities

## Related Concepts

- [[GitHub Actions]] - The execution environment for Agentic Workflows
- [[AI Agents]] - Autonomous systems that reason and act
- [[Model Context Protocol]] (MCP) - Interface for agents to interact with tools and data
- [[Prompt Injection]] - Attack technique where malicious inputs trick agents into misbehaving
- [[CI/CD]] - Continuous integration and deployment pipelines
- [[DevSecOps]] - Integration of security into the software development lifecycle
- [[GitHub Copilot]] - AI-powered code assistant
- [[LLM]] - Large Language Models that power agents

## See Also

- [[How AI Code Generation Works]]
- [[GitHub Actions Security]]
- [[Supply Chain Security]]
- [[Application Security]]

---

## Metadata

**Source**: GitHub Blog - AI & ML / Generative AI  
**Published**: March 9, 2026  
**Authors**: Landon Cox (Senior Principal Researcher, Microsoft Research) & Jiaxiao Zhou (Senior Software Engineer)  
**Original URL**: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-a