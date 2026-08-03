#!/usr/bin/env python3
"""Materialize compact 10-episode manuscript packets from frozen v3.4 canon.

The packets are read-only inputs for manuscript drafting. They never modify
canonical episode fields or final-canon sources.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "production" / "manuscript_packets"
EPISODE_FILES = [
    "data/episodes_001_010.json", "data/episodes_011_020.json",
    "data/episodes_021_030.json", "data/episodes_031_040.json",
    "data/episodes_041_080.json", "data/episodes_081_120.json",
    "data/episodes_121_160.json", "data/episodes_161_200.json",
]
BLUEPRINT_FILE = "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_4.json"


def load(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def compact_markdown(start: int, end: int, rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# EP{start:03d}~EP{end:03d} 집필 압축 패킷 v3.4",
        "",
        "> 보호 정본의 집필용 요약이다. 목표·선택·보상·훅·비용을 변경하지 않는다.",
        "",
    ]
    for row in rows:
        ep = row["canonical_episode"]
        lines.extend(
            [
                f"## EP{ep['episode']:03d} {ep['title']}",
                f"- Act/Subact: {ep['act']} / {ep['subact']} ({ep['subact_title']})",
                f"- 장소: {ep['location']}",
                f"- 등장: {', '.join(ep.get('cast', []))}",
                f"- 목표: {ep['goal']}",
                f"- 선택: {ep['choice']}",
                f"- 보상: {ep['reward']}",
                f"- 비용: {ep['cost']}",
                f"- 훅: {ep['hook']}",
                f"- 기능: {ep['episode_function']}",
            ]
        )
        blueprint = row.get("scene_blueprint")
        if blueprint:
            phases = [beat.get("phase", "") for beat in blueprint.get("scene_beats", [])]
            lines.append(f"- 6비트: {' → '.join(phases)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
    blueprints = {row["episode"]: row for row in blueprint_payload.get("episodes", [])}
    if set(blueprints) != set(range(21, 201)):
        raise ValueError("v3.4 blueprints must cover EP021..EP200 exactly")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for start in range(1, 201, 10):
        end = start + 9
        rows = [
            {
                "episode": episode,
                "canonical_episode": episodes[episode - 1],
                "scene_blueprint": blueprints.get(episode),
            }
            for episode in range(start, end + 1)
        ]
        payload = {
            "version": "v3.4-manuscript-packet-v1",
            "status": "derived_read_only_drafting_input",
            "protected_canon_unchanged": True,
            "range": [start, end],
            "episodes": rows,
        }
        (OUT_DIR / f"EPISODES_{start:03d}_{end:03d}_V3_4.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (OUT_DIR / f"EPISODES_{start:03d}_{end:03d}_COMPACT_V3_4.md").write_text(
            compact_markdown(start, end, rows), encoding="utf-8"
        )

    print("wrote 20 JSON packets and 20 minimal compact packets for EP001..EP200")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
