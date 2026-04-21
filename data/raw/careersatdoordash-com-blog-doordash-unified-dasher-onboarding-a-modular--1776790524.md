---
source_url: https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email
ingested_from: url
ingested_at: 2026-04-21T16:55:24.897159
---

# Unified Dasher Onboarding: A modular platform to scale globally  - DoorDash

**Source URL:** [https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email](https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/?utm_source=substack&utm_medium=email)
**Ingested:** 2026-04-21T16:55:24.897170

---

[Skip to content](https://careersatdoordash.com/blog/doordash-unified-dasher-onboarding-a-modular-platform-to-scale-globally/#content)

Blog

# Unified Dasher Onboarding: A modular platform to scale globally

February 2, 2026

\|

![Saurabh Gupta](https://careersatdoordash.com/wp-content/uploads/2024/04/saurabh.jpeg)

Saurabh Gupta

![](https://careersatdoordash.com/wp-content/uploads/2026/01/kenneth-li-sq15NflsDTc-unsplash.jpg)

Onboarding is the first critical step in a Dasher’s journey with DoorDash. As we have expanded into new countries, our initially streamlined signup flow gradually has evolved into a complex web of region-specific logic, custom validations, and disconnected systems. The onboarding experience has varied widely across markets, even within the same country, as well as across different countries and regions, leading to inconsistent user journeys and increasing maintenance overhead. To support global growth and deliver a scalable, adaptable onboarding experience, we needed to reimagine the system from the ground up.

Here we share how we rebuilt our onboarding platform into a unified, modular architecture that now powers signups across all DoorDash markets. We’ll walk through the core design principles, technical architecture, and how the new system enables rapid international launches, seamless localization, and alignment with our global strategy.

## Legacy System (Simplified View)

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-10.png)_Figure 1: This is a simplified, high-level version of DoorDash’s legacy architecture to manage Dasher onboarding in multiple countries._

## Key challenges in the legacy onboarding system

Over the years, our legacy onboarding system, as shown in Figure 1 above, evolved through multiple versions and one-off business requirements. While functional, it became increasingly difficult to maintain, extend, and scale. The challenges fell broadly into two categories: Architectural/systemic issues and operational/data management issues.

### Architectural/systemic issues

The legacy system included a number of structural deficiencies. Inconsistent architectures and a lack of standardization across regional modifications resulted in systemic difficulties, including:

- _Fragmented architecture: Three_ onboarding API versions coexisted, with newer APIs still calling older handlers for backward compatibility. Even V3 APIs continued to update V2 tables, creating tangled dependencies.
- _Hard-coded and brittle flows:_ Onboarding steps and their sequencing were embedded directly in the code, making it hard to introduce new flows or modify existing ones without risking regressions.
- _Tightly coupled business logic_:Country-specific, step-specific, and sequencing logic were spread throughout the codebase. Business logic began immediately after receiving gRPC requests, with deep _if/else_ chains based on country, step type, or prior state, making the system fragile and error-prone.
- _Vendor and service coupling:_ Onboarding steps interacted directly with downstream services and third-party vendors. Some steps invoked services that called vendors; others made vendor calls directly. This inconsistent layering made testing, debugging, and scaling more difficult.
- _Limited reusability and high duplication:_ Each market maintained its own version of the onboarding flow, duplicating logic across countries, slowing development, and complicating maintenance.
- _Scalability and maintenance bottlenecks:_ The system struggled to adapt to new markets or compliance needs. Adding a new country often required extensive updates across APIs, tables, and code branches, delaying launches and increasing engineering effort.
- _Accumulated technical debt:_ Years of incremental updates by multiple teams left behind dead code, outdated feature flags, and unclear dependencies, creating challenges to safely cleaning up or refactoring the system.

### Operational/data management issues

A second set of major challenges involved operational and data management issues that stemmed primarily from the fragmented and complex way that the Dasher onboarding progress had been tracked and maintained across multiple, disparate data tables.

- _Multiple status tables:_ Tracking onboarding progress required managing data across several status tables, increasing complexity and risking inconsistency.
- _Multi-table updates for new steps:_ Introducing a new onboarding step meant modifying multiple tables — each representing part of the workflow — which subsequently increased development time and the potential for errors.
- _Complex inter-table coordination:_ Ensuring synchronization between tables required close coordination across services, often leading to brittle integrations and data mismatches.

## System redesign: Building a scalable and modular onboarding platform

To address the limitations of the legacy system, we reimagined onboarding as a configurable, event-driven workflow platform instead of a tightly coupled set of APIs and hard-coded flows. The new architecture emphasizes flexibility, scalability, and reusability through clear separation of concerns, declarative workflows, and robust state management, enabling faster iterations, simpler maintenance, and reliable global expansion.

### Unified Dasher Onboarding Platform high-level architecture

The high-level architecture outlined below in Figure 2 shows the new Unified Dasher Onboarding Platform's design, which emphasizes clear separation of concerns and cleaner interfaces between its various modular components.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-12.png)_Figure 2: This high-level architecture shows the new Unified Dasher Onboarding Platform’s cleaner interfaces between various components._

### Internal architecture and sub-component interactions

As shown in Figure 3 below, major components interact within the system as follows:

- The client first communicates with a middle layer, such as a backend-for-frontend or, depending on the client, a foundry service, server-driven user interface ( SDUI, framework).
- The middle layer calls into the onboarding platform (DxO: Dasher Onboarding) through its public APIs.
- The workflow orchestrator evaluates the request parameters and context to determine which workflow should handle the request.
- The selected workflow routes the request through the appropriate steps based on its current state.
- Each step independently integrates with the required downstream services, which then interact with external vendors as needed.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-8.png)_Figure 3: These internal details of the Dasher onboarding, or DxO, system demonstrate how various sub-components are integrated._

## A modular architecture of workflows and steps

As we redesigned the system, our core idea was to break the monolithic process into discrete steps to allow us to define a configurable workflow that strings the steps together for any given market. Instead of hardcoding a single, rigid sequence of actions, we now treat each onboarding step as an independent module with a well-defined purpose and interface.

### Structured workflow definition

In the new architecture, onboarding flows are defined in a centralized workflow layer within the code, replacing the scattered and hard-coded sequences from the legacy system. This makes it much easier to introduce new steps, modify sequences, and support country-specific variations.

While the workflows are still defined programmatically, the platform is designed to evolve toward configuration-driven definitions, allowing future teams to modify flows dynamically without code changes.

For example, as shown in Figure 4, a simplified U.S. workflow might be: _Data collection #1 → Data collection #2 → Validation #1 → Validation #2 → Additional Validation_. Such a workflow can easily be adjusted or extended; if a country requires an extra step, such as “Additional data collection,” we simply plug that module into its workflow configuration. This flexibility has been a game-changer compared to the legacy system, in which adding a step meant touching core code.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-7.png)_Figure 4: Workflow definitions for three regions show that each can use steps in a different order._

The following example demonstrates how the US Workflow is defined as a class in Kotlin:

```
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

### Workflow routing and orchestration layer

At the heart of the new system is a lightweight orchestration layer, as shown in Figure 5, that is responsible for workflow selection and routing. Rather than executing or managing every step, this layer determines which workflow definition to use based on contextual inputs — such as country, market type, or onboarding state — and forwards the request to the appropriate workflow handler.

This design simplifies how onboarding flows are invoked while providing flexibility to introduce new workflows or region-specific variants without complex conditionals.

Key responsibilities include:

- Selecting the appropriate workflow based on attributes like country, region, or step type
- Routing incoming requests to the corresponding workflow definition

By keeping orchestration simple and declarative, we reduced unnecessary coupling and made it easier to plug in new workflow definitions as the platform evolves.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-11.png)_Figure 5: A workflow orchestrator routes requests based on contextual input._

### Modular step design

Each onboarding step is now implemented as an independent, reusable module. These modules encapsulate all the logic required for a specific onboarding action — such as collect personal details, identity verification, risk/compliance check, additional data collection, or document verification — and expose a standard interface to the workflow layer.

The workflow invokes the appropriate step module without needing to know its internal details, enabling a clean separation of concerns and making the system significantly easier to maintain and extend.

All the logic needed to perform a specific step’s function lives inside each module, including:

- What data to collect from the user
- How to validate that data
- When and how to call external services, for example, background check APIs
- How to handle completion, retries, or failures

Crucially, each step is self-contained and workflow-agnostic, knowing only how to do its own job and how to signal success or failure without being privy to the broader flow.

### Step ownership and extensibility

Each step can have a different owner across multiple teams, allowing domain teams to manage their respective parts of the onboarding process independently. The identity verification step, for instance, can be owned entirely by the security team, while the payment setup step can belong to the Finance team.

Because each step is an isolated, well-defined module, teams can iterate or enhance their steps without affecting others as long as they adhere to the shared interface contract with the workflow layer.

This ownership model encourages parallel development with high independence and domain autonomywith clear responsibilities, helping teams move faster without creating tight dependencies across organizational boundaries.

### Dynamic and reusable steps

The modular design allows us to:

- Easily add experimental or conditional steps, such as a _Waitlist_ that appears only in specific markets or supply conditions, and
- Reuse the same step in multiple places within a workflow — for example:

_Data Collection #1 → Waitlist → Validation #1 → Waitlist → Validation #2_

These capabilities make the onboarding flow highly flexible and adaptable to evolving product requirements without complex branching or code duplication.

As shown in Figure 6 below, each modular step within the DxO (Dasher Onboarding) system is designed as an independent, self-contained unit that encapsulates all the necessary logic for its specific onboarding action. This logic includes managing its own data collection and validation, as well as determining when and how to interact with required downstream services or third-party vendors (like a validation API). By keeping the vendor and service integration logic within the step itself, the system ensures a clean separation of concerns, making each step reusable, testable in isolation, and workflow-agnostic.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-13.png)_Figure 6: Each step independently interacts with downstream systems and, from there, with third-party vendors._

Figure 7 below illustrates the key concept that each modular step’s internal status is self-governing. Each step is responsible for updating its own state within the centralized status map, allowing for localized state transitions such as from _in progress_ to _completed_, _failed_, or _skipped_. This self-contained design allows each step to define its own unique completion criteria and recheck its progress independently, simplifying the overall workflow orchestration and making it more robust against failures or retries.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-14.png)_Figure 7: Each step independently handles its internal state and moves to various states as needed._

### Composite steps for product flexibility

We introduced composite steps to accommodate market-specific variations in how information is collected. A composite step groups multiple granular steps into a single logical unit. Two examples of this are shown in Figure 8:

- In one country, a single UI page might collectively gather all personal information.
- In another country, these might be separate screens or steps.

By defining a composite step — in this case, PersonalDetails — we can orchestrate these granular steps internally without changing the individual step implementations.

This enables us to handle country-specific product requirementsandUI variations cleanly, without increasing code complexity or breaking reuse across regions.

![](https://careersatdoordash.com/wp-content/uploads/2026/02/image-6-1024x469.png)_Figure 8: This diagram demonstrates how multiple workflows can reuse modular steps in different orders._

## Key benefits

By treating each step as a self-contained, composable module, we created a foundation that’s both technically robust and organizationally scalable — enabling rapid experimentation, clearer ownership, and seamless adaptation to new markets. Among the benefits are:

- _Loose coupling_: Each step can evolve independently without breaking others.
- _Reusability_: Common steps are shared across countries and workflows.
- _Simplified development_: Adding or updating a step doesn’t affect unrelated logic.
- _Improved testing:_ Each step can be tested and verified in isolation.
- _Parallelization:_ Independent steps can execute concurrently to improve performance.
- _Ownership flexibility:_ Different domain teams can own and manage their steps independently.

### Step module interface contract

To enable independent development and smooth integration of modules across teams, each step implements a standardized interface contract. This ensures that every module, regardless of its internal logic or ownership, can seamlessly plug into the onboarding platform.

### Standard interface design

Each step module exposes a minimal, consistent interface that defines how it interacts with the workflow layer. At a high level, the interface includes:

- _Input contract_ **:** Defines what contextual data the step requires to execute, such as user identifiers, onboarding context, country, or prior step outputs. This ensures each step receives only the data it needs, avoiding tight coupling with other modules or workflows.
- _Execution contract:_ Provides a standardized _execute() or process()_ method that encapsulates the main business logic. The workflow layer invokes this method, and the step handles:
  - Data collection and validation,
  - External service calls, if required,
  - Error handling and retries, and finally
  - Reporting completion or failure back to the workflow layer.
- _Output contract:_ Returns a consistent response structure indicating success, failure, or pending status, along with any data needed for the next step. This uniform response allows the workflow to progress deterministically without knowing the internal details of each step.

The method isStepCompleted() encapsulates the logic for determining whether the step should be considered complete. Rather than relying on fixed rules in the workflow, each step can implement custom logic.

This flexibility allows each step to decide completion semantics based on its own state and metadata, as shown here:

```
interface Step {
    // step name
    val stepName: String

    // List of possible status for the step.
    var states: List<StepStatus>

    /**
     * Based on the state of the applicant, return the context data for the step.
     */
    fun getResponseData(applicant: Applicant): OnboardingResponse

    /**
     * workflow can use it to move to next task
     * This function will check statusMap of applicant and see if current task has reached to its terminal state.
     */
    fun isStepComplete(applicant: Applicant): Boolean

    /**
     * processes all valid actions as requested by the client for the step
     */
    fun processStep(applicant: Applicant, updateRequest: UpdateRequest)
}
```

### Status map: Unified data and state management

One of the biggest challenges in the legacy platform was how to manage onboarding progress reliably across multiple systems. Each step used to track its own progress through flags or timestamps scattered across services, making it nearly impossible to get a consistent view of where an applicant stood in their onboarding journey.

Previously, different parts of the system maintained their own view of progress; for example, flags like _validation\_complete = true or documents\_uploaded = false_ persisted across different databases. Reconstructing an applicant’s actual position required querying multiple systems and inferring logic, often leading to errors when a user returned mid-flow.

To solve this, we introduced the status map, a unified data model for onboarding states.

### Step-driven state updates

In the new system, each step module is responsible for updating itself in the status map. When a step starts, completes, fails, or skips execution, it directly updates its entry in the map. This ensures that:

- State transitions are localized within the step’s domain,
- The workflow layer simply queries the step to know where the user stands, and
- Ownership of data integrity resides with the step that actually performs the work.

This pattern also makes it easier to extend or modify how individual steps interpret completion. For example, one step may treat a “skipped” state as completed, while another may not.

### Self-validation through isStepCompleted

Each step exposes an interface like _isStepCompleted()_ to determine whether it has achieved its goal based on the latest data and metadata in the status map. This allows steps to:

- Define custom completion logic, such as considering _SKIPPED_ as a terminal state
- Recheck their own progress on retries or restarts without relying on external inference, and
- Keeps the overall workflow simple and stateless.

### Benefits of the step-driven model

With decentralized control, steps own their state transitions and completion criteria. Additionally, simpler workflow logic means that the workflow doesn’t need to infer or synchronize its progress. This approach’s flexibility allows different steps to define what “complete” means in their own context.

The following shows how status-map is defined in Kotlin and provides a few examples of its usage:

```
val statusMap: MutableMap<String, StepDetails>? = mutableMapOf()

@Serializable
data class StepDetails(
    @SerialName("step_status")
    val stepStatus: StepStatus,
    @SerialName("step_metadata")
    val stepMetadata: IStepMetadata? = null,
)

@Serializable
sealed class IStepMetadata {
    companion object {
        const val SERIALIZATION_TYPE_IDENTIFIER_PERSONAL_INFO_METADATA = "PersonalInfoMetadata"
        const val SERIALIZATION_TYPE_IDENTIFIER_ADDITIONAL_INFO_METADATA = "AdditionalInfoMetadata"
        const val SERIALIZATION_TYPE_IDENTIFIER_VALIDATION_METADATA = "ValidationMetadata"
    }
}

@Serializable
@SerialName(SERIALIZATION_TYPE_IDENTIFIER_PERSONAL_INFO_METADATA)
data class PersonalInfoMetadata(
    @SerialName("name")
    val name: String,
) : IStepMetadata()

@Serializable
@SerialName(SERIALIZATION_TYPE_IDENTIFIER_ADDITIONAL_INFO_METADATA)
data class AdditionalInfoMetadata(
    @SerialName("address")
    val address: String,
) : IStepMetadata()

@Serializable
@SerialName(SERIALIZATION_TYPE_IDENTIFIER_VALIDATION_METADATA)
data class ValidationMetadata(
    @SerialName("validation_metadata")
    val validationMetadata: String,
) : IStepMetadata()

// Geeneric implementation for each step to check the status (Part of DefaultProcessing)
override suspend fun isStepComplete(applicant: DasherApplicant): Boolean {
    return applicant.statusMap?.get(stepName)?.stepStatus in stepSuccessStates
}

// How to update Address
private fun updateStatusMapForAddress(
    address: String,
    addressId: String,
) {
    val statusMap: MutableMap<String, StepDetails> = mutableMapOf()
    val addressMetaData = AddressMetadata(
        addressId = addressId,
        address = address,
    )

    statusMap[OnboardingStep.ADDRESS.name] = StepDetails(
        stepMetadata = addressMetaData,
        stepStatus = StepStatus.DONE,
    )

    saveStatusMapToDB(statusMap)
}

// NOTE: StatusMap is JSON object. Using 'COALESCE' make sure that only single JSON-Key is updated

// Something like:
// $COLUMN_STATUS_MAP = COALESCE($COLUMN_STATUS_MAP, '{}'::jsonb) || COALESCE(:value::jsonb, '{}'::jsonb),
```

## Composable workflows and market adaptability

While the new onboarding platform is still code-defined today, its architecture was built around composition and reuse, which has allowed us to assemble onboarding experiences for different markets without rewriting logic.

At its core, a workflow is simply an ordered composition of independent step modules. Each module encapsulates its own functionality and interacts only through defined interfaces and the shared status map. This design makes it easy to add, remove, or rearrange steps within a workflow while keeping the overall system stable.

For example, a region might require a few additional checks or an alternate ordering of steps to meet local regulations. In the new architecture, those adjustments are straightforward: Engineers can modify the workflow definition directly in code — for instance, inserting an existing step module, skipping one, or changing its sequence — without impacting any other markets.

This composability provides several tangible benefits:

- _Code reuse:_ Common modules like validation, data collection, or compliance are implemented once and reused everywhere.
- _Safe iteration:_ Because workflows are composed of isolated modules, changes to one flow don’t create side effects elsewhere.
- _Rapid adaptation:_ Market-specific variations or pilot experiments can be supported by small workflow edits rather than new feature branches.
- _Future readiness:_ The design already supports a future transition to configuration-driven workflows, where the same logic could be defined declaratively outside of code.

In short, by treating workflows as composable assemblies of reusable step modules, we made onboarding flexible enough to adapt to business needs quickly,  while keeping the codebase unified and maintainable.

## Case study: Address collection as a reusable step

One of the clearest demonstrations of the new platform’s flexibility can be found in the address collection step. In the legacy system, introducing a new step like this would have required touching multiple code paths and duplicating logic across markets in different countries. With the new modular architecture, we built the addresscollection as a standalone step module that encapsulates everything needed to capture, validate, and store a Dasher’s address.

When Australia’s onboarding flow required an address early in the process for compliance checks and communications, we simply inserted the module before that market’s compliance check step in the workflow definition. No special logic or branching was needed. The workflow automatically invoked it for Australian users and skipped it elsewhere.

Soon after, Canada adopted the same step for validation and service-area mapping. Because the module was designed to be location-agnostic through using international address libraries and shared metadata, it worked out-of-the-box. Later, for the U.S., the team experimented by enabling the same step in select regions — again, with no new code.

This example illustrates the plug-and-play nature of the system: Once a step module exists, it can be reused anywhere by referencing it in a workflow definition. It’s the architectural equivalent of snapping a new Lego piece into an existing set; the modification is instantly consistent, reliable, and maintainable across all markets.

### From U.S. launch to global rollout

Once the new onboarding platform was ready, our first goal wasn’t to expand to new markets. Instead, we focused on migrating existing onboarding systems in every country onto this unified architecture. Each region already had its own legacy flow, often with subtle differences accumulated over time. The challenge was to transition all of them smoothly, without disrupting active onboarding or requiring parallel systems to coexist for long.

We began with our largest and most complex market — the United States — as the proving ground. In  January 2025, the U.S. onboarding system was fully migrated to the new workflow-and-step architecture for all new Dasher signups. This successful migration validated the core design principles around modular steps, reusable workflows, and isolated ownership.

With that success, we progressively migrated the rest of our markets over the following months, leveraging the same framework and many of the same modules. Because the system was composable and reusable by design, each migration required minimal engineering work:

- _Australia_ migrated next and was completed in less than a month. The team added only two localized steps before reusing the rest of the existing workflow logic.
- _Canada_ followed within two weeks, reusing nearly all existing modules and introducing only a single new one for compliance reasons.
- _Puerto Rico_ took about a week, with a minor customization in the compliance step for regional differences.
- _New Zealand_ came on board soon after, requiring almost no new development because its process mirrored existing ones.

Even more important than speed was reliability. Every migration launched cleanly, with zero regressions or user-facing incidents in either new or existing countries. There was no onboarding downtime or spikes in support tickets. And there were no unexpected drop-offs in completion rates.

Each market switch was smooth and predictable, largely because the architecture emphasized reusability, isolation, and exhaustive testing. By the time later migrations occurred, most modules had already been exercised by thousands of Dashers in prior markets, turning every subsequent rollout into a low-risk deployment.

The global migration not only unified our onboarding infrastructure but also validated the resilience and scalability of the new design, proving that even complex, market-specific systems could be consolidated safely under a single, modular platform.

### Building for global scale: Unifying onboarding across countries

The unified onboarding platform we initially built was never meant to serve a single product or market. From the beginning, it was designed as a global foundation that would be flexible enough to support multiple countries and regions within a single architectural framework.

### Expanding beyond a single ecosystem

As DoorDash prepared to integrate Dasher onboarding with another large, independently developed ecosystem, the need for a scalable and adaptable foundation became even clearer. That system had its own mature onboarding flow, shaped by different operational models and regional requirements. Our goal was to bring two established onboarding experiences under one unified platform without disrupting existing users or workflows.

The architecture we had invested in, modular step components, workflow composition, and clearly defined state management all provided the right structure for this expansion. It allowed us to:

- Build integration-specific workflows while reusing much of the existing modular logic.
- Introduce new step modules where needed, without affecting other markets.
- Represent complex variations through combinations of smaller, composable steps.

This ensured consistency, flexibility, and reliable scaling across multiple onboarding paths.

### Strengthening the platform through ongoing integration

The integration work is still underway, and that ongoing effort has helped validate and solidify our design choices. As we collaborate across teams, we continue to uncover opportunities to extend the platform and make it even more adaptable for future partners and markets.

Some of the forward-looking capabilities on our roadmap include:

- _Dynamic configuration loading_ to enable new workflows or markets to go live primarily through configuration rather than code.
- _Step versioning_ to allow multiple iterations of a step to coexist safely during transitions, experiments, or phased rollouts.
- _Enhanced operational tooling_ to give non-engineering teams the ability to manage workflows and toggle steps for pilots, regional launches, or experiments.

These enhancements ensure the system isn’t just scalable, but also highly adaptable and able to evolve quickly as DoorDash continues to expand globally.

### A unified future

The unified onboarding platform now serves as the shared foundation across multiple internal ecosystems, with a common backend and a design that leaves room for long-term growth.

This work represents more than a technical integration. It reflects a shared commitment to building a global onboarding system that is flexible, resilient, and prepared for what’s next.

Through this journey, several architectural principles have been reinforced:

- Modularity enables extensibility.
- Shared foundations simplify future integrations.
- A forward-looking design accelerates long-term expansion.

What began as a modernization effort for DoorDash onboarding has evolved into the blueprint for a global onboarding engine — one capable of supporting multiple markets from a single, adaptable foundation.

## Migration challenges

Migrating any live, multi-market system to a completely new architecture is never straightforward. We weren’t starting with a blank slate; every country already had its own onboarding flow, integrations, and in-flight applicants. One of the most complex parts of our effort was to ensure a smooth transition while maintaining business continuity.

### Backward compatibility and controlled transition

To minimize disruption, the new platform was designed to coexist with existing V2 and V3 APIs.

We implemented a gradual migration plan, allowing new workflows to run side-by-side with legacy ones. Teams could progressively onboard new applicants and markets using the new system while older integrations continued to function reliably. This approach gave us the confidence to migrate incrementally rather than through a risky “big-bang” switch.

### Navigating parallel projects

During development, several other major initiatives were underway, each critical in its own right but often conflicting with the new onboarding design. Rather than treating these as blockers, we collaborated closely with those teams to understand their use cases and adapt our architecture where necessary. This iterative alignment helped us prevent rework and ensured that the final system served all active business needs.

### Data synchronization and legacy states

Another major challenge was keeping data in sync between old and new systems during the rollout.

Applicants who had partially completed onboarding under the legacy system needed a way to continue seamlessly even after the migration began. We built temporary synchronization mechanisms that mirrored progress between systems until the migration was complete. This ensured that no applicant lost progress or encountered inconsistent states, even as we switched over to the unified platform.

## Lessons learned

Several key lessons stand out as we reflect on this multi-year effort. We learned not just about architecture, but about how to approach large-scale platform transformations, including that we should:

- _Design for global scale early:_ Thinking from a global perspective and working backward from diverse market requirements leads to naturally extensible systems. Building for multiple regions from the start saved us from painful redesigns later.
- _Start from first principles:_ When rebuilding foundational systems, we can ensure that each component exists for the right reason by questioning assumptions and reasoning from first principles. This mindset helped us create a clean, maintainable architecture rather than layering patches on legacy complexity.
- _Invest in a strong foundation:_ Taking the time to define clear boundaries, reusable modules, and robust data contracts paid off significantly. A well-designed foundation enables faster iteration later and reduces long-term operational costs.
- _Prioritize backward compatibility and continuity:_ Migration and business continuity cannot be afterthoughts; they are integral to good system design. Building compatibility into the architecture from day one allowed us to modernize without disrupting active onboarding or existing integrations.
- _Recognize platform as a partnership:_ We learned to define and publish clear platform principles, step ownership, and versioned contracts so that responsibilities are clear across the board. Through providing flexible extension contracts and guardrails, we can ensure that domain expert teams own their business logic — such as fraud, authenticity, compliance, and payment matters — while the platform enforces consistency. Using joint key performance indicators and accountability mechanisms creates a win-win model; teams can move fast within safe boundaries while the platform scales reliably across markets.

Together, these lessons shaped not only the unified onboarding platform but also how we now approach platform evolution at DoorDash. We now start with scale in mind, build solid foundations, and never compromise on reliability during transition.

## Engineering efficiency and future growth

Rebuilding the Dasher onboarding platform from the ground up into a unified, modular system was one of the most ambitious engineering efforts undertaken at DoorDash — and it has delivered significant returns. We transformed what was once a fragmented, region-specific set of workflows into a global onboarding platform that is robust, flexible, and efficient. The impact has been felt immediately across engineering and operations:

- _Faster development velocity:_ Launching or migrating a market now takes days or weeks instead of months.
- _Improved reliability:_ Major launches have seen virtually zero regressions or user-impacting issues.
- _Simplified maintainability:_ Engineers can now reason about onboarding through a consistent, standardized framework instead of scattered logic.

## Looking ahead

The Unified Dasher Onboarding Platform now serves as a foundation for future innovation. As DoorDash continues to expand globally and integrate new lines of business, this unified platform ensures we can scale confidently — whether that means supporting new countries, new products, or new partners.

Moving from fragmentation to global unification wasn’t just about consolidating code — it was about redefining how we build for scale. By investing deeply in foundational architecture, we created a system that delivers speed, safety, and scalability together. The unified onboarding platform is more than a technical achievement. It’s a blueprint for how thoughtful platform engineering can unlock growth and reliability across an entire organization.

## Acknowledgement

Thank you to **Jason Yao** for working with me on the core platform work and supporting multiple country launches. I’m grateful to **Shan Zhong** and **Nandini Nagaraj** for always being available for brainstorming and thoughtful discussions. Thanks to **Devesh Sanghvi, Andrii Kurshyn, Linda Martinez, and Tom Zheng** for partnering with me to validate the platform. I also appreciate the continued leadership support from **Niting Qi, Srinivasaraghavan Vedanarayanan, and Monica Blaylock**, and the valuable product input provided by **Claire Blumenthal**.

## About the Author

- ![](https://careersatdoordash.com/wp-content/uploads/2024/04/saurabh.jpeg)






Saurabh Gupta is a Software Engineer on the DasherGrowth team at DoorDash. His focus is on developing backend systems, tools to solve existing and new problems. In his free time, he likes outdoors wherever possible and like to spend time with family and friends.


## Related Jobs

[View All Jobs](https://careersatdoordash.com/job-search/?department=Engineering%7C)

[Controls Engineer](https://careersatdoordash.com/jobs/controls-engineer/7798895)

Job ID: 3210575

Location

San Francisco, CA

Department

Engineering

[View Job](https://careersatdoordash.com/jobs/controls-engineer/7798895)

[Engineering Manager, Tax Platform](https://careersatdoordash.com/jobs/engineering-manager-tax-platform/7782911)

Job ID: 3021664

Location

Toronto, ON

Department

Engineering

[View Job](https://careersatdoordash.com/jobs/engineering-manager-tax-platform/7782911)

[Manager, Cyber Defense](https://careersatdoordash.com/jobs/manager-cyber-defense/7774182)

Job ID: 3404075

Location

San Francisco, CA; Seattle, WA; Tempe, AZ; United States - Remote

Department

Engineering

[View Job](https://careersatdoordash.com/jobs/manager-cyber-defense/7774182)

[Engineering Manager, Pricing Platform](https://careersatdoordash.com/jobs/engineering-manager-pricing-platform/7768624)

Job ID: 2728459

Location

San Francisco, CA; Sunnyvale, CA

Department

Engineering

[View Job](https://careersatdoordash.com/jobs/engineering-manager-pricing-platform/7768624)

[Staff Security Engineer, Proactive Security](https://careersatdoordash.com/jobs/staff-security-engineer-proactive-security/7767391)

Job ID: 3346007

Location

United States - Remote

Department

Engineering

[View Job](https://careersatdoordash.com/jobs/staff-security-engineer-proactive-security/7767391)

## Recent Blogs

[View All Blogs](https://careersatdoordash.com/blog)

[Our stance on AI and Interviewing\\
\\
culture\\
\\
DoorDash](https://careersatdoordash.com/blog/doordash-stance-ai-interviewing/)

[DoorDash celebrates the vibrant culture of Mexico City with new office opening\\
\\
culture\\
\\
DoorDash](https://careersatdoordash.com/blog/doordash-mexico-city-new-office-opening/)

[DoorDash enhances Canada presence with new Toronto office opening\\
\\
culture](https://careersatdoordash.com/blog/doordash-toronto-canada-new-office-opening/)

[Terms of Service](https://help.doordash.com/consumers/s/terms-and-conditions-us?language=en_US) [Consumer Privacy](https://help.doordash.com/consumers/s/privacy-policy-us?language=en_US) [Applicant Privacy Notice](https://help.doordash.com/legal/document?type=ax-privacy-notice&region=US&locale=en-US)

© 2026 DoorDash