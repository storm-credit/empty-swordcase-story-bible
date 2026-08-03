#!/usr/bin/env python3
"""Validate the approved v3.4 final design-bible artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
APPROVAL_ID = "AUTHOR-AUTO-V3.4-20260803"

PATHS = {
    "world": "data/effective_world_v3_4.json",
    "items": "data/collection_registry_120_v3_4.json",
    "sets": "data/set_registry_024_v3_4.json",
    "beasts": "data/beast_registry_018_v3_4.json",
    "supporting_cast": "data/supporting_cast_operability_028_v3_4.json",
    "blueprints": "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json",
    "approval": "data/canon_approval_v3_4.json",
    "audit": "data/final_semantic_audit_v3_4.json",
    "manifest": "data/project_manifest_v3_4.json",
    "freeze_doc": "docs/57_FINAL_CANON_FREEZE_V3_4.md",
}

EPISODE_FILES = [
    "data/episodes_001_010.json",
    "data/episodes_011_020.json",
    "data/episodes_021_030.json",
    "data/episodes_031_040.json",
    "data/episodes_041_080.json",
    "data/episodes_081_120.json",
    "data/episodes_121_160.json",
    "data/episodes_161_200.json",
]


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


def flatten_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for batch in payload.get("batches", []) for item in batch.get("items", [])]


def episode_map() -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for path in EPISODE_FILES:
        payload = load(path)
        if isinstance(payload, list):
            for row in payload:
                result[row["episode"]] = row
    return result


def contains_name(row: dict[str, Any], name: str) -> bool:
    if name in row.get("cast", []):
        return True
    parts: list[str] = []
    for value in row.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
    return name in " ".join(parts)


def main() -> int:
    world = load(PATHS["world"])
    items = load(PATHS["items"])
    sets = load(PATHS["sets"])
    beasts = load(PATHS["beasts"])
    supporting = load(PATHS["supporting_cast"])
    blueprints = load(PATHS["blueprints"])
    approval = load(PATHS["approval"])
    audit = load(PATHS["audit"])
    manifest = load(PATHS["manifest"])
    episodes = episode_map()

    require(len(episodes) == 200, f"canonical episode map has {len(episodes)}/200 episodes")
    require(world.get("version") == "3.4", "world version must be 3.4")
    require(world.get("status") == "approved_effective_world_canon", "world is not approved canon")
    require(len(world.get("regions", [])) == 8, "world must have 8 regions")
    require(len(world.get("settlements", [])) == 48, "world must have 48 settlements")
    require(len(world.get("routes", [])) == 20, "world must have 20 routes")
    require(len(world.get("factions", [])) == 18, "world must have 18 factions")
    require(len(world.get("subacts", [])) == 20, "world must have 20 subacts")

    item_rows = flatten_items(items)
    set_rows = sets.get("sets", [])
    beast_rows = beasts.get("beasts", [])
    cast_rows = supporting.get("characters", [])
    blueprint_rows = blueprints.get("episodes", [])

    require(items.get("status") == "approved_canon_registry", "items are not approved canon")
    require(sets.get("status") == "approved_canon_registry", "sets are not approved canon")
    require(beasts.get("status") == "approved_canon_registry", "beasts are not approved canon")
    require(len(item_rows) == 120, f"items must be 120, found {len(item_rows)}")
    require(len(set_rows) == 24, f"sets must be 24, found {len(set_rows)}")
    require(len(beast_rows) == 18, f"beasts must be 18, found {len(beast_rows)}")
    require(len(cast_rows) == 28, f"supporting cast must be 28, found {len(cast_rows)}")

    require([row.get("id") for row in item_rows] == [f"CI{i:03d}" for i in range(1, 121)], "item IDs must be CI001..CI120")
    require([row.get("id") for row in set_rows] == [f"SET{i:03d}" for i in range(1, 25)], "set IDs must be SET001..SET024")
    require([row.get("id") for row in beast_rows] == [f"BS{i:03d}" for i in range(1, 19)], "beast IDs must be BS001..BS018")
    require([row.get("id") for row in cast_rows] == [f"SC{i:03d}" for i in range(1, 29)], "supporting cast IDs must be SC001..SC028")

    source_voices = load("data/supporting_cast_voice_028_v2_9.json")
    require(
        [row.get("name") for row in cast_rows] == [row.get("name") for row in source_voices],
        "approved supporting cast must exactly match the 28 voice-card names and order",
    )
    for row in cast_rows:
        appearances = row.get("canonical_appearance_episodes", [])
        require(appearances == sorted(set(appearances)), f"{row.get('id')} appearance episodes must be sorted and unique")
        for episode in appearances:
            require(episode in episodes, f"{row.get('id')} has invalid episode {episode}")
            require(contains_name(episodes[episode], row["name"]), f"{row.get('id')} appearance EP{episode:03d} is not grounded")
        for field in (
            "private_goal", "hidden_insecurity", "refusal_line",
            "personal_loss_from_damun_choice", "choice_without_damun",
            "relationship_pressure", "ending_state",
        ):
            require(isinstance(row.get(field), str) and len(row[field].strip()) >= 18, f"{row.get('id')} weak/missing {field}")

    item_names = {row["name"] for row in item_rows}
    beast_names = {row["name"] for row in beast_rows}
    cast_names = {row["name"] for row in cast_rows}
    protected_main = {"담운", "서린화", "곽무석", "소예란", "진여강", "백장", "두리"}
    require(not (item_names & beast_names), "living beast name is duplicated in the item registry")
    require(not (beast_names & cast_names), "supporting human/beast name collision remains")
    require(not (beast_names & protected_main), "main character/beast name collision remains")

    require(blueprints.get("status") == "approved_canon_production_blueprint", "blueprints are not approved canon")
    require(blueprints.get("author_approval_required") is False, "blueprints still require approval")
    require([row.get("episode") for row in blueprint_rows] == list(range(21, 201)), "blueprints must cover EP021..EP200")
    require(len(blueprint_rows) == 180, "blueprint episode count must be 180")
    require(sum(len(row.get("scene_beats", [])) for row in blueprint_rows) == 1080, "blueprint beat count must be 1080")
    for row in blueprint_rows:
        episode = row["episode"]
        source = episodes[episode]
        require(len(row.get("scene_beats", [])) == 6, f"EP{episode:03d} must have six beats")
        require(row.get("status") == "canon_production_blueprint", f"EP{episode:03d} is not canon")
        require(row.get("author_approval_required") is False, f"EP{episode:03d} still requires approval")
        for key in ("goal", "choice", "reward", "hook", "location", "cast", "episode_function", "cost"):
            require(row.get("source_core", {}).get(key) == source.get(key), f"EP{episode:03d} changed protected {key}")

    require(approval.get("approval_id") == APPROVAL_ID, "approval ID mismatch")
    require(approval.get("approved") is True, "final canon is not approved")
    require(approval.get("audit_status") == "passed", "approval audit did not pass")
    require(audit.get("status") == "passed", "semantic audit did not pass")
    require(audit.get("critical_errors") == [], "semantic audit has critical errors")
    require(audit.get("protected_sources_modified") is False, "protected sources were marked modified")

    project = manifest.get("project", {})
    completion = manifest.get("completion", {})
    require(project.get("version") == "3.4-final-design-bible", "project manifest version mismatch")
    require(project.get("status") == "design_blueprint_world_bible_complete", "project is not marked design complete")
    for key in (
        "core_canon", "act_arc_subact_architecture", "episode_function_map_001_200",
        "effective_world_008_048_020_018", "collectible_registry_120", "set_registry_024",
        "beast_registry_018", "supporting_cast_operability_028",
        "production_blueprints_021_200_six_beats", "semantic_audit",
    ):
        require(completion.get(key) is True, f"manifest completion gate false: {key}")
    require(completion.get("prose_manuscript") is False, "manifest must not claim prose completion")
    require((ROOT / PATHS["freeze_doc"]).exists(), "final freeze document missing")

    result = {
        "version": "3.4",
        "status": "failed" if ERRORS else "passed",
        "approval_id": APPROVAL_ID,
        "errors": ERRORS,
        "verified": {
            "episodes": len(episodes),
            "blueprints": len(blueprint_rows),
            "scene_beats": sum(len(row.get("scene_beats", [])) for row in blueprint_rows),
            "regions": len(world.get("regions", [])),
            "settlements": len(world.get("settlements", [])),
            "routes": len(world.get("routes", [])),
            "factions": len(world.get("factions", [])),
            "items": len(item_rows),
            "sets": len(set_rows),
            "beasts": len(beast_rows),
            "supporting_cast": len(cast_rows),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
