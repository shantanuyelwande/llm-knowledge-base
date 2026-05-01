---
title: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524
source_file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
source_url: https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-01T05:45:59.391894
raw_file_updated: 2026-05-01T05:45:59.391894
version: 1
sources:
  - file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-01T05:45:59.391894
tags: []
related_topics: []
backlinked_by: []
---
# Unified Dasher Onboarding Platform

## Summary

DoorDash's Unified Dasher Onboarding Platform is a modular, event-driven workflow architecture designed to scale [[Dasher]] signup processes globally. Built to replace a fragmented legacy system, the platform uses composable step modules, centralized workflow orchestration, and unified state management to enable rapid international expansion, simplified maintenance, and consistent user experiences across markets.

## Overview

The Unified Dasher Onboarding Platform represents a complete architectural redesign of DoorDash's [[Dasher]] signup and onboarding process. Originally developed to address critical limitations in the legacy system, the platform has evolved into a global foundation supporting multiple markets, compliance requirements, and business variations from a single, unified codebase.

The platform emphasizes **modularity**, **reusability**, and **scalability** through clear separation of concerns, enabling different teams to own specific components independently while maintaining system-wide consistency and reliability.

## Legacy System Challenges

### Architectural Issues

The original onboarding system accumulated significant technical debt over years of incremental modifications:

- **Fragmented Architecture**: Three coexisting API versions (V1, V2, V3) with backward compatibility dependencies created tangled, difficult-to-navigate code structures
- **Hard-coded Flows**: Onboarding steps and sequencing were embedded directly in code, making modifications risky and error-prone
- **Tightly Coupled Logic**: Business logic spread throughout the codebase with deep conditional chains based on country, step type, or prior state
- **Vendor Coupling**: Inconsistent integration patterns with downstream services and third-party vendors made testing and scaling difficult
- **Limited Reusability**: Each market maintained duplicate versions of onboarding logic, slowing development and complicating maintenance
- **Scalability Bottlenecks**: Adding new countries required extensive updates across multiple APIs, databases, and code branches

### Operational Issues

Data management presented equally significant challenges:

- **Multiple Status Tables**: Onboarding progress tracking required managing data across several disparate status tables, increasing complexity and inconsistency risk
- **Multi-table Updates**: Introducing new steps required modifications to multiple tables, increasing development time and error potential
- **Complex Coordination**: Ensuring synchronization between tables required brittle, error-prone integrations

## Platform Architecture

### High-Level Design

The new platform implements a clear separation of concerns across distinct layers:

```
Client → Backend-for-Frontend/SDUI → DxO Public APIs → 
Workflow Orchestrator → Step Modules → Downstream Services → 
External Vendors
```

**Key Components:**

- **Workflow Orchestrator**: Routes requests to appropriate workflow based on contextual inputs (country, market type, onboarding state)
- **Workflow Definitions**: Ordered compositions of step modules specific to each market
- **Step Modules**: Independent, reusable units encapsulating specific onboarding actions
- **Status Map**: Unified data model for tracking onboarding state across all steps

### Workflow Orchestration Layer

The lightweight orchestration layer serves as the system's routing intelligence:

- **Workflow Selection**: Determines which workflow definition to use based on contextual attributes
- **Request Routing**: Forwards requests to appropriate workflow handlers
- **Declarative Design**: Reduces coupling and simplifies introduction of new workflow variants

Rather than executing or managing individual steps, the orchestrator maintains a simple, focused responsibility: selecting the right workflow and delegating execution to it.

## Modular Step Architecture

### Step Design Principles

Each onboarding step is implemented as an independent, self-contained module with a standardized interface contract. Steps encapsulate all logic necessary for specific actions such as:

- Personal data collection
- Identity verification
- Risk and compliance checking
- Document verification
- Address validation

**Key Characteristics:**

- **Self-contained**: Includes data collection, validation, external service calls, and error handling
- **Workflow-agnostic**: Knows only how to execute its own function, not the broader flow
- **Reusable**: Can be composed into multiple workflows in different orders
- **Independently testable**: Can be verified in isolation from other steps
- **Domain-owned**: Teams can manage and iterate on their steps independently

### Step Interface Contract

Each step implements a standardized interface ensuring seamless integration:

```kotlin
interface Step {
    val stepName: String
    var states: List<StepStatus>
    
    fun getResponseData(applicant: Applicant): OnboardingResponse
    fun isStepComplete(applicant: Applicant): Boolean
    fun processStep(applicant: Applicant, updateRequest: UpdateRequest)
}
```

**Contract Components:**

- **Input Contract**: Defines required contextual data (user identifiers, country, prior outputs)
- **Execution Contract**: Provides standardized `execute()` or `process()` method for business logic
- **Output Contract**: Returns consistent response structure indicating success, failure, or pending status

### Step Ownership and Extensibility

The modular design enables organizational scalability through distributed ownership:

- **Domain Team Ownership**: Different teams manage their respective steps (e.g., security team owns identity verification, finance team owns payment setup)
- **Independent Iteration**: Teams can enhance steps without affecting others, provided interface contracts remain stable
- **Parallel Development**: Multiple teams can work on different steps simultaneously without tight dependencies

## State Management: The Status Map

### Unified Data Model

The **Status Map** replaces the legacy system's fragmented progress tracking with a centralized, unified data structure:

```kotlin
val statusMap: MutableMap<String, StepDetails> = mutableMapOf()

@Serializable
data class StepDetails(
    val stepStatus: StepStatus,
    val stepMetadata: IStepMetadata? = null,
)
```

**Benefits:**

- **Single Source of Truth**: Provides consistent view of applicant's onboarding position
- **Localized Updates**: Each step updates only its own entry in the map
- **Metadata Flexibility**: Stores step-specific metadata for custom completion logic

### Step-Driven State Updates

Rather than external systems managing state, each step owns its state transitions:

- Steps update their status map entries when starting, completing, failing, or skipping
- Workflow layer queries steps to determine user position
- Data integrity responsibility resides with the step performing the work

### Self-Validation Pattern

The `isStepComplete()` method enables custom completion logic per step:

```kotlin
override suspend fun isStepComplete(applicant: DasherApplicant): Boolean {
    return applicant.statusMap?.get(stepName)?.stepStatus in stepSuccessStates
}
```

**Advantages:**

- **Custom Semantics**: Steps define what "complete" means in their context
- **Retry Resilience**: Steps can recheck progress without external inference
- **Simplified Orchestration**: Workflow remains stateless and straightforward

## Workflow Composition

### Structured Workflow Definition

Workflows are defined as ordered compositions of step modules, currently programmatically but designed for future configuration-driven evolution:

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

**Flexibility Features:**

- **Easy Modification**: Adding, removing, or reordering steps requires only workflow definition changes
- **Regional Variation**: Different markets can use steps in different orders without code duplication
- **Experimental Steps**: Conditional steps (e.g., Waitlist) can appear only in specific markets
- **Step Reuse**: Same step can appear multiple times in a workflow

### Composite Steps

Composite steps group multiple granular steps into single logical units, accommodating market-specific UI variations:

**Example**: A "PersonalDetails" composite step might collect all personal information on one page in one country but across multiple screens in another, without requiring changes to individual step implementations.

## Case Study: Address Collection Step

The address collection step exemplifies the platform's flexibility and reusability:

- **Australia**: Required address early for compliance; step was inserted before compliance check without modifications
- **Canada**: Adopted same step for validation and service-area mapping; worked out-of-the-box through location-agnostic design
- **United States**: Experimented with step in select regions; no new code required

This "plug-and-play" approach demonstrates how modular design eliminates duplicated logic across markets.

## Global Migration and Rollout

### Phased Migration Strategy

Rather than immediate global expansion, the platform focused first on consolidating existing systems:

**Timeline:**

- **January 2025**: United States migration completed successfully, validating core design principles
- **February 2025**: Australia migrated in less than one month with only two localized steps
- **February-March 2025**: