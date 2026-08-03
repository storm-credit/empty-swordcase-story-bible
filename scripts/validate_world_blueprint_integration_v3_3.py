#!/usr/bin/env python3
"""Validate v3.3 world-bible and blueprint integration.

The validator deliberately separates two things:

1. structural errors — broken counts, IDs, references, duplicate identities;
2. completion gaps — 6~10 scene beats and the 120/24/18 full registries.

Default mode returns success when structure is valid while printing open gaps.
Use ``--strict-completion`` to return exit code 2 while critical gaps remain.
"""

from __future__ import annotations

import argparse
import json
import re
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


def nonempty_fields(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    for field in fields:
        require(record.get(field) not in (None, "", []), f"{label} missing/empty field: {field}")


def expect_ids(actual: Iterable[str], expected: list[str], label: str) -> None:
    actual_list = list(actual)
    require(actual_list == expected, f"{label} IDs must be exactly {expected[0]}..{expected[-1]}")


def iter_named_lists(value: Any, path: str = "root") -> Iterable[tuple[str, list[Any]]]:
    if isinstance(value, list):
        yield path, value
        for index, item in enumerate(value):
            yield from iter_named_lists(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from iter_named_lists(child, f"{path}.{key}")


def discover_inventory(count: int, keywords: tuple[str, ...]) -> list[str]:
    matches: list[str] = []
    for path in sorted((ROOT / "data").glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for key_path, values in iter_named_lists(payload):
            haystack = f"{path.name} {key_path}".lower()
            if len(values) == count and any(keyword.lower() in haystack for keyword in keywords):
                matches.append(f"{path.relative_to(ROOT)}:{key_path}")
    return sorted(set(matches))


def validate_base_world() -> tuple[set[str], set[str], set[str], set[str]]:
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
        expect_ids([record.get("id", "") for record in regions], [f"R{i:02d}" for i in range(8)], "region")
    if len(settlements) == 48:
        expect_ids([record.get("id", "") for record in settlements], [f"ST{i:03d}" for i in range(1, 49)], "settlement")
    if len(routes) == 20:
        expect_ids([record.get("id", "") for record in routes], [f"RT{i:03d}" for i in range(1, 21)], "route")
    if len(factions) == 18:
        expect_ids([record.get("id", "") for record in factions], [f"FC{i:03d}" for i in range(1, 19)], "faction")
    if len(subacts) == 20:
        expect_ids([record.get("id", "") for record in subacts], [f"A{i:02d}" for i in range(1, 21)], "subact")

    region_ids = {record.get("id") for record in regions}
    settlement_ids = {record.get("id") for record in settlements}
    route_ids = {record.get("id") for record in routes}
    faction_ids = {record.get("id") for record in factions}

    for record in settlements:
        require(record.get("region_id") in region_ids, f"{record.get('id')} references unknown region {record.get('region_id')}")

    signatures_by_region: dict[str, list[tuple[Any, ...]]] = defaultdict(list)
    for record in settlements:
        signature = (
            record.get("current_tension"),
            record.get("entry_rule"),
            record.get("daily_operation"),
            record.get("logistics_bottleneck"),
            record.get("disaster_weakness"),
            tuple(record.get("sensory_marks", [])),
            tuple(record.get("local_terms", [])),
        )
        signatures_by_region[record.get("region_id", "")].append(signature)
    repeated_regions = sorted(
        region_id
        for region_id, signatures in signatures_by_region.items()
        if len(signatures) > 1 and len(set(signatures)) == 1
    )
    if repeated_regions:
        WARNINGS.append("base settlement data repeats one region template in: " + ", ".join(repeated_regions))

    causal_inputs = [record.get("causal_input") for record in subacts]
    if causal_inputs and len(set(causal_inputs)) <= 2:
        WARNINGS.append("base subact causal_input is generic; v3.3 causality overlay is mandatory")

    return region_ids, settlement_ids, route_ids, faction_ids


def validate_settlement_overlay(
    region_ids: set[str], settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]
) -> None:
    payload = load_json("data/settlement_identity_overlay_v3_3.json") or {}
    records = payload.get("settlements", [])
    require(len(records) == 48, f"settlement overlay expected 48, found {len(records)}")
    if len(records) != 48:
        return
    expect_ids([record.get("settlement_id", "") for record in records], [f"ST{i:03d}" for i in range(1, 49)], "settlement overlay")

    signatures: list[tuple[Any, ...]] = []
    for record in records:
        sid = record.get("settlement_id")
        nonempty_fields(
            record,
            [
                "name", "region_id", "linked_route_ids", "primary_function", "local_bottleneck",
                "civic_routine", "ownership_dispute", "signature_evidence", "failure_cascade",
                "primary_faction_id",
            ],
            f"settlement overlay {sid}",
        )
        require(sid in settlement_ids, f"unknown settlement reference: {sid}")
        require(record.get("region_id") in region_ids, f"{sid} references unknown region {record.get('region_id')}")
        for route_id in record.get("linked_route_ids", []):
            require(route_id in route_ids, f"{sid} references unknown route {route_id}")
        require(record.get("primary_faction_id") in faction_ids, f"{sid} references unknown faction")
        signatures.append(
            (
                record.get("primary_function"), record.get("local_bottleneck"),
                record.get("civic_routine"), record.get("ownership_dispute"),
            )
        )
    duplicate_signatures = [signature for signature, count in Counter(signatures).items() if count > 1]
    require(not duplicate_signatures, f"settlement overlay has {len(duplicate_signatures)} duplicate operational identities")


def validate_route_overlay(settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]) -> None:
    payload = load_json("data/route_operability_overlay_v3_3.json") or {}
    records = payload.get("routes", [])
    require(len(records) == 20, f"route overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    expect_ids([record.get("route_id", "") for record in records], [f"RT{i:03d}" for i in range(1, 21)], "route overlay")

    required = [
        "from_settlement_id", "to_settlement_id", "controlling_faction_ids", "normal_transit",
        "standard_capacity", "closure_trigger", "alternate_path", "failure_cascade", "ownership_question",
    ]
    for record in records:
        rid = record.get("route_id")
        nonempty_fields(record, required, f"route overlay {rid}")
        require(rid in route_ids, f"unknown route reference: {rid}")
        require(record.get("from_settlement_id") in settlement_ids, f"{rid} has unknown from settlement")
        require(record.get("to_settlement_id") in settlement_ids, f"{rid} has unknown to settlement")
        for faction_id in record.get("controlling_faction_ids", []):
            require(faction_id in faction_ids, f"{rid} references unknown faction {faction_id}")


def validate_faction_overlay(settlement_ids: set[str], faction_ids: set[str]) -> None:
    payload = load_json("data/faction_relation_overlay_v3_3.json") or {}
    nodes = payload.get("factions", [])
    relations = payload.get("relations", [])
    require(len(nodes) == 18, f"faction overlay expected 18 nodes, found {len(nodes)}")
    require(len(relations) == 25, f"faction overlay expected 25 relations, found {len(relations)}")
    if len(nodes) == 18:
        expect_ids([node.get("faction_id", "") for node in nodes], [f"FC{i:03d}" for i in range(1, 19)], "faction overlay")

    for node in nodes:
        fid = node.get("faction_id")
        nonempty_fields(
            node,
            ["name", "primary_settlement_ids", "victory_condition", "defeat_condition", "autonomous_action_without_damun"],
            f"faction overlay {fid}",
        )
        require(fid in faction_ids, f"unknown faction node: {fid}")
        for settlement_id in node.get("primary_settlement_ids", []):
            require(settlement_id in settlement_ids, f"{fid} references unknown settlement {settlement_id}")

    degree: Counter[str] = Counter()
    relation_ids: set[str] = set()
    relation_pairs: set[tuple[str, str]] = set()
    for relation in relations:
        rid = relation.get("relation_id")
        require(rid not in relation_ids, f"duplicate relation id: {rid}")
        relation_ids.add(rid)
        source = relation.get("from_faction_id")
        target = relation.get("to_faction_id")
        require(source in faction_ids and target in faction_ids, f"{rid} has unknown faction reference")
        require(source != target, f"{rid} cannot be a self relation")
        pair = tuple(sorted((source, target)))
        require(pair not in relation_pairs, f"duplicate faction pair in relation graph: {pair}")
        relation_pairs.add(pair)
        nonempty_fields(
            relation,
            ["relation_type", "disputed_resource", "escalation_trigger", "resolution_leverage"],
            f"relation {rid}",
        )
        degree[source] += 1
        degree[target] += 1
    isolated = sorted(faction_id for faction_id in faction_ids if degree[faction_id] == 0)
    require(not isolated, f"isolated factions: {isolated}")


def validate_subact_overlay() -> None:
    payload = load_json("data/subact_causality_overlay_v3_3.json") or {}
    records = payload.get("subacts", [])
    expected_ids = [f"A{i:02d}" for i in range(1, 21)]
    require(len(records) == 20, f"subact overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    expect_ids([record.get("subact_id", "") for record in records], expected_ids, "subact overlay")
    for index, record in enumerate(records):
        sid = record.get("subact_id")
        nonempty_fields(
            record,
            ["title", "incoming_cost", "present_problem", "damun_voluntary_goal", "irreversible_choice", "outgoing_cost"],
            f"subact {sid}",
        )
        expected_next = expected_ids[index + 1] if index < 19 else None
        require(record.get("next_subact_id") == expected_next, f"{sid} next_subact_id must be {expected_next}")
    require(len({record.get("outgoing_cost") for record in records}) == 20, "all outgoing_cost values must be concrete and unique")


def validate_scene_blueprint_status() -> None:
    packet_path = ROOT / "docs/PRODUCTION_PACKET_021_040_V2_5.md"
    if not packet_path.exists():
        ERRORS.append("missing docs/PRODUCTION_PACKET_021_040_V2_5.md")
    else:
        text = packet_path.read_text(encoding="utf-8")
        headings = list(re.finditer(r"^##\s+(\d+)화\b", text, flags=re.MULTILINE))
        require(len(headings) == 20, f"21~40 packet expected 20 episode headings, found {len(headings)}")
        low_beat_episodes: list[tuple[int, int]] = []
        for index, heading in enumerate(headings):
            section_start = heading.end()
            section_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            beat_count = len(re.findall(r"^\d+\.\s", text[section_start:section_end], flags=re.MULTILINE))
            if beat_count < 6:
                low_beat_episodes.append((int(heading.group(1)), beat_count))
        if low_beat_episodes:
            OPEN_GAPS.append(
                "21~40 episodes below 6 scene beats: "
                + ", ".join(f"EP{episode:03d}={count}" for episode, count in low_beat_episodes)
            )

    episode_files = [
        "data/episodes_001_010.json", "data/episodes_011_020.json",
        "data/episodes_021_030.json", "data/episodes_031_040.json",
        "data/episodes_041_080.json", "data/episodes_081_120.json",
        "data/episodes_121_160.json", "data/episodes_161_200.json",
    ]
    covered: list[int] = []
    detailed: set[int] = set()
    for path in episode_files:
        payload = load_json(path)
        if not isinstance(payload, list):
            continue
        for record in payload:
            episode = record.get("episode") or record.get("episode_no") or record.get("number")
            if isinstance(episode, int):
                covered.append(episode)
            beats = record.get("scene_beats")
            if isinstance(episode, int) and isinstance(beats, list) and 6 <= len(beats) <= 10:
                detailed.add(episode)
    require(sorted(set(covered)) == list(range(1, 201)), f"episode source coverage must be exactly 1..200; found {len(set(covered))}")
    missing_detailed = [episode for episode in range(21, 201) if episode not in detailed]
    if missing_detailed:
        OPEN_GAPS.append(f"21~200 episodes without confirmed 6~10 scene_beats in canonical JSON: {len(missing_detailed)}/180")


def validate_collection_inventory() -> None:
    item_sources = discover_inventory(120, ("collection", "collectible", "item", "artifact", "relic", "수집", "유산"))
    set_sources = discover_inventory(24, ("set", "세트"))
    beast_sources = discover_inventory(18, ("beast", "creature", "shinsu", "mount", "신수", "영물", "탈것"))

    if item_sources:
        WARNINGS.append("discoverable 120-entry source(s): " + ", ".join(item_sources))
    else:
        OPEN_GAPS.append("no discoverable 120-entry collectible registry in data/*.json")
    if set_sources:
        WARNINGS.append("discoverable 24-entry source(s): " + ", ".join(set_sources))
    else:
        OPEN_GAPS.append("no discoverable 24-entry set registry in data/*.json")
    if beast_sources:
        WARNINGS.append("discoverable 18-entry beast source(s): " + ", ".join(beast_sources))
    else:
        OPEN_GAPS.append("no discoverable 18-entry beast/mount registry in data/*.json")

    manifest = load_json("data/project_manifest_v2_7.json") or {}
    item_track_count = manifest.get("coverage", {}).get("item_tracks")
    require(item_track_count == 16, f"expected 16 documented long-term item tracks, found {item_track_count}")
    if item_track_count == 16:
        WARNINGS.append("16 long-term item tracks are verified; remaining declared items still need lifecycle coverage")


def validate_status_files() -> None:
    completion = load_json("data/world_blueprint_completion_manifest_v3_3.json") or {}
    categories = {record.get("id"): record for record in completion.get("categories", [])}
    for category_id in ("C14", "C15", "C16"):
        require(categories.get(category_id, {}).get("status") == "unverified", f"{category_id} must remain unverified until its full registry is proven")

    gap_register = load_json("data/world_integration_gap_register_v3_3.json") or {}
    gap_ids = {record.get("gap_id") for record in gap_register.get("gaps", [])}
    for required_gap in ("BP-G01", "BP-G02", "BP-G03", "CS-G01", "CS-G02", "CS-G03", "DOC-G01"):
        require(required_gap in gap_ids, f"gap register missing {required_gap}")


def report_payload() -> dict[str, Any]:
    return {
        "version": "3.3",
        "structural_status": "failed" if ERRORS else "passed",
        "errors": ERRORS,
        "warnings": WARNINGS,
        "critical_open_gaps": OPEN_GAPS,
        "final_completion": not ERRORS and not OPEN_GAPS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-completion", action="store_true")
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    region_ids, settlement_ids, route_ids, faction_ids = validate_base_world()
    validate_settlement_overlay(region_ids, settlement_ids, route_ids, faction_ids)
    validate_route_overlay(settlement_ids, route_ids, faction_ids)
    validate_faction_overlay(settlement_ids, faction_ids)
    validate_subact_overlay()
    validate_scene_blueprint_status()
    validate_collection_inventory()
    validate_status_files()

    payload = report_payload()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.report_json:
        output = args.report_json if args.report_json.is_absolute() else ROOT / args.report_json
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if ERRORS:
        return 1
    if args.strict_completion and OPEN_GAPS:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
