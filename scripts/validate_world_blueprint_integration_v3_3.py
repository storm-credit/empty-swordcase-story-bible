#!/usr/bin/env python3
"""Validate v3.3 world integration and blueprint completion layers.

Structural errors fail the command. Known completion gaps are reported separately.
Use --strict-completion to fail while any detailed scene-blueprint gap remains.
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


def load(path: str) -> Any:
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


def require_fields(record: dict[str, Any], fields: Iterable[str], label: str) -> None:
    for field in fields:
        require(record.get(field) not in (None, "", []), f"{label} missing/empty field: {field}")


def exact_ids(actual: Iterable[str], expected: list[str], label: str) -> None:
    require(list(actual) == expected, f"{label} IDs must be {expected[0]}..{expected[-1]} in order")


def validate_base() -> tuple[set[str], set[str], set[str], set[str]]:
    regions = load("data/world_regions_008.json") or []
    settlements = load("data/world_settlements_048.json") or []
    routes = load("data/world_routes_020.json") or []
    factions = load("data/world_factions_018.json") or []
    subacts = load("data/acts_subacts_005_020.json") or []

    require(len(regions) == 8, f"expected 8 regions, found {len(regions)}")
    require(len(settlements) == 48, f"expected 48 settlements, found {len(settlements)}")
    require(len(routes) == 20, f"expected 20 routes, found {len(routes)}")
    require(len(factions) == 18, f"expected 18 factions, found {len(factions)}")
    require(len(subacts) == 20, f"expected 20 subacts, found {len(subacts)}")

    if len(regions) == 8:
        exact_ids([record.get("id", "") for record in regions], [f"R{index:02d}" for index in range(8)], "region")
    if len(settlements) == 48:
        exact_ids([record.get("id", "") for record in settlements], [f"ST{index:03d}" for index in range(1, 49)], "settlement")
    if len(routes) == 20:
        exact_ids([record.get("id", "") for record in routes], [f"RT{index:03d}" for index in range(1, 21)], "route")
    if len(factions) == 18:
        exact_ids([record.get("id", "") for record in factions], [f"FC{index:03d}" for index in range(1, 19)], "faction")
    if len(subacts) == 20:
        exact_ids([record.get("id", "") for record in subacts], [f"A{index:02d}" for index in range(1, 21)], "subact")

    region_ids = {record.get("id") for record in regions}
    settlement_ids = {record.get("id") for record in settlements}
    route_ids = {record.get("id") for record in routes}
    faction_ids = {record.get("id") for record in factions}
    for record in settlements:
        require(record.get("region_id") in region_ids, f"{record.get('id')} references unknown region")

    signatures_by_region: dict[str, list[tuple[Any, ...]]] = defaultdict(list)
    for record in settlements:
        signatures_by_region[record.get("region_id", "")].append(
            (
                record.get("current_tension"), record.get("entry_rule"), record.get("daily_operation"),
                record.get("logistics_bottleneck"), record.get("disaster_weakness"),
                tuple(record.get("sensory_marks", [])), tuple(record.get("local_terms", [])),
            )
        )
    repeated = sorted(region for region, signatures in signatures_by_region.items() if len(signatures) > 1 and len(set(signatures)) == 1)
    if repeated:
        WARNINGS.append("base settlement file repeats one operational template in: " + ", ".join(repeated))
    if len({record.get("causal_input") for record in subacts}) <= 2:
        WARNINGS.append("base subact causal_input is generic; v3.3 overlay is required")
    return region_ids, settlement_ids, route_ids, faction_ids


def validate_settlements(region_ids: set[str], settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]) -> None:
    records = (load("data/settlement_identity_overlay_v3_3.json") or {}).get("settlements", [])
    require(len(records) == 48, f"settlement overlay expected 48, found {len(records)}")
    if len(records) != 48:
        return
    exact_ids([record.get("settlement_id", "") for record in records], [f"ST{index:03d}" for index in range(1, 49)], "settlement overlay")
    signatures: list[tuple[Any, ...]] = []
    for record in records:
        sid = record.get("settlement_id")
        require_fields(record, ["name","region_id","linked_route_ids","primary_function","local_bottleneck","civic_routine","ownership_dispute","signature_evidence","failure_cascade","primary_faction_id"], sid or "settlement")
        require(sid in settlement_ids, f"unknown settlement {sid}")
        require(record.get("region_id") in region_ids, f"{sid} unknown region")
        require(record.get("primary_faction_id") in faction_ids, f"{sid} unknown primary faction")
        for route_id in record.get("linked_route_ids", []):
            require(route_id in route_ids, f"{sid} unknown route {route_id}")
        signatures.append((record.get("primary_function"), record.get("local_bottleneck"), record.get("civic_routine"), record.get("ownership_dispute")))
    require(len(signatures) == len(set(signatures)), "settlement overlay contains duplicate operational identities")


def validate_routes(settlement_ids: set[str], route_ids: set[str], faction_ids: set[str]) -> None:
    records = (load("data/route_operability_overlay_v3_3.json") or {}).get("routes", [])
    require(len(records) == 20, f"route overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    exact_ids([record.get("route_id", "") for record in records], [f"RT{index:03d}" for index in range(1, 21)], "route overlay")
    for record in records:
        rid = record.get("route_id")
        require_fields(record, ["from_settlement_id","to_settlement_id","controlling_faction_ids","normal_transit","standard_capacity","closure_trigger","alternate_path","failure_cascade","ownership_question"], rid or "route")
        require(rid in route_ids, f"unknown route {rid}")
        require(record.get("from_settlement_id") in settlement_ids, f"{rid} unknown origin")
        require(record.get("to_settlement_id") in settlement_ids, f"{rid} unknown destination")
        for faction_id in record.get("controlling_faction_ids", []):
            require(faction_id in faction_ids, f"{rid} unknown controlling faction {faction_id}")


def validate_factions(settlement_ids: set[str], faction_ids: set[str]) -> None:
    payload = load("data/faction_relation_overlay_v3_3.json") or {}
    nodes = payload.get("factions", [])
    relations = payload.get("relations", [])
    require(len(nodes) == 18, f"faction overlay expected 18 nodes, found {len(nodes)}")
    require(len(relations) == 25, f"faction relation graph expected 25 edges, found {len(relations)}")
    if len(nodes) == 18:
        exact_ids([node.get("faction_id", "") for node in nodes], [f"FC{index:03d}" for index in range(1, 19)], "faction overlay")
    for node in nodes:
        fid = node.get("faction_id")
        require_fields(node, ["name","primary_settlement_ids","victory_condition","defeat_condition","autonomous_action_without_damun"], fid or "faction")
        require(fid in faction_ids, f"unknown faction node {fid}")
        for settlement_id in node.get("primary_settlement_ids", []):
            require(settlement_id in settlement_ids, f"{fid} unknown settlement {settlement_id}")
    degree: Counter[str] = Counter()
    pairs: set[tuple[str, str]] = set()
    relation_ids: set[str] = set()
    for relation in relations:
        relation_id = relation.get("relation_id")
        source = relation.get("from_faction_id")
        target = relation.get("to_faction_id")
        require(relation_id not in relation_ids, f"duplicate relation ID {relation_id}")
        relation_ids.add(relation_id)
        require(source in faction_ids and target in faction_ids and source != target, f"{relation_id} invalid faction endpoints")
        pair = tuple(sorted((source, target)))
        require(pair not in pairs, f"duplicate faction pair {pair}")
        pairs.add(pair)
        require_fields(relation, ["relation_type","disputed_resource","escalation_trigger","resolution_leverage"], relation_id or "relation")
        degree[source] += 1
        degree[target] += 1
    require(not [fid for fid in faction_ids if degree[fid] == 0], "faction graph has isolated nodes")


def validate_subacts() -> None:
    records = (load("data/subact_causality_overlay_v3_3.json") or {}).get("subacts", [])
    expected = [f"A{index:02d}" for index in range(1, 21)]
    require(len(records) == 20, f"subact overlay expected 20, found {len(records)}")
    if len(records) != 20:
        return
    exact_ids([record.get("subact_id", "") for record in records], expected, "subact overlay")
    for index, record in enumerate(records):
        sid = record.get("subact_id")
        require_fields(record, ["title","incoming_cost","present_problem","damun_voluntary_goal","irreversible_choice","outgoing_cost"], sid or "subact")
        expected_next = expected[index + 1] if index < 19 else None
        require(record.get("next_subact_id") == expected_next, f"{sid} next_subact_id must be {expected_next}")
    require(len({record.get("outgoing_cost") for record in records}) == 20, "subact outgoing costs must be unique")


def validate_episode_layers() -> None:
    packet = ROOT / "docs/PRODUCTION_PACKET_021_040_V2_5.md"
    if not packet.exists():
        ERRORS.append("missing docs/PRODUCTION_PACKET_021_040_V2_5.md")
    else:
        text = packet.read_text(encoding="utf-8")
        headings = list(re.finditer(r"^##\s+(\d+)화\b", text, flags=re.MULTILINE))
        require(len(headings) == 20, f"21~40 packet expected 20 headings, found {len(headings)}")
        low: list[str] = []
        for index, heading in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            count = len(re.findall(r"^\d+\.\s", text[heading.end():end], flags=re.MULTILINE))
            if count < 6:
                low.append(f"EP{int(heading.group(1)):03d}={count}")
        if low:
            OPEN_GAPS.append("21~40 below 6 scene beats: " + ", ".join(low))

    files = [
        "data/episodes_001_010.json","data/episodes_011_020.json","data/episodes_021_030.json","data/episodes_031_040.json",
        "data/episodes_041_080.json","data/episodes_081_120.json","data/episodes_121_160.json","data/episodes_161_200.json",
    ]
    covered: set[int] = set()
    detailed: set[int] = set()
    for path in files:
        records = load(path)
        if not isinstance(records, list):
            continue
        for record in records:
            episode = record.get("episode") or record.get("episode_no") or record.get("number")
            if isinstance(episode, int):
                covered.add(episode)
                beats = record.get("scene_beats")
                if isinstance(beats, list) and 6 <= len(beats) <= 10:
                    detailed.add(episode)
    require(covered == set(range(1, 201)), f"episode function map covers {len(covered)}/200")
    missing = [episode for episode in range(21, 201) if episode not in detailed]
    if missing:
        OPEN_GAPS.append(f"21~200 without confirmed 6~10 scene_beats: {len(missing)}/180")


def validate_status() -> None:
    completion = load("data/world_blueprint_completion_manifest_v3_3.json") or {}
    categories = {record.get("id"): record for record in completion.get("categories", [])}
    expected_status = "provisional_registry_complete_validation_pending"
    for category_id in ("C14", "C15", "C16"):
        require(categories.get(category_id, {}).get("status") == expected_status, f"{category_id} must show provisional registry completion")
    governance = load("data/collection_system_governance_v3_3.json") or {}
    require(governance.get("approval_required") is True, "candidate registries must require author approval")
    gaps = load("data/world_integration_gap_register_v3_3.json") or {}
    gap_ids = {record.get("gap_id") for record in gaps.get("gaps", [])}
    for gap_id in ("BP-G01","BP-G02","BP-G03","CS-G01","CS-G02","CS-G03","DOC-G01"):
        require(gap_id in gap_ids, f"gap register missing {gap_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-completion", action="store_true")
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()

    region_ids, settlement_ids, route_ids, faction_ids = validate_base()
    validate_settlements(region_ids, settlement_ids, route_ids, faction_ids)
    validate_routes(settlement_ids, route_ids, faction_ids)
    validate_factions(settlement_ids, faction_ids)
    validate_subacts()
    validate_episode_layers()
    validate_status()

    result = {
        "version":"3.3",
        "structural_status":"failed" if ERRORS else "passed",
        "errors":ERRORS,
        "warnings":WARNINGS,
        "open_completion_gaps":OPEN_GAPS,
        "final_completion":not ERRORS and not OPEN_GAPS,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.report_json:
        output = args.report_json if args.report_json.is_absolute() else ROOT / args.report_json
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    if ERRORS:
        return 1
    if args.strict_completion and OPEN_GAPS:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
