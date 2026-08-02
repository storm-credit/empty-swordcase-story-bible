#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BUILD = ROOT / "build"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    index = []
    for path in (
        DATA / "episode_world_cast_cost_001_050.json",
        DATA / "episode_world_cast_cost_051_100.json",
        DATA / "episode_world_cast_cost_101_150.json",
        DATA / "episode_world_cast_cost_151_200.json",
    ):
        index.extend(load(path))
    settlements = load(DATA / "world_settlements_048.json")
    supporting = load(DATA / "supporting_cast_028.json")
    effective_path = BUILD / "episodes_effective_001_200_v2_8.json"
    if not effective_path.exists():
        raise SystemExit("run build_effective_episodes_v2_8.py first")
    effective = load(effective_path)

    errors: list[str] = []
    if [row["episode"] for row in index] != list(range(1, 201)):
        errors.append("overlay coverage must be 1-200")
    if [row["episode"] for row in effective] != list(range(1, 201)):
        errors.append("effective coverage must be 1-200")

    settlement_by_id = {row["id"]: row for row in settlements}
    supporting_by_id = {row["id"]: row for row in supporting}
    settlement_counts: Counter[str] = Counter()
    supporting_counts: Counter[str] = Counter()
    costs: list[str] = []

    forbidden = (
        "시간·안전·관계 중 최소 하나",
        "시간·안전·관계 중 하나",
        "실제 대가로 지불한다",
    )

    for overlay, row in zip(index, effective):
        ep = row["episode"]
        if overlay["title"] != row["title"]:
            errors.append(f"E{ep:03d}: title mismatch between base and overlay")
        sids = overlay.get("settlement_ids", [])
        for sid in sids:
            if sid not in settlement_by_id:
                errors.append(f"E{ep:03d}: unknown settlement {sid}")
            settlement_counts[sid] += 1
        expected_location = "·".join(
            settlement_by_id[sid]["name"] for sid in sids if sid in settlement_by_id
        )
        if row.get("location") != expected_location:
            errors.append(f"E{ep:03d}: effective location mismatch")

        scids = overlay.get("supporting_cast_ids", [])
        for sid in scids:
            if sid not in supporting_by_id:
                errors.append(f"E{ep:03d}: unknown supporting cast {sid}")
                continue
            supporting_counts[sid] += 1
            if supporting_by_id[sid]["name"] not in row.get("cast", []):
                errors.append(f"E{ep:03d}: cast name missing for {sid}")

        cost = overlay.get("concrete_cost", "").strip()
        costs.append(cost)
        if row.get("cost") != cost:
            errors.append(f"E{ep:03d}: effective cost mismatch")
        if len(cost) < 20 or any(token in cost for token in forbidden):
            errors.append(f"E{ep:03d}: vague/placeholder cost")

    if set(settlement_counts) != set(settlement_by_id):
        errors.append("not all 48 settlements are linked")
    for sid in settlement_by_id:
        if settlement_counts[sid] < 2:
            errors.append(f"{sid}: fewer than two uses")
    if set(supporting_counts) != set(supporting_by_id):
        errors.append("not all 28 supporting cast are linked")
    for sid, info in supporting_by_id.items():
        for ep in info["planned_episodes"]:
            if sid not in index[ep - 1].get("supporting_cast_ids", []):
                errors.append(f"{sid}: planned episode {ep} missing")
    if len(set(costs)) != 200:
        errors.append("episode costs must be unique 200/200")

    if errors:
        raise SystemExit("\n".join(errors))
    print("v2.8 production linkage validation passed")
    print("episodes=200 settlements=48/48 supporting_cast=28/28 unique_costs=200/200")

if __name__ == "__main__":
    main()
