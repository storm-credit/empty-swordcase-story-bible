#!/usr/bin/env python3
"""Build a single effective v3.3 world payload from base canon + overlays."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data/effective_world_v3_3.json"


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def index(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        value = record[key]
        if value in result:
            raise ValueError(f"duplicate {key}: {value}")
        result[value] = record
    return result


def merge_record(base: dict[str, Any], overlay: dict[str, Any], overlay_name: str) -> dict[str, Any]:
    merged = dict(base)
    merged[overlay_name] = {key: value for key, value in overlay.items() if key not in {"settlement_id", "route_id", "faction_id", "subact_id"}}
    return merged


def build() -> dict[str, Any]:
    regions = read_json("data/world_regions_008.json")
    settlements = read_json("data/world_settlements_048.json")
    routes = read_json("data/world_routes_020.json")
    factions = read_json("data/world_factions_018.json")
    subacts = read_json("data/acts_subacts_005_020.json")

    settlement_overlay_payload = read_json("data/settlement_identity_overlay_v3_3.json")
    route_overlay_payload = read_json("data/route_operability_overlay_v3_3.json")
    faction_overlay_payload = read_json("data/faction_relation_overlay_v3_3.json")
    subact_overlay_payload = read_json("data/subact_causality_overlay_v3_3.json")

    settlement_overlay = index(settlement_overlay_payload["settlements"], "settlement_id")
    route_overlay = index(route_overlay_payload["routes"], "route_id")
    faction_overlay = index(faction_overlay_payload["factions"], "faction_id")
    subact_overlay = index(subact_overlay_payload["subacts"], "subact_id")

    base_settlement_ids = {record["id"] for record in settlements}
    base_route_ids = {record["id"] for record in routes}
    base_faction_ids = {record["id"] for record in factions}
    base_subact_ids = {record["id"] for record in subacts}

    if base_settlement_ids != set(settlement_overlay):
        raise ValueError("settlement base/overlay ID mismatch")
    if base_route_ids != set(route_overlay):
        raise ValueError("route base/overlay ID mismatch")
    if base_faction_ids != set(faction_overlay):
        raise ValueError("faction base/overlay ID mismatch")
    if base_subact_ids != set(subact_overlay):
        raise ValueError("subact base/overlay ID mismatch")

    effective_settlements = [merge_record(record, settlement_overlay[record["id"]], "operability_v3_3") for record in settlements]
    effective_routes = [merge_record(record, route_overlay[record["id"]], "operability_v3_3") for record in routes]
    effective_factions = [merge_record(record, faction_overlay[record["id"]], "relation_state_v3_3") for record in factions]
    effective_subacts = [merge_record(record, subact_overlay[record["id"]], "causality_v3_3") for record in subacts]

    return {
        "version": "3.3",
        "status": "effective_world_built_from_base_and_overlays",
        "source_files": [
            "data/world_regions_008.json",
            "data/world_settlements_048.json",
            "data/settlement_identity_overlay_v3_3.json",
            "data/world_routes_020.json",
            "data/route_operability_overlay_v3_3.json",
            "data/world_factions_018.json",
            "data/faction_relation_overlay_v3_3.json",
            "data/acts_subacts_005_020.json",
            "data/subact_causality_overlay_v3_3.json"
        ],
        "regions": regions,
        "settlements": effective_settlements,
        "routes": effective_routes,
        "factions": effective_factions,
        "faction_relations": faction_overlay_payload["relations"],
        "subacts": effective_subacts
    }


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if output is absent or stale")
    args = parser.parse_args()

    expected = render(build())
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        if not output.exists():
            print(f"missing generated file: {output.relative_to(ROOT)}")
            return 1
        actual = output.read_text(encoding="utf-8")
        if actual != expected:
            print(f"stale generated file: {output.relative_to(ROOT)}")
            return 1
        print(f"OK: {output.relative_to(ROOT)} is current")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
