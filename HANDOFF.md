# Homie project handoff

Updated: **2026-07-30**

## Where the project stands

Homie is a documentation-first exploration of a family–home agent. The repository now contains:

- A structural and ethical family–home model.
- A machine-readable ontology and validation rules.
- A ten-episode ordinary-weekday stress test.
- A federated personal, household, and institutional agent topology.
- An initial companion-interface proposition centered on the Hearth.
- An assessment of OpenClaw and Hermes as possible execution substrates.
- Session transcripts and recorded interactive decisions.

All current validators and tests pass.

## Decisions already made

- Model the **family–home system**, keeping family and home distinct but coupled.
- Use **layered membership** rather than biology, law, or residence alone.
- Separate descriptive structure from a normative health layer.
- Give the system a **dual mandate**: member flourishing and collective continuity.
- Protect a non-negotiable rights floor of safety, dignity, privacy, and basic autonomy.
- Use a **federated agent graph** with personal agents, a household steward, and external institutional agents.
- Treat Homie as a **delegated steward**, not a family member or sovereign.
- Scale autonomy by risk, reversibility, uncertainty, sensitivity, and disagreement.
- Begin interface exploration with one identity expressed through Whisper, Hearth, Home, Signal, and Door.
- Treat existing personal-agent frameworks as replaceable runtimes beneath a durable Homie governance kernel.
- Use OpenClaw first to test multi-agent routing and policy hooks; use Hermes to test personality, approved learning, intentional silence, and home embodiment.

## Current frontier

The major open problem remains Homie's experienced form, but the infrastructure boundary is now clearer: OpenClaw and Hermes can supply messaging, agent execution, tools, scheduling, memory mechanisms, and integrations; Homie must supply household identity, rights, consent, delegation, authority, risk policy, and shared-memory governance.

The current hypothesis is:

> Homie's primary form is a persistent household presence. Its iconic shared interface is the Hearth; private interaction occurs through Whisper; ambient action through Home; urgent interruption through Signal; and external representation through Door.

The recommended next infrastructure experiment is a synthetic weekday disruption involving an elder-care change and a school pickup conflict. Run the same scenario first on OpenClaw and then on Hermes, with simulated tools only. Test private-versus-shared disclosure, authority, confirmation, policy enforcement, episode logging, and companion quality.

## Suggested continuation prompt

> Read `HANDOFF.md`, `docs/foundational-model.md`, `docs/interface-concept.md`, `docs/existing-agent-infrastructure.md`, and the latest experiment. Design a synthetic prototype of the elder-care and school-pickup disruption using the Homie kernel/runtime boundary. Keep tools simulated and make every information disclosure, authorization, action, and memory update inspectable.

## Verification

```powershell
python scripts/validate_model.py
python -m unittest discover -s tests -v
```

## Session continuity

- Original Codex task ID: `019f6b8c-16d1-7a91-8ce0-8cdd32eeccb5`
- Task title: **Define family agent model**
- Foundation transcript: [`docs/sessions/2026-07-16-foundation.md`](docs/sessions/2026-07-16-foundation.md)
- Agent-infrastructure session: [`docs/sessions/2026-07-18-agent-infrastructure.md`](docs/sessions/2026-07-18-agent-infrastructure.md)
