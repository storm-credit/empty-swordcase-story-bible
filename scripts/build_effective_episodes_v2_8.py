#!/usr/bin/env python3
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "build"
OUT.mkdir(exist_ok=True)

SOURCE_FILES = [
    DATA / "episodes_001_010.json",
    DATA / "episodes_011_020.json",
    DATA / "episodes_021_030.json",
    DATA / "episodes_031_040.json",
    DATA / "episodes_041_080.json",
    DATA / "episodes_081_120.json",
    DATA / "episodes_121_160.json",
    DATA / "episodes_161_200.json",
]

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    episodes = []
    for path in SOURCE_FILES:
        episodes.extend(load(path))
    episodes.sort(key=lambda row: row["episode"])
    if [row["episode"] for row in episodes] != list(range(1, 201)):
        raise SystemExit("base episode coverage must be 1-200")

    overlay_rows = []
    for path in (
        DATA / "episode_world_cast_cost_001_050.json",
        DATA / "episode_world_cast_cost_051_100.json",
        DATA / "episode_world_cast_cost_101_150.json",
        DATA / "episode_world_cast_cost_151_200.json",
    ):
        overlay_rows.extend(load(path))
    overlay = {row["episode"]: row for row in overlay_rows}
    settlements = {row["id"]: row for row in load(DATA / "world_settlements_048.json")}
    supporting = {row["id"]: row for row in load(DATA / "supporting_cast_028.json")}

    for row in episodes:
        patch = overlay[row["episode"]]
        row["settlement_ids"] = patch["settlement_ids"]
        row["location"] = "·".join(settlements[sid]["name"] for sid in patch["settlement_ids"])
        row["supporting_cast_ids"] = patch["supporting_cast_ids"]
        cast = list(row.get("cast", []))
        for sid in patch["supporting_cast_ids"]:
            name = supporting[sid]["name"]
            if name not in cast:
                cast.append(name)
        row["cast"] = cast
        row["cost"] = patch["concrete_cost"]
        primary = settlements[patch["settlement_ids"][0]]
        row["world_link"] = {
            "settlements": patch["settlement_ids"],
            "local_tension": primary["current_tension"],
            "landmark": primary["landmark"],
        }

    json_path = OUT / "episodes_effective_001_200_v2_8.json"
    json_path.write_text(json.dumps(episodes, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = [
        "episode","act","act_title","subact","subact_title","arc","title","goal",
        "conflict","choice","reward","hook","pov","location","cast",
        "episode_function","stakes","cost","settlement_ids","supporting_cast_ids"
    ]
    with (OUT / "episodes_effective_001_200_v2_8.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in episodes:
            out = {key: row.get(key, "") for key in fields}
            for key in ("cast", "settlement_ids", "supporting_cast_ids"):
                if isinstance(out[key], list):
                    out[key] = "|".join(map(str, out[key]))
            writer.writerow(out)

    print("built effective v2.8 episodes: 200")

if __name__ == "__main__":
    main()
