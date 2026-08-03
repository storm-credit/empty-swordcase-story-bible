#!/usr/bin/env python3
"""Validate provisional registry governance and effective corrections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


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


def main() -> int:
    governance = load("data/collection_system_governance_v3_3.json")
    collection = load("data/collection_registry_120_v3_3.json")
    sets_payload = load("data/set_registry_024_v3_3.json")
    beasts = load("data/beast_registry_018_v3_3.json")

    require(governance.get("authority") == "official_governance_overlay", "governance overlay must be official")
    require(governance.get("approval_required") is True, "author approval must remain required")
    precedence = governance.get("registry_precedence", {})
    for path in (
        "data/collection_registry_120_v3_3.json",
        "data/set_registry_024_v3_3.json",
        "data/beast_registry_018_v3_3.json",
    ):
        require(precedence.get(path) == "provisional_candidate_registry", f"{path} must remain provisional")

    items = [item for batch in collection.get("batches", []) for item in batch.get("items", [])]
    item_by_id = {item.get("id"): item for item in items}
    item_names = {item.get("name") for item in items}
    sets = {record.get("id"): record for record in sets_payload.get("sets", [])}
    corrections = governance.get("effective_corrections", {})

    for set_id, record in sets.items():
        component_ids = record.get("component_ids", [])
        component_first = [item_by_id.get(component_id, {}).get("first_episode") for component_id in component_ids]
        require(all(isinstance(value, int) for value in component_first), f"{set_id} has a component without first_episode")
        effective_complete = corrections.get(set_id, {}).get("first_complete_episode", record.get("first_complete_episode"))
        if component_first:
            require(effective_complete >= max(component_first), f"{set_id} completes before all components appear")

    locked = governance.get("inherited_locked_elements", [])
    direct_or_collective_matches = {
        "무주함": "무주함" in item_names,
        "반치": "반치" in item_names,
        "빈 명패": "빈 명패" in item_names,
        "불먹장갑": "불먹장갑" in item_names,
        "소리 없는 망치": "소리 없는 망치" in item_names,
        "냉철못": "냉철못" in item_names,
        "모조 왕검": "모조 왕검" in item_names,
        "한숨풀무": "한숨풀무" in item_names,
        "잠든 숲 향로": "잠든 숲 향로" in item_names,
        "설갑 일곱 조각": "설갑 일곱 조각" in item_names,
        "사막을 접는 지도": "사막을 접는 지도" in item_names,
        "천품 파편": "천품 파편" in item_names,
        "기억 닻과 여섯 닻": {"기억 닻", "여섯 닻줄 허가패"}.issubset(item_names),
        "이름 지우는 가면": "이름 지우는 가면" in item_names,
        "어린 배달패": "어린 배달패" in item_names,
        "무명시 이름장부": "무명시 이름장부" in item_names,
        "육도 열쇠": all(f"CI{index:03d}" in item_by_id for index in range(85, 91)),
        "수장인": "수장인" in item_names,
        "중앙핵": "중앙핵" in item_names,
        "두리·신수 역계약": any(record.get("name") == "두리" for record in beasts.get("beasts", [])),
        "여섯 책임 조각": all(f"CI{index:03d}" in item_by_id for index in range(115, 121)),
    }
    for name in locked:
        require(direct_or_collective_matches.get(name) is True, f"locked inherited element missing from candidate registries: {name}")

    require(beasts.get("collectible") is False, "beasts must not be collectible")
    require(beasts.get("set_component_allowed") is False, "beasts must not be set components")
    require("author" == governance.get("approval_owner"), "only the author may approve candidate canon")

    result = {"version":"3.3","status":"failed" if ERRORS else "passed","errors":ERRORS}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    raise SystemExit(main())
