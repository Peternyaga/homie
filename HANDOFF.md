# Homie project handoff

Updated: **2026-07-17**

## Where the project stands

Homie is a documentation-first exploration of a family–home agent. The repository now contains:

- A structural and ethical family–home model.
- A machine-readable ontology and validation rules.
- A ten-episode ordinary-weekday stress test.
- A federated personal, household, and institutional agent topology.
- An initial companion-interface proposition centered on the Hearth.
- The full foundation-session transcript and recorded interactive decisions.

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

## Current frontier

The major open problem is Homie's experienced form: how it becomes an organic, attractive companion rather than a dashboard, task manager, group chat, or surveillance device.

The current hypothesis is:

> Homie's primary form is a persistent household presence. Its iconic shared interface is the Hearth; private interaction occurs through Whisper; ambient action through Home; urgent interruption through Signal; and external representation through Door.

The next experiment should enact the first thirty seconds after a tired member returns home. It should test silence, greeting, environmental action, emotional inference, consent, private versus shared context, and the transition into a household episode.

## Suggested continuation prompt

> Read `HANDOFF.md`, `docs/foundational-model.md`, `docs/interface-concept.md`, and the latest experiment. Continue the interactive exploration by modeling the first thirty seconds after a tired member returns home. Focus on what would make Homie feel companionable rather than computational while preserving privacy and avoiding unjustified emotional inference.

## Verification

```powershell
python scripts/validate_model.py
python -m unittest discover -s tests -v
```

## Session continuity

- Original Codex task ID: `019f6b8c-16d1-7a91-8ce0-8cdd32eeccb5`
- Task title: **Define family agent model**
- Transcript: [`docs/sessions/2026-07-16-foundation.md`](docs/sessions/2026-07-16-foundation.md)
