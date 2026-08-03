#!/usr/bin/env python3
"""Validate the v3.3 120-item, 24-set, and 18-beast canon registries."""

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


def expected_ids(prefix: str, count: int, width: int) -> list[str]:
    return [f"{prefix}{index:0{width}d}" for index in range(1, count + 1)]


def validate_items() -> tuple[list[dict[str, Any]], set[str], set[str]]:
    payload = load("data/collection_registry_120_v3_3.json")
    require(payload.get("count") == 120, "collection registry count must be 120")
    require(payload.get("living_entities_excluded") is True, "living_entities_excluded must be true")

    batches = payload.get("batches", [])
    require(len(batches) == 20, f"expected 20 collection batches, found {len(batches)}")
    items: list[dict[str, Any]] = []
    for batch_index, batch in enumerate(batches, start=1):
        expected_subact = f"A{batch_index:02d}"
        require(batch.get("subact_id") == expected_subact, f"batch {batch_index} subact must be {expected_subact}")
        batch_items = batch.get("items", [])
        require(len(batch_items) == 6, f"{expected_subact} must contain exactly 6 items")
        for item in batch_items:
            require(item.get("subact_id", expected_subact) == expected_subact, f"{item.get('id')} subact mismatch")
            items.append({**item, "_subact_id": expected_subact})

    require(len(items) == 120, f"expected 120 flattened items, found {len(items)}")
    actual_ids = [item.get("id") for item in items]
    require(actual_ids == expected_ids("CI", 120, 3), "item IDs must be CI001..CI120 in order")
    require(len({item.get("name") for item in items}) == 120, "all 120 item names must be unique")

    allowed_resolutions = {
        "temporary_custody", "use_without_ownership", "responsibility_transfer", "conditional_use",
        "return", "joint_management", "shared_use", "non_collection", "dismantle",
        "public_evidence", "return_and_seal", "destroy", "reject", "dismantle_into_responsibility",
    }
    allowed_roles = {
        "core_rule", "material_evidence", "logistics_pressure", "limited_utility",
        "relationship_cost", "responsibility_transfer",
    }
    item_ids = set(actual_ids)
    set_refs: set[str] = set()
    for item in items:
        label = item.get("id", "unknown item")
        require_fields(
            item,
            ["name", "category", "first_episode", "role_slot", "cost_axis", "resolution", "set_refs", "final_episode", "final_state"],
            label,
        )
        require(item.get("role_slot") in allowed_roles, f"{label} invalid role_slot {item.get('role_slot')}")
        require(item.get("resolution") in allowed_resolutions, f"{label} invalid resolution {item.get('resolution')}")
        first_episode = item.get("first_episode")
        final_episode = item.get("final_episode")
        require(isinstance(first_episode, int) and 1 <= first_episode <= 200, f"{label} invalid first_episode")
        require(isinstance(final_episode, int) and first_episode <= final_episode <= 200, f"{label} invalid final_episode")
        require("신수" not in str(item.get("category")) and "living" not in str(item.get("category")).lower(), f"{label} category may contain a living entity")
        for set_id in item.get("set_refs", []):
            set_refs.add(set_id)

    payoff = load("data/payoff_tracks_v2_7.json")
    valid_tracks = set((payoff.get("item_tracks") or {}).keys())
    for item in items:
        track_id = item.get("track_id")
        if track_id:
            require(track_id in valid_tracks, f"{item.get('id')} references unknown track {track_id}")

    return items, item_ids, set_refs


def validate_sets(items: list[dict[str, Any]], item_ids: set[str], item_set_refs: set[str]) -> set[str]:
    payload = load("data/set_registry_024_v3_3.json")
    require(payload.get("count") == 24, "set registry count must be 24")
    require("생명체는 세트 부품이 될 수 없다" in payload.get("rule", ""), "set registry must explicitly prohibit living components")
    sets = payload.get("sets", [])
    require(len(sets) == 24, f"expected 24 sets, found {len(sets)}")
    actual_ids = [record.get("id") for record in sets]
    require(actual_ids == expected_ids("SET", 24, 3), "set IDs must be SET001..SET024 in order")
    require(len({record.get("name") for record in sets}) == 24, "all set names must be unique")

    set_ids = set(actual_ids)
    signatures: list[tuple[str, ...]] = []
    component_to_sets: Counter[str] = Counter()
    set_components: dict[str, set[str]] = {}
    for record in sets:
        set_id = record.get("id")
        require_fields(
            record,
            ["name", "component_ids", "first_complete_episode", "activation_condition", "benefit", "synergy_cost", "break_condition", "ownership_model", "final_state"],
            set_id or "unknown set",
        )
        components = record.get("component_ids", [])
        require(len(components) == len(set(components)), f"{set_id} contains duplicate component IDs")
        require(len(components) >= 4, f"{set_id} must contain at least four components")
        for component in components:
            require(component in item_ids, f"{set_id} references unknown item {component}")
            component_to_sets[component] += 1
        set_components[set_id] = set(components)
        signatures.append(tuple(sorted(components)))
        episode = record.get("first_complete_episode")
        require(isinstance(episode, int) and 1 <= episode <= 200, f"{set_id} invalid first_complete_episode")
        require("신수" not in " ".join(components), f"{set_id} appears to include a living entity")
    require(len(signatures) == len(set(signatures)), "two or more sets use identical component signatures")

    missing_set_ids = sorted(item_set_refs - set_ids)
    require(not missing_set_ids, f"items reference unknown sets: {missing_set_ids}")
    for item in items:
        for set_id in item.get("set_refs", []):
            require(item.get("id") in set_components.get(set_id, set()), f"{item.get('id')} set_refs is not reciprocal with {set_id}")
    unassigned = sorted(item_id for item_id in item_ids if component_to_sets[item_id] == 0)
    require(not unassigned, f"items missing from all sets: {unassigned}")
    overused = sorted(item_id for item_id, count in component_to_sets.items() if count > 3)
    if overused:
        WARNINGS.append(f"items used by more than three sets: {overused}")
    return set_ids


def validate_beasts(item_names: set[str]) -> None:
    payload = load("data/beast_registry_018_v3_3.json")
    require(payload.get("count") == 18, "beast registry count must be 18")
    require(payload.get("collectible") is False, "beast registry collectible must be false")
    require(payload.get("set_component_allowed") is False, "beasts must not be allowed as set components")
    beasts = payload.get("beasts", [])
    require(len(beasts) == 18, f"expected 18 beasts, found {len(beasts)}")
    actual_ids = [record.get("id") for record in beasts]
    require(actual_ids == expected_ids("BS", 18, 3), "beast IDs must be BS001..BS018 in order")
    names = [record.get("name") for record in beasts]
    require(len(set(names)) == 18, "all beast names must be unique")
    require(not (set(names) & item_names), "a living entity name is duplicated as a collectible item")

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
        require(record.get("region_id") in {f"R{i:02d}" for i in range(8)}, f"{beast_id} invalid region")
        for settlement_id in record.get("home_settlement_ids", []):
            require(settlement_id in {f"ST{i:03d}" for i in range(1, 49)}, f"{beast_id} invalid settlement {settlement_id}")
        first_episode = record.get("first_episode")
        require(isinstance(first_episode, int) and 1 <= first_episode <= 200, f"{beast_id} invalid first_episode")
        episodes = record.get("major_episodes", [])
        require(episodes == sorted(set(episodes)), f"{beast_id} major_episodes must be sorted and unique")
        require(all(isinstance(ep, int) and first_episode <= ep <= 200 for ep in episodes), f"{beast_id} invalid major episode")
        require(any(word in record.get("refusal_condition", "") for word in ("소유", "가두", "묶", "채취", "독점", "강제", "전시품")), f"{beast_id} refusal condition is not concrete")
        require(len(record.get("withdrawal_trigger", "")) >= 15, f"{beast_id} withdrawal trigger is too vague")


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
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
