# Experiment 01: an ordinary weekday

Status: **completed model trace**

Model: **0.1**

Source data: [`ordinary-weekday.json`](ordinary-weekday.json)

## Question

Can the foundational family–home model explain an ordinary day containing routine cooperation, competing interests, dependencies, and unexpected changes without assuming a perfectly harmonious family or giving the home steward illegitimate authority?

## Fictional household

The River household is deliberately mixed enough to expose several kinds of participation:

| Participant | Layer | Relevant weekday position |
| --- | --- | --- |
| Maya | Core household | Hospital worker with an early shift; caregiver for Leila; support person for Miriam. |
| Jonah | Core household | Remote worker; caregiver for Leila; primary weekday carer for Pico. |
| Leila | Dependent | School-age member with care claims, growing autonomy, and age-appropriate household voice. |
| Miriam | Extended family | Nearby elder who sometimes needs transport support while retaining authority over her care. |
| Pico | Dependent | Companion animal with non-negotiable welfare needs. |
| Homie | Authorized participant | Delegated home steward with no family membership or independent sovereignty. |

This is an experimental instrument, not a preferred or universal family form.

## Day at a glance

```mermaid
timeline
    title River household — ordinary weekday
    05:45 : Quiet early-shift handoff
    06:35 : Bathroom and breakfast contention
    07:20 : School transport breaks down
    09:30 : Staples and pet food run low
    11:40 : Miriam's appointment moves
    15:30 : Leila returns during a work call
    17:10 : Water outage notice arrives
    18:30 : Dinner, chores, and connection
    20:00 : Homework and internet contention
    21:30 : Tomorrow and shared-memory review
```

## Episode trace

| Time | Episode | Components most visible | Decision authority | Steward mode | Result |
| --- | --- | --- | --- | --- | --- |
| 05:45 | Early-shift handoff | Participants, relationships, commons, coordination, continuity | Maya and Jonah | `automatic` | Executes a standing quiet routine and records only that the handoff occurred. |
| 06:35 | Bathroom and breakfast contention | Participants, relationships, commons, coordination | Leila and Jonah | `negotiate` | Fixed school time outranks flexible exercise; Leila helps choose the solution. |
| 07:20 | School transport disruption | Participants, care relationships, budget, coordination, external interface | Jonah as present caregiver | `confirm` | Compares vetted options; caregiver approves provider, spending, and minimal disclosure. |
| 09:30 | Staple replenishment | Participants, pantry, budget, coordination, market interface | Maya and Jonah through standing delegation | `automatic` | Orders exact approved staples below threshold; no subscription or sensitive inference. |
| 11:40 | Elder appointment change | All six components | Miriam for care; each adult for personal support; adults for shared budget | `escalate` | Miriam chooses the appointment; family boundaries remain visible; approved transport is booked. |
| 15:30 | Return from school | Participants, care, home, coordination, boundary | Caregivers for safety; Leila for private activity and bounded choices | `automatic` | Confirms safe entry without continuous surveillance and preserves decompression time. |
| 17:10 | Water outage | Participants, commons, coordination, continuity, utility interface | Affected household members | `propose` | Verifies the notice and offers a minimal plan; members divide preparation work. |
| 18:30 | Dinner and chores | Participants, relationships, commons, coordination, continuity | Maya, Jonah, and Leila within their roles | `negotiate` | Defers nonessential work and protects food, pet care, rest, and connection. |
| 20:00 | Homework and bandwidth | Participants, relationships, utility, coordination, boundary | Each content owner; household jointly for shared resources | `negotiate` | Sequences learning, work, and care without inspecting content or ranking by status. |
| 21:30 | Tomorrow and memory | Participants, relationships, coordination, continuity, boundary | Each person for commitments; affected members for shared-memory entries | `confirm` | Saves agreements and system lessons, not character judgments or private motives. |

## The feedback loop in one disruption

The elder-care episode exercises the full model without collapsing care into control.

```mermaid
sequenceDiagram
    participant Clinic as Clinic agent
    participant Homie as Home steward
    participant Miriam as Miriam
    participant Maya as Maya
    participant Jonah as Jonah
    participant Ride as Approved transport

    Clinic->>Homie: Earlier appointment is available
    Note over Clinic,Homie: Logistics only; no diagnosis
    Homie->>Miriam: Do you want the earlier appointment?
    Miriam-->>Homie: Yes; share minimum logistics
    par Ask about voluntary support
        Homie->>Maya: Can you provide transport?
        Maya-->>Homie: No during shift; evening check-in instead
    and
        Homie->>Jonah: Can you provide transport or approve budget?
        Jonah-->>Homie: Keep work call; approve ride budget
    end
    Homie->>Ride: Request approved trip with minimum data
    Ride-->>Homie: Trip confirmed
    Homie->>Clinic: Confirm accepted time
    Homie-->>Miriam: Appointment and transport confirmed
```

What matters is the allocation of authority:

- Miriam decides whether to accept care and what logistical information may be shared.
- Maya and Jonah each decide what personal support they can provide.
- The shared transport budget remains governed by its rights-holders.
- Homie coordinates the resulting commitments but does not choose care, reveal diagnosis, or conscript family labor.

## Information boundary test

The four information classes all appear in the experiment:

| Class | Example | Boundary behavior |
| --- | --- | --- |
| `private` | Sleep details, messages, work files, lesson content, health records, personal reflections | The home steward coordinates around these without reading or retaining them. |
| `shared` | Commitments, deadlines, resource availability, confirmed arrivals | Available for ongoing household coordination because participants intentionally shared it. |
| `purpose_delegated` | Appointment logistics, arrival window, maximum fare | Available only to complete a named purpose under a revocable delegation. |
| `external_approved` | Single-trip details, order items, service address | Released to a named external party with minimum necessary scope. |

The experiment exposes an important distinction: the steward often needs a constraint or conclusion, not the evidence behind it. “Unavailable until 10:00” can be shared while the reason remains private.

## Rights-floor test

Each episode records a rights-floor check before agent action:

- **Safety:** dependent transport uses vetted options; water and pet-care needs cannot be optimized away.
- **Dignity:** fatigue, delay, and dependence are not treated as moral failure.
- **Privacy:** the agent coordinates availability, bandwidth, and logistics without consuming content.
- **Basic autonomy:** people choose their commitments; Miriam chooses her care; Leila receives developmentally appropriate voice.

The rights floor does not eliminate disagreement. It defines what the negotiation may not sacrifice.

## Findings

1. **The steward coordinates constraints, not people as resources.** A useful agent exposes deadlines, dependencies, and feasible options while leaving legitimate decisions with their holders.
2. **Authority is contextual.** Technical access, age, income, or availability alone does not confer a right to decide. One episode can contain several simultaneous decision-holders.
3. **Privacy must govern inference and memory, not only disclosure.** Avoiding an external leak is insufficient if the household silently accumulates psychological or behavioral profiles.
4. **Invisible labor becomes a system state.** Care, planning, interruption, and deferred work need explicit owners or they repeatedly fall to the most available person.
5. **A dependent can have both care claims and agency.** Protection and voice are not opposites; the balance changes with capacity, context, and risk.
6. **Continuity is selective.** Healthy shared memory stores commitments, outcomes, and system lessons while refusing unnecessary judgments about character or private motives.
7. **Low-risk automation depends on prior governance.** An automatic purchase or arrival notification is legitimate only because its purpose, scope, thresholds, and revocation paths were established earlier.

## Model gaps exposed

The trace is coherent, but it reveals work for later versions:

1. **Delegation lifecycle:** creation, expiry, renewal, revocation, emergency suspension, and proof of current authority need a formal state model.
2. **Memory lifecycle:** shared entries need retention periods, correction, contestation, provenance, and retirement rules.
3. **Capacity transitions:** the model needs a principled way to evolve a dependent's privacy, voice, and decision authority over time.
4. **Power and coercion:** explicit voting or confirmation is not enough when a member cannot safely disagree.
5. **Unresolved conflict:** the model needs procedures for stalemate, mediation, temporary decisions, and appeal.
6. **Multi-household relationships:** Miriam participates in this family while governing her own home; overlapping family–home nodes need representation.
7. **Emergency doctrine:** urgent exceptions need strict scope, time limits, notice, and retrospective review.
8. **Care-network resilience:** the household currently depends on too few people for school transport and daytime elder support.

## Acceptance result

**Pass, with the gaps above carried forward.**

The model represents routine cooperation, conflicting interests, dependencies, and unexpected changes. It does so without treating family unity as permission to violate individual rights, and without turning the steward into the household's sovereign. The next experiment should focus on one of the exposed hard cases rather than add features abstractly.
