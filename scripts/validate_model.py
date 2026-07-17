#!/usr/bin/env python3
"""Validate Homie's reference family-home experiment without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCUMENT = ROOT / "experiments" / "ordinary-weekday.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "family-home.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object at its root")
    return value


def _enum(schema: Mapping[str, Any], name: str) -> set[str]:
    try:
        values = schema["$defs"][name]["enum"]
    except KeyError as exc:
        raise ValueError(f"schema is missing $defs.{name}.enum") from exc
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise ValueError(f"schema $defs.{name}.enum must be a string array")
    return set(values)


def _require_keys(
    value: Any,
    keys: Iterable[str],
    path: str,
    errors: list[str],
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return False
    missing = [key for key in keys if key not in value]
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")
        return False
    return True


def _require_nonempty_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: expected a non-empty string")


def _require_string_list(
    value: Any,
    path: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{path}: expected an array of strings")
        return []
    if nonempty and not value:
        errors.append(f"{path}: expected at least one item")
    if len(value) != len(set(value)):
        errors.append(f"{path}: contains duplicate values")
    return value


def _check_enum_values(
    values: Iterable[str],
    allowed: set[str],
    path: str,
    errors: list[str],
) -> None:
    unknown = sorted(set(values) - allowed)
    if unknown:
        errors.append(f"{path}: unknown values: {', '.join(unknown)}")


def _collect_unique_ids(
    records: Any,
    path: str,
    errors: list[str],
) -> tuple[list[dict[str, Any]], set[str]]:
    if not isinstance(records, list):
        errors.append(f"{path}: expected an array")
        return [], set()

    typed_records: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, record in enumerate(records):
        record_path = f"{path}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{record_path}: expected an object")
            continue
        typed_records.append(record)
        record_id = record.get("id")
        _require_nonempty_string(record_id, f"{record_path}.id", errors)
        if isinstance(record_id, str):
            if record_id in ids:
                errors.append(f"{record_path}.id: duplicate id {record_id!r}")
            ids.add(record_id)
    return typed_records, ids


def validate_document(document: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    """Return human-readable validation errors; an empty list means valid."""

    errors: list[str] = []
    top_level = [
        "model_version",
        "title",
        "mandate",
        "rights_floor",
        "components",
        "functions",
        "household",
        "episodes",
        "coverage",
    ]
    if not _require_keys(document, top_level, "$", errors):
        return errors

    component_values = _enum(schema, "component")
    information_values = _enum(schema, "informationClass")
    steward_values = _enum(schema, "stewardMode")
    dynamic_values = _enum(schema, "dynamic")
    member_layer_values = _enum(schema, "memberLayer")
    participant_kind_values = _enum(schema, "participantKind")
    resource_kind_values = _enum(schema, "resourceKind")
    relationship_kind_values = _enum(schema, "relationshipKind")

    _require_nonempty_string(document["title"], "$.title", errors)
    _require_nonempty_string(document["mandate"], "$.mandate", errors)
    if not isinstance(document["model_version"], str) or not re.fullmatch(
        r"\d+\.\d+", document["model_version"]
    ):
        errors.append("$.model_version: expected a major.minor string such as '0.1'")

    rights, right_ids = _collect_unique_ids(document["rights_floor"], "$.rights_floor", errors)
    required_rights = {"safety", "dignity", "privacy", "basic_autonomy"}
    if not required_rights.issubset(right_ids):
        missing = sorted(required_rights - right_ids)
        errors.append(f"$.rights_floor: missing foundational rights: {', '.join(missing)}")
    for index, right in enumerate(rights):
        _require_nonempty_string(right.get("definition"), f"$.rights_floor[{index}].definition", errors)

    components = _require_string_list(document["components"], "$.components", errors, nonempty=True)
    _check_enum_values(components, component_values, "$.components", errors)
    if set(components) != component_values:
        missing = sorted(component_values - set(components))
        if missing:
            errors.append(f"$.components: missing components: {', '.join(missing)}")

    functions, function_ids = _collect_unique_ids(document["functions"], "$.functions", errors)
    required_functions = {"sustain", "care_develop", "belong", "coordinate", "continue", "connect"}
    if not required_functions.issubset(function_ids):
        missing = sorted(required_functions - function_ids)
        errors.append(f"$.functions: missing functions: {', '.join(missing)}")
    for index, function in enumerate(functions):
        _require_nonempty_string(function.get("definition"), f"$.functions[{index}].definition", errors)

    household = document["household"]
    household_keys = [
        "id",
        "name",
        "description",
        "participants",
        "relationships",
        "resources",
        "governance",
    ]
    if not _require_keys(household, household_keys, "$.household", errors):
        return errors

    participants, participant_ids = _collect_unique_ids(
        household["participants"], "$.household.participants", errors
    )
    participant_kinds: dict[str, str] = {}
    delegated_agents: set[str] = set()
    for index, participant in enumerate(participants):
        path = f"$.household.participants[{index}]"
        required = ["id", "name", "kind", "member_layers", "roles", "needs", "rights"]
        if not _require_keys(participant, required, path, errors):
            continue
        participant_id = participant.get("id")
        kind = participant.get("kind")
        _require_nonempty_string(participant.get("name"), f"{path}.name", errors)
        if isinstance(kind, str):
            _check_enum_values([kind], participant_kind_values, f"{path}.kind", errors)
            if isinstance(participant_id, str):
                participant_kinds[participant_id] = kind
                if kind == "delegated_agent":
                    delegated_agents.add(participant_id)
        layers = _require_string_list(participant.get("member_layers"), f"{path}.member_layers", errors, nonempty=True)
        _check_enum_values(layers, member_layer_values, f"{path}.member_layers", errors)
        for field in ("roles", "needs", "rights"):
            _require_string_list(participant.get(field), f"{path}.{field}", errors, nonempty=True)
        if kind == "delegated_agent" and set(layers) != {"authorized_participant"}:
            errors.append(f"{path}.member_layers: delegated agents must only be authorized participants")

    if not delegated_agents:
        errors.append("$.household.participants: expected at least one delegated home steward")

    relationships, _ = _collect_unique_ids(
        household["relationships"], "$.household.relationships", errors
    )
    for index, relationship in enumerate(relationships):
        path = f"$.household.relationships[{index}]"
        required = ["id", "kind", "from", "to", "features"]
        if not _require_keys(relationship, required, path, errors):
            continue
        kind = relationship.get("kind")
        if isinstance(kind, str):
            _check_enum_values([kind], relationship_kind_values, f"{path}.kind", errors)
        for endpoint in ("from", "to"):
            endpoint_id = relationship.get(endpoint)
            if endpoint_id not in participant_ids:
                errors.append(f"{path}.{endpoint}: unknown participant {endpoint_id!r}")
        _require_string_list(relationship.get("features"), f"{path}.features", errors, nonempty=True)

    resources, _ = _collect_unique_ids(household["resources"], "$.household.resources", errors)
    for index, resource in enumerate(resources):
        path = f"$.household.resources[{index}]"
        required = ["id", "name", "kind", "shared_by", "governance_rule"]
        if not _require_keys(resource, required, path, errors):
            continue
        kind = resource.get("kind")
        if isinstance(kind, str):
            _check_enum_values([kind], resource_kind_values, f"{path}.kind", errors)
        sharers = _require_string_list(resource.get("shared_by"), f"{path}.shared_by", errors, nonempty=True)
        for participant_id in set(sharers) - participant_ids:
            errors.append(f"{path}.shared_by: unknown participant {participant_id!r}")
        _require_nonempty_string(resource.get("governance_rule"), f"{path}.governance_rule", errors)

    governance = household["governance"]
    if _require_keys(governance, ["decision_principles", "delegations"], "$.household.governance", errors):
        _require_string_list(
            governance.get("decision_principles"),
            "$.household.governance.decision_principles",
            errors,
            nonempty=True,
        )
        delegations, _ = _collect_unique_ids(
            governance.get("delegations"), "$.household.governance.delegations", errors
        )
        for index, delegation in enumerate(delegations):
            path = f"$.household.governance.delegations[{index}]"
            required = ["id", "delegate", "purpose", "scope", "limits", "revocable_by"]
            if not _require_keys(delegation, required, path, errors):
                continue
            delegate = delegation.get("delegate")
            if delegate not in delegated_agents:
                errors.append(f"{path}.delegate: {delegate!r} is not a delegated agent")
            _require_nonempty_string(delegation.get("purpose"), f"{path}.purpose", errors)
            for field in ("scope", "limits"):
                _require_string_list(delegation.get(field), f"{path}.{field}", errors, nonempty=True)
            revokers = _require_string_list(
                delegation.get("revocable_by"), f"{path}.revocable_by", errors, nonempty=True
            )
            for participant_id in set(revokers) - participant_ids:
                errors.append(f"{path}.revocable_by: unknown participant {participant_id!r}")

    episodes, _ = _collect_unique_ids(document["episodes"], "$.episodes", errors)
    seen_components: set[str] = set()
    seen_information: set[str] = set()
    seen_modes: set[str] = set()
    seen_dynamics: set[str] = set()
    previous_minutes = -1

    for index, episode in enumerate(episodes):
        path = f"$.episodes[{index}]"
        required = [
            "id",
            "time",
            "title",
            "trigger",
            "components",
            "dynamics",
            "affected",
            "information",
            "authority",
            "steward",
            "actions",
            "outcome",
        ]
        if not _require_keys(episode, required, path, errors):
            continue

        _require_nonempty_string(episode.get("title"), f"{path}.title", errors)
        _require_nonempty_string(episode.get("trigger"), f"{path}.trigger", errors)
        time_value = episode.get("time")
        if not isinstance(time_value, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", time_value):
            errors.append(f"{path}.time: expected a 24-hour HH:MM value")
        else:
            hour, minute = (int(part) for part in time_value.split(":"))
            current_minutes = hour * 60 + minute
            if current_minutes <= previous_minutes:
                errors.append(f"{path}.time: episodes must be in strictly increasing time order")
            previous_minutes = current_minutes

        episode_components = _require_string_list(
            episode.get("components"), f"{path}.components", errors, nonempty=True
        )
        _check_enum_values(episode_components, component_values, f"{path}.components", errors)
        seen_components.update(episode_components)

        episode_dynamics = _require_string_list(
            episode.get("dynamics"), f"{path}.dynamics", errors, nonempty=True
        )
        _check_enum_values(episode_dynamics, dynamic_values, f"{path}.dynamics", errors)
        seen_dynamics.update(episode_dynamics)

        affected = episode.get("affected")
        if not isinstance(affected, list) or not affected:
            errors.append(f"{path}.affected: expected at least one affected participant")
        else:
            for affected_index, item in enumerate(affected):
                item_path = f"{path}.affected[{affected_index}]"
                if not _require_keys(item, ["participant", "needs", "rights"], item_path, errors):
                    continue
                participant_id = item.get("participant")
                if participant_id not in participant_ids:
                    errors.append(f"{item_path}.participant: unknown participant {participant_id!r}")
                _require_string_list(item.get("needs"), f"{item_path}.needs", errors, nonempty=True)
                _require_string_list(item.get("rights"), f"{item_path}.rights", errors, nonempty=True)

        information = episode.get("information")
        if not isinstance(information, list) or not information:
            errors.append(f"{path}.information: expected at least one information item")
        else:
            for information_index, item in enumerate(information):
                item_path = f"{path}.information[{information_index}]"
                if not _require_keys(item, ["class", "subject", "purpose", "recipients"], item_path, errors):
                    continue
                classification = item.get("class")
                if isinstance(classification, str):
                    _check_enum_values([classification], information_values, f"{item_path}.class", errors)
                    seen_information.add(classification)
                _require_nonempty_string(item.get("subject"), f"{item_path}.subject", errors)
                _require_nonempty_string(item.get("purpose"), f"{item_path}.purpose", errors)
                recipients = _require_string_list(
                    item.get("recipients"), f"{item_path}.recipients", errors, nonempty=True
                )
                if classification == "private" and delegated_agents.intersection(recipients):
                    errors.append(f"{item_path}.recipients: private information cannot include the home steward")

        authority = episode.get("authority")
        if _require_keys(authority, ["holders", "basis", "rights_floor_check"], f"{path}.authority", errors):
            _require_string_list(
                authority.get("holders"), f"{path}.authority.holders", errors, nonempty=True
            )
            _require_nonempty_string(authority.get("basis"), f"{path}.authority.basis", errors)
            _require_nonempty_string(
                authority.get("rights_floor_check"), f"{path}.authority.rights_floor_check", errors
            )

        steward = episode.get("steward")
        steward_required = ["mode", "may_do", "must_not_do", "human_input", "escalation"]
        if _require_keys(steward, steward_required, f"{path}.steward", errors):
            mode = steward.get("mode")
            if isinstance(mode, str):
                _check_enum_values([mode], steward_values, f"{path}.steward.mode", errors)
                seen_modes.add(mode)
            _require_string_list(steward.get("may_do"), f"{path}.steward.may_do", errors, nonempty=True)
            _require_string_list(
                steward.get("must_not_do"), f"{path}.steward.must_not_do", errors, nonempty=True
            )
            _require_nonempty_string(steward.get("human_input"), f"{path}.steward.human_input", errors)
            _require_nonempty_string(steward.get("escalation"), f"{path}.steward.escalation", errors)

        actions = episode.get("actions")
        if not isinstance(actions, list) or not actions:
            errors.append(f"{path}.actions: expected at least one action")
        else:
            for action_index, action in enumerate(actions):
                action_path = f"{path}.actions[{action_index}]"
                if not _require_keys(action, ["actor", "action", "authorization"], action_path, errors):
                    continue
                for field in ("actor", "action", "authorization"):
                    _require_nonempty_string(action.get(field), f"{action_path}.{field}", errors)

        outcome = episode.get("outcome")
        outcome_fields = [
            "relationship_changes",
            "resource_changes",
            "shared_memory_updates",
            "unresolved",
        ]
        if _require_keys(outcome, outcome_fields, f"{path}.outcome", errors):
            for field in outcome_fields:
                _require_string_list(outcome.get(field), f"{path}.outcome.{field}", errors)

    coverage = document["coverage"]
    coverage_fields = {
        "required_components": (component_values, seen_components),
        "required_information_classes": (information_values, seen_information),
        "required_steward_modes": (steward_values, seen_modes),
        "required_dynamics": (dynamic_values, seen_dynamics),
    }
    if _require_keys(coverage, coverage_fields.keys(), "$.coverage", errors):
        for field, (allowed, seen) in coverage_fields.items():
            required = _require_string_list(
                coverage.get(field), f"$.coverage.{field}", errors, nonempty=True
            )
            _check_enum_values(required, allowed, f"$.coverage.{field}", errors)
            missing = sorted(set(required) - seen)
            if missing:
                errors.append(
                    f"$.coverage.{field}: values not exercised by any episode: {', '.join(missing)}"
                )

    return errors


def _coverage_summary(document: Mapping[str, Any]) -> str:
    episodes = document.get("episodes", [])
    modes = sorted({episode["steward"]["mode"] for episode in episodes})
    dynamics = sorted({item for episode in episodes for item in episode["dynamics"]})
    return (
        f"{len(episodes)} episodes; steward modes: {', '.join(modes)}; "
        f"dynamics: {', '.join(dynamics)}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", nargs="?", type=Path, default=DEFAULT_DOCUMENT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args(argv)

    try:
        document = load_json(args.document)
        schema = load_json(args.schema)
        errors = validate_document(document, schema)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Validation could not run: {exc}", file=sys.stderr)
        return 2

    if errors:
        print(f"INVALID: {args.document}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"VALID: {args.document}")
    print(_coverage_summary(document))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
