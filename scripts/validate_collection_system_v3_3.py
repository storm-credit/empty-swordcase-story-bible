#!/usr/bin/env python3
"""Validate the provisional v3.3 120-item, 24-set, and 18-beast registries."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def load(path: str) -> Any:
    full = ROOT / path
    if not full.exists():
        ERRORS.append(f"missing file: {path}")
        return {}
    try:
        return json.loads(full.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"invalid JSON {path}: {exc}")
        return {}


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def require_fields(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    for field in fields:
        require(record.get(field) not in (None, "", []), f"{label} missing/empty field: {field}")


def ids(prefix: str, count: int, width: int) -> list[str]:
    return [f"{prefix}{index:0{width}d}" for index in range(1, count + 1)]


def validate_items() -> tuple[list[dict[str, Any]], set[str], set[str]]:
    payload = load("data/collection_registry_120_v3_3.json")
    require(payload.get("count") == 120, "collection registry count must be 120")
    require(payload.get("living_entities_excluded") is True, "living entities must be excluded from items")
    batches = payload.get("batches", [])
    require(len(batches) == 20, f"expected 20 item batches, found {len(batches)}")

    items: list[dict[str, Any]] = []
    for index, batch in enumerate(batches, start=1):
        subact_id = f"A{index:02d}"
        require(batch.get("subact_id") == subact_id, f"batch {index} must be {subact_id}")
        batch_items = batch.get("items", [])
        require(len(batch_items) == 6, f"{subact_id} must contain 6 items")
        items.extend(batch_items)

    require(len(items) == 120, f"expected 120 items, found {len(items)}")
    item_id_list = [item.get("id") for item in items]
    require(item_id_list == ids("CI", 120, 3), "item IDs must be CI001..CI120")
    require(len({item.get("name") for item in items}) == 120, "all item names must be unique")

    roles = {
        "core_rule", "material_evidence", "logistics_pressure",
        "limited_utility", "relationship_cost", "responsibility_transfer",
    }
    resolutions = {
        "temporary_custody", "use_without_ownership", "responsibility_transfer",
        "conditional_use", "return", "joint_management", "shared_use",
        "non_collection", "dismantle", "public_evidence", "return_and_seal",
        "destroy", "reject", "dismantle_into_responsibility",
    }
    all_set_refs: set[str] = set()
    for item in items:
        label = item.get("id", "unknown item")
        require_fields(
            item,
            ["name", "category", "first_episode", "role_slot", "cost_axis", "resolution", "set_refs", "final_episode", "final_state"],
            label,
        )
        require(item.get("role_slot") in roles, f"{label} invalid role_slot")
        require(item.get("resolution") in resolutions, f"{label} invalid resolution")
        first_episode = item.get("first_episode")
        final_episode = item.get("final_episode")
        require(isinstance(first_episode, int) and 1 <= first_episode <= 200, f"{label} invalid first_episode")
        require(isinstance(final_episode, int) and isinstance(first_episode, int) and first_episode <= final_episode <= 200, f"{label} invalid final_episode")
        require("living" not in str(item.get("category", "")).lower(), f"{label} may contain a living entity")
        all_set_refs.update(item.get("set_refs", []))

    payoff = load("data/payoff_tracks_v2_7.json")
    valid_tracks = set((payoff.get("item_tracks") or {}).keys())
    for item in items:
        track_id = item.get("track_id")
        if track_id:
            require(track_id in valid_tracks, f"{item.get('id')} references unknown track {track_id}")
    return items, set(item_id_list), all_set_refs


def validate_sets(items: list[dict[str, Any]], item_ids: set[str], item_set_refs: set[str]) -> set[str]:
    payload = load("data/set_registry_024_v3_3.json")
    governance = load("data/collection_system_governance_v3_3.json")
    require(payload.get("count") == 24, "set registry count must be 24")
    require("생명체는 세트 부품이 될 수 없다" in payload.get("rule", ""), "set rule must prohibit living components")
    sets = payload.get("sets", [])
    require(len(sets) == 24, f"expected 24 sets, found {len(sets)}")
    set_id_list = [record.get("id") for record in sets]
    require(set_id_list == ids("SET", 24, 3), "set IDs must be SET001..SET024")
    require(len({record.get("name") for record in sets}) == 24, "all set names must be unique")

    item_by_id = {item.get("id"): item for item in items}
    corrections = governance.get("effective_corrections", {})
    signatures: set[tuple[str, ...]] = set()
    component_use: Counter[str] = Counter()
    components_by_set: dict[str, set[str]] = {}

    for record in sets:
        set_id = record.get("id")
        require_fields(
            record,
            ["name", "component_ids", "first_complete_episode", "activation_condition", "benefit", "synergy_cost", "break_condition", "ownership_model", "final_state"],
            set_id or "unknown set",
        )
        components = record.get("component_ids", [])
        require(len(components) >= 4, f"{set_id} must contain at least four components")
        require(len(components) == len(set(components)), f"{set_id} has duplicate components")
        for component in components:
            require(component in item_ids, f"{set_id} references unknown item {component}")
            component_use[component] += 1
        signature = tuple(sorted(components))
        require(signature not in signatures, f"{set_id} duplicates another set signature")
        signatures.add(signature)
        components_by_set[set_id] = set(components)

        effective_complete = corrections.get(set_id, {}).get("first_complete_episode", record.get("first_complete_episode"))
        first_episodes = [item_by_id.get(component, {}).get("first_episode") for component in components]
        require(all(isinstance(value, int) for value in first_episodes), f"{set_id} component episode missing")
        if first_episodes:
            require(effective_complete >= max(first_episodes), f"{set_id} completes before all components appear")
        require(isinstance(effective_complete, int) and 1 <= effective_complete <= 200, f"{set_id} invalid completion episode")

    set_ids = set(set_id_list)
    require(not (item_set_refs - set_ids), f"items reference unknown sets: {sorted(item_set_refs - set_ids)}")
    for item in items:
        for set_id in item.get("set_refs", []):
            require(item.get("id") in components_by_set.get(set_id, set()), f"{item.get('id')} set_refs not reciprocal with {set_id}")
    unassigned = sorted(item_id for item_id in item_ids if component_use[item_id] == 0)
    require(not unassigned, f"items missing from all sets: {unassigned}")
    overused = sorted(item_id for item_id, count in component_use.items() if count > 3)
    if overused:
        WARNINGS.append(f"items used by more than three sets: {overused}")
    return set_ids


def validate_beasts(item_names: set[str]) -> None:
    payload = load("data/beast_registry_018_v3_3.json")
    require(payload.get("count") == 18, "beast registry count must be 18")
    require(payload.get("collectible") is False, "beasts must not be collectible")
    require(payload.get("set_component_allowed") is False, "beasts must not be set components")
    beasts = payload.get("beasts", [])
    require(len(beasts) == 18, f"expected 18 beasts, found {len(beasts)}")
    require([record.get("id") for record in beasts] == ids("BS", 18, 3), "beast IDs must be BS001..BS018")
    beast_names = [record.get("name") for record in beasts]
    require(len(set(beast_names)) == 18, "all beast names must be unique")
    require(not (set(beast_names) & item_names), "a living entity is duplicated as an item")

    valid_regions = {f"R{index:02d}" for index in range(8)}
    valid_settlements = {f"ST{index:03d}" for index in range(1, 49)}
    for record in beasts:
        beast_id = record.get("id")
        require_fields(
            record,
            [
                "name", "kind", "type", "first_episode", "region_id", "home_settlement_ids",
                "independent_goal", "consent_condition", "refusal_condition", "withdrawal_trigger",
                "human_benefit", "human_cost", "major_episodes", "final_state",
            ],
            beast_id or "unknown beast",
        )
        require(record.get("region_id") in valid_regions, f"{beast_id} invalid region")
        for settlement_id in record.get("home_settlement_ids", []):
            require(settlement_id in valid_settlements, f"{beast_id} invalid settlement {settlement_id}")
        first_episode = record.get("first_episode")
        episodes = record.get("major_episodes", [])
        require(isinstance(first_episode, int) and 1 <= first_episode <= 200, f"{beast_id} invalid first_episode")
        require(episodes == sorted(set(episodes)), f"{beast_id} major_episodes must be sorted and unique")
        require(all(isinstance(episode, int) and first_episode <= episode <= 200 for episode in episodes), f"{beast_id} invalid major episode")
        require(len(record.get("independent_goal", "")) >= 20, f"{beast_id} independent goal is too vague")
        require(len(record.get("consent_condition", "")) >= 20, f"{beast_id} consent condition is too vague")
        require(len(record.get("refusal_condition", "")) >= 20, f"{beast_id} refusal condition is too vague")
        require(len(record.get("withdrawal_trigger", "")) >= 15, f"{beast_id} withdrawal trigger is too vague")
        require(len(record.get("human_cost", "")) >= 15, f"{beast_id} human cost is too vague")


def main() -> int:
    items, item_ids, item_set_refs = validate_items()
    validate_sets(items, item_ids, item_set_refs)
    validate_beasts({item.get("name") for item in items})
    result = {
        "version": "3.3",
        "status": "failed" if ERRORS else "passed",
        "errors": ERRORS,
        "warnings": WARNINGS,
        "verified_counts": {"collectibles": len(items), "sets": 24, "beasts_and_mounts": 18},
        "canon_status": "provisional_candidate_pending_author_approval",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
