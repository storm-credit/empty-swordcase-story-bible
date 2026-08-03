#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "subact_operability_overlay_v3_2.json"
OVERLAY = ROOT / "production" / "overlays" / "EPISODES_001_010_OPERABILITY_V3_2.md"
AUDIT = ROOT / "docs" / "51_ARCADIUM_YOTA_FOLLOWUP_AND_PROSE_OPERABILITY_V3_2.md"

REQUIRED_FIELDS = {
    "id",
    "conflict_engine",
    "lifestyle_pressure",
    "movement_change",
    "emotional_pressure",
    "damun_voluntary_goal",
    "post_climax_world_change",
}

PROTECTED_PHRASES = [
    "신수 비소유",
    "소유권·귀환·책임",
    "담운의 정체",
    "5액트 결말",
    "책임 분산",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def main() -> int:
    for path in (DATA, OVERLAY, AUDIT):
        if not path.exists():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    subacts = payload.get("subacts", [])
    if len(subacts) != 20:
        fail(f"expected 20 subacts, found {len(subacts)}")

    expected_ids = [f"A{i:02d}" for i in range(1, 21)]
    actual_ids = [item.get("id") for item in subacts]
    if actual_ids != expected_ids:
        fail(f"subact ids mismatch: {actual_ids}")

    previous_engine = None
    for item in subacts:
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            fail(f"{item.get('id')} missing fields: {sorted(missing)}")
        for field in REQUIRED_FIELDS - {"id"}:
            if not str(item[field]).strip():
                fail(f"{item['id']} has empty {field}")
        engine = item["conflict_engine"]
        if engine == previous_engine:
            fail(f"consecutive conflict engine duplicate at {item['id']}: {engine}")
        previous_engine = engine

    overlay_text = OVERLAY.read_text(encoding="utf-8")
    episodes = sorted({int(x) for x in re.findall(r"^## EP(\d{3})", overlay_text, re.M)})
    if episodes != list(range(1, 11)):
        fail(f"episode overlay must cover 001-010, found {episodes}")

    for ep in range(1, 11):
        block_match = re.search(
            rf"^## EP{ep:03d}.*?(?=^## EP\d{{3}}|\Z)", overlay_text, re.M | re.S
        )
        if not block_match:
            fail(f"missing EP{ep:03d} block")
        block = block_match.group(0)
        required_labels = [
            "현재 목표:",
            "지역 생활 압력:",
            "직업·물류 압력:",
            "담운의 자발적 목표:",
            "감정 압박:",
            "이동 전/후:",
            "갈등 후 세계 변화:",
            "감각 표식:",
            "설명 행동화:",
            "기존 사건 변경:",
        ]
        for label in required_labels:
            if label not in block:
                fail(f"EP{ep:03d} missing label: {label}")
        if "기존 사건 변경: 없음" not in block:
            fail(f"EP{ep:03d} changes canon without explicit approval marker")

    audit_text = AUDIT.read_text(encoding="utf-8")
    for phrase in PROTECTED_PHRASES:
        if phrase not in audit_text:
            fail(f"protected canon phrase missing from audit: {phrase}")

    forbidden = [
        "신수는 수집품이다",
        "담운은 선택받은 영웅이다",
        "중앙 권한을 담운이 소유한다",
    ]
    combined = audit_text + "\n" + overlay_text + "\n" + DATA.read_text(encoding="utf-8")
    for phrase in forbidden:
        if phrase in combined:
            fail(f"forbidden canon mutation detected: {phrase}")

    print("[PASS] prose operability v3.2")
    print("- 20 subacts present with all operability fields")
    print("- no consecutive conflict engine duplicates")
    print("- episodes 001-010 overlay complete")
    print("- protected canon phrases retained")
    return 0


if __name__ == "__main__":
    sys.exit(main())
