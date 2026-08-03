#!/usr/bin/env python3
"""Validate v3.3 world-bible and blueprint integration.

This validator distinguishes structural errors from known incompleteness.
- ERROR: broken IDs, counts, references, duplicate v3.3 identities, malformed chains.
- OPEN GAP: declared completion cannot yet be proven (scene beats, 120/24/18 registries).

Exit codes:
0 = structural validation passed and no critical open gap
1 = structural validation failed
2 = structure passed but critical completion gaps remain
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]

ERRORS: list[str] = []
WARNINGS: list[str] = []
OPEN_GAPS: list[str] = []


def load_json(path: str) -> Any:
    full = ROOT / path
    if not full.exists():
        ERRORS.append(f"missing file: {path}")
        return None
    try:
        return json.loads(full.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"invalid JSON {path}: {exc}")
        return None


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def warn(condition: bool, message: str) -> None:
    if not condition:
        WARNINGS.append(message)


def expect_sequence(values: Iterable[str], prefix: str, count: int, label: str) -> None:
    actual = list(values)
    expected = [f"{prefix}{i:03d}" for i in range(1, count + 1)]
    require(actual == expected, f"{label} IDs are not the exact sequence {expected[0]}..{expected[-1]}")


def nonempty_fields(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    for field in fields:
        value = record.get(field)
        require(value not in (None, "", []), f"{label} missing/empty field: {field}")


def iter_named_lists(value: Any, path: str = "root") -> Iterable[tuple[str, list[Any]]]:
    if isinstance(value, list):
        yield path, value
        for idx, item in enumerate(value):
            yield from iter_named_lists(item, f"{path}[{idx}]")
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from iter_named_lists(child, f"{path}.{key}")


def discover_inventory(count: int, keywords: tuple[str, ...]) -> list[str]:
    matches: list[str] = []
    lowered_keywords = tuple(k.lower() for k in keywords)
    for path in sorted((ROOT / "data").glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for key_path, values in iter_named_lists(payload):
            haystack = f"{path.name} {key_path}".lower()
            if len(values) == count and any(keyword in haystack for keyword in lowered_keywords):
                matches.append(f"{path.relative_to(ROOT)}:{key_path}")
    return sorted(set(matches))


def validate_world_counts() -> tuple[set[str], set[str], set[str], set[str]]:
    regions = load_json("data/world_regions_008.json") or []
    settlements = load_json("data/world_settlements_048.json") or []
    routes = load_json("data/world_routes_020.json") or []
    factions = load_json("data/world_factions_018.json") or []
    subacts = load_json("data/acts_subacts_005_020.json") or []

    require(len(regions) == 8, f"expected 8 regions, found {len(regions)}")
    require(len(settlements) == 48, f"expected 48 settlements, found {len(settlements)}")
    require(len(routes) == 20, f"expected 20 routes, found {len(routes)}")
    require(len(factions) == 18, f"expected 18 factions, found {len(factions)}")
    require(len(subacts) == 20, f"expected 20 subacts, found {len(subacts)}")

    if len(regions) == 8:
        expect_sequence([r.get("id", "") for r in regions], "R", 8, "region")
    if len(settlements) == 48:
        expect_sequence([s.get("id", "") for s in settlements], "ST", 48, "settlement")
    if len(routes) == 20:
        expect_sequence([r.get("id", "") for r in routes], "RT", 20, "route")
    if len(factions) == 18:
        expect_sequence([f.get("id", "") for f in factions], "FC", 18, "faction")

    # Record the known base problem rather than silently accepting it.
    signatures_by_region: dict[str, list[tuple[Any, ...]]] = defaultdict(list)
    for s in settlements:
        signature = (
            s.get("current_tension"),
            s.get("entry_rule"),
            s.get("daily_operation"),
            s.get("logistics_bottleneck"),
            s.get("disaster_weakness"),
            tuple(s.get("sensory_marks", [])),
            tuple(s.get("local_terms", [])),
        )
        signatures_by_region[s.get("region_id", "")].append(signature)
    repeated_regions = [rid for rid, signatures in signatures_by_region.items() if len(set(signatures)) == 1 and len(signatures) > 1]
    if repeated_regions:
        WARNINGS.append("base settlement data repeats one operational signature across each of: " + ", ".join(repeated_regions))

    causal_inputs = [s.get("causal_input") for s in subacts]
    if causal_inputs and len(set(causal_inputs)) <= 2:
        WARNINGS.append("base subact causal_input is generic/repeated; v3.3 overlay must remain mandatory")

    return (
        {r.get("id") for r in regions},
        {s.get("id") for s in settlements},
        {r.get("id") for r in routes},
        {f.get("id") for f in factions},
    )


def validate_settlement_overlay(settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]) -> None:
    payload = load_json("data/settlement_identity_overlay_v3_3.json") or {}
    records = payload.get("settlements", [])
    require(len(records) == 48, f"settlement overlay expected 48, found {len(records)}")
    if len(records) != 48:
        return
    expect_sequence([r.get("settlement_id", "") for r in records], "ST", 48, "settlement overlay")
    signatures: list[tuple[Any, ...]] = []
    for record in records:
        sid = record.get("settlement_id")
        nonempty_fields(
            record,
            ["name", "region_id", "linked_route_ids", "primary_function", "local_bottleneck", "civic_routine", "ownership_dispute", "signature_evidence", "failure_cascade", "primary_faction_id"],
            f"settlement overlay {sid}",
        )
        require(sid in settlement_ids, f"unknown settlement reference: {sid}")
        for route_id in record.get("linked_route_ids", []):
            require(route_id in route_ids, f"{sid} references unknown route {route_id}")
        require(record.get("primary_faction_id") in faction_ids, f"{sid} references unknown faction {record.get('primary_faction_id')}")
        signatures.append((record.get("primary_function"), record.get("local_bottleneck"), record.get("civic_routine"), record.get("ownership_dispute")))
    duplicates = [sig for sig, count in Counter(signatures).items() if count > 1]
    require(not duplicates, f"settlement overlay contains {len(duplicates)} duplicate operational identities")


def validate_route_overlay(settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]) -> None:
    payload = load_json("data/route_operability_overlay_v3_3.json") or {}
    records = payload.get("routes", [])
    require(len(records) == 20, f"route overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    expect_sequence([r.get("route_id", "") for r in records], "RT", 20, "route overlay")
    required = ["from_settlement_id", "to_settlement_id", "controlling_faction_ids", "normal_transit", "standard_capacity", "closure_trigger", "alternate_path", "failure_cascade", "ownership_question"]
    for record in records:
        rid = record.get("route_id")
        nonempty_fields(record, required, f"route overlay {rid}")
        require(rid in route_ids, f"unknown route reference: {rid}")
        require(record.get("from_settlement_id") in settlement_ids, f"{rid} unknown from settlement")
        require(record.get("to_settlement_id") in settlement_ids, f"{rid} unknown to settlement")
        for faction_id in record.get("controlling_faction_ids", []):
            require(faction_id in faction_ids, f"{rid} references unknown faction {faction_id}")


def validate_faction_overlay(settlement_ids: set[str], faction_ids: set[str]) -> None:
    payload = load_json("data/faction_relation_overlay_v3_3.json") or {}
    nodes = payload.get("factions", [])
    relations = payload.get("relations", [])
    require(len(nodes) == 18, f"faction overlay expected 18 nodes, found {len(nodes)}")
    require(len(relations) >= 18, f"faction overlay needs at least 18 relations, found {len(relations)}")
    if len(nodes) == 18:
        expect_sequence([n.get("faction_id", "") for n in nodes], "FC", 18, "faction overlay")
    degree: Counter[str] = Counter()
    for node in nodes:
        fid = node.get("faction_id")
        nonempty_fields(node, ["name", "primary_settlement_ids", "victory_condition", "defeat_condition", "autonomous_action_without_damun"], f"faction overlay {fid}")
        require(fid in faction_ids, f"unknown faction node: {fid}")
        for sid in node.get("primary_settlement_ids", []):
            require(sid in settlement_ids, f"{fid} references unknown settlement {sid}")
    relation_ids: set[str] = set()
    for relation in relations:
        rid = relation.get("relation_id")
        require(rid not in relation_ids, f"duplicate relation id {rid}")
        relation_ids.add(rid)
        a = relation.get("from_faction_id")
        b = relation.get("to_faction_id")
        require(a in faction_ids and b in faction_ids, f"{rid} has unknown faction reference")
        require(a != b, f"{rid} cannot be self relation")
        nonempty_fields(relation, ["relation_type", "disputed_resource", "escalation_trigger", "resolution_leverage"], f"relation {rid}")
        degree[a] += 1
        degree[b] += 1
    isolated = sorted(fid for fid in faction_ids if degree[fid] == 0)
    require(not isolated, f"isolated factions in relation graph: {isolated}")


def validate_subact_overlay() -> None:
    payload = load_json("data/subact_causality_overlay_v3_3.json") or {}
    records = payload.get("subacts", [])
    require(len(records) == 20, f"subact overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    expected_ids = [f"A{i:02d}" for i in range(1, 21)]
    require([r.get("subact_id") for r in records] == expected_ids, "subact overlay IDs/order must be A01..A20")
    for idx, record in enumerate(records):
        sid = record.get("subact_id")
        nonempty_fields(record, ["title", "incoming_cost", "present_problem", "damun_voluntary_goal", "irreversible_choice", "outgoing_cost"], f"subact {sid}")
        expected_next = expected_ids[idx + 1] if idx < 19 else None
        require(record.get("next_subact_id") == expected_next, f"{sid} next_subact_id must be {expected_next}")
    outgoing = [r.get("outgoing_cost") for r in records]
    require(len(set(outgoing)) == 20, "subact outgoing costs must all be concrete and unique")


def validate_scene_blueprint_status() -> None:
    packet = ROOT / "docs/PRODUCTION_PACKET_021_040_V2_5.md"
    if not packet.exists():
        ERRORS.append("missing docs/PRODUCTION_PACKET_021_040_V2_5.md")
    else:
        text = packet.read_text(encoding="utf-8")
        headings = list(re.finditer(r"^##\s+(\d+)화\b", text, flags=re.MULTILINE))
        require(len(headings) == 20, f"21~40 packet expected 20 episode headings, found {len(headings)}")
        low_beat_episodes: list[tuple[int, int]] = []
        for index, match in enumerate(headings):
            start = match.end()
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            section = text[start:end]
            beat_count = len(re.findall(r"^\d+\.\s", section, flags=re.MULTILINE))
            if beat_count < 6:
                low_beat_episodes.append((int(match.group(1)), beat_count))
        if low_beat_episodes:
            OPEN_GAPS.append("21~40 episodes below 6 scene beats: " + ", ".join(f"EP{ep:03d}={count}" for ep, count in low_beat_episodes))

    episode_files = [
        "data/episodes_001_010.json",
        "data/episodes_011_020.json",
        "data/episodes_021_030.json",
        "data/episodes_031_040.json",
        "data/episodes_041_080.json",
        "data/episodes_081_120.json",
        "data/episodes_121_160.json",
        "data/episodes_161_200.json",
    ]
    detailed: list[int] = []
    covered: list[int] = []
    for path in episode_files:
        payload = load_json(path)
        if not isinstance(payload, list):
            continue
        for episode in payload:
            ep = episode.get("episode") or episode.get("episode_no") or episode.get("number")
            if isinstance(ep, int):
                covered.append(ep)
            beats = episode.get("scene_beats")
            if isinstance(ep, int) and isinstance(beats, list) and 6 <= len(beats) <= 10:
                detailed.append(ep)
    require(sorted(set(covered)) == list(range(1, 201)), f"episode source coverage is not exactly 1..200; found {len(set(covered))} unique episodes")
    missing_detailed = [ep for ep in range(21, 201) if ep not in set(detailed)]
    if missing_detailed:
        OPEN_GAPS.append(f"21~200 episodes without confirmed 6~10 scene_beats in canonical JSON: {len(missing_detailed)}/180")


def validate_collection_inventory() -> None:
    item_sources = discover_inventory(120, ("collection", "collectible", "item", "artifact", "relic", "수집", "유산"))
    set_sources = discover_inventory(24, ("set", "세트"))
    beast_sources = discover_inventory(18, ("beast", "creature", "shinsu", "mount", "신수", "영물", "탈것"))

    if not item_sources:
        OPEN_GAPS.append("no discoverable 120-entry collectible registry in data/*.json")
    else:
        print("discovered 120-entry collectible source(s):", ", ".join(item_sources))
    if not set_sources:
        OPEN_GAPS.append("no discoverable 24-entry set registry in data/*.json")
    else:
        print("discovered 24-entry set source(s):", ", ".join(set_sources))
    if not beast_sources:
        OPEN_GAPS.append("no discoverable 18-entry beast/mount registry in data/*.json")
    else:
        print("discovered 18-entry beast source(s):", ", ".join(beast_sources))

    manifest = load_json("data/project_manifest_v2_7.json") or {}
    item_track_count = manifest.get("coverage", {}).get("item_tracks")
    warn(item_track_count == 16, f"expected documented long-term item tracks=16, found {item_track_count}")
    if item_track_count == 16:
        WARNINGS.append("only 16 long-term item payoff tracks are currently declared; remaining items still need first-use/final-state coverage")


def validate_status_files() -> None:
    completion = load_json("data/world_blueprint_completion_manifest_v3_3.json") or {}
    categories = {c.get("id"): c for c in completion.get("categories", [])}
    require(categories.get("C14", {}).get("status") == "unverified", "C14 collectible status must remain unverified until a 120-entry source is proven")
    require(categories.get("C15", {}).get("status") == "unverified", "C15 set status must remain unverified until a 24-entry source is proven")
    require(categories.get("C16", {}).get("status") == "unverified", "C16 beast status must remain unverified until an 18-entry source is proven")

    gap_register = load_json("data/world_integration_gap_register_v3_3.json") or {}
    gap_ids = {g.get("gap_id") for g in gap_register.get("gaps", [])}
    for required_gap in ("BP-G01", "BP-G02", "BP-G03", "CS-G01", "CS-G02", "CS-G03", "DOC-G01"):
        require(required_gap in gap_ids, f"gap register missing {required_gap}")


def main() -> int:
    region_ids, settlement_ids, route_ids, faction_ids = validate_world_counts()
    validate_settlement_overlay(settlement_ids, route_ids, faction_ids)
    validate_route_overlay(settlement_ids, route_ids, faction_ids)
    validate_faction_overlay(settlement_ids, faction_ids)
    validate_subact_overlay()
    validate_scene_blueprint_status()
    validate_collection_inventory()
    validate_status_files()

    print("\n=== v3.3 integration validation ===")
    print(f"errors: {len(ERRORS)}")
    for item in ERRORS:
        print(f"ERROR: {item}")
    print(f"warnings: {len(WARNINGS)}")
    for item in WARNINGS:
        print(f"WARNING: {item}")
    print(f"critical open gaps: {len(OPEN_GAPS)}")
    for item in OPEN_GAPS:
        print(f"OPEN: {item}")

    if ERRORS:
        return 1
    if OPEN_GAPS:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
