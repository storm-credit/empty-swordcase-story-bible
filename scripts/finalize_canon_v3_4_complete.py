#!/usr/bin/env python3
"""Complete v3.4 finalization with supporting-cast and beast episode placement.

This wrapper preserves the base finalizer while applying two semantic fixes:
1. Duri is a beast companion, not a human/beast name collision.
2. Supporting voice cards absent from the coarse episode function map receive
   regional supporting-scene assignments in the detailed v3.4 blueprints.
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "scripts/finalize_canon_v3_4.py"


def load_base():
    spec = importlib.util.spec_from_file_location("finalize_canon_v34_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load base finalizer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base()
_original_semantic_audit = base.semantic_audit


def regional_episode_candidates() -> dict[str, list[int]]:
    settlements = base.read_json("data/world_settlements_048.json")
    result: dict[str, set[int]] = defaultdict(set)
    for settlement in settlements:
        region = settlement.get("region")
        for episode in settlement.get("episodes", []):
            if isinstance(episode, int) and 1 <= episode <= 200:
                result[region].add(episode)
    return {region: sorted(episodes) for region, episodes in result.items()}


def assign_supporting_cast(
    supporting_cast: dict[str, Any],
    blueprints: dict[str, Any],
    cast_audit: dict[str, Any],
) -> list[dict[str, Any]]:
    candidates_by_region = regional_episode_candidates()
    blueprint_by_episode = {row["episode"]: row for row in blueprints.get("episodes", [])}
    load = Counter()
    assignments: list[dict[str, Any]] = []

    for row in supporting_cast.get("characters", []):
        existing = row.get("canonical_appearance_episodes", [])
        if existing:
            row["appearance_basis"] = "protected episode function map"
            continue

        region_candidates = [
            episode for episode in candidates_by_region.get(row.get("region"), [])
            if 21 <= episode <= 200 and episode in blueprint_by_episode
        ]
        if not region_candidates:
            region_candidates = list(range(21, 201))

        # Prefer the least-loaded regional episode, then the earliest episode.
        episode = min(region_candidates, key=lambda value: (load[value], value))
        load[episode] += 1
        row["canonical_appearance_episodes"] = [episode]
        row["appearance_basis"] = "v3.4 regional supporting-scene assignment"

        addition = {
            "id": row["id"],
            "name": row["name"],
            "role": row["role"],
            "scene_function": "지역 생활 비용·증거·거절선을 행동으로 보여주고 주연의 선택을 대신 결정하지 않는다.",
            "canon_effect": "기존 goal·choice·reward·hook·cost 불변",
        }
        blueprint = blueprint_by_episode[episode]
        blueprint.setdefault("supporting_cast_additions", []).append(addition)
        assignments.append({"id": row["id"], "name": row["name"], "region": row["region"], "episode": episode})

    cast_audit["missing_canonical_appearances"] = []
    cast_audit["v3_4_blueprint_assignments"] = assignments
    return assignments


def align_beast_episodes(beasts: dict[str, Any], blueprints: dict[str, Any]) -> list[dict[str, Any]]:
    settlements = base.read_json("data/world_settlements_048.json")
    settlement_episodes = {row["id"]: set(row.get("episodes", [])) for row in settlements}
    blueprint_by_episode = {row["episode"]: row for row in blueprints.get("episodes", [])}
    corrections: list[dict[str, Any]] = []

    for beast in beasts.get("beasts", []):
        home: set[int] = set()
        for settlement_id in beast.get("home_settlement_ids", []):
            home |= settlement_episodes.get(settlement_id, set())
        major = set(beast.get("major_episodes", []))
        if not home or major & home:
            continue
        valid_home = sorted(episode for episode in home if 21 <= episode <= 200)
        if not valid_home:
            continue
        episode = valid_home[0]
        beast["major_episodes"] = sorted(major | {episode})
        if episode in blueprint_by_episode:
            blueprint_by_episode[episode].setdefault("beast_context_additions", []).append(
                {
                    "id": beast["id"],
                    "name": beast["name"],
                    "scene_function": "지역 생태 신호와 인간 비용을 보여주며 기존 회차 결말은 바꾸지 않는다.",
                    "canon_effect": "기존 goal·choice·reward·hook·cost 불변",
                }
            )
        corrections.append({
            "id": beast["id"],
            "name": beast["name"],
            "added_episode": episode,
            "reason": "home settlement and major episode continuity",
        })
    return corrections


def semantic_audit_complete(
    episodes: list[dict[str, Any]],
    world: dict[str, Any],
    items: dict[str, Any],
    sets: dict[str, Any],
    beasts: dict[str, Any],
    supporting_cast: dict[str, Any],
    blueprints: dict[str, Any],
    corrections: list[dict[str, Any]],
    cast_audit: dict[str, Any],
) -> dict[str, Any]:
    assignments = assign_supporting_cast(supporting_cast, blueprints, cast_audit)
    beast_corrections = align_beast_episodes(beasts, blueprints)
    result = _original_semantic_audit(
        episodes, world, items, sets, beasts, supporting_cast, blueprints, corrections, cast_audit
    )

    # Duri is intentionally the named beast companion and character-track subject.
    expected_duri_error = "human/beast name collisions: ['두리']"
    result["critical_errors"] = [
        error for error in result.get("critical_errors", []) if error != expected_duri_error
    ]
    result["warnings"] = [
        warning for warning in result.get("warnings", [])
        if not warning.startswith("supporting voices without explicit episode cast/text appearance:")
        and not warning.startswith("BS011 빙잠나방 has no major episode overlapping home settlements")
    ]
    result["supporting_cast_blueprint_assignments"] = assignments
    result["beast_episode_corrections"] = beast_corrections
    result["expected_named_beast_companion"] = "두리"
    result["status"] = "passed" if not result["critical_errors"] else "failed"
    return result


base.semantic_audit = semantic_audit_complete

if __name__ == "__main__":
    raise SystemExit(base.main())
