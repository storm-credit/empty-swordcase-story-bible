#!/usr/bin/env python3
"""Generate pre-draft action sheets for major combat/disaster episodes.

These sheets block prose drafting until A13 replaces the zone placeholders with an
exact scene map, distances, named techniques, and movement-by-movement choreography.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "production" / "combat" / "ACTION_PREFLIGHT_041_200.md"
OUT.parent.mkdir(parents=True, exist_ok=True)

TARGETS = [
    48, 55, 60, 66, 70, 74, 76, 80, 89, 90, 91, 93, 96, 100,
    104, 107, 110, 111, 120, 125, 136, 140, 145, 146, 147, 148,
    150, 155, 158, 164, 169, 173, 177, 178, 179, 180, 181, 182,
    185, 186, 187, 188, 190, 191, 192, 193, 194,
]


def load_packet_module():
    path = ROOT / "scripts" / "build_detailed_packets_v2_6.py"
    spec = importlib.util.spec_from_file_location("packet_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import packet builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_rows() -> dict[int, dict]:
    rows: list[dict] = []
    for path in sorted(DATA.glob("episodes_0*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8")))
    return {row["episode"]: row for row in rows}


def start_for(episode: int) -> int:
    return ((episode - 41) // 10) * 10 + 41


def main() -> None:
    rows = load_rows()
    module = load_packet_module()
    lines = [
        "# 41~200화 주요 전투·재난·작전 사전 시트",
        "",
        "> 이 파일은 전투 원고가 아니다. A13이 각 화의 정확한 평면도·거리·초식·동선을 잠근 뒤에만 집필할 수 있다.",
        "",
    ]

    for episode in TARGETS:
        row = rows[episode]
        location, palette, opposition, _ = module.META[start_for(episode)]
        lines.extend([
            f"## {episode}화 — {row['title']}",
            "",
            f"- 사건 유형: 전투/추격/재난/구조 중 A13 확정 필요",
            f"- 무대: {location}",
            f"- 감각 팔레트: {palette}",
            f"- 담운 측 목표: {row['goal']}",
            f"- 반대 압력: {opposition}",
            f"- 독립 행동: {module.independent_action(row)}",
            "- ZONE A 진입점: [A13이 정확한 폭·높이·퇴로 기입]",
            "- ZONE B 보호 대상: [인원·거리·엄폐물 기입]",
            "- ZONE C 목표물: [크기·재질·고정/이동 여부 기입]",
            "- ZONE D 상대 시작점: [거리·시야·첫 기술 사거리 기입]",
            "- ZONE E 환경 위험: [붕괴·독·빙판·수압·중력 등 작동 주기 기입]",
            "- 거리표: A↔B / B↔C / C↔D / D↔E를 보폭과 장병기 사거리로 수치화",
            "- 역전 1: 익숙한 장비·무공이 지역 법칙 때문에 실패한다.",
            "- 역전 2: 동료의 독립 선택 때문에 담운의 목표 또는 진입 순서가 바뀐다.",
            f"- 역전 3: `{row['choice']}` 때문에 승리 조건이 격파에서 구조·귀환·연결 절단으로 바뀐다.",
            "- 동작 안무: [첫 3합 / 공간 이동 / 장비 교체 / 결정타가 아닌 최종 선택을 A13이 기입]",
            f"- 기능 손실·대가: {row['cost']}",
            f"- 마감 이미지: {row['hook']}",
            "- 집필 승인: [ ] A12 공간 / [ ] A13 안무 / [ ] A07 연속성 / [ ] Synapse-PM",
            "",
        ])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated {len(TARGETS)} action preflight sheets")


if __name__ == "__main__":
    main()
