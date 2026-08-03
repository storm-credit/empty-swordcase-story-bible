#!/usr/bin/env python3
"""Materialize compact 10-episode manuscript packets from frozen v3.4 canon.

The packets are reading inputs for manuscript drafting. They do not alter any
canonical episode field or final-canon source.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "production" / "manuscript_packets"
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
BLUEPRINT_FILE = "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json"


def load(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    episodes: list[dict[str, Any]] = []
    for path in EPISODE_FILES:
        payload = load(path)
        if not isinstance(payload, list):
            raise ValueError(f"{path} must contain a list")
        episodes.extend(payload)
    episodes.sort(key=lambda row: row["episode"])
    if [row["episode"] for row in episodes] != list(range(1, 201)):
        raise ValueError("canonical episode files must cover EP001..EP200 exactly")

    blueprint_payload = load(BLUEPRINT_FILE)
    blueprint_rows = blueprint_payload.get("episodes", [])
    blueprints = {row["episode"]: row for row in blueprint_rows}
    if set(blueprints) != set(range(21, 201)):
        raise ValueError("v3.4 blueprints must cover EP021..EP200 exactly")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for start in range(1, 201, 10):
        end = start + 9
        rows: list[dict[str, Any]] = []
        for episode in range(start, end + 1):
            canonical = episodes[episode - 1]
            rows.append(
                {
                    "episode": episode,
                    "canonical_episode": canonical,
                    "scene_blueprint": blueprints.get(episode),
                }
            )
        payload = {
            "version": "v3.4-manuscript-packet-v1",
            "status": "derived_read_only_drafting_input",
            "protected_canon_unchanged": True,
            "range": [start, end],
            "episodes": rows,
        }
        target = OUT_DIR / f"EPISODES_{start:03d}_{end:03d}_V3_4.json"
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("wrote 20 manuscript packets for EP001..EP200")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
