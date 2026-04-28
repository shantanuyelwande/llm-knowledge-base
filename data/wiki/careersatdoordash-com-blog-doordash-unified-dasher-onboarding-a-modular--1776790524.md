---
title: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524
source_file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
source_url: https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-04-28T05:35:16.298450
raw_file_updated: 2026-04-28T05:35:16.298450
version: 1
sources:
  - file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-04-28T05:35:16.298450
tags: []
related_topics: []
backlinked_by: []
---
# Unified Dasher Onboarding Platform

## Summary

The **Unified Dasher Onboarding Platform** is a modular, event-driven workflow system developed by [[DoorDash]] to manage [[Dasher]] signup and verification processes across multiple global markets. Designed to replace a fragmented legacy system, the platform uses composable steps, workflow orchestration, and centralized state management to enable rapid international expansion, simplified maintenance, and consistent user experiences across different regions.

---

## Overview

[[Onboarding]] represents a critical first step in a [[Dasher]]'s journey with [[DoorDash]]. As the company expanded into new countries, its initial streamlined signup flow evolved into a complex web of region-specific logic, custom validations, and disconnected systems. The resulting inconsistent user experiences and increasing maintenance overhead necessitated a complete architectural redesign.

The new Unified Dasher Onboarding Platform (DxO) reimagines onboarding as a configurable, [[event-driven architecture|event-driven]] workflow system rather than a tightly coupled set of APIs and hard-coded flows. This approach emphasizes flexibility, scalability, and reusability through clear [[separation of concerns]], [[declarative workflows]], and robust [[state management]].

---

## Legacy System Challenges

### Architectural Issues

The legacy onboarding system suffered from several critical structural deficiencies:

- **Fragmented architecture**: Three incompatible API versions coexisted, with newer versions still calling older handlers for [[backward compatibility]], creating tangled dependencies
- **Hard-coded flows**: Onboarding steps and sequencing were embedded directly in code, making modifications risky and error-prone
- **Tightly coupled business logic**: Country-specific and step-specific logic were scattered throughout the codebase with deep conditional chains based on context
- **Vendor coupling**: Inconsistent patterns for interacting with third-party services and downstream systems
- **Limited reusability**: Each market maintained duplicate logic across countries, slowing development
- **Scalability bottlenecks**: Adding new countries required extensive updates across multiple systems
- **Technical debt**: Years of incremental updates left dead code, outdated feature flags, and unclear dependencies

### Operational Issues

Data management problems compounded architectural challenges:

- **Multiple status tables**: Onboarding progress tracked across several disparate tables increased complexity and inconsistency risk
- **Multi-table updates**: Adding new steps required modifying multiple tables, increasing development time and error potential
- **Complex coordination**: Synchronizing data across tables led to brittle integrations and mismatches

---

## Platform Architecture

### High-Level Design

The new platform emphasizes clear [[separation of concerns]] with the following component structure:

1. **Client Layer**: Mobile or web applications initiating signup requests
2. **Middleware Layer**: Backend-for-frontend (BFF) or [[server-driven UI]] (SDUI) frameworks
3. **Onboarding Platform (DxO)**: Core orchestration and workflow execution
4. **Downstream Services**: External APIs and third-party vendors

### Internal Architecture

The system follows a layered approach:

- Clients communicate through middleware to the onboarding platform's public APIs
- A **workflow orchestrator** evaluates request parameters and context to determine which workflow should handle the request
- The selected workflow routes requests through appropriate steps based on current state
- Each step independently integrates with required downstream services and external vendors

---

## Core Design Principles

### Modular Step Architecture

Each onboarding step is implemented as an independent, reusable module encapsulating all logic required for a specific action:

- **Data collection**: Gathering required user information
- **Validation**: Verifying collected data
- **Service integration**: Calling external APIs and third-party vendors
- **Error handling**: Managing failures and retries
- **State management**: Updating own status within the centralized status map

Steps expose a standardized interface to the workflow layer without revealing internal details, enabling clean separation of concerns.

### Workflow Definition and Orchestration

Workflows are defined as ordered compositions of step modules:

```kotlin
class USWorkflow {
    private var steps: List<Step> = listOf(
       data_collection_1,
       data_collection_2,
       validation_1,
       validation_2,
       additional_validation
    )
    fun processStep()
    fun getCurrentStep()
}
```

The **workflow orchestrator** selects appropriate workflows based on contextual inputs such as country, market type, or onboarding state, then routes requests to corresponding handlers. This lightweight orchestration layer:

- Selects workflows based on attributes like country or region
- Routes incoming requests to selected workflow definitions
- Maintains simple, declarative logic without unnecessary coupling

### Step Ownership and Extensibility

The modular design enables domain team ownership:

- Different teams can manage respective onboarding steps independently
- [[Identity verification]] steps may be owned by security teams
- Payment setup steps may belong to finance teams
- Teams iterate on their steps without affecting others, provided they maintain the shared interface contract

This ownership model encourages parallel development with high independence and domain autonomy while maintaining clear responsibilities.

### Status Map: Unified State Management

A centralized **status map** replaces multiple tracking tables, providing a unified data model for onboarding states:

```kotlin
val statusMap: MutableMap<String, StepDetails>? = mutableMapOf()

@Serializable
data class StepDetails(
    @SerialName("step_status")
    val stepStatus: StepStatus,
    @SerialName("step_metadata")
    val stepMetadata: IStepMetadata? = null,
)
```

Key characteristics:

- Each step module updates its own entry in the status map
- State transitions are localized within the step's domain
- The workflow layer queries steps to determine user progress
- Data integrity ownership resides with the step performing the work
- Steps define custom completion logic through the `isStepCompleted()` interface

---

## Step Module Interface Contract

To enable independent development and smooth integration across teams, each step implements a standardized interface:

### Input Contract

Defines required contextual data:
- User identifiers
- Onboarding context
- Country and region information
- Prior step outputs

This ensures steps receive only necessary data, avoiding tight coupling.

### Execution Contract

Provides standardized `execute()` or `process()` methods encapsulating business logic:
- Data collection and validation
- External service calls
- Error handling and retries
- Completion or failure reporting

### Output Contract

Returns consistent response structures indicating:
- Success, failure, or pending status
- Data needed for subsequent steps
- Uniform responses enabling deterministic workflow progression

### Step Interface Definition

```kotlin
interface Step {
    val stepName: String
    var states: List<StepStatus>
    
    fun getResponseData(applicant: Applicant): OnboardingResponse
    fun isStepComplete(applicant: Applicant): Boolean
    fun processStep(applicant: Applicant, updateRequest: UpdateRequest)
}
```

---

## Advanced Features

### Composite Steps

Composite steps group multiple granular steps into logical units, accommodating market-specific variations:

- A single UI page may collectively gather personal information in one country
- The same information may be collected across separate screens in another country
- Composite steps orchestrate granular steps internally without changing individual implementations
- Enables handling country-specific product requirements cleanly without increasing code complexity

### Dynamic and Reusable Steps

The modular design enables:

- **Experimental steps**: Conditional steps like _Waitlist_ appearing only in specific markets or supply conditions
- **Step reuse**: Same step appearing multiple times within a workflow (e.g., _Data Collection #1 → Waitlist → Validation #1 → Waitlist → Validation #2_)
- **Flexible adaptation**: Onboarding flows adapt to evolving product requirements without complex branching or duplication

---

## Key Benefits

### Technical Advantages

- **Loose coupling**: Each step evolves independently without breaking others
- **Reusability**: Common steps shared across countries and workflows
- **Simplified development**: Adding or updating steps doesn't affect unrelated logic
- **Improved testing**: Each step tested and verified in isolation
- **Parallelization**: Independent steps execute concurrently for improved performance

### Organizational Advantages

- **Ownership flexibility**: Different domain teams manage respective steps independently
- **Clear responsibilities**: Each team owns specific business logic domains
- **Reduced dependencies**: Teams move faster within safe boundaries
- **Scalable growth**: System scales reliably across markets and integrations

---

## Case Study: Address Collection Step

The address collection step exemplifies the platform's flexibility. In the legacy system, introducing this step would have required touching multiple code paths and duplicating logic across countries.

With the new architecture:

- Built as a standalone step module encapsulating all address capture, validation, and storage logic
- When [[Australia]] required address collection early in onboarding for compliance, the step was simply inserted before