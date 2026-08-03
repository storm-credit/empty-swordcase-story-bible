#!/usr/bin/env python3
"""Validate generated 6-beat episode blueprints against canonical episode data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_3.json"
EPISODE_FILES = [
    "data/episodes_001_010.json", "data/episodes_011_020.json",
    "data/episodes_021_030.json", "data/episodes_031_040.json",
    "data/episodes_041_080.json", "data/episodes_081_120.json",
    "data/episodes_121_160.json", "data/episodes_161_200.json",
]
ERRORS: list[str] = []


def load(path: Path | str) -> Any:
    full = path if isinstance(path, Path) else ROOT / path
    if not full.exists():
        ERRORS.append(f"missing file: {full.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(full.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"invalid JSON {full.relative_to(ROOT)}: {exc}")
        return {}


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> int:
    canonical: dict[int, dict[str, Any]] = {}
    for source in EPISODE_FILES:
        payload = load(source)
        if isinstance(payload, list):
            for record in payload:
                canonical[record["episode"]] = record

    payload = load(BLUEPRINT)
    records = payload.get("episodes", []) if isinstance(payload, dict) else []
    require(payload.get("episode_count") == 180, "blueprint episode_count must be 180")
    require(payload.get("scene_beat_count") == 1080, "blueprint scene_beat_count must be 1080")
    require(payload.get("author_approval_required") is True, "generated blueprints must require author approval")
    require([record.get("episode") for record in records] == list(range(21, 201)), "blueprints must cover EP021..EP200 in order")

    required_phases = [
        "hook_recovery", "world_pressure", "first_attempt",
        "evidence_and_counterpressure", "irreversible_choice", "reward_cost_and_next_hook",
    ]
    source_keys = ["goal", "choice", "reward", "hook", "location", "cast", "episode_function", "cost"]
    for record in records:
        episode = record.get("episode")
        label = f"EP{episode:03d}" if isinstance(episode, int) else "unknown episode"
        require(record.get("status") == "derived_production_blueprint_candidate", f"{label} invalid status")
        require(record.get("author_approval_required") is True, f"{label} must require author approval")
        require(record.get("protected_canon_unchanged") is True, f"{label} must protect canon")
        source = canonical.get(episode)
        require(source is not None, f"{label} missing canonical source")
        if source is None:
            continue
        source_core = record.get("source_core", {})
        for key in source_keys:
            require(source_core.get(key) == source.get(key), f"{label} changed canonical field {key}")
        beats = record.get("scene_beats", [])
        require(len(beats) == 6, f"{label} must have exactly six beats")
        require([beat.get("beat_no") for beat in beats] == [1,2,3,4,5,6], f"{label} beat numbers invalid")
        require([beat.get("phase") for beat in beats] == required_phases, f"{label} beat phases invalid")
        for beat in beats:
            for key in ("objective", "pressure", "action", "reaction", "state_change", "source_fields"):
                require(beat.get(key) not in (None, "", []), f"{label} beat {beat.get('beat_no')} missing {key}")
        before = record.get("state_before", {})
        after = record.get("state_after", {})
        require(before.get("previous_hook") == canonical[episode - 1].get("hook"), f"{label} previous hook mismatch")
        require(before.get("previous_cost") == canonical[episode - 1].get("cost"), f"{label} previous cost mismatch")
        require(after.get("paid_cost") == source.get("cost"), f"{label} paid cost mismatch")
        require(after.get("earned_reward") == source.get("reward"), f"{label} reward mismatch")
        require(after.get("next_hook") == source.get("hook"), f"{label} next hook mismatch")
        require("prose" not in record, f"{label} must not contain manuscript prose")

    result = {
        "version":"3.3",
        "status":"failed" if ERRORS else "passed",
        "errors":ERRORS,
        "verified_episode_count":len(records),
        "verified_scene_beat_count":sum(len(record.get("scene_beats", [])) for record in records),
        "canon_status":"derived_candidate_pending_author_approval",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
