---
title: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524
source_file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
source_url: https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-06-07T06:30:24.819044
raw_file_updated: 2026-06-07T06:30:24.819044
version: 1
sources:
  - file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-06-07T06:30:24.819044
tags: []
related_topics: []
backlinked_by: []
---
# Unified Dasher Onboarding Platform

## Summary

The **Unified Dasher Onboarding Platform** is DoorDash's modernized architecture for managing new driver (Dasher) registration and onboarding across global markets. Rebuilt from a fragmented, region-specific legacy system into a modular, event-driven workflow platform, it enables rapid international expansion, consistent user experiences, and simplified maintenance through reusable step modules, declarative workflow composition, and unified state management.

## Overview

Onboarding represents the critical first touchpoint in a [[Dasher|Dasher's]] journey with DoorDash. As the company expanded into new countries, the initially streamlined signup flow evolved into a complex system with region-specific logic, custom validations, and disconnected services. This led to inconsistent user experiences across markets and increasing engineering overhead.

To support global growth and deliver a scalable, adaptable experience, DoorDash reimagined the onboarding system from first principles, creating a unified platform that now powers signups across all markets while maintaining flexibility for local requirements.

## Legacy System Challenges

### Architectural Issues

The legacy [[onboarding]] system suffered from several structural deficiencies:

- **Fragmented Architecture**: Three coexisting API versions (V1, V2, V3) with backward compatibility dependencies, creating tangled code paths
- **Hard-coded Flows**: Onboarding steps and sequencing embedded directly in code, making modifications risky
- **Tightly Coupled Business Logic**: Country-specific and step-specific logic scattered throughout the codebase with deep conditional branches
- **Vendor Coupling**: Inconsistent patterns for integrating with downstream services and third-party vendors
- **Limited Reusability**: Duplicate logic across markets, slowing development and complicating maintenance
- **Scalability Bottlenecks**: Adding new countries required extensive updates across multiple code layers
- **Technical Debt**: Years of incremental updates left dead code, outdated feature flags, and unclear dependencies

### Operational Issues

Data management posed equally significant challenges:

- **Multiple Status Tables**: Progress tracking required managing data across several disparate tables
- **Multi-table Updates**: Introducing new steps meant modifying multiple tables, increasing error risk
- **Complex Coordination**: Ensuring synchronization between tables required brittle inter-service coordination

## System Redesign Architecture

### High-Level Design

The new platform reimagines onboarding as a configurable, [[event-driven architecture|event-driven]] workflow system emphasizing:

- **Flexibility**: Modular components that can be composed in different configurations
- **Scalability**: Clear separation of concerns enabling independent team ownership
- **Reusability**: Shared step modules across countries and workflows
- **Maintainability**: Simplified logic through declarative workflow definitions

### Component Interactions

The architecture follows a layered approach:

1. **Client Layer**: Mobile or web clients communicate through a middle layer (backend-for-frontend or [[SDUI|server-driven UI]])
2. **API Layer**: Public APIs expose the onboarding platform (DxO: Dasher Onboarding)
3. **Orchestration Layer**: Workflow orchestrator evaluates context and routes to appropriate workflow
4. **Workflow Layer**: Selected workflow routes requests through steps based on current state
5. **Step Layer**: Individual steps independently integrate with downstream services and vendors

## Modular Architecture

### Workflow Definition and Composition

Onboarding flows are defined as ordered compositions of independent step modules. Rather than hard-coding sequences, workflows declaratively specify which steps execute and in what order.

**Example U.S. Workflow**:
```
Data Collection #1 → Data Collection #2 → Validation #1 → 
Validation #2 → Additional Validation
```

Different markets can reuse the same steps in different sequences:
- **Australia**: Data Collection #1 → Compliance Check → Data Collection #2
- **Canada**: Data Collection #1 → Data Collection #2 → Validation #1
- **Puerto Rico**: Data Collection #1 → Regional Validation → Data Collection #2

### Workflow Orchestration

A lightweight orchestration layer determines which workflow definition to use based on contextual inputs such as:

- Country or region
- Market type
- Current onboarding state
- User attributes

This layer routes requests to appropriate workflow handlers without executing steps directly, reducing coupling and enabling new workflows to be added without complex conditionals.

### Modular Step Design

Each onboarding step is implemented as an independent, reusable module encapsulating all logic for a specific action:

- Personal data collection
- Identity verification
- Risk and compliance checks
- Document verification
- Payment setup
- Background checks

Steps expose a standardized interface and are self-contained and workflow-agnostic. All logic lives within the step, including:

- Data collection requirements
- Validation rules
- External service calls
- Failure and retry handling
- Completion signaling

### Step Ownership Model

Each step can be owned by different domain teams, enabling:

- **Parallel Development**: Teams iterate independently on their steps
- **Domain Autonomy**: Clear responsibilities and minimal dependencies
- **Faster Iteration**: Changes to one step don't affect others as long as interface contracts are maintained

Examples of step ownership:
- **Security Team**: Identity verification step
- **Finance Team**: Payment setup step
- **Compliance Team**: Regulatory validation steps

### Dynamic and Reusable Steps

The modular design enables:

- **Experimental Steps**: Conditional steps like waitlists appearing only in specific markets
- **Step Reuse**: Same step appearing multiple times in a workflow (e.g., Data Collection → Waitlist → Validation → Waitlist → Validation)
- **Flexible Composition**: Steps can be combined to handle country-specific variations

### Composite Steps

Composite steps group multiple granular steps into logical units to handle market-specific variations:

- **Country A**: Single UI page collecting all personal information
- **Country B**: Same information split across multiple screens

A composite step like "PersonalDetails" orchestrates granular steps internally without changing individual implementations, enabling country-specific product requirements without increasing complexity.

## State Management: The Status Map

### Unified Data Model

The legacy system tracked progress through scattered flags and timestamps across multiple databases. The new system uses a **status map** — a unified data structure representing onboarding state:

```kotlin
val statusMap: MutableMap<String, StepDetails> = mutableMapOf()

data class StepDetails(
    val stepStatus: StepStatus,
    val stepMetadata: IStepMetadata? = null
)
```

### Step-Driven State Updates

Each step module is responsible for updating its own entry in the status map:

- When a step starts, completes, fails, or skips, it updates the map directly
- State transitions are localized within the step's domain
- The workflow layer queries steps to determine user progress
- Data integrity ownership resides with the step performing the work

### Self-Validation Through isStepCompleted()

Each step exposes an `isStepCompleted()` method to determine if it has achieved its goal:

```kotlin
interface Step {
    val stepName: String
    var states: List<StepStatus>
    
    fun getResponseData(applicant: Applicant): OnboardingResponse
    fun isStepComplete(applicant: Applicant): Boolean
    fun processStep(applicant: Applicant, updateRequest: UpdateRequest)
}
```

Steps can define custom completion logic:
- Some steps treat "SKIPPED" as a terminal state
- Others require explicit completion
- Steps recheck progress on retries without external inference

### Benefits of Step-Driven Model

- **Decentralized Control**: Steps own their state transitions and completion criteria
- **Simplified Workflow Logic**: Workflows don't need to infer or synchronize progress
- **Flexibility**: Different steps define "complete" in their own context
- **Resilience**: Clear state ownership prevents synchronization errors

## Key Benefits

### Technical Advantages

- **Loose Coupling**: Each step evolves independently without breaking others
- **Reusability**: Common steps shared across countries and workflows
- **Simplified Development**: Adding or updating steps doesn't affect unrelated logic
- **Improved Testing**: Steps can be tested in isolation
- **Parallelization**: Independent steps can execute concurrently
- **Clear Ownership**: Domain teams manage their steps independently

### Organizational Advantages

- **Faster Development Velocity**: Markets launch in days or weeks instead of months
- **Reduced Maintenance Overhead**: Standardized framework replaces scattered logic
- **Clear Responsibilities**: Step ownership prevents coordination overhead
- **Safe Iteration**: Isolated changes don't create unexpected side effects

## Global Migration and Expansion

### Migration Strategy

Rather than a risky "big-bang" switch, DoorDash implemented gradual migration:

- New platform coexisted with legacy V2 and V3 APIs
- New applicants and markets progressively transitioned
- Legacy