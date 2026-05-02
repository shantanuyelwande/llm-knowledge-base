---
title: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524
source_file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
source_url: https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email
ingested_from: url
source_hash: 0000000000000000000000000000000000000000000000000000000000000000
compiled_at: 2026-05-02T05:15:16.777469
raw_file_updated: 2026-05-02T05:15:16.777469
version: 1
sources:
  - file: careersatdoordash-com-blog-doordash-unified-dasher-onboarding-a-modular--1776790524.md
    hash: 0000000000000000000000000000000000000000000000000000000000000000
    added_at: 2026-05-02T05:15:16.777469
tags: []
related_topics: []
backlinked_by: []
---
# Unified Dasher Onboarding Platform

## Summary

The **Unified Dasher Onboarding Platform** is a modular, event-driven workflow system developed by [[DoorDash]] to streamline and standardize the onboarding process for Dashers (delivery drivers) across multiple countries and regions. Launched in 2025, the platform replaced a fragmented legacy system with a scalable architecture featuring independent, composable step modules, centralized workflow orchestration, and unified state management. The redesign enables rapid market expansion, simplified maintenance, and improved reliability across DoorDash's global operations.

---

## Overview

As [[DoorDash]] expanded internationally, its original Dasher onboarding system evolved into a complex, region-specific collection of workflows with inconsistent architectures, hard-coded logic, and scattered data management. To support continued global growth while maintaining reliability and engineering efficiency, DoorDash undertook a comprehensive platform redesign, transforming onboarding into a unified, modular system capable of serving all markets from a single codebase.

The new platform treats each onboarding step as an independent, reusable module and defines workflows as composable sequences of these steps. This architectural approach enables teams to launch new markets in days or weeks rather than months, reduces technical debt, and allows domain teams to own and iterate on their respective onboarding components independently.

---

## Legacy System Challenges

### Architectural Issues

The legacy onboarding system suffered from several structural deficiencies that hindered scalability and maintainability:

- **Fragmented architecture**: Three coexisting API versions (V2, V3, and earlier) created tangled dependencies, with newer APIs still calling older handlers for backward compatibility
- **Hard-coded flows**: Onboarding sequences were embedded directly in code, making modifications risky and error-prone
- **Tightly coupled business logic**: Country-specific and step-specific logic were scattered throughout the codebase in deep if/else chains, creating fragility
- **Vendor coupling**: Inconsistent patterns for integrating with downstream services and third-party vendors complicated testing and scaling
- **Limited reusability**: Each market maintained duplicate versions of onboarding flows, slowing development and complicating maintenance
- **Accumulated technical debt**: Years of incremental updates left dead code, outdated feature flags, and unclear dependencies

### Operational Issues

Beyond architectural problems, the system faced significant data management challenges:

- **Multiple status tables**: Onboarding progress tracking required managing data across several disparate status tables, increasing complexity and risking inconsistency
- **Multi-table updates**: Adding new onboarding steps required modifying multiple tables, increasing development time and error potential
- **Complex coordination**: Ensuring synchronization between tables required brittle integrations and often resulted in data mismatches

---

## Platform Architecture

### High-Level Design

The new Unified Dasher Onboarding Platform emphasizes **clear separation of concerns** and **modular composition**. The architecture comprises:

1. **Client Layer**: Mobile or web applications initiating onboarding requests
2. **Middle Layer**: Backend-for-frontend (BFF) or server-driven UI (SDUI) framework services
3. **Onboarding Platform (DxO)**: Core platform exposing public APIs
4. **Workflow Orchestrator**: Routes requests to appropriate workflows based on context
5. **Workflow Layer**: Defines and executes step sequences for specific markets
6. **Step Modules**: Independent, self-contained implementations of onboarding actions
7. **Downstream Services**: External systems and third-party vendor integrations

### Workflow Orchestration and Routing

The lightweight orchestration layer determines which workflow definition to use based on contextual inputs such as:

- Country and region
- Market type
- Current onboarding state
- User attributes

Rather than executing steps directly, the orchestrator forwards requests to the appropriate workflow handler, reducing coupling and enabling flexible workflow composition.

### Modular Step Design

Each onboarding step is implemented as an independent, reusable module encapsulating:

- Data collection logic
- Validation rules
- External service integration
- Error handling and retries
- State management and completion criteria

Steps expose a standardized interface to the workflow layer, enabling clean separation of concerns and allowing teams to develop and iterate on their steps independently.

#### Step Interface Contract

Every step module implements a consistent interface defining:

- **Input contract**: Specifies required contextual data (user identifiers, country, prior outputs)
- **Execution contract**: Provides standardized `execute()` or `process()` method encapsulating business logic
- **Output contract**: Returns consistent response structure indicating success, failure, or pending status
- **Completion logic**: `isStepComplete()` method determines whether a step has achieved its goal

```kotlin
interface Step {
    val stepName: String
    var states: List<StepStatus>
    
    fun getResponseData(applicant: Applicant): OnboardingResponse
    fun isStepComplete(applicant: Applicant): Boolean
    fun processStep(applicant: Applicant, updateRequest: UpdateRequest)
}
```

### Status Map: Unified State Management

The **status map** is a centralized data model replacing the fragmented status tracking of the legacy system. Key characteristics:

- **Single source of truth**: Unified representation of each applicant's onboarding progress
- **Step-driven updates**: Each step module is responsible for updating its own entry in the status map
- **Self-contained state transitions**: Steps define their own completion criteria and state transitions
- **Simplified workflow logic**: The workflow layer simply queries steps to determine applicant progress

Each step updates its entry in the status map as it progresses through states such as:
- `IN_PROGRESS`
- `COMPLETED`
- `FAILED`
- `SKIPPED`

```kotlin
val statusMap: MutableMap<String, StepDetails> = mutableMapOf()

@Serializable
data class StepDetails(
    @SerialName("step_status")
    val stepStatus: StepStatus,
    @SerialName("step_metadata")
    val stepMetadata: IStepMetadata? = null,
)
```

### Step Ownership and Extensibility

The modular architecture enables **domain-based ownership**, allowing different teams to manage their respective onboarding components:

- **Security team**: Identity verification and risk assessment steps
- **Finance team**: Payment setup and banking information steps
- **Compliance team**: Regulatory and documentation verification steps

Because steps are isolated modules with well-defined interfaces, teams can iterate independently without creating tight dependencies across organizational boundaries.

### Composite Steps

**Composite steps** group multiple granular steps into a single logical unit, accommodating market-specific variations in information collection:

- One market may collect all personal information on a single UI page
- Another market may require separate screens or sequential steps

By defining a composite step (e.g., `PersonalDetails`), the platform orchestrates granular steps internally without changing individual step implementations, enabling country-specific product requirements without increasing code complexity.

---

## Key Architectural Benefits

The modular, composable design delivers significant advantages:

- **Loose coupling**: Each step evolves independently without breaking others
- **Reusability**: Common steps are shared across countries and workflows
- **Simplified development**: Adding or updating a step doesn't affect unrelated logic
- **Improved testing**: Each step can be tested in isolation
- **Parallelization**: Independent steps can execute concurrently
- **Ownership flexibility**: Domain teams manage their steps independently
- **Market adaptability**: New markets can be launched through workflow composition without new code

---

## Global Implementation and Migration

### Migration Strategy

Rather than attempting a risky "big-bang" migration, DoorDash implemented a **gradual, controlled transition**:

1. **Coexistence**: New platform ran side-by-side with legacy V2 and V3 APIs
2. **Incremental rollout**: New applicants and markets progressively migrated to the new system
3. **Data synchronization**: Temporary mechanisms mirrored progress between systems during transition
4. **Backward compatibility**: Legacy integrations continued functioning reliably

### Market Rollout Timeline

The platform successfully migrated multiple markets with minimal disruption:

| Market | Timeline | Key Characteristics |
|--------|----------|-------------------|
| **United States** | January 2025 | Largest and most complex market; proved core design principles |
| **Australia** | ~1 month | Added two localized steps; reused existing modules |
| **Canada** | ~2 weeks | Reused nearly all modules; one new compliance step |
| **Puerto Rico** | ~1 week | Minor compliance step customization |
| **New Zealand** | Quick | Mirrored existing processes; minimal new development |

Each migration launched cleanly with zero regressions, no onboarding downtime, and no unexpected drop-offs in completion rates.

### Case Study: Address Collection Step

The address collection step exemplifies the platform's flexibility:

- **Australia**: Required address early for compliance;