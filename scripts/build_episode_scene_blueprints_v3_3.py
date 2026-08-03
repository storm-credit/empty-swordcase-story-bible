#!/usr/bin/env python3
"""Derive non-destructive 6-beat production blueprints for episodes 21~200.

The generator does not invent new plot outcomes. It preserves each canonical
``goal / choice / reward / hook / location / cast / cost`` field and turns
those fields into a consistent scene packet that can later receive author
approved concrete staging.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "production/blueprints/EPISODES_021_200_SCENE_BLUEPRINT_V3_3.json"
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


def read_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def load_episodes() -> list[dict[str, Any]]:
    episodes: list[dict[str, Any]] = []
    for path in EPISODE_FILES:
        payload = read_json(path)
        if not isinstance(payload, list):
            raise ValueError(f"{path} must contain a list")
        episodes.extend(payload)
    episodes.sort(key=lambda record: record["episode"])
    if [record["episode"] for record in episodes] != list(range(1, 201)):
        raise ValueError("episode sources must cover 1..200 exactly")
    return episodes


def canonical_subact_id(source_id: str) -> str:
    match = re.fullmatch(r"ACT(\d+)-SA(\d+)", source_id or "")
    if not match:
        raise ValueError(f"unsupported source subact id: {source_id}")
    act = int(match.group(1))
    local_subact = int(match.group(2))
    return f"A{((act - 1) * 4 + local_subact):02d}"


def load_collection_refs() -> tuple[dict[int, list[str]], dict[int, list[str]], dict[int, list[str]]]:
    items_payload = read_json("data/collection_registry_120_v3_3.json")
    sets_payload = read_json("data/set_registry_024_v3_3.json")
    beasts_payload = read_json("data/beast_registry_018_v3_3.json")
    governance = read_json("data/collection_system_governance_v3_3.json")

    item_events: dict[int, list[str]] = {}
    for batch in items_payload["batches"]:
        for item in batch["items"]:
            item_events.setdefault(item["first_episode"], []).append(f"{item['id']}:first")
            item_events.setdefault(item["final_episode"], []).append(f"{item['id']}:final")

    set_events: dict[int, list[str]] = {}
    corrections = governance.get("effective_corrections", {})
    for record in sets_payload["sets"]:
        episode = corrections.get(record["id"], {}).get("first_complete_episode", record["first_complete_episode"])
        set_events.setdefault(episode, []).append(f"{record['id']}:complete")

    beast_events: dict[int, list[str]] = {}
    for record in beasts_payload["beasts"]:
        for episode in record["major_episodes"]:
            beast_events.setdefault(episode, []).append(record["id"])
    return item_events, set_events, beast_events


def build_beat(
    number: int,
    phase: str,
    objective: str,
    pressure: str,
    action: str,
    reaction: str,
    state_change: str,
    source_fields: list[str],
) -> dict[str, Any]:
    return {
        "beat_no": number,
        "phase": phase,
        "objective": objective,
        "pressure": pressure,
        "action": action,
        "reaction": reaction,
        "state_change": state_change,
        "source_fields": source_fields,
    }


def build() -> dict[str, Any]:
    episodes = load_episodes()
    by_number = {record["episode"]: record for record in episodes}
    causality_payload = read_json("data/subact_causality_overlay_v3_3.json")
    causality = {record["subact_id"]: record for record in causality_payload["subacts"]}
    item_events, set_events, beast_events = load_collection_refs()

    records: list[dict[str, Any]] = []
    for episode_number in range(21, 201):
        episode = by_number[episode_number]
        previous = by_number[episode_number - 1]
        subact_id = canonical_subact_id(episode["subact"])
        subact = causality[subact_id]
        cast = episode.get("cast", [])
        lead_cast = "·".join(cast[:2]) if cast else "담운"
        reference_events = {
            "items": sorted(item_events.get(episode_number, [])),
            "sets": sorted(set_events.get(episode_number, [])),
            "beasts": sorted(beast_events.get(episode_number, [])),
        }
        evidence_label = ", ".join(reference_events["items"] + reference_events["sets"] + reference_events["beasts"])
        if not evidence_label:
            evidence_label = episode["reward"]

        beats = [
            build_beat(
                1,
                "hook_recovery",
                f"직전 화의 훅을 {episode['location']}에서 즉시 행동 문제로 회수한다.",
                previous["hook"],
                f"{lead_cast}가 직전 훅의 물리적 결과를 확인하고 이번 목표를 선택한다.",
                episode["goal"],
                "이번 화의 즉시 목표와 실패 손실이 고정된다.",
                ["previous.hook", "location", "goal"],
            ),
            build_beat(
                2,
                "world_pressure",
                "지역 운영 규칙과 생활 병목이 목표를 제한하는 방식을 장면화한다.",
                episode["episode_function"],
                f"{episode['location']}의 검문·거래·수선·운송·생계 중 현재 비용과 직접 맞닿은 행동을 수행한다.",
                episode["cost"],
                "시간·돈·장비·권리·관계 중 최소 하나가 악화된다.",
                ["location", "episode_function", "cost"],
            ),
            build_beat(
                3,
                "first_attempt",
                episode["goal"],
                subact["present_problem"],
                f"{lead_cast}가 가장 직접적인 해결 시도를 실행한다.",
                f"시도는 {episode['choice']}라는 선택 없이는 끝낼 수 없는 상태를 만든다.",
                "초기 해법이 불완전하다는 사실과 반대자의 정당성이 드러난다.",
                ["goal", "choice", "subact.present_problem"],
            ),
            build_beat(
                4,
                "evidence_and_counterpressure",
                "문서 설명보다 생활 흔적·사용 기록·관계 반응을 먼저 확인한다.",
                evidence_label,
                f"후보 참조({evidence_label})를 소유 보상이 아니라 증거·제약·책임으로 사용한다.",
                episode["reward"],
                "첫 해석이 수정되고 비가역 선택의 기준이 생긴다.",
                ["reward", "collection_registry", "set_registry", "beast_registry"],
            ),
            build_beat(
                5,
                "irreversible_choice",
                episode["choice"],
                subact["incoming_cost"],
                f"담운 또는 핵심 동료가 하나의 이익·권한·전력·관계를 실제로 포기한다.",
                episode["cost"],
                "비용이 즉시 지불되고 이전 상태로 돌아갈 수 없게 된다.",
                ["choice", "cost", "subact.incoming_cost"],
            ),
            build_beat(
                6,
                "reward_cost_and_next_hook",
                episode["reward"],
                subact["outgoing_cost"] if episode_number % 10 == 0 else episode["cost"],
                "보상·정보·관계 변화가 실제 행동이나 물건 상태로 확인된다.",
                episode["hook"],
                "다음 화의 첫 행동을 발생시키는 물리·관계·권리 잔여가 남는다.",
                ["reward", "hook", "cost", "subact.outgoing_cost"],
            ),
        ]

        records.append(
            {
                "episode": episode_number,
                "act": episode["act"],
                "subact_id": subact_id,
                "source_subact": episode["subact"],
                "title": episode["title"],
                "status": "derived_production_blueprint_candidate",
                "author_approval_required": True,
                "protected_canon_unchanged": True,
                "source_core": {
                    "goal": episode["goal"],
                    "choice": episode["choice"],
                    "reward": episode["reward"],
                    "hook": episode["hook"],
                    "location": episode["location"],
                    "cast": cast,
                    "episode_function": episode["episode_function"],
                    "cost": episode["cost"],
                },
                "state_before": {
                    "previous_hook": previous["hook"],
                    "previous_cost": previous["cost"],
                    "incoming_subact_cost": subact["incoming_cost"],
                },
                "scene_beats": beats,
                "state_after": {
                    "paid_cost": episode["cost"],
                    "earned_reward": episode["reward"],
                    "next_hook": episode["hook"],
                    "outgoing_subact_cost": subact["outgoing_cost"] if episode_number % 10 == 0 else None,
                },
                "registry_events": reference_events,
            }
        )

    return {
        "version": "3.3",
        "status": "derived_production_blueprint_candidate",
        "author_approval_required": True,
        "range": [21, 200],
        "episode_count": len(records),
        "scene_beat_count": sum(len(record["scene_beats"]) for record in records),
        "generation_rule": "canonical episode fields preserved; six non-destructive beats derived per episode",
        "source_files": EPISODE_FILES + [
            "data/subact_causality_overlay_v3_3.json",
            "data/collection_registry_120_v3_3.json",
            "data/set_registry_024_v3_3.json",
            "data/beast_registry_018_v3_3.json",
            "data/collection_system_governance_v3_3.json",
        ],
        "episodes": records,
    }


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(build())
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        if not output.exists():
            print(f"missing generated file: {output.relative_to(ROOT)}")
            return 1
        if output.read_text(encoding="utf-8") != expected:
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
