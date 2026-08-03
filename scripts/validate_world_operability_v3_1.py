#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> int:
    regions = load("world_regions_008.json")
    settlements = load("world_settlements_048.json")
    factions = load("world_factions_018.json")
    routes = load("world_routes_020.json")
    secrets = load("world_secrets_036.json")
    glossary = load("world_glossary_120.json")
    subacts = load("acts_subacts_005_020.json")
    supporting = load("supporting_cast_028.json")

    errors: list[str] = []
    if len(regions) != 8:
        errors.append("regions must be 8/8")
    if len(settlements) != 48:
        errors.append("settlements must be 48/48")
    if len(factions) != 18:
        errors.append("factions must be 18/18")
    if len(routes) != 20:
        errors.append("routes must be 20/20")
    if len(secrets) != 36:
        errors.append("secrets must be 36/36")
    if len(glossary) != 120:
        errors.append("glossary must be 120/120")
    if len(subacts) != 20:
        errors.append("subacts must be 20/20")

    region_ids = {row["id"] for row in regions}
    if region_ids != {f"R{i:02d}" for i in range(8)}:
        errors.append("region ids must be R00-R07")
    settlement_ids = {row["id"] for row in settlements}
    if settlement_ids != {f"ST{i:03d}" for i in range(1, 49)}:
        errors.append("settlement ids must be ST001-ST048")
    faction_ids = {row["id"] for row in factions}
    if faction_ids != {f"FC{i:03d}" for i in range(1, 19)}:
        errors.append("faction ids must be FC001-FC018")

    for settlement in settlements:
        if settlement["region_id"] not in region_ids:
            errors.append(f"{settlement['id']}: unknown region {settlement['region_id']}")
        if len(settlement["episodes"]) < 2:
            errors.append(f"{settlement['id']}: fewer than two episode uses")
        for field in (
            "landmark",
            "current_tension",
            "entry_rule",
            "daily_operation",
            "logistics_bottleneck",
            "disaster_weakness",
            "event_seed",
        ):
            if not str(settlement.get(field, "")).strip():
                errors.append(f"{settlement['id']}: missing {field}")

    for region in regions:
        for field in (
            "staple_food",
            "shortage_trigger",
            "transport",
            "bottleneck",
            "taboo",
            "ownership_custom",
            "civic_schedule",
            "disaster_weakness",
            "irrational_rule",
            "finale_contribution",
        ):
            if not str(region.get(field, "")).strip():
                errors.append(f"{region['id']}: missing {field}")
        if len(region.get("sensory_marks", [])) != 3:
            errors.append(f"{region['id']}: sensory marks must be exactly 3")
        if len(region.get("local_terms", [])) != 2:
            errors.append(f"{region['id']}: local terms must be exactly 2")

    for field in ("staple_food", "taboo", "bottleneck"):
        dupes = [value for value, count in Counter(row[field] for row in regions).items() if count > 1]
        if dupes:
            errors.append(f"region {field} duplicates: {dupes}")

    cast_names = {row["name"] for row in supporting}
    for faction in factions:
        for field in (
            "monopoly_resource",
            "external_dependency",
            "income_source",
            "largest_fixed_cost",
            "public_goal",
            "hidden_survival_goal",
            "hardline_faction",
            "moderate_faction",
            "beneficiary_cast",
            "losing_cast",
            "if_damun_disappears",
            "post_act5_conflict",
        ):
            if not str(faction.get(field, "")).strip():
                errors.append(f"{faction['id']}: missing {field}")
        if faction["beneficiary_cast"] == faction["losing_cast"]:
            errors.append(f"{faction['id']}: beneficiary and loser overlap")
        if (
            faction["beneficiary_cast"] not in cast_names
            and faction["beneficiary_cast"] not in {"백장", "무석", "귀족 대리인", "피해 상인", "젊은 역부", "하급 필사관", "가난한 방계", "잡역꾼", "피난민", "하급 세리", "삭제 인격", "짐꾼", "분류된 동료"}
        ):
            errors.append(f"{faction['id']}: beneficiary cast is not recognizable")

    signature_groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for faction in factions:
        signature_groups[
            (
                faction["monopoly_resource"],
                faction["income_source"],
                faction["public_goal"],
            )
        ].append(faction["id"])
    for signature, ids in signature_groups.items():
        if len(ids) > 1:
            errors.append(f"faction functional duplicate {ids}: {signature}")

    route_ids = [row["id"] for row in routes]
    if route_ids != [f"RT{i:03d}" for i in range(1, 21)]:
        errors.append("route ids must be RT001-RT020 in order")

    secret_ids = [row["id"] for row in secrets]
    if secret_ids != [f"WS{i:03d}" for i in range(1, 37)]:
        errors.append("secret ids must be WS001-WS036 in order")

    glossary_ids = [row["id"] for row in glossary]
    if glossary_ids != [f"GL{i:03d}" for i in range(1, 121)]:
        errors.append("glossary ids must be GL001-GL120 in order")
    glossary_terms = [row["term"] for row in glossary]
    if len(glossary_terms) != len(set(glossary_terms)):
        repeated = [term for term, count in Counter(glossary_terms).items() if count > 1]
        errors.append(f"glossary duplicate terms: {repeated}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("v3.1 world operability validation passed")
    print("regions=8 settlements=48 factions=18 routes=20 secrets=36 glossary=120 subacts=20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
